import speech_recognition as sr
import threading
import tkinter as tk
from tkinter import scrolledtext

recording = True  # Flag global para controlar la grabación
audio_container = []  # Contenedor global para el audio grabado
recognizer = sr.Recognizer()

def listen_for_audio(recognizer, source, audio_container):
    """Escucha el audio mientras la grabación esté activa."""
    global recording
    text_area.insert(tk.END, "Di algo, para escribirlo! (Presiona ENTER para detener)\n")

    while recording:
        try:
            # Capturar audio con un pequeño timeout para poder verificar `recording`
            audio = recognizer.listen(source, timeout=2)  # Aumentamos el timeout para no cortar frases
            if audio:  # Solo agregar si se capturó algo
                audio_container.append(audio)
        except sr.WaitTimeoutError:
            continue

def stop_recording():
    """Detiene la grabación cuando el usuario presiona ENTER."""
    global recording
    recording = False  # Cambia el flag para detener el bucle en `listen_for_audio`

def start_recording():
    global recording, audio_container
    recording = True
    audio_container = []

    with sr.Microphone() as source:
        text_area.insert(tk.END, "Ajustando el ruido de fondo, por favor espera...\n")
        recognizer.adjust_for_ambient_noise(source, duration=1)  # Reduce el ruido ambiental
        text_area.insert(tk.END, "Listo! Puedes hablar.\n")

        # Crear y ejecutar hilos
        audio_thread = threading.Thread(target=listen_for_audio, args=(recognizer, source, audio_container))
        audio_thread.start()

        # Esperar a que el usuario presione el botón de detener
        stop_button.wait_variable(stop_var)
        stop_recording()
        audio_thread.join()  # Espera a que la grabación finalice

        # Procesar el audio grabado si hay contenido
        if audio_container:
            text_area.insert(tk.END, "Procesando el audio...\n")
            combined_audio = sr.AudioData(
                b"".join(a.frame_data for a in audio_container),  # Concatenar los fragmentos de audio
                audio_container[0].sample_rate,
                audio_container[0].sample_width
            )

            try:
                text = recognizer.recognize_google(combined_audio, language='es-ES')
                text_area.insert(tk.END, f"Has dicho: {text}\n")
            except sr.RequestError as e:
                text_area.insert(tk.END, f"No se pudo solicitar resultados de Google Speech Recognition; {e}\n")
            except sr.UnknownValueError:
                text_area.insert(tk.END, "Google Speech Recognition no pudo entender el audio\n")
        else:
            text_area.insert(tk.END, "No se detectó ningún audio.\n")

def on_start_button_click():
    start_recording()

def on_stop_button_click():
    stop_var.set(1)

# Crear la interfaz gráfica
root = tk.Tk()
root.title("Transcripción de Voz a Texto")

start_button = tk.Button(root, text="Iniciar Grabación", command=on_start_button_click)
start_button.pack(pady=10)

stop_var = tk.IntVar()
stop_button = tk.Button(root, text="Detener Grabación", command=on_stop_button_click)
stop_button.pack(pady=10)

text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=10)
text_area.pack(pady=10)

root.mainloop()