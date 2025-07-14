import os
from azure.storage.blob import BlobServiceClient
import requests

# Verbindung
connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
blob_service_client = BlobServiceClient.from_connection_string(connection_string)

# Zielcontainer
container_name = "itlandcontainer2"
container_client = blob_service_client.get_container_client(container_name)

# Webseite crawlen (z. B. Startseite)
url = "https://it-land.net"
response = requests.get(url)
html_content = response.text

# In Blob speichern (als .json, damit Azure Indexer es akzeptiert)
blob_name = "itlandnet.json"
blob_data = '{"url": "%s", "content": "%s"}' % (url, html_content.replace('"', "'"))
container_client.upload_blob(name=blob_name, data=blob_data, overwrite=True)

print(f"✅ Inhalt von {url} gespeichert als {blob_name}")
