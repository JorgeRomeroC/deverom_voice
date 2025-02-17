import time
import threading
import speech_recognition as sr
from utils import process_audio  # O desde donde esté definida

class AudioRecorder:
    def __init__(self, app):
        self.app = app
        self.recognizer = sr.Recognizer()
        self.recording = False
        self.audio_container = []

    def start_recording(self):
        """Inicia la grabación en un hilo separado."""
        self.recording = True
        self.audio_container = []
        self.app.text_area.insert("end", "🎙 Ajustando el ruido de fondo...\n")
        threading.Thread(target=self.listen_for_audio, daemon=True).start()

    def stop_recording(self):
        """Detiene la grabación y ejecuta el procesamiento en un hilo separado."""
        self.recording = False
        threading.Thread(target=lambda: process_audio(self.app, self.audio_container), daemon=True).start()

    def listen_for_audio(self):
        """Escucha y almacena fragmentos de audio."""
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=2)
            self.app.text_area.insert("end", "🗣 ¡Puedes hablar ahora!\n")

            while self.recording:
                try:
                    audio = self.recognizer.listen(source, phrase_time_limit=10)
                    if audio:
                        self.audio_container.append(audio)
                except sr.WaitTimeoutError:
                    continue

    def process_audio(self):
        """Procesa y transcribe el audio."""
        self.app.text_area.insert("end", "🔄 Procesando el audio...\n")
        if self.audio_container:
            combined_audio = sr.AudioData(
                b"".join(a.frame_data for a in self.audio_container),  # Concatenar los fragmentos de audio
                self.audio_container[0].sample_rate,
                self.audio_container[0].sample_width
            )
            try:
                text = self.recognizer.recognize_google(combined_audio, language='es-ES')
                self.app.text_area.insert("end", f"📝 {text.capitalize()}\n")
            except Exception:
                self.app.text_area.insert("end", "❌ No se pudo entender el audio.\n")
        else:
            self.app.text_area.insert("end", "⚠ No se detectó audio.\n")