import speech_recognition as sr
import threading

recording = True  # Flag global para controlar la grabación


def listen_for_audio(recognizer, source, audio_container):
    """Escucha el audio mientras la grabación esté activa."""
    global recording
    print("Di algo, para escribirlo! (Presiona ENTER para detener)")

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
    input("Presiona ENTER para detener la grabación...\n")
    recording = False  # Cambia el flag para detener el bucle en `listen_for_audio`


def main():
    global recording
    r = sr.Recognizer()
    audio_container = []

    with sr.Microphone() as source:
        print("Ajustando el ruido de fondo, por favor espera...")
        r.adjust_for_ambient_noise(source, duration=1)  # Reduce el ruido ambiental
        print("Listo! Puedes hablar.")

        # Crear y ejecutar hilos
        audio_thread = threading.Thread(target=listen_for_audio, args=(r, source, audio_container))
        input_thread = threading.Thread(target=stop_recording)

        audio_thread.start()
        input_thread.start()

        input_thread.join()  # Espera a que el usuario presione ENTER
        audio_thread.join()  # Espera a que la grabación finalice

        # Procesar el audio grabado si hay contenido
        if audio_container:
            print("Procesando el audio...")
            combined_audio = sr.AudioData(
                b"".join(a.frame_data for a in audio_container),  # Concatenar los fragmentos de audio
                audio_container[0].sample_rate,
                audio_container[0].sample_width
            )

            try:
                text = r.recognize_google(combined_audio, language='es-ES')
                print(f"Has dicho: {text}")
            except sr.RequestError as e:
                print(f"No se pudo solicitar resultados de Google Speech Recognition; {e}")
            except sr.UnknownValueError:
                print("Google Speech Recognition no pudo entender el audio")
        else:
            print("No se detectó ningún audio.")


if __name__ == "__main__":
    main()