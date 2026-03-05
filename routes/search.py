from flask import Blueprint, jsonify, request
from bs4 import BeautifulSoup
from config import BASE_URL, API_BASE
from utils.scrapper import get_dynamic_html

search_bp = Blueprint('search', __name__)


@search_bp.route("/search", methods=["GET"])
def search_komik():
    query = request.args.get('q', '').strip()
    if not query:
        return jsonify({"error": "Parameter 'q' diperlukan, contoh /search?q=tokidoki+bosotto"}), 400

    url = f"{BASE_URL}/?post_type=manga&s={query.replace(' ', '+')}"

    try:
        html = get_dynamic_html(url)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    soup = BeautifulSoup(html, 'html.parser')
    manga_list = []

    for manga in soup.select("div.bge"):
        title_tag = manga.select_one("div.kan h3")
        img_tag = manga.select_one("div.bgei img")
        link_tag = manga.select_one("div.bgei a")

        if not (title_tag and img_tag and link_tag):
            continue

        title = title_tag.get_text(strip=True)
        raw_link = link_tag.get("href", "")
        link = f"{API_BASE}{raw_link}" if raw_link.startswith('/') else raw_link
        img = img_tag.get("src")

        tipe_tag = manga.select_one("div.tpe1_inf b")
        tipe = tipe_tag.get_text(strip=True) if tipe_tag else ""

        genre_tag = manga.select_one("div.tpe1_inf")
        genre_text = genre_tag.get_text(strip=True).replace(tipe, "").strip() if genre_tag else ""

        deskripsi_tag = manga.select_one("div.kan p")
        deskripsi = deskripsi_tag.get_text(strip=True) if deskripsi_tag else ""

        manga_list.append({
            "title": title,
            "type": tipe,
            "genre": genre_text,
            "description": deskripsi,
            "thumbnail": img,
            "link": link
        })

    if not manga_list:
        return jsonify({"message": f"tidak menemukan hasil untuk '{query}'"}), 404

    return jsonify({
        "query": query,
        "results": manga_list,
        "count": len(manga_list)
    })