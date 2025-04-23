import hashlib
import requests
from PyPDF2 import PdfReader
from io import BytesIO

KEYWORDS = ["subvención", "convocatoria", "plazo", "ayuda"]

def get_md5_of_text(text):
    return hashlib.md5(text.encode('utf-8')).hexdigest()

def check_url_for_changes(url, old_hash):
    try:
        response = requests.get(url)
        if response.status_code != 200:
            return False, old_hash, None

        reader = PdfReader(BytesIO(response.content))
        full_text = "".join(page.extract_text() or "" for page in reader.pages)

        if not any(word in full_text.lower() for word in KEYWORDS):
            return False, old_hash, None

        new_hash = get_md5_of_text(full_text)

        return (new_hash != old_hash), new_hash, full_text
    except Exception as e:
        print(f"Error: {e}")
        return False, old_hash, None
