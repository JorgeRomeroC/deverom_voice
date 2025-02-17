import os
import time
import speech_recognition as sr
import threading
import tkinter as tk
from tkinter import ttk, scrolledtext
from PIL import Image, ImageTk  # Para manejar imágenes


class VoiceTranscriptionApp:
    def __init__(self, root):
        """Inicializa la aplicación de transcripción de voz a texto."""
        self.root = root
        self.root.title("Transcripción de Voz a Texto")
        self.root.configure(bg="#333")  # Fondo oscuro
        self.root.attributes("-topmost", True)  # Mantener siempre arriba

        self.recording = False
        self.audio_container = []
        self.recognizer = sr.Recognizer()
        self.transcribed_text = ""  # **Almacenar solo la transcripción final**

        self.configure_styles()
        self.create_widgets()
        self.center_window(700, 580)  # Ajuste para incluir el botón "Copiar Texto"

    def configure_styles(self):
        """Configura los estilos de la interfaz."""
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 14, "bold"), padding=12)
        style.map("TButton",
                  background=[("active", "darkgreen"), ("!disabled", "green")],
                  foreground=[("active", "white"), ("!disabled", "white")])

        style.map("Red.TButton",
                  background=[("active", "darkred"), ("!disabled", "red")],
                  foreground=[("active", "white"), ("!disabled", "white")])

    def create_widgets(self):
        """Crea los elementos de la interfaz gráfica."""
        top_frame = tk.Frame(self.root, bg="#333")
        top_frame.pack(fill=tk.X, padx=10, pady=5, anchor="w")

        # **Cargar la imagen del logo**
        logo_path = "img/logo-deverom.png"
        if os.path.exists(logo_path):
            try:
                image = Image.open(logo_path)
                image = image.resize((50, 50), Image.Resampling.LANCZOS)
                self.logo = ImageTk.PhotoImage(image)
                self.logo_label = tk.Label(top_frame, image=self.logo, bg="#333")
                self.logo_label.pack(side=tk.LEFT, padx=10)
            except Exception as e:
                print(f"⚠ Error al cargar la imagen: {e}")

        # **Texto "Deverom"**
        self.brand_label = tk.Label(top_frame, text="Deverom", fg="white", bg="#333",
                                    font=("Arial", 14, "bold"))
        self.brand_label.pack(side=tk.LEFT, anchor="w")

        # **Botones**
        frame = tk.Frame(self.root, bg="#333")
        frame.pack(pady=15, padx=10)

        button_frame = tk.Frame(frame, bg="#333")
        button_frame.pack(pady=5)

        self.start_button = ttk.Button(button_frame, text=" 🎤 Iniciar Grabación", command=self.start_recording, style="TButton")
        self.start_button.pack(pady=8, ipadx=15, ipady=10)

        self.stop_var = tk.IntVar()
        self.stop_button = ttk.Button(button_frame, text=" ⏹ Detener Grabación", command=self.stop_recording, style="Red.TButton")
        self.stop_button.pack(pady=8, ipadx=15, ipady=10)

        self.help_label = tk.Label(frame, text="Habla con claridad y a un ritmo moderado para mejorar la precisión de la transcripción.",
                                   fg="white", bg="#333", font=("Arial", 11, "italic"))
        self.help_label.pack(pady=5)

        # **Área de texto**
        text_frame = tk.Frame(self.root, bg="#333")
        text_frame.pack(expand=True, fill=tk.BOTH, pady=0, padx=0)

        self.scrollbar = ttk.Scrollbar(text_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.text_area = scrolledtext.ScrolledText(text_frame, wrap=tk.WORD, width=60, height=15,
                                                   bg="white", fg="black", font=("Arial", 11),
                                                   borderwidth=0, highlightthickness=0,
                                                   yscrollcommand=self.scrollbar.set)
        self.text_area.pack(expand=True, fill=tk.BOTH)
        self.scrollbar.config(command=self.text_area.yview)

        # **Botón "Copiar Texto"**
        self.copy_button = ttk.Button(self.root, text="📋 Copiar Texto", command=self.copy_to_clipboard, style="TButton")
        self.copy_button.pack(pady=10, ipadx=15, ipady=10)

    def center_window(self, width, height):
        """Centra la ventana en la pantalla."""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        position_x = (screen_width - width) // 2
        position_y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{position_x}+{position_y}")

    def copy_to_clipboard(self):
        """Copia **solo** el texto transcrito al portapapeles."""
        if self.transcribed_text.strip():
            self.root.clipboard_clear()
            self.root.clipboard_append(self.transcribed_text.strip())
            self.root.update()
            self.text_area.insert(tk.END, "\n✅ Texto copiado al portapapeles.\n")
        else:
            self.text_area.insert(tk.END, "\n⚠ No hay texto para copiar.\n")

    def start_recording(self):
        """Inicia la grabación de audio en un hilo separado."""
        self.recording = True
        self.audio_container = []
        self.transcribed_text = ""

        self.text_area.insert(tk.END, "Ajustando el ruido de fondo, por favor espera...\n")
        self.text_area.update_idletasks()

        self.audio_thread = threading.Thread(target=self.listen_for_audio)
        self.audio_thread.start()

    def stop_recording(self):
        """Detiene la grabación y procesa el audio."""
        self.recording = False
        self.audio_thread.join()
        self.process_audio()

    def listen_for_audio(self):
        """Escucha el audio dentro del hilo y guarda los fragmentos grabados."""
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=2)  
            self.text_area.insert(tk.END, "Listo! Puedes hablar.\n")
            self.text_area.update_idletasks()

            time.sleep(1)  # **Retraso antes de grabar para evitar capturar ruido ambiental**

            while self.recording:
                try:
                    audio = self.recognizer.listen(source, phrase_time_limit=5)
                    if audio:
                        self.audio_container.append(audio)
                except sr.WaitTimeoutError:
                    continue

    def process_audio(self):
        """Procesa el audio grabado y transcribe el texto."""
        self.text_area.insert(tk.END, "\nProcesando el audio...\n")
        self.text_area.update_idletasks()

        if self.audio_container:
            try:
                text = self.recognizer.recognize_google(self.audio_container[0], language='es-ES')
                self.transcribed_text = text  
                self.text_area.insert(tk.END, f"\n📝 {text}\n")
            except sr.UnknownValueError:
                self.text_area.insert(tk.END, "❌ No se pudo entender el audio.\n")
            except sr.RequestError as e:
                self.text_area.insert(tk.END, f"⚠ Error en la transcripción: {e}\n")
        else:
            self.text_area.insert(tk.END, "⚠ No se detectó ningún audio.\n")


if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceTranscriptionApp(root)
    root.mainloop()