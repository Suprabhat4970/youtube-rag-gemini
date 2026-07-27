import os

api_key = os.getenv("GEMINI_API_KEY")

print("=" * 50)
print("Checking Gemini API Key...")

if api_key:
    print("✅ API Key Found")
    print("Starts with:", api_key[:6])   # Only prints first 6 characters
    print("Length:", len(api_key))
else:
    print("❌ API Key NOT Found")

print("=" * 50)