import os
import time
from google import genai
from dotenv import load_dotenv

def main():
    print("================================")
    print("MeetIntel Gemini Diagnostics")
    print("================================")
    
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("\nAPI key configured: NO")
        return
    print("\nAPI key configured: YES")
    
    primary = os.getenv("GEMINI_PRIMARY_MODEL", "gemini-3.6-flash")
    fallbacks_str = os.getenv("GEMINI_FALLBACK_MODELS", "gemini-flash-latest,gemini-2.5-flash-lite,gemini-3.5-flash-lite,gemini-2.5-flash")
    fallbacks = [m.strip() for m in fallbacks_str.split(",") if m.strip()]
    
    print(f"\nPrimary model:\n{primary}")
    print(f"\nFallback models:\n{', '.join(fallbacks)}")
    
    try:
        client = genai.Client(api_key=api_key)
        print("\nClient initialization:\nPASS")
    except Exception as e:
        print(f"\nClient initialization:\nFAIL\nError: {e}")
        return

    # Check models connectivity
    for model in [primary] + fallbacks:
        print(f"\nTesting model: {model}")
        try:
            start_time = time.time()
            response = client.models.generate_content(
                model=model,
                contents="Hello. Please reply with exactly the word 'PASS'. Do not add any punctuation."
            )
            latency = int((time.time() - start_time) * 1000)
            text = response.text.strip()
            if "PASS" in text:
                print("Connectivity: PASS")
                print(f"Latency: {latency} ms")
            else:
                print("Connectivity: FAIL")
                print(f"Error: Unexpected response: {text}")
        except Exception as e:
            print("Connectivity: FAIL")
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
