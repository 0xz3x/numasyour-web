# NumAsYouR - Application Web Flask

Application Flask issue de la migration du site vitrine NumAsYouR.

Le projet a été nettoyé pour ne garder que l'application Python, les templates Jinja, les assets statiques nécessaires et le contenu centralisé dans `app.py`.

## Arborescence

- `app.py` : application Flask
- `wsgi.py` : point d'entrée production pour `gunicorn`
- `templates/` : templates Jinja
- `css/` : styles du site
- `js/app.js` : interactions front-end
- `img/` : logos et favicon

Les anciennes pages HTML statiques et les anciens scripts d'injection ont été retirés pour éviter les doublons.

## Prérequis

- Python 3.11 ou supérieur
- `pip`
- `gunicorn`
- `systemd` et un reverse proxy Linux comme `nginx`

## Installation

```bash
git clone <votre-depot>
cd site-web
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Lancement en local

```bash
python app.py
```

L'application est alors disponible sur `http://127.0.0.1:5000`.

## Déploiement Linux avec systemd

Architecture recommandée:

- `gunicorn` exécute l'application Flask via `wsgi:app`
- `systemd` supervise le processus Python
- `nginx` termine le TLS et relaie les requêtes vers `gunicorn`

### Exemple de service systemd

Créer `/etc/systemd/system/numasyour.service`:

```ini
[Unit]
Description=NumAsYouR Flask App
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/numasyour
Environment="PATH=/var/www/numasyour/.venv/bin"
ExecStart=/var/www/numasyour/.venv/bin/gunicorn --workers 3 --bind 127.0.0.1:8000 wsgi:app
Restart=always

[Install]
WantedBy=multi-user.target
```

Activer le service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable numasyour
sudo systemctl start numasyour
sudo systemctl status numasyour
```

### Exemple de configuration nginx

```nginx
server {
	listen 80;
	server_name example.com;

	location / {
		proxy_pass http://127.0.0.1:8000;
		proxy_set_header Host $host;
		proxy_set_header X-Real-IP $remote_addr;
		proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
		proxy_set_header X-Forwarded-Proto $scheme;
	}
}
```

## Points d'attention

- Le formulaire de contact est validé côté serveur mais n'envoie pas encore d'email.
- Le champ hébergeur des mentions légales reste à compléter.
- Le bandeau cookies repose sur `localStorage`.

## Vérification rapide

```bash
python -m py_compile app.py
gunicorn --bind 127.0.0.1:8000 wsgi:app
```
