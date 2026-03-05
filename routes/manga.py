from flask import Blueprint, jsonify
from bs4 import BeautifulSoup
import requests
from config import BASE_URL, HEADERS, API_BASE, TIMEOUT

manga_bp = Blueprint('manga', __name__)

@manga_bp.route('/manga/<slug>/', methods=['GET'])
def get_manga_detail(slug):
    url = f"{BASE_URL}/manga/{slug}"

    try:
        resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        resp.raise_for_status()
    except Exception as e:
        return jsonify({
            "message": str(e),
            "status": "Offline",
            "Response": "500"
        }), 500

    soup = BeautifulSoup(resp.text, 'html.parser')
    
    title_tag = soup.select_one('#Judul span[itemprop="name"]')
    title = title_tag.text.strip() if title_tag else None

    indonesia_title_tag = soup.select_one('#Judul p.j2')
    indonesia_title = short_desc_tag.text.strip() if short_desc_tag else None
    
    img_tag = soup.select_one('.ims img')
    image_url = img_tag['src'] if img_tag else None
    
    sinopsis_tag = soup.select_one('p.desc')
    sinopsis = sinopsis_tag.text.strip() if sinopsis_tag else ""
    
    genres = [g.text.strip() for g in soup.select("ul.genre li span")]
    
    short_description = ""
    for row in soup.select("table.inftable tr"):
        cols = row.find_all("td")
        if len(cols) >= 2:
            if cols[0].text.strip() == "Judul Indonesia":
                short_description = cols[1].text.strip()

    chapter_list = []
    for row in soup.select('#Daftar_Chapter tbody tr'):
        cols = row.find_all('td')
        if not cols:
            continue

        a_tag = cols[0].select_one('a')
        if not a_tag:
            continue

        chapter_title = a_tag.text.strip()
        raw_url = a_tag.get('href', '')
        chapter_slug = raw_url.strip('/').split('/')[-1].replace(f"{slug}-", "")
        chapter_url = f"{API_BASE}/manga/{slug}/{chapter_slug}/"

        views = cols[1].text.strip() if len(cols) > 1 else ""
        date = cols[2].text.strip() if len(cols) > 2 else ""

        chapter_list.append({
            "title": chapter_title,
            "url": chapter_url,
            "views": views,
            "date": date
        })

    return jsonify({
        "title": title,
        "Indonesia_title": Indonesia_title,
        "image_url": image_url,
        "short_description" : short_description,
        "long_description": long_description,
        "sinopsis": sinopsis,
        "genres" : genres
        "chapters": chapter_list
    })

@manga_bp.route('/manga/<slug>/<chapter_slug>/', methods=['GET'])
def get_manga_content(slug, chapter_slug):
    url = f"{BASE_URL}/{slug}-{chapter_slug}/"

    try:
        resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        resp.raise_for_status()
    except Exception as e:
        return jsonify({
            "message": str(e),
            "status": "Offline",
            "Response": "500"
        }), 500

    soup = BeautifulSoup(resp.text, 'html.parser')

    title_elem = soup.select_one("#Judul header h1")
    chapter_title = title_elem.text.strip() if title_elem else chapter_slug
    
    page_image = []
    for img in soup.select("#Baca_Komik img.klazy"):
        src = img.get("src")
        if src and src.startswith("https://img.komiku.org"):
            page_image.append(src.strip())

    return jsonify({
        "title": chapter_title,
        "images": page_image
    })
