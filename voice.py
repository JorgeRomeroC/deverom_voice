import speech_recognition as sr
import threading
import tkinter as tk
from tkinter import ttk, scrolledtext

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

        self.configure_styles()
        self.create_widgets()
        self.center_window(700, 450)

    def configure_styles(self):
        """Configura los estilos para los botones y la barra de desplazamiento."""
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 12, "bold"), padding=5)
        style.map("TButton",
                  background=[("active", "darkgreen"), ("!disabled", "green")],
                  foreground=[("active", "white"), ("!disabled", "white")])

        style.map("Red.TButton",
                  background=[("active", "darkred"), ("!disabled", "red")],
                  foreground=[("active", "white"), ("!disabled", "white")])

        style.configure("Dark.Vertical.TScrollbar",
                        troughcolor="#333",
                        background="#333",
                        arrowcolor="#333",
                        borderwidth=0)

    def create_widgets(self):
        """Crea los elementos de la interfaz gráfica."""
        frame = tk.Frame(self.root, bg="#333")
        frame.pack(pady=10, padx=10)

        # Botones
        button_frame = tk.Frame(frame, bg="#333")
        button_frame.pack(pady=5)

        self.start_button = ttk.Button(button_frame, text="Iniciar Grabación", command=self.start_recording, style="TButton")
        self.start_button.pack(pady=5)

        self.stop_var = tk.IntVar()
        self.stop_button = ttk.Button(button_frame, text="Detener Grabación", command=lambda: self.stop_var.set(1), style="Red.TButton")
        self.stop_button.pack(pady=5)

        # Área de texto
        text_frame = tk.Frame(self.root, bg="#333")
        text_frame.pack(expand=True, fill=tk.BOTH, pady=0, padx=0)

        self.scrollbar = ttk.Scrollbar(text_frame, style="Dark.Vertical.TScrollbar")
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.text_area = scrolledtext.ScrolledText(text_frame, wrap=tk.WORD, width=60, height=15,
                                                   bg="white", fg="black", font=("Arial", 11),
                                                   borderwidth=0, highlightthickness=0,
                                                   yscrollcommand=self.scrollbar.set)
        self.text_area.pack(expand=True, fill=tk.BOTH)
        self.scrollbar.config(command=self.text_area.yview)

    def center_window(self, width, height):
        """Centra la ventana en la pantalla."""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        position_x = (screen_width - width) // 2
        position_y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{position_x}+{position_y}")

    def listen_for_audio(self, recognizer, source):
        """Escucha el audio sin cortar la grabación hasta que el usuario lo detenga."""
        self.text_area.insert(tk.END, "Di algo para escribirlo! (Presiona ENTER para detener)\n")
        recognizer.energy_threshold = 100  # Ajusta la sensibilidad del micrófono
        recognizer.dynamic_energy_threshold = True  # Permite ajuste dinámico

        while self.recording:
            try:
                # Captura sin límite de tiempo y sin interrupciones
                audio = recognizer.listen(source, phrase_time_limit=None)  
                if audio:
                    self.audio_container.append(audio)
            except sr.WaitTimeoutError:
                continue

    def stop_recording(self):
        """Detiene la grabación cuando el usuario presiona el botón de detener."""
        self.recording = False

    def start_recording(self):
        """Inicia la grabación de audio con mejor calidad y procesamiento."""
        self.recording = True
        self.audio_container = []

        with sr.Microphone() as source:
            self.text_area.insert(tk.END, "Ajustando el ruido de fondo, por favor espera...\n")
            self.recognizer.adjust_for_ambient_noise(source, duration=2)  # Ajuste de ruido mejorado
            self.text_area.insert(tk.END, "Listo! Puedes hablar.\n")

            audio_thread = threading.Thread(target=self.listen_for_audio, args=(self.recognizer, source))
            audio_thread.start()

            self.stop_button.wait_variable(self.stop_var)
            self.stop_recording()
            audio_thread.join()

            self.process_audio()

    def process_audio(self):
        """Procesa el audio grabado y transcribe el texto."""
        if self.audio_container:
            self.text_area.insert(tk.END, "Procesando el audio...\n")
            
            # Concatenar todos los fragmentos de audio en uno solo
            combined_audio = sr.AudioData(
                b"".join(a.frame_data for a in self.audio_container),
                self.audio_container[0].sample_rate,
                self.audio_container[0].sample_width
            )

            try:
                text = self.recognizer.recognize_google(combined_audio, language='es-ES')
                self.text_area.insert(tk.END, f"Has dicho: {text}\n")
            except sr.RequestError as e:
                self.text_area.insert(tk.END, f"No se pudo solicitar resultados de Google Speech Recognition; {e}\n")
            except sr.UnknownValueError:
                self.text_area.insert(tk.END, "Google Speech Recognition no pudo entender el audio\n")
        else:
            self.text_area.insert(tk.END, "No se detectó ningún audio.\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceTranscriptionApp(root)
    root.mainloop()