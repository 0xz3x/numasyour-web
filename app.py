from __future__ import annotations

import copy
import json
import html
import re
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen

from flask import Flask, flash, redirect, render_template, request, send_from_directory, url_for


app = Flask(__name__)
app.secret_key = "numasyour-dev-secret"
BASE_DIR = Path(__file__).resolve().parent
CERT_FEED_URL = "https://www.cert.ssi.gouv.fr/feed/"
CERT_FEED_CACHE_TTL_SECONDS = 3600

MONTH_NAMES = {
    1: "janvier",
    2: "février",
    3: "mars",
    4: "avril",
    5: "mai",
    6: "juin",
    7: "juillet",
    8: "août",
    9: "septembre",
    10: "octobre",
    11: "novembre",
    12: "décembre",
}

CERT_FEED_CACHE: dict[str, object] = {"fetched_at": None, "articles": None}

SITE_PATH = BASE_DIR / "data" / "site.json"


def load_site_config() -> dict[str, object]:
    with SITE_PATH.open(encoding="utf-8") as site_file:
        return json.load(site_file)


SITE = load_site_config()


def format_french_date(date_value: datetime) -> str:
    return f"{date_value.day} {MONTH_NAMES[date_value.month]} {date_value.year}"


def normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(value)).strip()


def strip_html(value: str) -> str:
    return re.sub(r"<[^>]+>", "", value)


def parse_feed_datetime(value: str | None) -> datetime:
    if not value:
        return datetime.now(timezone.utc)

    try:
        parsed_value = parsedate_to_datetime(value)
    except (TypeError, ValueError):
        return datetime.now(timezone.utc)

    if parsed_value.tzinfo is None:
        return parsed_value.replace(tzinfo=timezone.utc)

    return parsed_value


def classify_cert_item(link: str) -> dict[str, str]:
    if "/alerte/" in link:
        return {"tag": "Critique", "tag_class": "critical", "subject": "audit", "action_label": "Vérifier votre exposition"}

    if "/avis/" in link:
        return {"tag": "Important", "tag_class": "warning", "subject": "supervision", "action_label": "Planifier les correctifs"}

    if "/actualite/" in link:
        return {"tag": "Information", "tag_class": "info", "subject": "conseil", "action_label": "Structurer un plan d'action"}

    if "/dur/" in link:
        return {"tag": "Information", "tag_class": "info", "subject": "conseil", "action_label": "Structurer un plan d'action"}

    return {"tag": "Information", "tag_class": "info", "subject": "conseil", "action_label": "En savoir plus"}


def build_cert_article(item: ET.Element) -> dict[str, str | datetime]:
    title = normalize_text(item.findtext("title", default=""))
    link = normalize_text(item.findtext("link", default=""))
    description = normalize_text(strip_html(item.findtext("description", default="")))
    published_at = parse_feed_datetime(item.findtext("pubDate"))
    classification = classify_cert_item(link)

    title = re.sub(r"\s*\((?:\d{1,2}\s+[a-zéûîôàèùç]+\s+\d{4})\)$", "", title, flags=re.IGNORECASE)

    return {
        "tag": classification["tag"],
        "tag_class": classification["tag_class"],
        "date": format_french_date(published_at),
        "title": title,
        "desc": description,
        "source": "CERT-FR",
        "subject": classification["subject"],
        "action_label": classification["action_label"],
        "published_at": published_at,
    }


def fallback_cert_articles() -> list[dict[str, str]]:
    return list(SITE["veille"]["articles"])


def fetch_cert_articles() -> list[dict[str, str]]:
    cached_articles = CERT_FEED_CACHE["articles"]
    cached_at = CERT_FEED_CACHE["fetched_at"]
    now = datetime.now(timezone.utc)

    if cached_articles is not None and cached_at is not None:
        if (now - cached_at).total_seconds() < CERT_FEED_CACHE_TTL_SECONDS:
            return list(cached_articles)

    try:
        with urlopen(CERT_FEED_URL, timeout=5) as response:
            feed_xml = response.read()
    except URLError:
        return list(cached_articles) if cached_articles is not None else fallback_cert_articles()

    try:
        root = ET.fromstring(feed_xml)
    except ET.ParseError:
        return list(cached_articles) if cached_articles is not None else fallback_cert_articles()

    channel = root.find("channel")
    if channel is None:
        return list(cached_articles) if cached_articles is not None else fallback_cert_articles()

    articles = [build_cert_article(item) for item in channel.findall("item")]
    articles.sort(key=lambda article: article["published_at"], reverse=True)

    normalized_articles: list[dict[str, str]] = []
    for article in articles[:6]:
        normalized_articles.append({key: value for key, value in article.items() if key != "published_at"})

    CERT_FEED_CACHE["articles"] = normalized_articles
    CERT_FEED_CACHE["fetched_at"] = now
    return list(normalized_articles)


def site_data() -> dict[str, object]:
    site = copy.deepcopy(SITE)
    site["veille"]["articles"] = fetch_cert_articles()
    return site


def service_menu_items(active_slug: str | None = None) -> list[dict[str, object]]:
    return [
        {
            "slug": item["slug"],
            "title": item["title"],
            "icon": item["icon"],
            "desc": item["desc"],
            "active": item["slug"] == active_slug,
        }
        for item in SITE["services"]
    ]


@app.context_processor
def inject_site() -> dict[str, object]:
    return {"site": site_data(), "service_menu": service_menu_items()}


@app.route("/")
def index():
    return render_template(
        "index.html",
        active_page="index",
        page_title=f"{SITE['company']} — {SITE['baseline']}",
        page_description="Site vitrine Flask de NumAsYouR : audit, supervision, architecture réseau et conseil IT.",
    )


@app.route("/a-propos")
def about():
    return render_template(
        "a-propos.html",
        active_page="about",
        page_title="Qui sommes-nous ? — NumAsYouR",
        page_description="Découvrez le parcours et les valeurs qui animent NumAsYouR au quotidien.",
    )


@app.route("/veille-securite")
def veille():
    return render_template(
        "veille-securite.html",
        active_page="veille",
        page_title="Veille Sécurité — NumAsYouR",
        page_description="Alertes, vulnérabilités et bonnes pratiques : restez informé des dernières menaces IT.",
    )


@app.route("/mentions-legales")
def mentions_legales():
    return render_template(
        "mentions-legales.html",
        active_page="legal",
        page_title="Mentions Légales — NumAsYouR",
        page_description="Mentions légales, politique de confidentialité et gestion des cookies du site NumAsYouR.",
    )


@app.route("/contact", methods=["GET", "POST"])
def contact():
    form_data = {"name": "", "email": "", "phone": "", "company": "", "subject": "", "message": ""}
    if request.method == "GET":
        subject = request.args.get("subject", "").strip()
        valid_subjects = {item["value"] for item in SITE["contact"]["subjects"]}
        if subject in valid_subjects:
            form_data["subject"] = subject
    if request.method == "POST":
        form_data = {key: request.form.get(key, "").strip() for key in form_data}

        if not form_data["name"] or not form_data["email"] or not form_data["subject"] or not form_data["message"]:
            flash("Veuillez remplir tous les champs obligatoires.", "error")
        elif not re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", form_data["email"]):
            flash("Veuillez entrer une adresse email valide.", "error")
        else:
            flash("Merci pour votre message. Nous vous répondrons dans les plus brefs délais.", "success")
            return redirect(url_for("contact"))

    return render_template(
        "contact.html",
        active_page="contact",
        page_title="Contact — NumAsYouR",
        page_description="Contactez NumAsYouR pour un audit, un devis ou une question.",
        form_data=form_data,
    )


@app.route("/services/<slug>")
def service_detail(slug: str):
    service = SITE["service_pages"].get(slug)
    if service is None:
        return render_template(
            "mentions-legales.html",
            active_page="legal",
            page_title="Page introuvable — NumAsYouR",
            page_description="La page demandée n'existe pas.",
        ), 404

    plain_title = re.sub(r"<[^>]+>", "", service["page_title"]).strip()

    return render_template(
        "service_detail.html",
        active_page="services",
        service_slug=slug,
        service=service,
        service_plain_title=plain_title,
        page_title=f"{plain_title} — NumAsYouR",
        page_description=service["page_desc"],
    )


@app.route("/healthz")
def healthz():
    return "ok", 200


if __name__ == "__main__":
    app.run(debug=True)
