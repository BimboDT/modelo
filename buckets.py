import oci  #type: ignore
from oci.config import from_file    #type: ignore
from oci.object_storage import ObjectStorageClient    #type: ignore

# Configura el cliente de Object Storage
config = oci.config.from_file()  # Carga la configuración desde el archivo .oci/config
object_storage_client = ObjectStorageClient(config)

# Parámetros de tu bucket
namespace = object_storage_client.get_namespace().data  # Obtén el namespace en el que trabajar
# print(f"Conectado a Object Storage en el namespace: {namespace}")
bucket_name = 'fotos-web'
compartment_id=config['tenancy']

try:
    # Lista todos los buckets en el namespace
    buckets = object_storage_client.list_buckets(namespace, compartment_id).data

    # Verifica si el bucket existe
    bucket_exists = any(bucket.name == bucket_name for bucket in buckets)

    if bucket_exists:
        print(f"El bucket '{bucket_name}' existe.")
    else:
        create_bucket_details = oci.object_storage.models.CreateBucketDetails(
            name=bucket_name,
            compartment_id=compartment_id
        )

        new_bucket = object_storage_client.create_bucket(namespace, create_bucket_details).data
        print(f"El bucket '{bucket_name}' fue creado exitosamente.")
except oci.exceptions.ServiceError as e:
    print(f"Error al acceder al servicio de Object Storage: {e}")