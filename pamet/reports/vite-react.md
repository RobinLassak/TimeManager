# Návod: instalace Vite + React v TimeManager

Tento dokument popisuje, jak ve složce `web/` založit a spouštět frontend (Vite + React + TypeScript). Drží se postupu z 2026-08-20. Kód píše uživatel; tento soubor je jen dokumentace. Postup je určen pro macOS (zsh).

---

## 1. Co to je

**Vite** je vývojový server a bundler pro frontend.  
**React** je knihovna na UI.  
**TypeScript** přidává typy (stejný důvod jako typy v Pythonu na backendu).

Struktura projektu:

```text
TimeManager/
├── backend/     Django + Ninja (API)
├── web/         Vite + React (frontend)
└── pamet/
```

Frontend běží zvlášť na portu **5173**. Backend na **8000**. Zatím se nevolají navzájem.

---

## 2. Předpoklady

### 2.1 Node.js a npm

```bash
node -v
npm -v
```

Pokud Node chybí, na macOS:

```bash
brew install node
```

Ověřené verze při zakládání (2026-08-20): npm 11.8.0, Vite 8.2.

### 2.2 Odkud příkaz pouštět

Vždy z **kořene TimeManager**, ne z `backend/` a ne z už existující `web/`.

```bash
cd /Applications/MyProjects/Programming/TimeManager
```

Když příkaz `create vite … web` spustíš už uvnitř `web/`, vznikne `web/web/`. To je špatně.

---

## 3. Vytvoření projektu

### 3.1 Šablona

Používáme TypeScript:

```bash
cd /Applications/MyProjects/Programming/TimeManager
npm create vite@latest web -- --template react-ts
```

Jen JavaScript (nepoužíváme):

```bash
npm create vite@latest web -- --template react
```

`npx` se může zeptat `Ok to proceed?` — potvrď `y`.

### 3.2 Otázky průvodce

| Otázka | Volba |
|---|---|
| Which linter to use? | **Oxlint** (výchozí, Enter) |
| Install with npm and start now? | **Yes** — nainstaluje závislosti a spustí server |

Oxlint je rychlejší výchozí linter u nového Vite. ESLint ber jen když ho chceš cíleně.

### 3.3 Správný výsledek

Projekt musí ležet přímo v `TimeManager/web/`:

```text
TimeManager/web/
├── src/
├── public/
├── index.html
├── package.json
├── package-lock.json
├── vite.config.ts
├── tsconfig.json
└── …
```

`package.json` patří sem, ne do `web/web/package.json`.

### 3.4 Když vznikne `web/web/`

Vite jsi spustil zevnitř `web/`. Přesuň obsah o úroveň výš.

V **zsh** nepoužívej `!` v příkazu (`event not found`). Použij:

```bash
cd /Applications/MyProjects/Programming/TimeManager
cp -R web/web/. web/
rm -rf web/web
```

Ověření:

```bash
ls web
```

Musíš vidět `package.json`, `src`, `index.html` — ne další složku `web`.

---

## 4. Závislosti a první start

Když jsi v průvodci dal „Install with npm and start now? Yes“, `npm install` už proběhlo.

Ručně (kdykoli později):

```bash
cd /Applications/MyProjects/Programming/TimeManager/web
npm install
npm run dev
```

Prohlížeč:

```text
http://127.0.0.1:5173/
```

Uvidíš výchozí stránku Vite + React („Get started“, tlačítko Count). To znamená, že frontend běží.

Zastavení serveru: `Ctrl + C`.

---

## 5. Denní spuštění

Dva terminály.

**Backend:**

```bash
cd /Applications/MyProjects/Programming/TimeManager/backend
source .venv/bin/activate
python manage.py runserver
```

```text
http://127.0.0.1:8000/api/docs
```

**Frontend:**

```bash
cd /Applications/MyProjects/Programming/TimeManager/web
npm run dev
```

```text
http://127.0.0.1:5173/
```

---

## 6. Užitečné příkazy v `web/`

| Příkaz | Účel |
|---|---|
| `npm run dev` | vývojový server (Vite) |
| `npm run build` | produkční sestavení (`dist/`) |
| `npm run preview` | náhled po `build` |
| `npm run lint` | Oxlint |
| `npm install` | doinstalovat závislosti po `git pull` |

---

## 7. Co patří do gitu a co ne

Do gitu patří mimo jiné:

- `web/src/`
- `web/package.json`
- `web/package-lock.json`
- `web/vite.config.ts`
- `web/tsconfig*.json`
- `web/index.html`

Do gitu **nepatří** (řeší kořenový `.gitignore`):

- `node_modules/`
- `dist/`, `dist-ssr/`
- `.vite/`
- `.env`, `.env.*` (kromě `.env.example`)
- `*.local`, `*.tsbuildinfo`, `.oxlintcache`

`package-lock.json` se neignoruje.

---

## 8. Čeho se držet

- Frontend je ve `web/`, backend v `backend/`. Nemíchej je.
- `create vite` pouštěj z kořene TimeManager.
- Šablona je `react-ts`.
- Linter je Oxlint.
- API (CORS, `fetch` na `/api/customers/`) řeš až budeš napojovat backend. Samotný Vite na to nečeká.
- Výchozí soubory (`App.tsx`, loga) můžeš později nahradit vlastní aplikací. Teď stačí, že projekt startuje.

---

## 9. Časté chyby

| Chyba | Co se stane | Řešení |
|---|---|---|
| `create vite` zevnitř `web/` | vznikne `web/web/` | přesunout obsah výš, smazat vnořenou `web` |
| `mv … .[!.]*` v zsh | `event not found: .]` | použít `cp -R web/web/. web/` |
| `npm run dev` z `backend/` | není `package.json` | `cd web` |
| Node není v PATH | `command not found: npm` | `brew install node` |
| Port 5173 obsazený | Vite nabídne jiný port | použij vypsanou URL, nebo ukonči starý proces |

---

## 10. Checklist „od nuly k běžícímu Vite“

```bash
# 1) kořen projektu
cd /Applications/MyProjects/Programming/TimeManager

# 2) Node
node -v
npm -v

# 3) Vite + React + TS
npm create vite@latest web -- --template react-ts
# Oxlint → Enter
# Install and start → Yes

# 4) ověř, že projekt NENÍ v web/web/
ls web/package.json

# 5) prohlížeč
# http://127.0.0.1:5173/
```

Pozdější start stačí `cd web && npm run dev`.

---

## 11. Co dál (až běží základ)

- Smazat / nahradit výchozí `App.tsx`
- Volání Django API (`/api/customers/`, `/api/projects/`, `/api/works/`)
- CORS na backendu, až frontend začne volat API z jiného portu
- Sdílené typy s DTO (později)

---

## Zdroje

- Vite: https://vite.dev/guide/
- React: https://react.dev/
- Vzor v projektu: `web/package.json`, `web/vite.config.ts`, `web/src/App.tsx`
- Backend API: `pamet/reports/ninja-swagger.md`
