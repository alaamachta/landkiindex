print("Crawler gestartet")
import os
import asyncio
from playwright.async_api import async_playwright
from azure.storage.blob import BlobServiceClient

connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
container_name = "itlandcontainer2"
blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_client = blob_service_client.get_container_client(container_name)

async def crawl_and_upload(url: str, filename: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url)
        content = await page.content()
        await browser.close()

        # In Blob hochladen
        blob_name = f"{filename}.html"
        container_client.upload_blob(name=blob_name, data=content, overwrite=True)
        print(f"✅ '{url}' → '{blob_name}' hochgeladen")

if __name__ == "__main__":
    asyncio.run(crawl_and_upload("https://landki.com", "landki-startseite"))
