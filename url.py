import oci  #type: ignore
from oci.config import from_file    #type: ignore
from oci.object_storage import ObjectStorageClient    #type: ignore
from datetime import datetime, timedelta

# Configura el cliente de Object Storage
config = oci.config.from_file()  # Carga la configuración desde el archivo .oci/config
object_storage_client = ObjectStorageClient(config)

# Parámetros
namespace = object_storage_client.get_namespace().data  # Namespace
bucket_name = 'fotos-web'  # Nombre del bucket
object_name = 'gansito.png'  # Nombre del objeto
region = config['region']  # Región de tu bucket (extraída del archivo de configuración)


# Construir la URL
url = f"https://objectstorage.{region}.oraclecloud.com/n/{namespace}/b/{bucket_name}/o/{object_name}"
print(f"URL pública para acceder al objeto: {url}")
