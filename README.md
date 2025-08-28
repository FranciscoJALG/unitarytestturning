📂 Proyecto: Cloud Function con Google Cloud Storage
📌 Descripción

Este proyecto implementa una Cloud Function en Google Cloud Platform (GCP) que se activa automáticamente cuando se carga un archivo en un bucket de Cloud Storage.
La función procesa el evento recibido y genera logs para verificar su correcto funcionamiento.

Se incluye además:

Configuración de ciclo de vida en el bucket.
<img width="1554" height="687" alt="image" src="https://github.com/user-attachments/assets/8304f6e7-5c3f-49f1-9b90-6bccb4fb17ec" />

<img width="1011" height="191" alt="image" src="https://github.com/user-attachments/assets/d5cae1cc-a0b2-4d93-96fe-a381ecf21af6" />


Pruebas unitarias para validar el flujo exitoso y el manejo de errores.
<img width="1508" height="847" alt="image" src="https://github.com/user-attachments/assets/d71aed8f-eefa-4e15-95ae-0aeb5d28099e" />


Documentación del flujo de trabajo.

[ Usuario sube archivo ]
           │
           ▼
[ Bucket de GCS ]  --->  [ Cloud Function (process_gcs) ]
           │
           ▼
[ Logs / Procesamiento ]

⚙️ Requisitos

Cuenta en Google Cloud Platform con permisos para:

Cloud Functions

Cloud Storage

Google Cloud SDK o acceso a Google Cloud Console

Python 3.10+

Librerías:

google-cloud-storage

cloudevents

pytest

🚀 Despliegue de la Cloud Function

Clonar el repositorio:

git clone https://github.com/usuario/repositorio.git
cd repositorio/functions/python


Crear un entorno virtual y activarlo:

python3 -m venv venv
source venv/bin/activate


Instalar dependencias:

pip install -r requirements.txt


Desplegar la Cloud Function en GCP:

gcloud functions deploy process_gcs \
    --runtime python310 \
    --trigger-event google.storage.object.finalize \
    --trigger-resource NOMBRE_DEL_BUCKET

<img width="1906" height="795" alt="image" src="https://github.com/user-attachments/assets/6c9c1c50-3070-482d-8cfb-8f853f18af5f" />

🧪 Ejecución de Pruebas Unitarias

Desde la carpeta functions/python/, exportar el PYTHONPATH:

export PYTHONPATH=$(pwd)


Ejecutar pytest:

pytest -v tests/


Ejemplo de salida esperada:

<img width="1299" height="188" alt="image" src="https://github.com/user-attachments/assets/37b5a884-4eff-4732-88e0-d5a4ac894f9e" />


📊 Flujo de Trabajo

📌 Diagrama simplificado del flujo:

<img width="382" height="532" alt="FlujoCouldFunction drawio" src="https://github.com/user-attachments/assets/e33ca6ca-0ab7-466a-b7aa-2028b7e21da7" />


📂 Estructura del Proyecto

<img width="349" height="334" alt="image" src="https://github.com/user-attachments/assets/cc7a1f44-0e48-467b-95f4-30278403326b" />


✍️ Notas de Implementación

Se utilizó cloudevents.http.CloudEvent para simular eventos en pruebas.

El bucket cuenta con política de ciclo de vida para automatizar la gestión de archivos.

Los comentarios en main.py explican las decisiones técnicas y manejo de errores.

👨‍💻 Autor

Francisco Javier Alcala Guzmán

Proyecto de práctica con Google Cloud Functions y QA
