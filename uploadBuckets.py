import oci  #type: ignore
from oci.config import from_file    #type: ignore
from oci.object_storage import ObjectStorageClient    #type: ignore

# Configura el cliente de Object Storage
config = oci.config.from_file()  # Carga la configuración desde el archivo .oci/config
object_storage_client = ObjectStorageClient(config)

# Parámetros de tu bucket
namespace = object_storage_client.get_namespace().data  # Obtén el namespace en el que trabajar
bucket_name = 'fotos-web'
file_path = "C:\\Users\\alana\\Downloads\\cajas.jpg"  # Ruta del archivo en tu máquina local
folder_name = 'Almacen'  # Nombre de la carpeta en la que se guardará el archivo
object_name = f'{folder_name}/cajas.jpg'  # Nombre del archivo dentro del bucket

region = config['region']  # Región de tu bucket (extraída del archivo de configuración)


try:
    # Abre el archivo que deseas subir
    with open(file_path, 'rb') as file_data:
        # Usa el cliente de Object Storage para subir el archivo
        object_storage_client.put_object(
            namespace,
            bucket_name,
            object_name,
            file_data
        )

        # url = f"https://objectstorage.{region}.oraclecloud.com/n/{namespace}/b/{bucket_name}/o/{object_name}"
        # print(f"URL pública para acceder al objeto: {url}")

    print(f"El archivo '{file_path}' se ha subido correctamente a '{bucket_name}' con el nombre '{object_name}'.")
except Exception as e:
    print(f"Ocurrió un error al intentar subir el archivo: {e}")
