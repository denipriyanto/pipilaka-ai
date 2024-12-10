from flask import Flask, request, jsonify, render_template
from speech_recognition import Recognizer, AudioFile
from pydub import AudioSegment
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

response_data = {
    "halo": {"karakter": "Pipilaka", "audio":"/static/audio/greetings.mp3", "jawaban": "Halo saya Pipilaka! Ada yang bisa saya bantu?"},
    "hai": {"karakter": "Pipilaka", "audio":"/static/audio/greetings.mp3", "jawaban": "Halo saya Pipilaka! Ada yang bisa saya bantu?"},
    "selamat pagi": {"karakter": "Tari", "audio":"/static/morning.mp3", "jawaban": "Selamat pagi! Semoga harimu menyenangkan!"},
    "terima kasih": {"karakter": "pipilaka_thankyou", "audio":"/static/audio/thankyou.mp3", "jawaban": "Sama-sama! Senang bisa membantu."},
    "apa itu": {"karakter": "Pipilaka", "audio":"/static/audio/apa_pipilaka.mp3", "jawaban": "Dalam bahasa Sanskerta, 'Pipilika' (पिपिलिका) adalah kata untuk 'Semut'. Oleh karena itu, di balik PIPILAKA FOUNDATION, terdapat filosofi bahwa, seperti halnya semut, bersama-sama dan melalui tindakan kecil, hasil yang signifikan dapat dicapai. Dengan melakukan tindakan kecil setiap hari, kita bisa menciptakan tindakan besar dan mencapai hasil yang besar."},
    "yayasan": {"karakter": "Pipilaka", "audio":"/static/audio/yayasan_pipilaka.mp3", "jawaban": "Yayasan Pipilaka adalah organisasi non-profit yang didirikan oleh sekelompok teman multikultural yang tinggal dan bekerja di Yogyakarta, pusat tradisi dan seni kontemporer, yang memiliki kepedulian bersama terhadap lingkungan dan kemanusiaan. Fokus utamanya adalah pada penyelenggaraan kegiatan sosial, budaya, dan seni."},
}

def get_response(question):
    question = question.lower()
    for questionkey, info in response_data.items():
        if questionkey in question:
            return info
    
    return None

def convert_to_wav(input_file_path, output_file_path):
    # Menggunakan pydub untuk mengonversi file audio ke WAV
    audio = AudioSegment.from_file(input_file_path)
    audio.export(output_file_path, format="wav")

@app.route('/questions', methods=['POST'])
def proses_audio():
    file = request.files.get('file')
    if not file:
        return jsonify({"error": "Tidak ada file audio yang dikirim."}), 400

    temp_input_file = "input_audio"
    file.save(temp_input_file)
    
    temp_output_file = "output_audio.wav"
    
    try:
        convert_to_wav(temp_input_file, temp_output_file)
    except Exception as e:
        return jsonify({"error": "Gagal mengonversi file audio ke WAV.", "details": str(e)}), 500

    recognizer = Recognizer()
    try:
        with AudioFile(temp_output_file) as source:
            audio = recognizer.record(source)
            teks = recognizer.recognize_google(audio, language="id-ID")
            print(f"Teks yang dikenali: {teks}")

            # Cari respons
            respons = get_response(teks)
            if respons:
                return jsonify(respons)
            else:  
                return jsonify({"error": "Response tidak ada yang cocok."}),404
    except Exception as e:        
        return jsonify({"error": str(e)}),500
    finally:
        # Hapus file sementara setelah diproses
        if os.path.exists(temp_input_file):
            os.remove(temp_input_file)
        if os.path.exists(temp_output_file):
            os.remove(temp_output_file)
            
@app.route('/', methods=['get'])
def index():
    data = {
        "title": "Selamat Datang di Pipilaka AI",
        "description": "Pipilaka AI adalah proyek interaktif berbasis suara."
    }
    return render_template('index.html', data=data)

if __name__ == "__main__":
    app.run(debug=True)