import json
import pytest
from cloudevents.http import CloudEvent
from main import process_gcs

# -----------------------------------------------------------------------------
# Helper: make_event
# -----------------------------------------------------------------------------
# Función auxiliar para simular un evento de Cloud Storage como lo recibe
# la Cloud Function. Devuelve un objeto CloudEvent con los datos codificados
# en bytes, que es el formato real que llega en Cloud Functions Gen 2.
# -----------------------------------------------------------------------------
def make_event(data: dict):
    attributes = {
        "id": "1234",  # ID de evento simulado
        "source": "//storage.googleapis.com/projects/_/buckets/test-bucket",
        "type": "google.cloud.storage.object.v1.finalized",
    }
    # json.dumps -> convierte dict a string, .encode("utf-8") -> bytes
    return CloudEvent(attributes, json.dumps(data).encode("utf-8"))

# -----------------------------------------------------------------------------
# Test caso exitoso
# -----------------------------------------------------------------------------
# Este test simula la subida de un archivo válido al bucket y verifica que
# la función procese correctamente los metadatos y devuelva el dict esperado.
# -----------------------------------------------------------------------------
def test_process_gcs_success():
    event = make_event({
        "bucket": "test-bucket",
        "name": "archivo.txt",
        "size": "1234",
        "contentType": "text/plain"
    })

    result = process_gcs(event)

    # Validaciones
    assert result["ok"] is True                  # Flujo correcto
    assert result["file"] == "archivo.txt"      # Nombre del archivo correcto

# -----------------------------------------------------------------------------
# Test caso error
# -----------------------------------------------------------------------------
# Este test simula un evento incompleto (sin nombre de archivo). La función
# debe levantar un ValueError según la validación que implementamos.
# -----------------------------------------------------------------------------
def test_process_gcs_missing_name():
    event = make_event({
        "bucket": "test-bucket"
        # falta "name"
    })

    # Verifica que se lance un ValueError
    with pytest.raises(ValueError):
        process_gcs(event)
