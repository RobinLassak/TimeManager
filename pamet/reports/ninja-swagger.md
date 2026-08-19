# Návod: Django Ninja a Swagger v TimeManager

Tento dokument popisuje, jak v projektu TimeManager používáme Django Ninja a vestavěný Swagger UI. Drží se rozhodnutí z 2026-08-19. Kód píše uživatel; tento soubor je jen dokumentace.

---

## 1. Co to je a proč to používáme

**Django Ninja** je knihovna nad Djangem. Umí:

- routy (`GET`, `POST`, `PUT`, `DELETE`)
- validaci těla requestu přes `Schema`
- automatické OpenAPI schéma
- **Swagger UI** na `/api/docs`

Je to stejný princip jako Swagger v Nestu nebo .NETu: dokumentace je součástí projektu, ne samostatný Postman.

Čisté Django `View` + `JsonResponse` Swagger samo nevyrobí. Proto jsme `CustomerController` převedli z `View` na Ninja `Router`.

---

## 2. Tok vrstev (neměnit)

```text
HTTP request
  → Router (controller)
    → Schema (CustomerIn)          jen HTTP / Swagger
      → DTO (CustomerDTO)          mezivrstva k service
        → Service
          → Entity                 Django model, DB
            → DB
```

Zpět:

```text
Entity → DTO → asdict → Schema (CustomerOut) → JSON
```

Pravidla:

- Controller **nesahá** na `Customer.objects` ani `save()`.
- Service **nevrací** entitu ven, jen DTO.
- `Schema` (`CustomerIn` / `CustomerOut`) je jen pro HTTP a Swagger.
- Do service vždy jde `CustomerDTO`, ne Ninja Schema.

---

## 3. Instalace

V aktivním venv ve složce `backend/`:

```bash
source .venv/bin/activate
pip install django-ninja
pip freeze > requirements.txt
```

Ninja se **nepřidává** do `INSTALLED_APPS`.

---

## 4. Soubory a kdo co vlastní

| Soubor | Účel |
|---|---|
| `app/api.py` | jedna instance `NinjaAPI`, sem se připojují routery |
| `app/controllers/<nazev>_controller.py` | `Router`, `Schema`, funkce endpointů |
| `config/urls.py` | `path("api/", api.urls)` |
| `app/services/` | CRUD, beze změny kvůli Ninja |

`NinjaAPI` **nepatří** do controlleru. Controller exportuje jen `router`.

`app/urls.py` u API **nepoužíváme**. Cesty skládá Ninja.

---

## 5. `app/api.py` — vstupní bod

```python
from ninja import NinjaAPI

from app.controllers.customer_controller import router as customer_router

api = NinjaAPI(title="TimeManager", version="1.0.0")
api.add_router("/customers", customer_router)
```

Další zdroj (Project, Work) se přidá stejným způsobem:

```python
from app.controllers.project_controller import router as project_router

api.add_router("/projects", project_router)
```

Prefix `/customers` + routa `/` = `/api/customers/`.  
Prefix `/customers` + routa `/{id}` = `/api/customers/5/`.

`/api` dodá `config/urls.py`.

---

## 6. `config/urls.py`

```python
from django.contrib import admin
from django.urls import path

from app.api import api

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
]
```

Hotové adresy:

```text
http://127.0.0.1:8000/api/docs          Swagger UI
http://127.0.0.1:8000/api/customers/    seznam / create
http://127.0.0.1:8000/api/customers/1/  detail / update / delete
```

---

## 7. Controller — vzor (Customer)

### 7.1 Importy

Jen to, co controller opravdu používá:

```python
from dataclasses import asdict
from datetime import datetime

from ninja import Router, Schema
from ninja.errors import HttpError

from app.dto.customer_dto import CustomerDTO
from app.services.customer_service import CustomerService
```

Nepoužívat v controlleru: `NinjaAPI`, `json`, `JsonResponse`, `View`, `csrf_exempt`.

### 7.2 Router a service

```python
router = Router(tags=["customers"])
service = CustomerService()
```

`tags` seskupí endpointy ve Swaggeru. Pro Project: `tags=["projects"]`.

Není to Django `View` třída. Jsou to **funkce** na jednom `router`.

### 7.3 Schémata In / Out

- **`XxxIn`** — tělo requestu (create / update). Bez `id`, bez `created_at`, bez `updated_at`.
- **`XxxOut`** — odpověď. S `id` a timestampy.

```python
class CustomerIn(Schema):
    first_name: str
    last_name: str
    # ... business pole

class CustomerOut(Schema):
    id: int
    first_name: str
    # ... stejná business pole
    created_at: datetime
    updated_at: datetime
```

`created_at` / `updated_at` piš jako `datetime`, ne `str`. `asdict` z DTO vrací `datetime`.

### 7.4 Převod Schema → DTO

```python
def _to_dto(payload: CustomerIn, id: int | None = None) -> CustomerDTO:
    return CustomerDTO(**payload.dict(), id=id)
```

`id` u update ber z URL, ne z těla: `_to_dto(payload, id)`.

### 7.5 Routy

Každá HTTP metoda má **vlastní funkci**. List a detail jsou dvě `GET` routy, ne jedna `get` s `if id`.

| Metoda | Cesta | Status OK | Service |
|---|---|---|---|
| GET | `/` | 200 | `get_all_*` |
| GET | `/{id}` | 200 / 404 | `get_*_by_id` |
| POST | `/` | 201 | `create_*` |
| PUT | `/{id}` | 200 / 404 | `update_*` |
| DELETE | `/{id}` | 204 / 404 | `delete_*` |

`id` v cestě je `{id}` (Ninja). Django `path` používal `<int:id>`.

### 7.6 Odpovědi a chyby

```python
# seznam — asdict na KAŽDÝ prvek, ne na list
return [asdict(item) for item in items]

# jeden objekt
return asdict(item)

# create (dekorátor musí sedět s return)
@router.post("/", response={201: CustomerOut})
def create(...):
    return 201, asdict(item)

# delete
@router.delete("/{id}", response={204: None})
def delete(...):
    return 204, None

# nenalezeno
raise HttpError(404, "Customer not found")
```

Když v dekorátoru napíšeš `response={201: CustomerOut}`, **musíš** vrátit `return 201, tělo`. Stejně u 204.

`asdict` umí jen **jeden** dataclass. Na seznam vždy comprehension.

---

## 8. Jak přidat nový zdroj (Project / Work)

1. Zkopíruj vzor z `customer_controller.py`.
2. Přejmenuj Router tag, Schema, service, hlášky 404.
3. U Project: `ProjectIn` má `customer_id`. U Work: `WorkIn` má `project_id`.
4. Datumy (`start_date`, `end_date`) ve Schema jako `date`.
5. V `api.py` přidej `add_router("/projects", project_router)` (resp. `/works`).
6. Service neměň, pokud už CRUD existuje.
7. Ověř ve Swaggeru na `/api/docs`.

---

## 9. Práce ve Swagger UI

1. Spusť venv a server:

```bash
cd backend
source .venv/bin/activate
python manage.py runserver
```

2. Otevři `http://127.0.0.1:8000/api/docs`.
3. Rozbal endpoint → **Try it out** → vyplň JSON / `id` → **Execute**.
4. Prohlížeč umí jen GET. Create / update / delete zkoušej ve Swaggeru, ne v adresním řádku.

Příklad těla pro Customer (create / update):

```json
{
  "first_name": "Jan",
  "last_name": "Novak",
  "ico": "",
  "dic": "",
  "street": "",
  "city": "",
  "zip": "",
  "country": "",
  "email": "jan@example.com",
  "phone": "123456789",
  "website": ""
}
```

Povinná pole bere `CustomerIn`. Chybí-li pole, Ninja vrátí **422**, ne 400. To je v pořádku — validuje Schema.

---

## 10. Čeho se držet

- Jedna `NinjaAPI` v `app/api.py`. Další API instance nezakládej.
- Jeden `Router` na jeden zdroj (customers, projects, works).
- `id` u PUT/DELETE vždy z URL.
- 404 jen přes `HttpError`, když service vrátí `None` nebo `False`.
- Create = 201, delete = 204 bez těla.
- HTTP Schema ≠ DTO ≠ Entity. Tři různé věci.
- Controller je tenký: přečti request, zavolej service, vrať JSON / chybu.

---

## 11. Časté chyby

| Chyba | Co se stane | Řešení |
|---|---|---|
| `Router` není v importu | `NameError` | `from ninja import Router, Schema` |
| `NinjaAPI` v controlleru | zmatek, víc API | `NinjaAPI` jen v `api.py` |
| `asdict(seznam)` | pád, `asdict` chce jeden objekt | `[asdict(x) for x in seznam]` |
| `response={201: ...}` a `return asdict(...)` | status 200 nebo chyba | `return 201, asdict(...)` |
| `created_at: str` ve `XxxOut` | pád při prvním záznamu | použij `datetime` |
| `config/urls.py` pořád `include("app.urls")` | starý View / 404 | `path("api/", api.urls)` |
| Service volaná se Schema místo DTO | `payload.first_name` vs dict | `_to_dto` před service |

---

## 12. Co Ninja řeší za tebe

- parsování JSON těla do `payload: XxxIn`
- validace povinných polí (422)
- `Content-Type: application/json`
- serializace `datetime` v odpovědi
- CSRF u těchto API rout
- stránka `/api/docs` a schéma `/api/openapi.json`

Proto v Ninja controlleru není `json.loads`, `try/except JSONDecodeError`, `DjangoJSONEncoder` ani `csrf_exempt`.

---

## 13. Checklist nového endpointu

1. Funkce na `router` s dekorátorem (`@router.get` / `post` / `put` / `delete`).
2. `response=` sedí s tím, co `return` vrací (včetně status kódu).
3. Tělo requestu je `payload: XxxIn`.
4. Do service jde `_to_dto(...)`.
5. Ven jde `asdict(...)` nebo seznam `asdict`.
6. `None` / `False` ze service → `HttpError(404, ...)`.
7. Router je v `api.py` přes `add_router`.
8. Endpoint je vidět na `/api/docs` a jde ho kliknout.

---

## Zdroje

- Django Ninja: https://django-ninja.dev/
- OpenAPI / Swagger: https://swagger.io/specification/
- Vzor v projektu: `backend/app/controllers/customer_controller.py`, `backend/app/api.py`
- Worklog dne zavedení: `pamet/work/2026-08-19.md`
