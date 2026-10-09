# Hablar con Gemini desde la terminal

Este ejemplo permite hacer una pregunta con un comando o mantener una conversación por texto. El código está en [`src/chat_gemini.py`](../src/chat_gemini.py) y tiene comentarios para explicar cada paso.

## 1. Preparar el entorno

Abre una terminal en la carpeta del proyecto: `practica-1-python`.

Ya tienes el entorno `.venv` creado. Actívalo en Linux o macOS:

```bash
source .venv/bin/activate
```

Si estás preparando una copia nueva del proyecto y todavía no existe `.venv`, créalo primero con `python3 -m venv .venv` y luego actívalo.

Instala las dependencias:

```bash
python -m pip install -r requirements.txt
```

Las dos librerías principales de este ejemplo son:

- `google-genai`: se comunica con la API de Gemini.
- `python-dotenv`: lee las variables del archivo `.env`.

## 2. Usar tu llave

Tu `.env` ya está configurado. El programa busca una variable llamada exactamente `API_KEY`:

```dotenv
API_KEY=tu_llave_real
```

Este bloque solo muestra el formato; conserva la llave que ya tienes. El programa lee ese archivo automáticamente y pasa la llave al cliente de Gemini. `.env` está excluido de Git mediante `.gitignore`.

## 3. Hacer una pregunta con un comando

```bash
python src/chat_gemini.py "Explícame qué es una variable en Python con un ejemplo simple"
```

Gemini responde en la terminal y el programa termina. Las comillas agrupan tu pregunta en un solo argumento. Cada ejecución comienza una conversación nueva.

Otro ejemplo:

```bash
python src/chat_gemini.py "¿Cuál es la diferencia entre una lista y un diccionario?"
```

## 4. Conversar con varias preguntas

Ejecuta el programa sin una pregunta:

```bash
python src/chat_gemini.py
```

Cuando aparezca `Tú:`, escribe tu mensaje y presiona Enter. Por ejemplo:

```text
Tú: Estoy aprendiendo Python. Explícame qué es una función.
Gemini: [Aquí aparecerá la respuesta de Gemini]

Tú: Ahora dame un ejemplo de lo que acabas de explicar.
Gemini: [Aquí aparecerá otra respuesta usando el contexto anterior]

Tú: salir
¡Hasta luego!
```

El chat recuerda los mensajes mientras el programa está abierto. Al cerrarlo, el historial local se pierde; este ejemplo no lo guarda en un archivo. También puedes salir con Ctrl+C. Si presionas Enter sin escribir nada, no se envía ninguna consulta.

## 5. Entender el código

Estos son los pasos que realiza `main()`:

1. `Path(__file__)` ubica el script y permite encontrar el `.env` en la raíz del proyecto.
2. `load_dotenv(...)` carga las variables del `.env`. Si ya existe una variable del mismo nombre en tu terminal, conserva ese valor.
3. `os.getenv("API_KEY", "")` obtiene tu llave. Si está vacía, el programa termina con un mensaje explicativo.
4. `genai.Client(api_key=api_key)` crea el cliente que enviará las consultas a Google.
5. `cliente.chats.create(model=modelo)` crea una conversación y administra su historial.
6. `sys.argv[1:]` obtiene las palabras que escribiste después del nombre del archivo. Si hay una pregunta, se envía una sola vez.
7. `while True` mantiene abierto el chat. `input()` lee tu mensaje; `break` sale del ciclo y `continue` omite una entrada vacía.
8. `chat.send_message(pregunta)` envía el mensaje; `respuesta.text` contiene el texto que mostramos con `print()`.

El bloque `if __name__ == "__main__":` inicia el programa cuando ejecutas este archivo directamente. Los bloques `except` muestran mensajes sencillos si interrumpes el programa, falla la API o hay un problema de conexión.

## 6. Cambiar el modelo (opcional)

El ejemplo usa `gemini-3.5-flash-lite`. Para elegir otro modelo, agrega esta variable a tu `.env`, debajo de tu llave:

```dotenv
GEMINI_MODEL=gemini-3.8-flash
```

Luego vuelve a ejecutar el programa. Los nombres y la disponibilidad se pueden consultar en el [catálogo oficial de modelos de Gemini](https://ai.google.dev/gemini-api/docs/models).

## 7. Resolver problemas comunes

| Mensaje o problema | Qué hacer |
| --- | --- |
| `No module named 'dotenv'` o falta `google.genai` | Activa `.venv` e instala las dependencias con `python -m pip install -r requirements.txt`. |
| `Falta API_KEY` | Comprueba que `.env` esté en la raíz del proyecto y contenga `API_KEY` con un valor. |
| Error HTTP 400 o 403 | Revisa que la llave sea válida para Gemini y tenga acceso a la API. |
| Error HTTP 404 | Comprueba el nombre del modelo y su disponibilidad para tu cuenta. |
| Error HTTP 429 | Revisa la cuota de tu cuenta; si alcanzaste un límite temporal, espera antes de volver a intentar. |
| No se pudo conectar | Revisa tu conexión a Internet y vuelve a ejecutar el programa. |

Cada pregunta hace una llamada a la API y usa la cuota de tu cuenta. Si ocurre un error de API o conexión, el programa termina; puedes iniciarlo otra vez cuando hayas resuelto la causa.

Para salir del entorno virtual cuando termines:

```bash
deactivate
```

Referencia del chat utilizado: [documentación oficial de conversaciones con Gemini](https://ai.google.dev/gemini-api/docs/generate-content/text-generation#multi-turn-conversations-chat).
