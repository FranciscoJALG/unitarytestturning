import json
from cloudevents.http import CloudEvent

# -----------------------------------------------------------------------------
# Cloud Function: process_gcs
# -----------------------------------------------------------------------------
# Esta función se ejecuta automáticamente cada vez que un archivo es subido a
# un bucket de Cloud Storage configurado como trigger.
#
# Flujo:
#  1. Recibe un evento tipo CloudEvent desde GCP.
#  2. Extrae metadatos básicos del archivo subido (nombre, tamaño, tipo, bucket).
#  3. Registra los metadatos en Cloud Logging con un formato estructurado JSON.
#  4. Incluye validaciones y manejo de errores para mayor robustez.
#
# Decisiones técnicas:
#  - Se usa `print(json.dumps(...))` porque en Cloud Functions esto se envía
#    directamente a Cloud Logging en formato estructurado.
#  - Se implementa validación de campos mínimos (`bucket` y `name`) para evitar
#    procesar eventos incompletos.
#  - Se utiliza try/except para capturar cualquier excepción y dejarla registrada
#    en los logs antes de propagar el error.
#
# Entrada:
#  - cloud_event (CloudEvent): evento enviado por Cloud Storage.
#
# Salida:
#  - dict: {"ok": True, "file": <nombre_archivo>} en caso exitoso.
#  - Excepción (ValueError u otra) en caso de error.
# -----------------------------------------------------------------------------
def process_gcs(cloud_event: CloudEvent):
    try:
        # Extraemos el payload del evento (metadatos del archivo en JSON)
          # Decodificar el payload si viene en bytes
        if isinstance(cloud_event.data, (bytes, bytearray)):
            data = json.loads(cloud_event.data.decode("utf-8"))
        else:
            data = cloud_event.data or {}

        # Se obtienen los campos más importantes
        bucket = data.get("bucket")            # Nombre del bucket origen
        name = data.get("name")                # Nombre del archivo
        size = int(data.get("size", 0))        # Tamaño en bytes (default: 0)
        content_type = data.get("contentType", "unknown")  # Tipo MIME

        # Se registran los metadatos en Cloud Logging
        # Formato JSON estructurado -> facilita búsquedas en Logs Explorer
        print(json.dumps({
            "severity": "INFO",                 # Nivel de log
            "message": "gcs_object_finalized",  # Evento procesado
            "bucket": bucket,
            "name": name,
            "size": size,
            "content_type": content_type,
        }))

        # Validación básica: bucket y name son obligatorios
        if not bucket or not name:
            raise ValueError("Evento sin bucket o name")

        # Retorno para facilitar pruebas unitarias
        return {"ok": True, "file": name}

    except Exception as e:
        # Captura de cualquier error inesperado
        # Se deja registro en logs con nivel ERROR
        print(json.dumps({
            "severity": "ERROR",
            "message": "error_processing_gcs_event",
            "error": str(e),
        }))
        # Propagamos el error para que Cloud Functions lo marque como fallo
        raise