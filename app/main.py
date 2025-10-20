"""
Video Analysis API - Simple version with OpenAI Vision support
Analyzes video cuts and generates keyword descriptions (hospitality-focused)
"""
import os
import tempfile
import logging
import base64
import io
from pathlib import Path
from typing import Optional

import cv2
import requests
from fastapi import FastAPI, HTTPException, Header, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from scenedetect import detect, ContentDetector
from PIL import Image

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import config
from .config import settings

# FastAPI app
app = FastAPI(title="Video Analysis API - Hospup", version="1.0.0")

# Global captioner cache
_captioner_client = None


# Schemas
class Clip(BaseModel):
    order: int
    start: float
    end: float
    duration: float
    description: str


class AnalysisResult(BaseModel):
    clips: list[Clip]
    texts: list = []


# Captioner initialization (lazy loading)
def get_captioner():
    """Get or initialize captioner based on backend"""
    global _captioner_client

    if _captioner_client is None:
        if settings.CAPTION_BACKEND == "openai":
            # OpenAI Vision
            if not settings.OPENAI_API_KEY:
                raise ValueError("OPENAI_API_KEY not configured")

            from openai import OpenAI
            _captioner_client = OpenAI(api_key=settings.OPENAI_API_KEY)
            logger.info("✅ OpenAI Vision captioner initialized")

        else:
            raise ValueError(f"Unknown CAPTION_BACKEND: {settings.CAPTION_BACKEND}. Only 'openai' is supported.")

    return _captioner_client


def download_video(url: str, output_path: str) -> None:
    """Download video from URL"""
    logger.info(f"Downloading video from {url[:100]}...")
    response = requests.get(url, stream=True, timeout=60)
    response.raise_for_status()

    with open(output_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    logger.info(f"Video downloaded: {os.path.getsize(output_path) / 1024 / 1024:.2f} MB")


def detect_scenes(video_path: str, threshold: float = 27.0, min_scene_len: int = 15) -> list[tuple[float, float]]:
    """Detect scene cuts using PySceneDetect"""
    logger.info("Detecting scenes...")

    scene_list = detect(
        video_path,
        ContentDetector(threshold=threshold, min_scene_len=min_scene_len)
    )

    if not scene_list:
        # Fallback: get video duration and create single scene
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = frame_count / fps if fps > 0 else 10.0
        cap.release()
        logger.warning(f"No scenes detected, using full video as single scene (duration: {duration}s)")
        return [(0.0, duration)]

    # Convert to (start, end) tuples in seconds
    scenes = [
        (scene[0].get_seconds(), scene[1].get_seconds())
        for scene in scene_list
    ]

    logger.info(f"Detected {len(scenes)} scenes")
    return scenes


def extract_frame_at_time(video_path: str, timestamp: float) -> Optional[Image.Image]:
    """Extract frame at specific timestamp"""
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)

    if fps <= 0:
        cap.release()
        return None

    frame_number = int(timestamp * fps)
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

    ret, frame = cap.read()
    cap.release()

    if not ret:
        return None

    # Convert BGR to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return Image.fromarray(frame_rgb)


def frame_to_base64(image: Image.Image) -> str:
    """Convert PIL Image to base64 for OpenAI"""
    # Resize if too large (OpenAI limit)
    max_size = 1024
    if max(image.size) > max_size:
        ratio = max_size / max(image.size)
        new_size = (int(image.size[0] * ratio), int(image.size[1] * ratio))
        image = image.resize(new_size, Image.Resampling.LANCZOS)

    # Convert to JPEG bytes
    buffer = io.BytesIO()
    image.save(buffer, format='JPEG', quality=85)

    # Encode to base64
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return f"data:image/jpeg;base64,{image_base64}"


def caption_image(image: Image.Image) -> str:
    """Generate caption using hospitality prompt (keywords)"""
    captioner = get_captioner()

    # OpenAI Vision with hospitality prompt
    base64_image = frame_to_base64(image)

    response = captioner.chat.completions.create(
        model=settings.OPENAI_MODEL,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": settings.CAPTION_PROMPT},
                    {"type": "image_url", "image_url": {"url": base64_image}}
                ]
            }
        ],
        max_tokens=150,
        temperature=0.1,  # Low temperature for factual keywords
        timeout=settings.OPENAI_TIMEOUT
    )

    return response.choices[0].message.content.strip()


def analyze_video(video_path: str, threshold: float = 27.0, max_cuts: int = 30) -> AnalysisResult:
    """Main analysis pipeline"""
    logger.info(f"Starting analysis of {video_path}")

    # 1. Detect scenes
    scenes = detect_scenes(video_path, threshold=threshold)

    # Limit number of scenes
    if len(scenes) > max_cuts:
        logger.warning(f"Limiting scenes from {len(scenes)} to {max_cuts}")
        scenes = scenes[:max_cuts]

    # 2. Process each scene
    clips = []
    for idx, (start, end) in enumerate(scenes, 1):
        duration = end - start

        # Get middle frame
        mid_time = start + (duration / 2)
        frame = extract_frame_at_time(video_path, mid_time)

        if frame is None:
            logger.warning(f"Failed to extract frame for scene {idx}")
            description = "Frame extraction failed"
        else:
            # Caption frame
            description = caption_image(frame)
            logger.info(f"Scene {idx}: {description}")

        clips.append(Clip(
            order=idx,
            start=round(start, 1),
            end=round(end, 1),
            duration=round(duration, 1),
            description=description
        ))

    return AnalysisResult(clips=clips, texts=[])


# API Endpoints
@app.get("/health")
async def health():
    """Health check"""
    return {
        "ok": True,
        "backend": settings.CAPTION_BACKEND,
        "model_loaded": _captioner_client is not None
    }


@app.post("/analyze")
async def analyze(
    url: str = Form(...),
    threshold: float = Form(27.0),
    max_cuts: int = Form(30),
    x_api_key: str = Header(None, alias="x-api-key")
):
    """
    Analyze video from URL

    - **url**: Video URL (Instagram, S3, etc.)
    - **threshold**: Scene detection threshold (default: 27.0, lower = more cuts)
    - **max_cuts**: Maximum number of cuts to analyze (default: 30)
    """
    # Auth
    if x_api_key != settings.API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

    # Create temp directory
    with tempfile.TemporaryDirectory() as tmpdir:
        video_path = Path(tmpdir) / "video.mp4"

        try:
            # Download video
            download_video(url, str(video_path))

            # Analyze
            result = analyze_video(
                str(video_path),
                threshold=threshold,
                max_cuts=max_cuts
            )

            return JSONResponse(content=result.model_dump())

        except requests.exceptions.RequestException as e:
            logger.error(f"Download failed: {e}")
            raise HTTPException(status_code=422, detail=f"Failed to download video: {str(e)}")

        except Exception as e:
            logger.error(f"Analysis failed: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@app.on_event("startup")
async def startup_event():
    """Preload model on startup (optional)"""
    # Uncomment to preload model
    # load_captioner()
    logger.info("API started")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
