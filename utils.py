import speech_recognition as sr

def copy_to_clipboard(app):
    """Copia el texto transcrito."""
    text = app.text_area.get("1.0", "end-1c").strip()
    if text:
        app.root.clipboard_clear()
        app.root.clipboard_append(text)
        app.root.update()
        app.text_area.insert("end", "\n✅ Copiado al portapapeles.\n")

def clear_text(app):
    """Limpia el área de transcripción."""
    app.text_area.delete("1.0", "end")

def process_audio(app, audio_container):
    """Procesa y transcribe el audio."""
    app.text_area.insert("end", "🔄 Procesando el audio...\n")
    app.text_area.update_idletasks()  # Actualizar la UI

    if audio_container:
        combined_audio = sr.AudioData(
            b"".join(a.frame_data for a in audio_container),  # Concatenar los fragmentos de audio
            audio_container[0].sample_rate,
            audio_container[0].sample_width
        )
        try:
            text = sr.Recognizer().recognize_google(combined_audio, language='es-ES')
            app.text_area.insert("end", f"📝 {text.capitalize()}\n")
        except sr.UnknownValueError:
            app.text_area.insert("end", "❌ No se pudo entender el audio.\n")
        except sr.RequestError as e:
            app.text_area.insert("end", f"⚠ Error en la transcripción: {e}\n")
    else:
        app.text_area.insert("end", "⚠ No se detectó audio.\n")

    app.text_area.update_idletasks()