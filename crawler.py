import time
from playwright.sync_api import sync_playwright
from azure.storage.blob import BlobServiceClient
import os

# Konfiguration
URL = "https://www.example.com"
AZURE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
CONTAINER_NAME = "itlandcontainer2"
BLOB_NAME = "webcrawler-output.txt"

print("Crawler startet...")

try:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(URL)
        content = page.content()
        print("Seite geladen:", URL)

        # Blob-Client initialisieren
        blob_service = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
        blob_client = blob_service.get_blob_client(container=CONTAINER_NAME, blob=BLOB_NAME)

        # Hochladen in Azure Blob
        blob_client.upload_blob(content, overwrite=True)
        print("Inhalt erfolgreich in Azure Blob gespeichert.")
        browser.close()

except Exception as e:
    print("Fehler beim Crawling oder Speichern:", str(e))

# Für Log-Tests sichtbar lassen
print("Warte 60 Sekunden...")
time.sleep(60)
print("Crawler beendet.")
