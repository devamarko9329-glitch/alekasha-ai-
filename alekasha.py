import requests
import os

API_KEY = os.getenv("GEMINI_API_KEY")

print("नमस्ते! मैं Alekasha AI हूँ।")
print("बाहर निकलने के लिए exit लिखो।")

while True:
    print("बोलिए, Alekasha सुन रही है...")
    question = os.popen("termux-speech-to-text").read().strip()
    print("तुम:", question)

    if question.lower() == "exit":
        print("Alekasha: फिर मिलेंगे!")
        break

    if not question:
        print("आवाज़ समझ नहीं आई। फिर से बोलिए।")
        continue

    if not API_KEY:
        print("API Key नहीं मिली।")
        break

    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent"

    try:
        response = requests.post(
            url,
            headers={"x-goog-api-key": API_KEY},
            json={
                "system_instruction": {
                    "parts": [
                        {
                            "text": "तुम्हारा नाम Alekasha AI है। तुम हिंदी में दोस्ताना तरीके से जवाब देती हो।"
                        }
                    ]
                },
                "contents": [
                    {
                        "parts": [
                            {"text": question}
                        ]
                    }
                ]
            }
        )

        result = response.json()

        if response.ok:
            answer = result["candidates"][0]["content"]["parts"][0]["text"]
            print("Alekasha:", answer)
            os.system("termux-tts-speak " + repr(answer))
        else:
            print("API की समस्या:", result.get("error", {}).get("message", "अज्ञात त्रुटि"))

    except Exception as e:
        print("कनेक्शन की समस्या:", e)
    again = input("फिर सुनना है? (हाँ/नहीं): ")
    if again.strip().lower() not in ["हाँ", "ha", "yes", "y"]:
        break
