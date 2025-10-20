"""Configuration settings"""
import os
from typing import Literal

class Settings:
    # API
    API_KEY: str = os.getenv("API_KEY", "your-secret-key")
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))

    # Captioning backend
    CAPTION_BACKEND: Literal["openai", "moondream2"] = os.getenv("CAPTION_BACKEND", "openai")

    # OpenAI (if using openai backend)
    OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    OPENAI_TIMEOUT: int = int(os.getenv("OPENAI_TIMEOUT", "30"))

    # Scene detection
    DEFAULT_THRESHOLD: float = float(os.getenv("DEFAULT_THRESHOLD", "27.0"))
    DEFAULT_MIN_SCENE_LEN: int = int(os.getenv("DEFAULT_MIN_SCENE_LEN", "15"))
    MAX_CUTS: int = int(os.getenv("MAX_CUTS", "30"))

    # The EXACT prompt from your openai_vision_service.py (lines 153-185)
    CAPTION_PROMPT: str = """You are analyzing a property video (hotel, villa, Airbnb, vacation rental). Describe what you see using ONLY concrete keywords (nouns), separated by commas.

RULES - SIMPLE:
1. List ONLY what you actually see in the frames
2. Use concrete nouns (pool, bed, table, ocean, etc.)
3. NO adjectives (beautiful, luxury, nice) - just facts
4. Separate keywords with commas
5. Be honest - if you see it, list it. If not, don't.

COMMON PROPERTY FEATURES (just examples - you can use other words too):

Pool & Water: pool, infinity pool, jacuzzi, hot tub, sun loungers, pool deck, water
Rooms & Bedrooms: bedroom, bed, suite, living room, furniture, window, balcony, sofa
Bathroom: shower, bathtub, sink, mirror, tiles, toilet
Food & Beverage: restaurant, kitchen, dining table, bar, coffee machine, wine glasses
Views & Scenery: ocean, sea, beach, mountain, sunset, garden, landscape, sky
Outdoors: terrace, patio, deck, palm trees, plants, flowers, lawn, bbq
Interior: lobby, hallway, stairs, fireplace, artwork, chandelier

The categories above are just EXAMPLES to help you. You can use ANY keyword that describes what you see.

EXAMPLES:

✅ GOOD: "infinity pool, ocean, sun loungers, palm trees"
✅ GOOD: "bedroom, bed, window, balcony"
✅ GOOD: "kitchen, dining table, chairs, ocean view, sunset"
✅ GOOD: "bathroom, bathtub, shower, mirror, tiles"

❌ WRONG: "beautiful pool, luxury bedroom, elegant restaurant"
(no adjectives!)

Just list what you see. Simple.
"""

settings = Settings()
