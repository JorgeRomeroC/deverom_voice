# 🗣️ Programa Python - Transcripción de Voz a Texto en Tiempo Real

<p align="center">
  <img src="img/logo_deverom.png" alt="Deverom Logo" width="80" height="80"><br>
  <strong>Deverom - Jorge Romero C</strong>
</p>

Este programa en **Python** captura audio en tiempo real desde el micrófono y lo transcribe a texto utilizando **Google Speech Recognition**.  

✅ **Interfaz gráfica avanzada con botones interactivos**  
✅ **Procesamiento de audio optimizado para mejor precisión**  
✅ **Opciones de copiar y limpiar el texto transcrito**  
✅ **Código refactorizado en clases y funciones para mayor escalabilidad**  

---

## 📌 **Características**
- 🎤 **Captura de audio en tiempo real** desde el micrófono.
- 🚀 **Interfaz gráfica interactiva** desarrollada con `tkinter`.
- 🔄 **Procesamiento de audio mejorado** para mayor precisión y reducción de ruido.
- 📋 **Opción de copiar el texto transcrito** al portapapeles con un solo clic.
- 🗑️ **Botón para limpiar la transcripción** y reiniciar el área de texto.
- 🎨 **Diseño mejorado** con botones estilizados e iconos.
- 🧵 **Uso de hilos (`threading`)** para evitar bloqueos en la interfaz.
- 📝 **Formato mejorado del texto** (primera letra en mayúscula).
- 🔧 **Código modularizado y refactorizado** en clases para mayor escalabilidad.

---

## 🖥️ **Interfaz del Programa**
<p align="center">
  <img src="img/interfaz.png" alt="Interfaz del Programa" width="700">
</p>

La interfaz cuenta con:
1. **Botón Iniciar Grabación 🎤**: Comienza la transcripción de audio en tiempo real.
2. **Botón Detener Grabación ⏹️**: Finaliza la grabación y procesa el texto.
3. **Mensaje de estado**: Indica cuando el audio está siendo procesado.
4. **Área de transcripción**: Muestra el texto detectado por el programa.
5. **Botón Copiar Texto 📋**: Permite copiar solo el texto transcrito al portapapeles.
6. **Botón Limpiar 🗑️**: Borra el contenido del área de transcripción.

---

## 🛠️ **Requisitos y Dependencias**
Antes de ejecutar el script, asegúrate de tener instaladas las siguientes dependencias:

### 📦 **Librerías necesarias**
Este programa usa las siguientes librerías de Python:

| Librería               | Descripción |
|------------------------|------------|
| `speech_recognition`   | Permite el reconocimiento de voz. |
| `threading`           | Manejo de múltiples hilos para escuchar y procesar el audio en paralelo. |
| `tkinter`             | Construcción de la interfaz gráfica. |
| `pillow`              | Manejo de imágenes dentro de la GUI. |

---

## 🛠️ **Requisitos y Dependencias**
Antes de ejecutar el script, asegúrate de tener instaladas las siguientes dependencias:

### 📦 **Librerías necesarias**
Este script usa las siguientes librerías de Python:

| Librería               | Descripción |
|------------------------|------------|
| `speech_recognition`   | Permite el reconocimiento de voz. |
| `threading`            | Manejo de múltiples hilos para escuchar y procesar el audio en paralelo. |
| `pillow`               | Manejo de imagenes y su procesamiento. |

### 🔧 **Instalación**

Clona este repositorio en tu máquina local:
```bash
  git clone <URL_DEL_REPOSITORIO>
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