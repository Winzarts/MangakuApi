from flask import Blueprint, jsonify
from bs4 import BeautifulSoup
from config import BASE_URL, API_BASE
from utils.scrapper import get_dynamic_html

latest_bp = Blueprint('latest', __name__)


def _parse_latest_items(soup):
    manga_list = []
    for manga in soup.select("div.bge"):
        title_tag = manga.select_one("div.kan h3")
        img_tag = manga.select_one("div.bgei img")
        link_tag = manga.select_one("div.bgei a")
        if not (title_tag and img_tag and link_tag):
            continue

        title = title_tag.get_text(strip=True)
        raw_link = link_tag["href"]
        link = f"{API_BASE}{raw_link}" if raw_link.startswith('/') else raw_link
        slug = raw_link.strip('/').split('/')[-1]
        img = img_tag["src"]
        tipe = manga.select_one("div.tpe1_inf b").get_text(strip=True)
        genre = manga.select_one("div.tpe1_inf").get_text(strip=True).replace(tipe, "").strip()
        pembaca = manga.select_one("span.judul2 span b").get_text(strip=True)
        waktu_span = manga.select_one("span.judul2")
        waktu = waktu_span.get_text(strip=True).split("|")[1].strip() if waktu_span and "|" in waktu_span.get_text() else ""
        deskripsi = manga.select_one("div.kan p").get_text(strip=True)

        new_links = manga.select("div.new1 a")
        awal = f"{API_BASE}{new_links[0]['href']}" if len(new_links) >= 1 else None
        terbaru = f"{API_BASE}{new_links[-1]['href']}" if len(new_links) >= 1 else None

        manga_list.append({
            "title": title,
            "slug": slug,
            "type": tipe,
            "genre": genre,
            "readers": pembaca,
            "updated": waktu,
            "description": deskripsi,
            "thumbnail": img,
            "link": link,
            "chapter_awal": awal,
            "chapter_terbaru": terbaru
        })
    return manga_list


@latest_bp.route("/latest", methods=["GET"])
def latest_komik():
    url = f"{BASE_URL}/pustaka/?orderby=update&tipe=&genre=&genre2=&status="
    try:
        html = get_dynamic_html(url)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify(_parse_latest_items(BeautifulSoup(html, "html.parser")))


@latest_bp.route('/latest-manga', methods=['GET'])
def latest_manga():
    url = f"{BASE_URL}/pustaka/?orderby=update&tipe=manga"
    try:
        html = get_dynamic_html(url)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify(_parse_latest_items(BeautifulSoup(html, "html.parser")))


@latest_bp.route("/latest-manhwa", methods=["GET"])
def latest_manhwa():
    url = f"{BASE_URL}/pustaka/?orderby=update&tipe=manhwa"
    try:
        html = get_dynamic_html(url)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify(_parse_latest_items(BeautifulSoup(html, "html.parser")))


@latest_bp.route("/latest-manhua", methods=["GET"])
def latest_manhua():
    url = f"{BASE_URL}/pustaka/?orderby=update&tipe=manhua"
    try:
        html = get_dynamic_html(url)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify(_parse_latest_items(BeautifulSoup(html, "html.parser")))
