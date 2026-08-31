# Налаштування динамічного профілю (SVG + GitHub Actions)

Цей репозиторій має називатися **точно як твій нікнейм**: `kxardas/kxardas`.
Тоді `README.md` показується вгорі твого профілю, а `today.py` щодня оновлює статистику в `dark_mode.svg` / `light_mode.svg`.

## Файли
- `README.md` — вбудовує SVG (темний/світлий за темою GitHub).
- `dark_mode.svg`, `light_mode.svg` — сам «термінал». Статичний текст (OS, Host, мови, хобі, контакти, ASCII-портрет) редагуєш руками; поля статистики (`id="..."`) заповнює скрипт.
- `today.py` — тягне статистику з GitHub GraphQL API.
- `cache/requirements.txt` — залежності Python.
- `.github/workflows/build.yaml` — запуск щодня о 04:00 UTC + при кожному push.

## Кроки

### 1. Створи Personal Access Token (classic)
GitHub → Settings → Developer settings → Personal access tokens → **Tokens (classic)** → Generate new token.
Постав галочки: **`repo`** і **`read:user`**. Скопіюй токен.

### 2. Створи репозиторій і залий файли
```bash
cd /Users/kxardas/coding/github/readme
git init
git add .
git commit -m "dynamic profile readme"
gh repo create kxardas --public --source=. --push
```

### 3. Додай секрети в репозиторій
Repo → Settings → Secrets and variables → **Actions** → New repository secret:
- `ACCESS_TOKEN` = твій токен з кроку 1
- `USER_NAME` = `kxardas`

### 4. Постав свою дату народження
У `today.py` (рядок ~450) заміни `datetime.datetime(2000, 1, 1)` на свою дату — це поле **Uptime**.

### 5. Запусти вручну перший раз
Repo → **Actions** → «README build» → Run workflow.
Після завершення скрипт закомітить оновлені SVG зі справжньою статистикою.

## Що редагувати вручну (не чіпаючи `id=`)
У `dark_mode.svg` і `light_mode.svg` онови текстові `value`-поля:
OS, Host, Kernel, IDE, Languages, Hobbies, Contact (LinkedIn/Discord).
`kxardas@github`, email `galimurkap@gmail.com` вже підставлені.

## Оновити ASCII-іконку
Зараз ліворуч — логотип із `merlin.txt` (build-скрипт автоматично масштабує шрифт,
щоб арт вмістився в ліву колонку, і прибирає neofetch-коди кольору `${c1..}`).
Щоб змінити — поклади новий ASCII у файл і дай мені перезібрати SVG
(або онови рядки в блоці `<text x="15" ...>` обох SVG вручну).

## Локальна перевірка (опційно)
```bash
python3 -m venv venv && ./venv/bin/pip install -r cache/requirements.txt
ACCESS_TOKEN=xxx USER_NAME=kxardas ./venv/bin/python today.py
```
