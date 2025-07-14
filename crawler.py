print("Crawler gestartet")
import os
from azure.storage.blob import BlobServiceClient

connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
print("Verbindung zur Azure Blob Storage wird getestet...")

try:
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    print("✅ Verbindung erfolgreich!")

    container_name = "itlandcontainer2"
    container_client = blob_service_client.get_container_client(container_name)

    blob_name = "test.txt"
    blob_data = "Crawler erfolgreich gestartet."

    container_client.upload_blob(name=blob_name, data=blob_data, overwrite=True)
    print(f"✅ Datei '{blob_name}' erfolgreich hochgeladen.")

except Exception as e:
    print(f"❌ Fehler: {e}")
