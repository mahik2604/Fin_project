import requests, os, json, re
from bs4 import BeautifulSoup
from urllib.parse import urljoin, parse_qs, urlparse

TRACKER_FILE = "tracker.json"
DOWNLOAD_DIR = "SEBI_RHPs"
BASE_URL = "https://www.sebi.gov.in"

def load_tracker():
    if os.path.exists(TRACKER_FILE):
        try:
            with open(TRACKER_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("⚠️ tracker.json is empty or invalid, starting fresh.")
            return {}
    return {}

def save_tracker(data):
    with open(TRACKER_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def sanitize_filename(name):
    return re.sub(r'[^a-zA-Z0-9]', '_', name)

def initialize_tracker(limit=10):
    headers = { "User-Agent": "Mozilla/5.0" }
    response = requests.get(f"{BASE_URL}/sebiweb/home/HomeAction.do?doListing=yes&sid=3&ssid=15&smid=11", headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    known = {}
    count = 0

    for row in soup.find_all('tr'):
        if count >= limit:
            break
        cols = row.find_all('td')
        if len(cols) == 2:
            title = cols[1].text.strip()
            link = cols[1].find('a', href=True)
            if not link:
                continue

            intermediate_url = urljoin(BASE_URL, link['href'])
            intermediate_response = requests.get(intermediate_url, headers=headers)
            iframe = BeautifulSoup(intermediate_response.content, 'html.parser').find('iframe')

            if iframe and 'src' in iframe.attrs:
                iframe_url = urljoin(BASE_URL, iframe['src'])
                parsed = urlparse(iframe_url)
                pdf_url = parse_qs(parsed.query).get('file', [None])[0]
                if pdf_url:
                    pdf_response = requests.get(pdf_url, headers=headers)
                    if 'application/pdf' in pdf_response.headers.get('Content-Type', ''):
                        filename = sanitize_filename(title) + ".pdf"
                        filepath = os.path.join(DOWNLOAD_DIR, filename)
                        with open(filepath, 'wb') as f:
                            f.write(pdf_response.content)

                        print(f"[INIT] Downloaded: {title}")
                        known[title] = pdf_url
                        count += 1

    if count:
        save_tracker(known)
        print(f"[INIT] Successfully initialized tracker with {count} entries.")
    else:
        print("[INIT] No PDFs were downloaded. Check page structure or network.")

    return count


def check_for_new_ipos(limit=10):
    known = load_tracker()
    updated = False
    headers = { "User-Agent": "Mozilla/5.0" }
    response = requests.get(f"{BASE_URL}/sebiweb/home/HomeAction.do?doListing=yes&sid=3&ssid=15&smid=11", headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    count = 0
    for row in soup.find_all('tr'):
        if count >= limit:
            break
        cols = row.find_all('td')
        if len(cols) == 2:
            title = cols[1].text.strip()
            if title in known:
                continue  # Already known

            link = cols[1].find('a', href=True)
            if not link:
                continue

            intermediate_url = urljoin(BASE_URL, link['href'])
            intermediate_response = requests.get(intermediate_url, headers=headers)
            iframe = BeautifulSoup(intermediate_response.content, 'html.parser').find('iframe')

            if iframe and 'src' in iframe.attrs:
                iframe_url = urljoin(BASE_URL, iframe['src'])
                parsed = urlparse(iframe_url)
                pdf_url = parse_qs(parsed.query).get('file', [None])[0]
                if pdf_url:
                    pdf_response = requests.get(pdf_url, headers=headers)
                    if 'application/pdf' in pdf_response.headers.get('Content-Type', ''):
                        filename = sanitize_filename(title) + ".pdf"
                        filepath = os.path.join(DOWNLOAD_DIR, filename)
                        with open(filepath, 'wb') as f:
                            f.write(pdf_response.content)

                        print(f"Downloaded new IPO: {title}")
                        known[title] = pdf_url
                        updated = True
                        count += 1

    if updated:
        save_tracker(known)
        print("Tracker updated.")
    else:
        print("No new IPOs found.")

    return updated

