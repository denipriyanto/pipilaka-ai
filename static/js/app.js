let mediaRecorder;
let audioChunks = [];
let isRecording = false;

async function startRecording() {
    // Minta izin untuk menggunakan mikrofon
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);
    audioChunks = [];

    mediaRecorder.ondataavailable = event => {
        audioChunks.push(event.data);
    };

    mediaRecorder.onstart = () => {
        document.getElementById("status").textContent = "Merekam...";
    };

    mediaRecorder.onstop = () => {
        document.getElementById("status").textContent = "Tahan untuk bicara.";
        // Buat file audio dari potongan yang direkam
        const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
        const audioUrl = URL.createObjectURL(audioBlob);
        const playback = document.getElementById("playback");
        playback.src = audioUrl;

        // Kirim file audio ke backend
        sendAudioToBackend(audioBlob);
    };

    mediaRecorder.start();
    isRecording = true;
}

function stopRecording() {
    if (isRecording && mediaRecorder) {
        mediaRecorder.stop();
        isRecording = false;
    }
}

async function sendAudioToBackend(audioBlob) {
    const formData = new FormData();
    formData.append('file', audioBlob, 'recording.wav');

    try {
        const response = await fetch('http://127.0.0.1:5000/questions', {
            method: 'POST',
            body: formData,
        });

        if (response.ok) {
            const data = await response.json();
            // alert(`Karakter: ${data.karakter}\nJawaban: ${data.jawaban}`);

            const audioElement = document.getElementById("playback");
            audioElement.src = "http://127.0.0.1:5000/" + data.audio;
            audioElement.play();
        } else {
            const error = await response.json();

            const audioElement = document.getElementById("playback");
            audioElement.src = "http://127.0.0.1:5000/static/audio/not_found.mp3";
            audioElement.play();
        }
    } catch (err) {
        console.error('Error sending audio to backend:', err);
    }
}