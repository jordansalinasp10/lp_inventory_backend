from azure.storage.blob import BlobServiceClient, BlobSasPermissions, generate_blob_sas
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
load_dotenv()

connect_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
container_name = os.getenv("DEFAULT_AZURE_CONTAINER_NAME")
account_name = os.getenv("AZURE_STORAGE_ACCOUNT_NAME")
account_key = os.getenv("AZURE_STORAGE_ACCOUNT_KEY")

def upload_image_to_azure(image_file, sku):
    blob_name = f"{sku}.jpg"
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    blob_client.upload_blob(image_file.read(), overwrite=True)
    return blob_client.url


def generate_signed_url(sku, expiry_minutes=30):
    blob_name = f"{sku}.jpg"
    expiry_time = datetime.utcnow() + timedelta(minutes=expiry_minutes)

    # Genera el SAS token
    sas_token = generate_blob_sas(
        account_name=account_name,
        account_key=account_key,
        container_name=container_name,
        blob_name=blob_name,
        permission=BlobSasPermissions(read=True),
        expiry=expiry_time
    )

    signed_url = f"https://{account_name}.blob.core.windows.net/{container_name}/{blob_name}?{sas_token}"
    return signed_url
