#!/bin/bash

# Test script for Video Analysis API
# Tests with your Instagram video URL

set -e

API_URL="http://localhost:8190"
API_KEY="your-secret-key-change-me"
INSTAGRAM_URL="https://scontent-lax3-1.cdninstagram.com/o1/v/t16/f2/m86/AQMhQBW9nNDrEg76Om3itggV6htOVUFu4jpcQQPKnoIDo3tTiuxJwSIsTxjp9Ch-SN90UdfZh-GGXLZmpeFkj80TjcFgg6vd9edLXz4.mp4?stp=dst-mp4&efg=eyJxZV9ncm91cHMiOiJbXCJpZ193ZWJfZGVsaXZlcnlfdnRzX290ZlwiXSIsInZlbmNvZGVfdGFnIjoidnRzX3ZvZF91cmxnZW4uY2xpcHMuYzIuNzIwLmJhc2VsaW5lIn0&_nc_cat=110&vs=1783337319281816_1984711560&_nc_vs=HBksFQIYUmlnX3hwdl9yZWVsc19wZXJtYW5lbnRfc3JfcHJvZC9CODRFMUJBQUY0ODI0RjQwMUQ4MTg3MkZERTMzMThCMl92aWRlb19kYXNoaW5pdC5tcDQVAALIARIAFQIYOnBhc3N0aHJvdWdoX2V2ZXJzdG9yZS9HTWFpZXg3YkhQSzkxaHNDQUxLQ2plS3pxMmdHYnFfRUFBQUYVAgLIARIAKAAYABsAFQAAJuTPoImc161BFQIoAkMzLBdAG3bItDlYEBgSZGFzaF9iYXNlbGluZV8xX3YxEQB1%2Fgdl5p0BAA%3D%3D&_nc_rid=7fc41811d6&ccb=9-4&oh=00_AffOK2xxt0JnzbOA-uXar5faO2Wgh1yeCvqGQZPRErgvEw&oe=68F7FD7F&_nc_sid=10d13b"

echo "🧪 Testing Video Analysis API"
echo "=============================="
echo ""

# Test 1: Health check
echo "1️⃣  Testing /health..."
HEALTH=$(curl -s "$API_URL/health")
echo "Response: $HEALTH"
echo ""

# Test 2: Analyze video
echo "2️⃣  Testing /analyze with Instagram video..."
echo "URL: ${INSTAGRAM_URL:0:100}..."
echo ""

RESULT=$(curl -s -X POST "$API_URL/analyze" \
  -H "x-api-key: $API_KEY" \
  -F "url=$INSTAGRAM_URL" \
  -F "threshold=25" \
  -F "max_cuts=8")

echo "✅ Analysis complete!"
echo ""
echo "Results:"
echo "$RESULT" | python3 -m json.tool

echo ""
echo "🎉 Tests completed!"
