from __future__ import annotations

import re
from pathlib import Path

from flask import Flask, flash, redirect, render_template, request, send_from_directory, url_for


app = Flask(__name__)
app.secret_key = "numasyour-dev-secret"
BASE_DIR = Path(__file__).resolve().parent


@app.route("/css/<path:filename>")
def css_assets(filename: str):
    return send_from_directory(BASE_DIR / "css", filename)


@app.route("/js/<path:filename>")
def js_assets(filename: str):
    return send_from_directory(BASE_DIR / "js", filename)


@app.route("/img/<path:filename>")
def img_assets(filename: str):
    return send_from_directory(BASE_DIR / "img", filename)


SITE = {
    "company": "NumAsYouR",
    "baseline": "Le numérique à votre service",
    "year": "2025",
    "founder": "Xavier Pietin",
    "founder_title": "Gérant / Consultant IT — Infrastructure, Sécurité & Supervision",
    "phone": "02 57 62 02 57",
    "phone_full": "+33257620257",
    "email": "contact@numasyour.com",
    "address": "Marzan, Bretagne, France",
    "hours": "Du lundi au vendredi, 9h00 — 18h00",
    "linkedin": "https://www.linkedin.com",
    "footer_desc": "Le numérique à votre service. Consultant IT expert en infrastructure, cybersécurité et supervision pour les PME en Bretagne.",
    "cookie_message": 'Nous utilisons des cookies pour améliorer votre expérience de navigation. En continuant, vous acceptez notre <a href="/mentions-legales#cookies">politique de cookies</a>.',
    "hero": {
        "badge": '<i class="fa-solid fa-bolt"></i> Consultant IT — Bretagne',
        "title": 'Le <span class="highlight">numérique</span> à votre service',
        "description": "Expert en infrastructure, cybersécurité et supervision, NumAsYouR accompagne les PME et TPE dans leur transformation numérique avec des solutions sur-mesure et performantes.",
        "cta1": "Découvrir nos services",
        "cta2": "Nous contacter",
    },
    "hero_stats": [
        {"number": "15+", "label": "Années d'expertise"},
        {"number": "100%", "label": "Solutions sur-mesure"},
        {"number": "24/7", "label": "Monitoring continu"},
        {"number": "ANSSI", "label": "Conformité garantie"},
    ],
    "figures": [
        {"icon": '<i class="fa-solid fa-trophy"></i>', "count": 15, "suffix": "+", "label": "Années d'expérience"},
        {"icon": '<i class="fa-solid fa-rocket"></i>', "count": 50, "suffix": "+", "label": "Projets réalisés"},
        {"icon": '<i class="fa-solid fa-handshake"></i>', "count": 30, "suffix": "+", "label": "Clients accompagnés"},
        {"icon": '<i class="fa-solid fa-shield-halved"></i>', "count": 100, "suffix": "%", "label": "Engagement qualité"},
    ],
    "services_intro": {
        "title": "Nos domaines d'expertise",
        "subtitle": "Des solutions complètes pour sécuriser, optimiser et piloter votre infrastructure informatique.",
    },
    "services": [
        {"slug": "audit-securite", "icon": '<i class="fa-solid fa-lock"></i>', "title": "Audit & Sécurité", "desc": "Évaluation des vulnérabilités, sauvegardes immuables, conformité ANSSI, sensibilisation aux risques cyber et plans de reprise d'activité."},
        {"slug": "supervision", "icon": '<i class="fa-solid fa-chart-column"></i>', "title": "Supervision & Monitoring", "desc": "Déploiement de solutions open source (Zabbix, Grafana, Wazuh), surveillance 24/7, dashboards personnalisés et alerting intelligent."},
        {"slug": "architecture-reseau", "icon": '<i class="fa-solid fa-globe"></i>', "title": "Architecture Réseau", "desc": "Conception d'architectures LAN/WAN/WLAN, segmentation réseau, interconnexion SD-WAN/SASE et solutions cloud hybrides."},
        {"slug": "conseil", "icon": '<i class="fa-solid fa-handshake"></i>', "title": "Conseil & Accompagnement", "desc": "Gestion de projet IT, rédaction de normes SI, formation des équipes, stratégies de sauvegarde et contrats de maintenance."},
    ],
    "why": {
        "title": "Pourquoi choisir NumAsYouR ?",
        "subtitle": "Un partenaire de confiance pour votre transformation numérique, avec une approche humaine et pragmatique.",
        "cards": [
            {"icon": '<i class="fa-solid fa-bullseye"></i>', "title": "Expertise terrain", "desc": "Plus de 15 ans d'expérience opérationnelle dans des environnements industriels, maritimes et tertiaires."},
            {"icon": '<i class="fa-solid fa-lock-open"></i>', "title": "Solutions open source", "desc": "Des outils éprouvés, performants et économiques : Zabbix, Grafana, Wazuh, Elastic Stack."},
            {"icon": '<i class="fa-solid fa-scissors"></i>', "title": "Approche sur-mesure", "desc": "Chaque entreprise est unique. Nos solutions sont adaptées à vos besoins, votre budget et vos contraintes."},
            {"icon": '<i class="fa-solid fa-shield-halved"></i>', "title": "Conformité ANSSI", "desc": "Mise en œuvre des recommandations de l'ANSSI pour garantir un niveau de sécurité optimal."},
        ],
    },
    "cta": {
        "title": "Un projet ? Parlons-en.",
        "desc": "Contactez-nous pour un audit gratuit de votre infrastructure ou pour discuter de vos besoins en cybersécurité.",
        "cta1": "Demander un devis",
        "cta2": '<i class="fa-solid fa-phone"></i> 02 57 62 02 57',
    },
    "timeline": [
        {"years": "2010 — 2020", "title": "Brioche Pasquier", "desc": "Plus de 10 ans d'expérience en analyse et supervision industrielle. Gestion de projets réseau, mise en place de systèmes de monitoring et cybersécurité dans un environnement industriel critique."},
        {"years": "2020 — 2021", "title": "Compagnie des Ports du Morbihan", "desc": "Responsable informatique. Gestion complète de l'infrastructure IT portuaire : réseaux, sécurité, supervision. Environnement maritime avec des contraintes spécifiques de disponibilité et de sécurité."},
        {"years": "2021 — Aujourd'hui", "title": "NumAsYouR — Fondateur & Consultant", "desc": "Création de NumAsYouR pour accompagner les PME et TPE dans leur transformation numérique. Audit de sécurité, supervision, architecture réseau et conseil : une offre complète et sur-mesure."},
    ],
    "skills": [
        {"icon": '<i class="fa-solid fa-chart-column"></i>', "name": "Zabbix"},
        {"icon": '<i class="fa-solid fa-chart-line"></i>', "name": "Grafana"},
        {"icon": '<i class="fa-solid fa-shield-halved"></i>', "name": "Wazuh"},
        {"icon": '<i class="fa-solid fa-magnifying-glass"></i>', "name": "Elastic Stack"},
        {"icon": '<i class="fa-solid fa-cloud"></i>', "name": "AWS"},
        {"icon": '<i class="fa-solid fa-circle-check"></i>', "name": "CheckMK"},
        {"icon": '<i class="fa-solid fa-folder"></i>', "name": "Nextcloud"},
        {"icon": '<i class="fa-solid fa-globe"></i>', "name": "SD-WAN"},
        {"icon": '<i class="fa-solid fa-lock"></i>', "name": "PAM"},
        {"icon": '<i class="fa-brands fa-linux"></i>', "name": "Linux"},
        {"icon": '<i class="fa-brands fa-windows"></i>', "name": "Windows Server"},
        {"icon": '<i class="fa-solid fa-server"></i>', "name": "VMware"},
    ],
    "values": [
        {"icon": '<i class="fa-solid fa-handshake"></i>', "title": "Proximité", "desc": "Un interlocuteur unique, à l'écoute de vos besoins. Nous privilégions la relation humaine et la communication directe."},
        {"icon": '<i class="fa-solid fa-bullseye"></i>', "title": "Expertise terrain", "desc": "Des solutions éprouvées, issues de plus de 15 ans d'expérience opérationnelle dans des environnements variés et exigeants."},
        {"icon": '<i class="fa-solid fa-lock-open"></i>', "title": "Open source", "desc": "Nous privilégions les solutions open source : performantes, pérennes et économiques. La transparence au service de votre SI."},
        {"icon": '<i class="fa-solid fa-scissors"></i>', "title": "Sur-mesure", "desc": "Chaque entreprise est unique. Nos solutions sont conçues sur-mesure, adaptées à votre contexte, vos contraintes et vos objectifs."},
        {"icon": '<i class="fa-solid fa-magnifying-glass"></i>', "title": "Transparence", "desc": "Des propositions claires, une communication franche, des résultats mesurables. Pas de jargon inutile, que du concret."},
        {"icon": '<i class="fa-solid fa-building-columns"></i>', "title": "Conformité", "desc": "Respect des cadres réglementaires et des bonnes pratiques ANSSI. La conformité n'est pas une option, c'est un fondement."},
    ],
    "service_pages": {
        "audit-securite": {
            "page_title": '<i class="fa-solid fa-lock"></i> Audit & Sécurité',
            "page_desc": "Protégez votre entreprise avec un audit complet de votre infrastructure et des solutions de cybersécurité adaptées à vos enjeux.",
            "sidebar_title": "Besoin d'un audit ?",
            "sidebar_desc": "Évaluez le niveau de sécurité de votre infrastructure avec un audit personnalisé.",
            "sidebar_cta": "Demander un audit",
            "cta_title": "Sécurisez votre infrastructure dès maintenant",
            "cta_desc": "Ne laissez pas les cybermenaces compromettre votre activité. Contactez-nous pour un premier échange.",
            "prestations": [
                {"icon": '<i class="fa-solid fa-magnifying-glass"></i>', "title": "Audit de sécurité complet", "desc": "Évaluation complète des vulnérabilités de votre système d'information, analyse de la surface d'attaque et recommandations hiérarchisées pour renforcer votre posture de sécurité."},
                {"icon": '<i class="fa-solid fa-hard-drive"></i>', "title": "Immutabilité des sauvegardes", "desc": "Mise en place de sauvegardes immuables pour garantir l'intégrité de vos données face aux ransomwares et aux menaces internes."},
                {"icon": '<i class="fa-solid fa-envelope-open-text"></i>', "title": "Protection des emails", "desc": "Sécurisation des flux de messagerie contre le phishing, le spam et les malwares. Mise en place de SPF, DKIM, DMARC et solutions de filtrage avancées."},
                {"icon": '<i class="fa-solid fa-graduation-cap"></i>', "title": "Formation des utilisateurs", "desc": "Programmes de sensibilisation aux risques cyber : phishing, ingénierie sociale, bonnes pratiques de sécurité au quotidien."},
                {"icon": '<i class="fa-solid fa-triangle-exclamation"></i>', "title": "Réponse aux incidents", "desc": "Diagnostic d'impact rapide, assistance au dépôt de plainte, analyse forensique et accompagnement dans la gestion de crise."},
                {"icon": '<i class="fa-solid fa-arrows-rotate"></i>', "title": "Plan de reprise d'activité (PRA)", "desc": "Élaboration, documentation et tests réguliers de plans de continuité et de reprise d'activité pour minimiser l'impact des incidents sur votre business."},
                {"icon": '<i class="fa-solid fa-tower-observation"></i>', "title": "Bastion de sécurité", "desc": "Déploiement de bastions d'administration pour contrôler et tracer les accès privilégiés à vos systèmes critiques."},
                {"icon": '<i class="fa-solid fa-building-columns"></i>', "title": "Conformité ANSSI", "desc": "Mise en œuvre des recommandations de l'ANSSI et déploiement de solutions PAM pour une gestion rigoureuse des accès à privilèges."},
            ],
        },
        "supervision": {
            "page_title": '<i class="fa-solid fa-chart-column"></i> Supervision & Monitoring',
            "page_desc": "Gardez le contrôle sur votre infrastructure grâce à des solutions de surveillance open source, performantes et évolutives.",
            "sidebar_title": "Besoin de monitoring ?",
            "sidebar_desc": "Déployez une solution de supervision adaptée à votre infrastructure.",
            "sidebar_cta": "Discutons-en",
            "cta_title": "Surveillez votre infrastructure en temps réel",
            "cta_desc": "Déployez des solutions de monitoring puissantes et open source pour anticiper les incidents.",
            "prestations": [
                {"icon": '<i class="fa-solid fa-desktop"></i>', "title": "Déploiement monitoring", "desc": "Installation et configuration de solutions open source éprouvées : Zabbix, Wazuh, Elastic Stack, Grafana et CheckMK."},
                {"icon": '<i class="fa-solid fa-magnifying-glass"></i>', "title": "Surveillance infrastructure", "desc": "Monitoring continu de votre réseau, systèmes, services et applications 24/7. Détection proactive des anomalies avant qu'elles n'impactent votre activité."},
                {"icon": '<i class="fa-solid fa-shield-halved"></i>', "title": "Analyse de failles", "desc": "Veille proactive sur les vulnérabilités affectant vos systèmes. Identification, évaluation de la criticité et recommandations de correctifs prioritaires."},
                {"icon": '<i class="fa-solid fa-clipboard-list"></i>', "title": "Audit des logs", "desc": "Centralisation et analyse intelligente des logs réseaux et applicatifs. Corrélation d'événements pour une vision claire de l'activité de votre SI."},
                {"icon": '<i class="fa-solid fa-chart-line"></i>', "title": "Tableaux de bord personnalisés", "desc": "Création de dashboards sur-mesure avec Grafana, adaptés à vos besoins métier. Visualisation en temps réel de vos indicateurs clés."},
                {"icon": '<i class="fa-solid fa-bell"></i>', "title": "Alerting & Notification", "desc": "Configuration d'alertes intelligentes en temps réel : email, SMS, Slack ou Teams. Réduisez le temps de réaction face aux incidents critiques."},
            ],
        },
        "architecture-reseau": {
            "page_title": '<i class="fa-solid fa-globe"></i> Architecture Réseau',
            "page_desc": "Des architectures réseau robustes, sécurisées et évolutives pour tous vos environnements : industriel, maritime et tertiaire.",
            "sidebar_title": "Un projet réseau ?",
            "sidebar_desc": "Concevons ensemble l'architecture réseau idéale pour votre entreprise.",
            "sidebar_cta": "Nous contacter",
            "cta_title": "Concevons ensemble votre réseau de demain",
            "cta_desc": "Des architectures pensées pour la performance, la sécurité et la croissance de votre entreprise.",
            "prestations": [
                {"icon": '<i class="fa-solid fa-diagram-project"></i>', "title": "Conception d'architectures", "desc": "Conception et déploiement d'architectures WAN, LAN et WLAN optimisées pour vos environnements industriels, maritimes et bureautiques."},
                {"icon": '<i class="fa-solid fa-shuffle"></i>', "title": "Segmentation réseau", "desc": "Mise en place d'architectures réseau segmentées et sécurisées. Isolation des flux, micro-segmentation et contrôle d'accès pour limiter la surface d'attaque."},
                {"icon": '<i class="fa-solid fa-earth-europe"></i>', "title": "SD-WAN / SASE", "desc": "Interconnexion de vos sites distants avec des solutions SD-WAN et SASE modernes. Optimisation de la bande passante, haute disponibilité et sécurité intégrée."},
                {"icon": '<i class="fa-solid fa-tower-observation"></i>', "title": "Bastion d'administration", "desc": "Déploiement et gestion de bastions d'administration pour un accès sécurisé et auditable à vos équipements réseau et serveurs critiques."},
                {"icon": '<i class="fa-solid fa-cloud"></i>', "title": "Solutions cloud", "desc": "Architectures cloud sur AWS, déploiement Nextcloud et solutions hybrides adaptées à vos besoins. Migrez en toute confiance vers le cloud avec un accompagnement expert."},
            ],
        },
        "conseil": {
            "page_title": '<i class="fa-solid fa-handshake"></i> Conseil & Accompagnement',
            "page_desc": "Un partenaire de confiance pour piloter vos projets IT, former vos équipes et structurer votre système d'information.",
            "sidebar_title": "Un projet à piloter ?",
            "sidebar_desc": "Bénéficiez d'un accompagnement expert pour mener à bien vos projets IT.",
            "sidebar_cta": "Parlons-en",
            "cta_title": "Accompagnons ensemble votre transformation",
            "cta_desc": "De la stratégie à l'opérationnel, nous sommes à vos côtés pour structurer et sécuriser votre SI.",
            "prestations": [
                {"icon": '<i class="fa-solid fa-bullseye"></i>', "title": "Gestion de projet IT", "desc": "Pilotage complet de vos projets d'infrastructure de A à Z : cadrage, planification, exécution et mise en production."},
                {"icon": '<i class="fa-solid fa-scroll"></i>', "title": "Spécification de normes SI", "desc": "Rédaction et mise en œuvre de référentiels techniques et organisationnels pour structurer votre système d'information."},
                {"icon": '<i class="fa-solid fa-circle-check"></i>', "title": "Mise aux normes", "desc": "Accompagnement vers la conformité réglementaire et les bonnes pratiques : RGPD, recommandations ANSSI, normes sectorielles."},
                {"icon": '<i class="fa-solid fa-graduation-cap"></i>', "title": "Formation", "desc": "Transfert de compétences aux équipes techniques : administration réseau, supervision, bonnes pratiques de sécurité."},
                {"icon": '<i class="fa-solid fa-hard-drive"></i>', "title": "Plans de sauvegarde", "desc": "Définition et mise en œuvre de stratégies de sauvegarde robustes : politique de rétention, sauvegarde 3-2-1, tests de restauration réguliers."},
                {"icon": '<i class="fa-solid fa-wrench"></i>', "title": "Maintenance", "desc": "Contrats de maintenance et support pour assurer la continuité de service de votre infrastructure. Interventions rapides et support réactif."},
            ],
        },
    },
    "contact": {
        "page_title": '<i class="fa-solid fa-phone"></i> Contactez-nous',
        "page_desc": "Un projet, une question, un besoin d'audit ? Parlons-en. Nous vous répondons sous 24h.",
        "form_title": "Envoyez-nous un message",
        "form_subtitle": "Remplissez le formulaire ci-dessous et nous vous recontacterons rapidement.",
        "submit_btn": "Envoyer le message",
        "subjects": [
            {"value": "audit", "label": "Demande d'audit de sécurité"},
            {"value": "supervision", "label": "Supervision & Monitoring"},
            {"value": "reseau", "label": "Architecture réseau"},
            {"value": "conseil", "label": "Conseil & Accompagnement"},
            {"value": "devis", "label": "Demande de devis"},
            {"value": "autre", "label": "Autre"},
        ],
    },
    "veille": {
        "page_title": '<i class="fa-solid fa-shield-halved"></i> Veille Sécurité',
        "page_desc": "Les dernières alertes cybersécurité, bulletins de vulnérabilité et recommandations pour protéger votre infrastructure.",
        "section_title": "Alertes & Bulletins récents",
        "section_subtitle": "Restez informé des dernières menaces et vulnérabilités identifiées par les organismes de référence.",
        "cta_title": "Protégez votre entreprise",
        "cta_desc": "Besoin d'un audit de sécurité ou d'une solution de surveillance ? Contactez-nous pour un premier échange gratuit.",
        "articles": [
            {"tag": "Critique", "tag_class": "critical", "date": "28 mars 2026", "title": "Vulnérabilité critique dans OpenSSL 3.x", "desc": "Une faille de type buffer overflow a été identifiée dans OpenSSL 3.x permettant une exécution de code à distance. Mise à jour recommandée immédiatement.", "source": "CERT-FR"},
            {"tag": "Important", "tag_class": "warning", "date": "25 mars 2026", "title": "Campagne de phishing ciblant les PME françaises", "desc": "L'ANSSI alerte sur une vague de phishing sophistiqué usurpant l'identité de fournisseurs courants. Vigilance accrue recommandée sur les emails entrants.", "source": "ANSSI"},
            {"tag": "Critique", "tag_class": "critical", "date": "20 mars 2026", "title": "Mise à jour de sécurité Windows Server — mars 2026", "desc": "Microsoft publie un correctif pour plusieurs vulnérabilités critiques affectant Windows Server 2019/2022, dont une élévation de privilèges Active Directory.", "source": "Microsoft MSRC"},
            {"tag": "Information", "tag_class": "info", "date": "18 mars 2026", "title": "Guide ANSSI : sécuriser son infrastructure Active Directory", "desc": "L'ANSSI publie un guide actualisé des bonnes pratiques pour sécuriser Active Directory : durcissement, surveillance et gestion des comptes à privilèges.", "source": "ANSSI"},
            {"tag": "Important", "tag_class": "warning", "date": "15 mars 2026", "title": "Vulnérabilité Zabbix Server — exécution de code", "desc": "Une vulnérabilité permettant une exécution de code à distance a été identifiée dans Zabbix Server 6.x. La mise à jour vers la dernière version est fortement recommandée.", "source": "CVE / Zabbix"},
            {"tag": "Information", "tag_class": "info", "date": "10 mars 2026", "title": "Recommandations pour la sauvegarde 3-2-1-1-0", "desc": "Retour sur la règle 3-2-1-1-0 pour des sauvegardes résilientes : 3 copies, 2 types de supports, 1 hors site, 1 immuable, 0 erreur de restauration.", "source": "NumAsYouR"},
        ],
    },
}


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
    return {"site": SITE, "service_menu": service_menu_items()}


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
        page_title="À propos — NumAsYouR",
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
