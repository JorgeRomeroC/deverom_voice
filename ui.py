import os
import tkinter as tk
from tkinter import ttk, scrolledtext
from PIL import Image, ImageTk  # Para manejar imágenes
from config import WINDOW_WIDTH, WINDOW_HEIGHT
from utils import copy_to_clipboard, clear_text
from recorder import AudioRecorder

class VoiceTranscriptionApp:
    def __init__(self, root):
        """Inicializa la aplicación de transcripción de voz a texto."""
        self.root = root
        self.root.title("Transcripción de Voz a Texto")
        self.root.configure(bg="#333")  
        self.root.attributes("-topmost", True)  
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.resizable(False, False)

        self.recorder = AudioRecorder(self)  # Instancia del grabador

        self.configure_styles()
        self.create_widgets()

    def configure_styles(self):
        """Configura los estilos de los botones."""
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 14, "bold"), padding=12)
        style.map("TButton", background=[("active", "darkgreen"), ("!disabled", "green")], foreground=[("active", "white")])

        style.map("Red.TButton", background=[("active", "darkred"), ("!disabled", "red")], foreground=[("active", "white")])

    def create_widgets(self):
        """Crea la interfaz gráfica."""
        top_frame = tk.Frame(self.root, bg="#333")
        top_frame.pack(fill=tk.X, padx=10, pady=5, anchor="w")

        logo_path = "img/logo_deverom.png"
        if os.path.exists(logo_path):
            try:
                image = Image.open(logo_path)
                image = image.resize((50, 50), Image.Resampling.LANCZOS)
                self.logo = ImageTk.PhotoImage(image)
                self.logo_label = tk.Label(top_frame, image=self.logo, bg="#333")
                self.logo_label.pack(side=tk.LEFT, padx=10)
            except Exception as e:
                print(f"⚠ Error al cargar la imagen del logo: {e}")

        self.brand_label = tk.Label(top_frame, text="Deverom", fg="white", bg="#333", font=("Arial", 14, "bold"))
        self.brand_label.pack(side=tk.LEFT, anchor="w")

        frame = tk.Frame(self.root, bg="#333")
        frame.pack(pady=15, padx=10)

        button_frame = tk.Frame(frame, bg="#333")
        button_frame.pack(pady=5)

        self.start_button = ttk.Button(button_frame, text=" 🎤 Iniciar Grabación", command=self.recorder.start_recording, style="TButton")
        self.start_button.pack(pady=5, ipadx=15, ipady=10)

        self.stop_button = ttk.Button(button_frame, text=" ⏹ Detener Grabación", command=self.recorder.stop_recording, style="Red.TButton")
        self.stop_button.pack(pady=5, ipadx=15, ipady=10)

        self.help_label = tk.Label(frame, text="Habla con claridad y a un ritmo moderado para mejorar la precisión.", fg="white", bg="#333", font=("Arial", 13, "italic"))
        self.help_label.pack(pady=5)

        text_frame = tk.Frame(self.root, bg="#333")
        text_frame.pack(expand=True, fill=tk.BOTH, pady=0, padx=0)

        self.scrollbar = ttk.Scrollbar(text_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.text_area = scrolledtext.ScrolledText(text_frame, wrap=tk.WORD, width=60, height=15, bg="white", fg="black", font=("Arial", 13), borderwidth=0, highlightthickness=0, yscrollcommand=self.scrollbar.set)
        self.text_area.pack(expand=True, fill=tk.BOTH)
        self.scrollbar.config(command=self.text_area.yview)

        button_container = tk.Frame(self.root, bg="#333")
        button_container.pack(pady=10)

        self.copy_button = ttk.Button(button_container, text="📋 Copiar Texto", command=lambda: copy_to_clipboard(self), style="TButton")
        self.copy_button.pack(side=tk.LEFT, padx=5, ipadx=15, ipady=10)

        self.clear_button = ttk.Button(button_container, text="🗑 Limpiar Texto", command=lambda: clear_text(self), style="Red.TButton")
        self.clear_button.pack(side=tk.LEFT, padx=5, ipadx=15, ipady=10)