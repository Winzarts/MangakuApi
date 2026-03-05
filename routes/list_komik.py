from flask import Blueprint, jsonify, request
from bs4 import BeautifulSoup
import requests
from config import BASE_URL, HEADERS, API_BASE, TIMEOUT

list_bp = Blueprint("list", __name__)

def _parse_ls4_items(soup):
    manga_list = []

    for item in soup.select("article.manga-card"):
        title_tag = item.select_one("h4 a")
        img_tag = item.select_one("img.lazy")
        meta_tag = item.select_one("p.meta")

        if not title_tag:
            continue

        title = title_tag.text.strip()
        raw_link = title_tag["href"]
        url = f"{API_BASE}{raw_link}" if raw_link.startswith("/") else raw_link

        thumbnail = img_tag.get("data-src") if img_tag else None

        type_manga = ""
        genre = ""
        status = ""

        if meta_tag:
            lines = meta_tag.get_text("\n", strip=True).split("\n")

            if len(lines) >= 1:
                parts = lines[0].split("•")
                type_manga = parts[0].strip() if len(parts) > 0 else ""
                genre = parts[1].strip() if len(parts) > 1 else ""

            if len(lines) >= 2:
                status = lines[1].replace("Status:", "").strip()

        manga_list.append({
            "title": title,
            "url": url,
            "thumbnail": thumbnail,
            "type": type_manga,
            "genre": genre,
            "status": status
        })

    return manga_list


@list_bp.route("/list-semua-komik", methods=["GET"])
def list_semua():
    page = int(request.args.get("page", 1))
    url = f"{BASE_URL}/daftar-komik/page/{page}/"

    try:
        resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        resp.raise_for_status()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    soup = BeautifulSoup(resp.text, "html.parser")
    manga_list = _parse_ls4_items(soup)

    return jsonify({
        "page": page,
        "count": len(manga_list),
        "List_Manga": manga_list
    })


@list_bp.route("/list-manga", methods=["GET"])
def semua_manga():
    url = f"{BASE_URL}/daftar-komik/?tipe=manga"

    try:
        resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        resp.raise_for_status()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    soup = BeautifulSoup(resp.text, "html.parser")
    manga_list = _parse_ls4_items(soup)

    return jsonify({"count": len(manga_list), "List_Manga": manga_list})


@list_bp.route("/list-manhwa", methods=["GET"])
def semua_manhwa():
    url = f"{BASE_URL}/daftar-komik/?tipe=manhwa"

    try:
        resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        resp.raise_for_status()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    soup = BeautifulSoup(resp.text, "html.parser")
    manga_list = _parse_ls4_items(soup)

    return jsonify({"count": len(manga_list), "List_Manga": manga_list})


@list_bp.route("/list-manhua", methods=["GET"])
def semua_manhua():
    url = f"{BASE_URL}/daftar-komik/?tipe=manhua"

    try:
        resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        resp.raise_for_status()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    soup = BeautifulSoup(resp.text, "html.parser")
    manga_list = _parse_ls4_items(soup)

    return jsonify({"count": len(manga_list), "List_Manga": manga_list})
