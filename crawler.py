import os
import requests
from azure.storage.blob import BlobServiceClient

# Verbindung zu Azure Blob Storage
connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_name = "itlandcontainer2"
container_client = blob_service_client.get_container_client(container_name)

# Webseite laden
url = "https://it-land.net"
response = requests.get(url)
html_content = response.text.replace('"', "'")  # Anführungszeichen für JSON ersetzen

# JSON-Dokument erzeugen
blob_data = f'{{"url": "{url}", "content": "{html_content}"}}'
blob_name = "index-itlandnet.json"

# Hochladen
container_client.upload_blob(name=blob_name, data=blob_data, overwrite=True)
print(f"✅ Website {url} erfolgreich gespeichert als {blob_name}")
