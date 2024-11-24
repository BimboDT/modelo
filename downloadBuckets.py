import oci  #type: ignore
from oci.config import from_file    #type: ignore
from oci.object_storage import ObjectStorageClient    #type: ignore

# Configura el cliente de Object Storage
config = oci.config.from_file()  # Carga la configuración desde el archivo .oci/config
object_storage_client = ObjectStorageClient(config)

# Parámetros de tu bucket y archivo
namespace = object_storage_client.get_namespace().data  # Obtiene el namespace
bucket_name = 'fotos-web'  # Nombre del bucket desde el que descargarás el archivo
object_name = 'gansito.png'  # Nombre del archivo dentro del bucket que deseas descargar
destination_path = f"C:\\Users\\alana\\Documents\\GitHub\\modelo\\{object_name}"  # Ruta local para guardar el archivo

# # Listar los objetos en el bucket
# try:
#     # Lista los objetos en el bucket
#     objects = object_storage_client.list_objects(namespace, bucket_name)

#     # Si hay objetos en el bucket, los imprime
#     if objects.data.objects:
#         print(f"Objetos en el bucket '{bucket_name}':")
#         for obj in objects.data.objects:
#             print(f"- {obj.name}")
#     else:
#         print(f"El bucket '{bucket_name}' está vacío.")
# except Exception as e:
#     print(f"Ocurrió un error al intentar listar los objetos: {e}")

# Descargar el archivo desde el bucket
try:
    # Obtén el archivo desde el bucket
    response = object_storage_client.get_object(namespace, bucket_name, object_name)

    # Guarda el archivo en la ruta de destino
    with open(destination_path, 'wb') as file:
        file.write(response.data.content)

    print(f"El archivo '{object_name}' se ha descargado correctamente a '{destination_path}'.")
except Exception as e:
    print(f"Ocurrió un error al intentar descargar el archivo: {e}")
