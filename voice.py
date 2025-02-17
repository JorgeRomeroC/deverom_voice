import speech_recognition as sr
import threading
import tkinter as tk
from tkinter import ttk, scrolledtext

recording = True  # Flag global para controlar la grabación
audio_container = []  # Contenedor global para el audio grabado
recognizer = sr.Recognizer()

def listen_for_audio(recognizer, source, audio_container):
    """Escucha el audio mientras la grabación esté activa."""
    global recording
    text_area.insert(tk.END, "Di algo, para escribirlo! (Presiona ENTER para detener)\n")

    while recording:
        try:
            audio = recognizer.listen(source, timeout=2)  # Captura audio con un pequeño timeout
            if audio:  
                audio_container.append(audio)
        except sr.WaitTimeoutError:
            continue

def stop_recording():
    """Detiene la grabación cuando el usuario presiona el botón de detener."""
    global recording
    recording = False  # Cambia el flag para detener el bucle en `listen_for_audio`

def start_recording():
    global recording, audio_container
    recording = True
    audio_container = []

    with sr.Microphone() as source:
        text_area.insert(tk.END, "Ajustando el ruido de fondo, por favor espera...\n")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        text_area.insert(tk.END, "Listo! Puedes hablar.\n")

        audio_thread = threading.Thread(target=listen_for_audio, args=(recognizer, source, audio_container))
        audio_thread.start()

        stop_button.wait_variable(stop_var)
        stop_recording()
        audio_thread.join()

        if audio_container:
            text_area.insert(tk.END, "Procesando el audio...\n")
            combined_audio = sr.AudioData(
                b"".join(a.frame_data for a in audio_container),
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

# Crear la interfaz gráfica mejorada
root = tk.Tk()
root.title("Transcripción de Voz a Texto")
root.configure(bg="#333")  # Fondo oscuro

# Forzar colores de botones en macOS
root.option_add("*Button.highlightBackground", "#333")
root.option_add("*Button.highlightColor", "#333")

frame = tk.Frame(root, bg="#333")
frame.pack(pady=10, padx=10)

# Estilos para `ttk.Button`
style = ttk.Style()
style.configure("TButton", font=("Arial", 12, "bold"), padding=5)
style.map("TButton",
          background=[("active", "darkgreen"), ("!disabled", "green")],
          foreground=[("active", "white"), ("!disabled", "white")])

style.map("Red.TButton",
          background=[("active", "darkred"), ("!disabled", "red")],
          foreground=[("active", "white"), ("!disabled", "white")])

# Contenedor de botones
button_frame = tk.Frame(frame, bg="#333")
button_frame.pack(pady=5)

# Botón de inicio con `ttk.Button`
start_button = ttk.Button(button_frame, text="Iniciar Grabación", command=on_start_button_click, style="TButton")
start_button.pack(pady=5)

# Botón de detener con `ttk.Button`
stop_var = tk.IntVar()
stop_button = ttk.Button(button_frame, text="Detener Grabación", command=on_stop_button_click, style="Red.TButton")
stop_button.pack(pady=5)

# Área de texto con colores mejorados
text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=15, bg="white", fg="black", font=("Arial", 11))
text_area.pack(expand=True, fill=tk.BOTH, pady=10, padx=10)

root.geometry("700x450")
root.mainloop()