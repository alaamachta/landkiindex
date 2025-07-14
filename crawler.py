import os
import requests
from azure.storage.blob import BlobServiceClient

# Verbindung zu Azure Blob Storage
connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_name = "itlandcontainer2"
container_client = blob_service_client.get_container_client(container_name)

# 🔁 Bestehende index-Dateien entfernen
for blob in container_client.list_blobs():
    if blob.name.startswith("index-"):
        container_client.delete_blob(blob.name)
        print(f"🧹 Alte Datei gelöscht: {blob.name}")

# 🌍 Website abrufen
url = "https://it-land.net"
response = requests.get(url)
html_content = response.text.replace('"', "'")  # Anführungszeichen für JSON ersetzen

# 📝 JSON erstellen und hochladen
blob_data = f'{{"url": "{url}", "content": "{html_content}"}}'
blob_name = "index-itlandnet.json"
container_client.upload_blob(name=blob_name, data=blob_data, overwrite=True)
print(f"✅ Website {url} erfolgreich gespeichert als {blob_name}")
