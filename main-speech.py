import speech_recognition as sr

recognizer = sr.Recognizer()

def answer(question, response):
    question = question.lower()
    
    for key, info in response.items():
        if key.lower() in question:
            character = info.get("karakter", "Karakter tidak diketahui")
            answer = info.get("jawaban", "Jawaban tidak diketahui")
            return (f"Karakter: {character}\nJawaban: {answer}")
    
    return "Maaf tidak ada respon yang cocok"

def speech(response):
    with sr.Microphone() as source:
        print("Silahkan Bicara...")

        recognizer.adjust_for_ambient_noise(source)

        audio = recognizer.listen(source)
        
        try:
            text = recognizer.recognize_google(audio, language="id-ID")
            print("Anda Mengatakan: ", text)
            
            hasil = answer(text, response)
            print(hasil)
            
        except sr.UnknownValueError:
            print("Maaf, tidak dapat mengenali ucapan.")
        except sr.RequestError as e:
            print(f"Error pada layanan: {e}") 

if __name__ == "__main__":
    response_data = {
        "halo": {"karakter": "Pipilaka", "jawaban": "Halo saya Pipilaka! Ada yang bisa saya bantu?"},
        "hai": {"karakter": "Pipilaka", "jawaban": "Halo saya Pipilaka! Ada yang bisa saya bantu?"},
        "selamat pagi": {"karakter": "Tari", "jawaban": "Selamat pagi! Semoga harimu menyenangkan!"},
        "terima kasih": {"karakter": "pipilaka_thankyou", "jawaban": "Sama-sama! Senang bisa membantu."}
    }
    
    speech(response_data)