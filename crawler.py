import os
import json
from azure.storage.blob import BlobServiceClient
import requests

# Verbindung zu Azure Blob Storage
connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_client = blob_service_client.get_container_client("itlandcontainer2")

# Beispielseite abrufen und als JSON speichern
url = "https://it-land.net"
response = requests.get(url)

data = {
    "url": url,
    "content": response.text
}

# JSON-Datei hochladen
blob_client = container_client.get_blob_client("itland_page.json")
blob_client.upload_blob(json.dumps(data), overwrite=True)
print("✅ Seite gespeichert.")
