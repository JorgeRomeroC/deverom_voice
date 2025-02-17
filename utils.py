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