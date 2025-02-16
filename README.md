# 🗣️ Programa Python - Para traducir voz a texto en tiempo real

<p align="center">
  <img src="img/logo-deverom.png" alt="Deverom Logo" width="80" height="80"><br>
  <strong>Deverom - Jorge Romero C</strong>
</p>

Este script en Python permite grabar audio desde el micrófono y transcribirlo a texto utilizando **Google Speech Recognition**. La grabación se ejecuta en un hilo separado y puede detenerse presionando la tecla **ENTER**.

## 📌 **Características**
- Captura audio en tiempo real desde el micrófono 🎤
- Usa **hilos (`threading`)** para escuchar y capturar entrada del usuario simultáneamente.
- **Reduce el ruido de fondo** antes de iniciar la grabación.
- **Concatenación de fragmentos de audio** para mejorar la precisión de la transcripción.
- Procesa el audio y lo convierte en texto usando **Google Speech Recognition API**.
- **Detención manual** con la tecla **ENTER**.

---

## 🛠️ **Requisitos y Dependencias**
Antes de ejecutar el script, asegúrate de tener instaladas las siguientes dependencias:

### 📦 **Librerías necesarias**
Este script usa las siguientes librerías de Python:

| Librería               | Descripción |
|------------------------|------------|
| `speech_recognition`   | Permite el reconocimiento de voz. |
| `threading`           | Manejo de múltiples hilos para escuchar y procesar el audio en paralelo. |

### 🔧 **Instalación**

Clona este repositorio en tu máquina local:
```bash
  git clone 
```

Crear un entorno virtual:
```bash
  python -m venv venv
```

Activa el entorno virtual:
```bash
  source venv/bin/activate
```
Ejecuta el siguiente comando para instalar las dependencias:

```bash
  pip install -r requirements.txt
```

Ejecuta el script:

```bash
  python voice.py
```