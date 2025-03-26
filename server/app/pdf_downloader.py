import requests
from bs4 import BeautifulSoup
import os
import re
import logging
from urllib.parse import urljoin, parse_qs, urlparse
from fastapi import FastAPI
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# FastAPI app
app = FastAPI()

# SEBI URLs
BASE_URL = "https://www.sebi.gov.in"
SEBI_IPO_PAGE = f"{BASE_URL}/sebiweb/home/HomeAction.do?doListing=yes&sid=3&ssid=15&smid=11"

# Directory to save PDFs
DOWNLOAD_DIR = "SEBI_RHPs"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def fetch_page_content(url):
    """Fetch and return page content."""
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.content

def extract_rhp_links():
    """Extract links to RHP documents from SEBI page."""
    soup = BeautifulSoup(fetch_page_content(SEBI_IPO_PAGE), "html.parser")
    pdf_links = []
    
    for row in soup.find_all("tr"):
        columns = row.find_all("td")
        if len(columns) == 2:
            title = columns[1].text.strip()
            link = columns[1].find("a", href=True)
            if link:
                pdf_links.append((title, urljoin(BASE_URL, link["href"])))
    
    return pdf_links

def extract_pdf_url(intermediate_url):
    """Extract actual PDF URL from intermediate page."""
    soup = BeautifulSoup(fetch_page_content(intermediate_url), "html.parser")
    iframe = soup.find("iframe")
    if iframe and "src" in iframe.attrs:
        parsed_url = urlparse(urljoin(BASE_URL, iframe["src"]))
        return parse_qs(parsed_url.query).get("file", [None])[0]
    return None

def download_pdf(title, pdf_url):
    """Download and save the PDF file."""
    if not pdf_url:
        logging.warning(f"No PDF URL found for {title}")
        return None
    
    response = requests.get(pdf_url)
    response.raise_for_status()
    if "application/pdf" not in response.headers.get("Content-Type", ""):
        logging.error(f"Invalid PDF response for {title}")
        return None
    
    pdf_filename = os.path.join(DOWNLOAD_DIR, f"{re.sub(r'[^a-zA-Z0-9]', '_', title)}.pdf")
    with open(pdf_filename, "wb") as pdf_file:
        pdf_file.write(response.content)
    logging.info(f"Downloaded: {pdf_filename}")
    
    return {"title": title, "file_path": pdf_filename, "download_date": datetime.now().isoformat()}

@app.get("/download-rhp")
def download_rhp_files():
    """FastAPI endpoint to trigger RHP downloads."""
    pdf_links = extract_rhp_links()
    results = []
    for title, intermediate_url in pdf_links[:5]:  # Limit to 5 PDFs
        pdf_url = extract_pdf_url(intermediate_url)
        result = download_pdf(title, pdf_url)
        if result:
            results.append(result)
    return {"downloaded_files": results}
