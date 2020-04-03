# Výdej materiálu

Aplikace na výdej materiálu jako roušek v období Coronavirové krize.

[![license: AGPL v3](https://img.shields.io/badge/license-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![code style: Black](https://img.shields.io/badge/code%20style-Black-000000.svg)](https://github.com/psf/black)
[![powered by: Django](https://img.shields.io/badge/powered%20by-Django-brightgreen)](https://www.djangoproject.com)

## Konfigurace

Je třeba nastavit environment proměnné:

| proměnná | default | popis |
| --- | --- | --- |
| `DATABASE_URL` | | DSN k databázi (např. `postgres://user:pass@localhost:5342/vydej`) |

V produkci musí být navíc nastaveno:

| proměnná | default | popis |
| --- | --- | --- |
| `DJANGO_SECRET_KEY` | | tajný šifrovací klíč |
| `DJANGO_ALLOWED_HOSTS` | | allowed hosts (více hodnot odděleno čárkami) |
| `SITE_URL` | | adresa webu bez lomítka na konci (vkládá se do emailů) |
| `MAILGUN_API_KEY` | | Mailgun API klíč |

Další konfigurační parametry:

| proměnná | default | popis |
| --- | --- | --- |
| `MAILGUN_API_URL` | "https://api.eu.mailgun.net/v3" | Mailgun API URL |
| `MAILGUN_SENDER_DOMAIN` | "mail.vydej-materialu.cz" | Mailgun sender domain |
| `EMAIL_FROM` | "noreply@vydej-materialu.cz" | adresa pro emaily z aplikace |

## Management projektu

### Command load_groups

Do databáze je třeba nahrát předdefinované uživatelské skupiny s oprávněními.
K tomu slouží management command `load_groups`:

    $ python manage.py load_groups

Tento command se v Docker kontejneru pouští automaticky před startem serveru.

## Vývoj

Pro vývoj je definován pomocný `Makefile` pro časté akce.

### Lokální instalace a spuštění

#### Vytvoření virtualenv pro instalaci závislostí

Vytvoř virtualenv:

    $ make venv

Vytvoří virtualenv ve složce `.venv`. Předpokládá že výchozí `python` v terminálu
je Python 3. Pokud tomu tak není, použijte třeba [Pyenv](https://github.com/pyenv/pyenv)
pro instalaci více verzí Pythonu bez rizika rozbití systému.

#### Aktivace virtualenvu

Před prací na projektu je třeba aktivovat virtualenv. To bohužel nejde dělat
pomocí nástroje `make`. Je třeba zavolat příkaz:

    $ source .venv/bin/activate

Můžete asi na to vytvořit alias pro shell. Do `~/.bash_profile` nebo `~/.zshrc`
nebo jiného konfiguračního souboru dle vašeho shellu přidejte:

    alias senv='source .venv/bin/activate'

A pak můžete virtualenv aktivovat pouze jednoduchým voláním:

    $ senv

Pro sofistikovanější řešení, které vám aktivuje virtualenv při změně adresáře na
adresář s projektem, slouží nástroj [direnv](https://direnv.net/).

Deaktivace virtualenvu se dělá příkazem:

    $ deactivate

#### Instalace závislostí

V aktivovaném virtualenvu spusťte:

    $ make install

To nainstaluje Pythonní závislosti pro vývoj projektu na lokále.

#### Nastavení environment proměnných

Nastav environment proměnné (viz konfigurace výše). Pro jednoduchost doporučujeme
použít [direnv](https://direnv.net/), který nastaví environment proměnné pro vývoj
při změně adresáře na adresář s projektem. 

Příklad `.envrc`:

    export DATABASE_URL=postgres://db:db@localhost:5432/vydej

Pro lokální vývoj obsahují settings:

    DEBUG = True
    ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"]
    SITE_URL = "http://localhost:8008"
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

### Management projektu

#### Migrace databáze

Aplikuj migrace databáze:

    $ make migrate

Při změně modelů vygeneruj migrace pomocí:

    $ make migrations

#### Spuštění development serveru

Django development server na portu `8008` se spustí příkazem:

    $ make run

Poté můžete otevřít web na adrese [http://localhost:8008](http://localhost:8008)

#### Django shell

Django shell používající `shell_plus` z Django extensions spustíte:

    $ make shell

### Testy

Používá se testovací framework [pytest](https://pytest.org). Spuštění testů:

    $ pytest

Případně přes `make`, ale bez možnosti parametrizovat spuštění testů:

    $ make test

Coverage report:

    $ make coverage

### Code quality

K formátování kódu se používá [black](https://github.com/psf/black). Doporučujeme
ho nainstalovat do vašeho editoru kódu, aby soubory přeformátoval po uložení.

Přeformátování kódu nástrojem `black` je součástí `pre-commit` hooks (viz níže).

Součástí `pre-commit` hooků je také automatické seřazení importů v Pythonních
souborech nástrojem [isort](https://github.com/timothycrosley/isort/).

### Pre-commit hooky

Použivá se [pre-commit](https://pre-commit.com/) framework pro management git
pre-commit hooks.

Máte-li pre-commit framework [nainstalovaný](https://pre-commit.com/#installation)
spusttě příkaz:

    $ make install-hooks

Ten naisntaluje hooky pro projekt. A poté při každém commitu dojde k požadovaným
akcím na změněných souborech.

Ručně se dají hooky na všechny soubory spustit příkazem:

    $ make hooks

## Upgrade závislostí

K upgrade se používají [pip-tools](https://github.com/jazzband/pip-tools) (`pip install pip-tools`):

    $ cd requirements/
    $ pip-compile -U base.in
    $ pip-compile -U dev.in
    $ pip-compile -U prod.in

Tím se vygenerují `base.txt`, `dev.txt` a `prod.txt`

## Docker

Zatím provizorní řešení přes manuální build a push do Docker HUB.

Build image s aplikací:

    $ make build

Push do Docker Hub:

    $ make release
