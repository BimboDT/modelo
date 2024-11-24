import oci  #type: ignore
from oci.config import from_file    #type: ignore
from oci.object_storage import ObjectStorageClient    #type: ignore

# Configura el cliente de Object Storage
config = oci.config.from_file()  # Carga la configuración desde el archivo .oci/config
object_storage_client = ObjectStorageClient(config)

# Parámetros de tu bucket
namespace = object_storage_client.get_namespace().data  # Obtén el namespace en el que trabajar
bucket_name = 'fotos-web'
compartment_id=config['tenancy']
file_path = "C:\\Users\\alana\\Documents\\GitHub\\app-web\\bimbo-web\\src\\img\\gansito.png"  # Ruta del archivo en tu máquina local
object_name = 'gansito.png'  # Nombre del archivo dentro del bucket

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

    print(f"El archivo '{file_path}' se ha subido correctamente a '{bucket_name}' con el nombre '{object_name}'.")
except Exception as e:
    print(f"Ocurrió un error al intentar subir el archivo: {e}")
