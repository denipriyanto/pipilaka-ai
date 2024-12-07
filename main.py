import speech_recognition as sr
import pyttsx3

speaker = pyttsx3.init()
recognizer = sr.Recognizer()

# Menampilkan daftar semua perangkat input audio
for index, name in enumerate(sr.Microphone.list_microphone_names()):
    print(f"{index}: {name}")

try:
    with sr.Microphone() as source:
        speaker.say("Hello, Im Pipilaka. Silahkan tanya tentang aku.")
        speaker.runAndWait()

        print("Silahkan Bicara...")

        recognizer.adjust_for_ambient_noise(source)

        audio = recognizer.listen(source)
        
        try:
            text = recognizer.recognize_google(audio)
            print("Anda Mengatakan: ", text)
        except sr.UnknownValueError:
            print("Maaf, tidak dapat mengenali ucapan.")
        except sr.RequestError as e:
            print(f"Error pada layanan: {e}")
except Exception as e:
    print(f"Terjadi kesalahan saat mendengarkan: {e}")