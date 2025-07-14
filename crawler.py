import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from azure.storage.blob import BlobServiceClient
import json

# Konfiguration
BASE_URL = "https://it-land.net"
EXCLUDE_URLS = ["/impressum/", "/datenschutz/"]
CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
CONTAINER_NAME = "itlandcontainer2"
BLOB_NAME = "index-itlandnet.json"
LOCAL_FILE = "index-itlandnet.json"

# Alle Links auf der Website sammeln (außer ausgeschlossene)
def get_all_links(base_url):
    visited = set()
    to_visit = [base_url]
    urls = []

    while to_visit:
        url = to_visit.pop()
        if url in visited:
            continue
        visited.add(url)

        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")
            urls.append(url)

            for link in soup.find_all("a", href=True):
                full_url = urljoin(url, link["href"])
                if full_url.startswith(base_url) and full_url not in visited and not any(excl in full_url for excl in EXCLUDE_URLS):
                    to_visit.append(full_url)

        except Exception as e:
            print(f"⚠️ Fehler beim Laden von {url}: {e}")

    return urls

# Nur sichtbaren Text extrahieren
def extract_text_from_url(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        return soup.get_text(separator="\n", strip=True)
    except Exception as e:
        print(f"⚠️ Fehler beim Extrahieren von {url}: {e}")
        return ""

# Hauptfunktion: Crawlen, JSON speichern, in Azure hochladen
def main():
    all_urls = get_all_links(BASE_URL)
    data = []

    for url in all_urls:
        print(f"📄 Lade: {url}")
        text_only = extract_text_from_url(url)
        if text_only.strip():
            data.append({
                "url": url,
                "content": text_only
            })

    blob_json = json.dumps(data, ensure_ascii=False, indent=2)

    # Lokal speichern
    with open(LOCAL_FILE, "w", encoding="utf-8") as f:
        f.write(blob_json)

    print(f"💾 Lokal gespeichert als {LOCAL_FILE}")

    # In Azure hochladen
    blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
    container_client = blob_service_client.get_container_client(CONTAINER_NAME)
    container_client.upload_blob(name=BLOB_NAME, data=blob_json, overwrite=True)

    print(f"✅ {len(data)} Seiten gecrawlt und in Azure als {BLOB_NAME} gespeichert.")

if __name__ == "__main__":
    main()
