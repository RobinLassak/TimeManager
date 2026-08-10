# Podrobný postup: zprovoznění Django frameworku

Tento návod popisuje kompletní postup od instalace Pythonu až po spuštění vývojového serveru a základní strukturu projektu. Postup je určen pro macOS (zsh), ale principy platí i jinde.

---

## 1. Předpoklady

### 1.1 Python

Django běží na Pythonu 3.10+. Ověř verzi:

```bash
python3 --version
```

Pokud Python chybí, na macOS doporučeně přes Homebrew:

```bash
brew install python
```

### 1.2 pip a venv

S Pythonem obvykle přijde i `pip` a modul `venv`:

```bash
python3 -m pip --version
python3 -m venv --help
```

---

## 2. Příprava projektu a virtuálního prostředí

Virtuální prostředí izoluje závislosti projektu od zbytku systému.

### 2.1 Vytvoř složku projektu

Například v backendu TimeManager:

```bash
cd /Applications/MyProjects/Programming/TimeManager/backend
mkdir django_app
cd django_app
```

### 2.2 Vytvoř a aktivuj venv

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Po aktivaci by měl prompt začínat `(.venv)`.

Deaktivace (kdykoli později):

```bash
deactivate
```

### 2.3 Aktualizuj pip

```bash
python -m pip install --upgrade pip
```

---

## 3. Instalace Django

### 3.1 Instalace balíčku

```bash
pip install django
```

Ověření:

```bash
python -m django --version
```

### 3.2 Uložení závislostí

```bash
pip freeze > requirements.txt
```

Pozdější instalace na jiném stroji:

```bash
pip install -r requirements.txt
```

---

## 4. Vytvoření Django projektu

### 4.1 `django-admin startproject`

V aktuální složce (např. `django_app`):

```bash
django-admin startproject config .
```

Tečka na konci znamená: vytvoř projekt *v této složce*, ne v podsložce.

Alternativa (vytvoří podsložku `mysite`):

```bash
django-admin startproject mysite
cd mysite
```

### 4.2 Typická struktura po `startproject config .`

```text
django_app/
├── .venv/
├── manage.py
├── requirements.txt
└── config/
    ├── __init__.py
    ├── asgi.py
    ├── settings.py
    ├── urls.py
    └── wsgi.py
```

- `manage.py` — CLI nástroj Django (migrace, server, shell, …)
- `config/settings.py` — nastavení projektu
- `config/urls.py` — hlavní směrování URL
- `config/wsgi.py` / `asgi.py` — vstupní body pro produkční servery

---

## 5. První spuštění vývojového serveru

### 5.1 Migrace databáze

Django má vestavěnou SQLite DB (výchozí). Nejdřív aplikuj výchozí migrace:

```bash
python manage.py migrate
```

Vznikne soubor `db.sqlite3` (pokud používáš výchozí nastavení).

### 5.2 Spuštění serveru

```bash
python manage.py runserver
```

Ve výchozím nastavení běží na:

```text
http://127.0.0.1:8000/
```

Jiný port:

```bash
python manage.py runserver 8080
```

Dostupné v síti (pozor — jen pro vývoj):

```bash
python manage.py runserver 0.0.0.0:8000
```

Uvidíš uvítací stránku Django — projekt běží.

Zastavení serveru: `Ctrl + C`.

---

## 6. Vytvoření administrátora (volitelné, ale užitečné)

```bash
python manage.py createsuperuser
```

Zadej username, e-mail a heslo. Pak:

```text
http://127.0.0.1:8000/admin/
```

---

## 7. Vytvoření vlastní aplikace (app)

Projekt = celý web; app = modul (např. `users`, `tasks`, `time_entries`).

### 7.1 Vytvoř appku

```bash
python manage.py startapp tasks
```

Struktura:

```text
tasks/
├── __init__.py
├── admin.py
├── apps.py
├── migrations/
├── models.py
├── tests.py
└── views.py
```

### 7.2 Zaregistruj appku v `settings.py`

Otevři `config/settings.py` a přidej do `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "tasks",  # tvoje appka
]
```

---

## 8. Model, migrace a admin

### 8.1 Příklad modelu v `tasks/models.py`

```python
from django.db import models


class Task(models.Model):
    title = models.CharField(max_length=200)
    done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
```

### 8.2 Migrace

```bash
python manage.py makemigrations
python manage.py migrate
```

- `makemigrations` — vygeneruje migrační soubory podle změn modelů
- `migrate` — aplikuje je do databáze

### 8.3 Zobrazení v adminu (`tasks/admin.py`)

```python
from django.contrib import admin
from .models import Task

admin.site.register(Task)
```

---

## 9. View, URL a šablona (minimální stránka)

### 9.1 View v `tasks/views.py`

```python
from django.http import HttpResponse


def home(request):
    return HttpResponse("TimeManager Django běží.")
```

### 9.2 URL v appce — `tasks/urls.py` (nový soubor)

```python
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
]
```

### 9.3 Napojení v hlavním `config/urls.py`

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("tasks.urls")),
]
```

Obnov stránku na `http://127.0.0.1:8000/` — měla by se zobrazit textová odpověď.

### 9.4 (Volitelně) HTML šablona

Vytvoř `tasks/templates/tasks/home.html`:

```html
<!DOCTYPE html>
<html lang="cs">
<head>
  <meta charset="utf-8">
  <title>TimeManager</title>
</head>
<body>
  <h1>TimeManager Django běží.</h1>
</body>
</html>
```

View:

```python
from django.shortcuts import render


def home(request):
    return render(request, "tasks/home.html")
```

Django hledá šablony v `templates/` uvnitř nainstalovaných appů automaticky.

---

## 10. Důležitá nastavení ve `settings.py` (vývoj)

### 10.1 `DEBUG` a `ALLOWED_HOSTS`

Pro lokální vývoj:

```python
DEBUG = True
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]
```

V produkci musí být `DEBUG = False` a `ALLOWED_HOSTS` vyplněné skutečnými doménami.

### 10.2 `SECRET_KEY`

Nikdy necommituj produkční secret do gitu. Pro vývoj stačí generovaný klíč z `startproject`; později přesměřuj na env proměnnou:

```python
import os

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "dev-only-unsafe-key")
```

### 10.3 Databáze

Výchozí SQLite:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
```

Pro PostgreSQL později typicky:

```bash
pip install psycopg[binary]
```

a úprava `DATABASES` na `django.db.backends.postgresql`.

### 10.4 Časová zóna a jazyk (ČR)

```python
LANGUAGE_CODE = "cs"
TIME_ZONE = "Europe/Prague"
USE_I18N = True
USE_TZ = True
```

---

## 11. Časté příkazy `manage.py`

| Příkaz | Účel |
|--------|------|
| `python manage.py runserver` | vývojový server |
| `python manage.py migrate` | aplikovat migrace |
| `python manage.py makemigrations` | vytvořit migrace z modelů |
| `python manage.py createsuperuser` | admin účet |
| `python manage.py shell` | interaktivní Django shell |
| `python manage.py check` | kontrola konfigurace |
| `python manage.py collectstatic` | sesbírat static soubory (hlavně produkce) |
| `python manage.py startapp nazev` | nová appka |
| `python manage.py showmigrations` | stav migrací |

---

## 12. Doporučený denní workflow

1. Přejdi do složky projektu.
2. Aktivuj venv: `source .venv/bin/activate`
3. (Volitelně) `pip install -r requirements.txt` po pullu změn
4. `python manage.py migrate`
5. `python manage.py runserver`
6. Pracuj v prohlížeči na `http://127.0.0.1:8000/`
7. Po změně modelů: `makemigrations` → `migrate`

---

## 13. `.gitignore` (doporučení)

Do kořene Django projektu přidej mimo jiné:

```gitignore
.venv/
__pycache__/
*.py[cod]
db.sqlite3
*.log
.env
staticfiles/
media/
.DS_Store
```

---

## 14. Typické problémy a řešení

### `command not found: django-admin`

Venv není aktivní, nebo Django není nainstalované:

```bash
source .venv/bin/activate
pip install django
```

### `ModuleNotFoundError: No module named 'django'`

Spouštíš `python` mimo venv, nebo máš jiný interpret. Používej:

```bash
source .venv/bin/activate
which python
python manage.py runserver
```

### Port 8000 je obsazený

```bash
python manage.py runserver 8001
```

### Migrace po změně modelu nefungují

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py showmigrations
```

### `DisallowedHost`

Doplň hostitele do `ALLOWED_HOSTS` v `settings.py`.

### Static soubory v produkci

Ve vývoji Django servíruje static automaticky při `DEBUG=True`. V produkci použij `collectstatic` a webserver (Nginx) nebo WhiteNoise.

---

## 15. Rychlý checklist „od nuly k běžícímu Django“

```bash
# 1) složka + venv
mkdir django_app && cd django_app
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip

# 2) Django
pip install django
pip freeze > requirements.txt

# 3) projekt
django-admin startproject config .

# 4) DB + server
python manage.py migrate
python manage.py runserver
```

Otevři `http://127.0.0.1:8000/`.

---

## 16. Co dál (až běží základ)

- REST API: Django REST Framework (`djangorestframework`)
- Auth: vestavěný `django.contrib.auth`, případně token/JWT
- Frontend: šablony Django, nebo oddělený React/Vue proti API
- Produkce: Gunicorn/Uvicorn + Nginx, PostgreSQL, `DEBUG=False`, env secret
- Testy: `python manage.py test`

---

## Zdroje

- Oficiální dokumentace: https://docs.djangoproject.com/
- Tutorial (Writing your first Django app): https://docs.djangoproject.com/en/stable/intro/tutorial01/
- Instalace: https://docs.djangoproject.com/en/stable/topics/install/
