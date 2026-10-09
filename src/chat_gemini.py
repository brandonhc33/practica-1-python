"""Ejemplo sencillo para conversar con Gemini desde la terminal."""

import os  # Permite leer variables de entorno, como API_KEY.
import sys  # Permite leer la pregunta escrita después del comando.
from pathlib import Path  # Ayuda a construir la ruta del archivo .env.

from dotenv import load_dotenv  # Carga las variables del archivo .env.
from google import genai  # SDK de Google para comunicarnos con Gemini.
from google.genai import errors  # Errores que puede devolver la API.
from httpx import HTTPError  # Errores de conexión a Internet.


def main():
    # El .env está en la raíz del proyecto, un nivel por encima de src/.
    # Usar la ruta del script permite encontrarlo desde cualquier carpeta.
    carpeta_proyecto = Path(__file__).resolve().parent.parent
    load_dotenv(carpeta_proyecto / ".env")

    # Leemos la llave sin escribirla en el código ni mostrarla en pantalla.
    api_key = os.getenv("API_KEY", "").strip()
    if not api_key:
        raise SystemExit("Falta API_KEY. Revisa el archivo .env del proyecto.")

    # Puedes cambiar el modelo agregando GEMINI_MODEL en tu .env.
    modelo = os.getenv("GEMINI_MODEL", "").strip() or "gemini-3.5-flash-lite"

    # El cliente usa tu llave para conectarse a Gemini.
    # 'with' cierra la conexión al terminar, incluso si ocurre un error.
    with genai.Client(api_key=api_key) as cliente:
        # El chat conserva el historial mientras este programa esté abierto.
        chat = cliente.chats.create(model=modelo)

        # Si escribiste una pregunta en el comando, respondemos y terminamos.
        # Ejemplo: python src/chat_gemini.py "¿Qué es una variable?"
        if len(sys.argv) > 1:
            pregunta = " ".join(sys.argv[1:]).strip()
            if not pregunta:
                raise SystemExit("Escribe una pregunta que no esté vacía.")
            respuesta = chat.send_message(pregunta)
            print(respuesta.text or "Gemini no devolvió una respuesta de texto.")
            return

        print(f"Chat con Gemini ({modelo}). Escribe 'salir' para terminar.\n")

        # Sin una pregunta en el comando, conversamos en un ciclo.
        while True:
            pregunta = input("Tú: ").strip()

            if pregunta.lower() == "salir":
                print("¡Hasta luego!")
                break  # Sale del ciclo y termina el programa.

            if not pregunta:
                continue  # Si solo presionaste Enter, vuelve a preguntar.

            # Aquí se envía tu pregunta a Gemini y se espera su respuesta.
            respuesta = chat.send_message(pregunta)
            texto = respuesta.text or "Gemini no devolvió una respuesta de texto."
            print(f"\nGemini: {texto}\n")


# Ejecutamos main() solamente cuando se inicia este archivo como programa.
if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        # Ctrl+C o el fin de la entrada permiten cerrar el chat sin un traceback.
        print("\nChat terminado.")
    except errors.APIError as error:
        # Mostramos el código del error, sin imprimir credenciales.
        print(
            f"Error de Gemini (HTTP {error.code}). "
            "Revisa tu API_KEY, el modelo y la cuota de tu cuenta.",
            file=sys.stderr,
        )
        raise SystemExit(1)
    except HTTPError:
        print("No se pudo conectar con Gemini. Revisa tu conexión a Internet.", file=sys.stderr)
        raise SystemExit(1)
