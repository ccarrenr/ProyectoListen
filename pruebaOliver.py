import requests
import json
import time

def analyze_audio_streaming():
    try:
        # Configura clave API de Oliver
        api_key = "decc72dfb9515ad250e64c7ee7ad44ee"

        # Configura los encabezados de la solicitud
        headers = {
            "Authorization": "Bearer " + api_key,
        }

        # Abre una nueva sesión de streaming
        session_response = requests.post("https://api.behavioralsignals.com/1.0/streaming", headers=headers)

        # Comprueba si la solicitud fue exitosa
        if session_response.status_code == 200:
            # Decodifica la respuesta
            session_data = json.loads(session_response.text)

            # Obtiene el ID de la sesión
            session_id = session_data['id']

            # Inicia una nueva tarea de procesamiento
            task_response = requests.post(f"https://api.behavioralsignals.com/1.0/streaming/{session_id}/task", headers=headers)

            # Comprueba si la solicitud fue exitosa
            if task_response.status_code == 200:
                # Decodifica la respuesta
                task_data = json.loads(task_response.text)

                # Obtiene el ID de la tarea
                task_id = task_data['id']

                # Envía el audio y obtiene los resultados
                with open("audioPrueba1_mono.wav", "rb") as audio_file:
                    content = audio_file.read()
                    audio_response = requests.post(f"https://api.behavioralsignals.com/1.0/streaming/{session_id}/task/{task_id}/audio", headers=headers, data=content)

                # Comprueba si la solicitud fue exitosa
                if audio_response.status_code == 200:
                    # Decodifica la respuesta
                    audio_data = json.loads(audio_response.text)

                    # Imprime los resultados del análisis
                    print("Resultados del análisis: ", audio_data)
                else:
                    print("Ocurrió un error al enviar el audio: ", audio_response.text)

                # Termina la tarea y cierra la sesión
                end_response = requests.delete(f"https://api.behavioralsignals.com/1.0/streaming/{session_id}/task/{task_id}", headers=headers)

                # Comprueba si la solicitud fue exitosa
                if end_response.status_code != 200:
                    print("Ocurrió un error al terminar la tarea y cerrar la sesión: ", end_response.text)
            else:
                print("Ocurrió un error al iniciar la tarea de procesamiento: ", task_response.text)
        else:
            print("Ocurrió un error al abrir la sesión de streaming: ", session_response.text)
            print("Respuesta completa: ", session_response.content)
    except Exception as e:
        print("Ocurrió un error: ", e)

# Llama a la función para analizar el audio
analyze_audio_streaming()