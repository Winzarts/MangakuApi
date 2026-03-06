from flask import Blueprint, jsonify, request
from bs4 import BeautifulSoup
import requests
from config import BASE_URL, HEADERS, API_BASE, TIMEOUT
from utils.scrapper import get_dynamic_html

genre_bp = Blueprint('genre', __name__)

@genre_bp.route('/genre/', methods=['GET'])
def list_genre():
    url = f"{BASE_URL}/pustaka/"

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

    genre_list = []
    
    for opt in soup.select("select[name='genre'] option"):
        genre = opt.get_text(strip=True)

        if not genre:
            continue

        genre_list.append({
            "genre": genre,
            "url": f"{API_BASE}/genre/{genre}"
        })

    return jsonify(genre_list)

@genre_bp.route('/genre/<slug>/', methods=['GET'])
def get_manga_by_genre(slug):
    orderby = request.args.get('orderby', 'update')
    limit = int(request.args.get('limit', 30))
    page = 1
    manga_list = []

    try:
        while len(manga_list) < limit:
            url = f"{BASE_URL}/genre/{slug}/?orderby={orderby}&page={page}"
            html = get_dynamic_html(url)
            soup = BeautifulSoup(html, "html.parser")

            items = soup.select("div.bge")
            if not items:
                break

            for manga in items:
                title_tag = manga.select_one("div.kan h3")
                img_tag = manga.select_one("div.bgei img")
                link_tag = manga.select_one("div.bgei a")

                if not (title_tag and img_tag and link_tag):
                    continue

                title = title_tag.get_text(strip=True)
                raw_link = link_tag["href"]
                link = f"{API_BASE}{raw_link}" if raw_link.startswith('/') else raw_link
                slug_comic = raw_link.strip('/').split('/')[-1]
                img = img_tag["src"]

                tipe_tag = manga.select_one("div.tpe1_inf b")
                tipe = tipe_tag.get_text(strip=True) if tipe_tag else ""

                genre_tag = manga.select_one("div.tpe1_inf")
                genre_text = genre_tag.get_text(strip=True).replace(tipe, "").strip() if genre_tag else ""

                reader_tag = manga.select_one("span.judul2")
                readers = reader_tag.get_text(strip=True) if reader_tag else ""

                deskripsi_tag = manga.select_one("div.kan p")
                deskripsi = deskripsi_tag.get_text(strip=True) if deskripsi_tag else ""

                new_links = manga.select("div.new1 a")
                awal = f"{API_BASE}{new_links[0]['href']}" if len(new_links) >= 1 else None
                terbaru = f"{API_BASE}{new_links[-1]['href']}" if len(new_links) >= 1 else None

                manga_list.append({
                    "title": title,
                    "slug": slug_comic,
                    "type": tipe,
                    "genre": genre_text,
                    "readers": readers,
                    "description": deskripsi,
                    "thumbnail": img,
                    "link": link,
                    "chapter_awal": awal,
                    "chapter_terbaru": terbaru
                })

                if len(manga_list) >= limit:
                    break

            page += 1

    except Exception as e:
        return jsonify({
            "message": str(e),
            "status": "Offline",
            "Response": "500"
        }), 500

    return jsonify(manga_list)
