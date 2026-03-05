from flask import Blueprint, jsonify, request
from bs4 import BeautifulSoup
import requests
from config import BASE_URL, HEADERS, API_BASE, TIMEOUT

list_bp = Blueprint("list", __name__)

def _parse_ls4_items(soup):
    manga_list = []
    for item in soup.select('div.ls4'):
        a_title = item.select_one('h4 a')
        img = item.select_one('div.ls4v img.lazy')
        span_genre = item.select('span.ls4s')

        if not a_title:
            continue

        title = a_title.text.strip()
        manga_url = f"{API_BASE}{a_title['href']}"

        genres = []
        for g in span_genre:
            text = g.text.replace('Genre : ', '').strip()
            genres.extend([x.strip() for x in text.split(',') if x.strip()])

        manga_list.append({
            "title": title,
            "url": manga_url,
            "thumbnail": img.get('data-src') if img else None,
            "genres": genres
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