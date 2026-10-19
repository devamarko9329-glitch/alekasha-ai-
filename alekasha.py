
import requests
import os
import time
import subprocess

API_KEY = os.getenv("GEMINI_API_KEY")

def offline_answer(question):
    q = question.lower()

    if "नमस्ते" in q or "हेलो" in q or "hello" in q:
        return "नमस्ते! मैं Alekasha हूँ। अभी ऑफलाइन मोड में हूँ।"

    if "तुम्हारा नाम" in q or "कौन हो" in q:
        return "मेरा नाम Alekasha AI है।"

    if "समय" in q or "टाइम" in q:
        return "अभी फोन में समय है " + time.strftime("%I:%M %p")

    if "मदद" in q or "help" in q:
        return "मैं नमस्ते, अपना नाम और समय जैसे आसान सवालों का जवाब दे सकती हूँ।"

    return "अभी इंटरनेट नहीं है। मैं ऑफलाइन हूँ। इंटरनेट चालू करके फिर पूछिए।"


print("नमस्ते! मैं Alekasha AI हूँ।")
print("बाहर निकलने के लिए exit बोलिए।")

while True:
    print("बोलिए, Alekasha सुन रही है...")
    question = os.popen("termux-speech-to-text").read().strip()
    print("तुम:", question)

    if question.lower() in ["exit", "बाहर निकलो", "बंद करो"]:
        print("Alekasha: फिर मिलेंगे!")
        break

    if not question:
        print("आवाज़ समझ नहीं आई। फिर से बोलिए।")
        continue

    answer = None

    if API_KEY:
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent"

        try:
            response = requests.post(
                url,
                headers={"x-goog-api-key": API_KEY},
                json={
                    "system_instruction": {
                        "parts": [{
                            "text": "तुम Alekasha AI हो। हिंदी में दोस्ताना जवाब दो।"
                        }]
                    },
                    "contents": [{
                        "parts": [{"text": question}]
                    }]
                },
                timeout=20
            )

            if response.ok:
                result = response.json()
                answer = result["candidates"][0]["content"]["parts"][0]["text"]
            else:
                print("ऑनलाइन सेवा उपलब्ध नहीं है।")

        except Exception:
            print("इंटरनेट कनेक्शन नहीं मिला।")

    if not answer:
        answer = offline_answer(question)

    print("Alekasha:", answer)

    subprocess.run(["termux-tts-speak", answer])

    again = input("फिर सुनना है? (हाँ/नहीं): ")
    if again.strip().lower() not in ["हाँ", "हां", "ha", "yes", "y"]:
        break
