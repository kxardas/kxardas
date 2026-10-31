import os
import re

WORK = os.path.dirname(os.path.abspath(__file__))
PORTRAIT = os.path.join(WORK, "merlin.txt")

# ---- 1. ASCII art block (left <text x="15">) ----
def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

with open(PORTRAIT, encoding="utf-8") as f:
    art_lines = [ln.rstrip("\n") for ln in f.readlines()]
# strip neofetch color codes like ${c1} ${c2} ...
art_lines = [re.sub(r"\$\{c\d+\}", "", ln).rstrip() for ln in art_lines]
# drop leading/trailing fully-empty lines
while art_lines and not art_lines[0].strip():
    art_lines.pop(0)
while art_lines and not art_lines[-1].strip():
    art_lines.pop()

n = len(art_lines)
w = max((len(ln) for ln in art_lines), default=1)

# Fit the art into the left column: ~360px wide, ~500px tall.
# Consolas advance width ~= 0.55 * font-size.
LEFT_W, LEFT_H = 360, 500
fs_by_w = int(LEFT_W / (0.58 * max(w, 1)))
fs_by_h = int(LEFT_H / max(n, 1)) - 1
ASCII_FS = max(6, min(16, fs_by_w, fs_by_h))
ASCII_LH = max(ASCII_FS + 2, min(20, LEFT_H // max(n, 1)))
start_y = ASCII_FS + 12

ascii_tspans = ["\n"]
y = start_y
for ln in art_lines:
    ascii_tspans.append(f'<tspan x="15" y="{y}">{esc(ln)}</tspan>\n')
    y += ASCII_LH
ascii_inner = "".join(ascii_tspans)
print(f"art: {n} lines x {w} cols -> font-size {ASCII_FS}px, line-height {ASCII_LH}px")

# ---- 2. Right info panel (<text x="390">) ----
DASH = "-—————————————————————————————————————————-—-"  # ~45 cells
TOTAL = 59  # target visible chars per line (panel fits within 985px width)

def row(y, label_parts, value, value_class="value", dots_min=2):
    """label_parts: list of label words joined by '.'; produces key spans.
    Dots are sized so the whole line ends near a fixed right column."""
    vis_label = ".".join(label_parts)
    # fixed overhead: ". "(2) + ":"(1) + space-before-dots(1) + space-after-dots(1)
    dots = TOTAL - 5 - len(vis_label) - len(value)
    if dots < dots_min:
        dots = dots_min
    key_markup = ".".join(f'<tspan class="key">{esc(p)}</tspan>' for p in label_parts)
    return (f'<tspan x="390" y="{y}" class="cc">. </tspan>{key_markup}'
            f':<tspan class="cc"> {"."*dots} </tspan>'
            f'<tspan class="{value_class}">{esc(value)}</tspan>\n')

def section(y, title):
    return f'<tspan x="390" y="{y}">- {esc(title)}</tspan> {DASH}\n'

rows = ["\n"]
# header
rows.append(f'<tspan x="390" y="30">kxardas@github</tspan> {DASH}\n')
rows.append(row(50,  ["OS"], "macOS, Linux"))
# Uptime uses id age_data / age_data_dots (filled by today.py)
rows.append('<tspan x="390" y="70" class="cc">. </tspan><tspan class="key">Uptime</tspan>:'
            '<tspan class="cc" id="age_data_dots"> .................... </tspan>'
            '<tspan class="value" id="age_data">XX years, XX months, XX days</tspan>\n')
rows.append(row(90,  ["Host"], "Appexoft"))
rows.append(row(110, ["Kernel"], "Full-Stack Developer"))
rows.append(row(130, ["IDE"], "VSCode"))
rows.append(row(170, ["Languages", "Programming"], "TypeScript, JavaScript, SQL"))
rows.append(row(190, ["Languages", "Frameworks"], "Node.js, React.js, Next.js"))
rows.append(row(210, ["Languages", "Real"], "Ukrainian, English"))
rows.append(row(250, ["Stack", "Backend"], "NestJS, Prisma, NextAuth"))
rows.append(row(270, ["Stack", "Database"], "PostgreSQL, Supabase"))
rows.append(row(290, ["Stack", "Styling"], "Tailwind CSS"))
rows.append(section(330, "Contact"))
rows.append(row(350, ["Email"], "pavlogallimurka@gmail.com"))
rows.append(row(370, ["GitHub"], "kxardas"))
rows.append(row(390, ["Location"], "Lviv, Ukraine"))
rows.append(row(410, ["LinkedIn"], "pavlo-halimurka"))
rows.append(section(450, "GitHub Stats"))
# stats rows with ids (today.py fills these)
rows.append('<tspan x="390" y="470" class="cc">. </tspan><tspan class="key">Repos</tspan>:'
            '<tspan class="cc" id="repo_data_dots"> .... </tspan><tspan class="value" id="repo_data">0</tspan>'
            ' {<tspan class="key">Contributed</tspan>: <tspan class="value" id="contrib_data">0</tspan>}'
            ' | <tspan class="key">Stars</tspan>:<tspan class="cc" id="star_data_dots"> ........... </tspan>'
            '<tspan class="value" id="star_data">0</tspan>\n')
rows.append('<tspan x="390" y="490" class="cc">. </tspan><tspan class="key">Commits</tspan>:'
            '<tspan class="cc" id="commit_data_dots"> ................. </tspan>'
            '<tspan class="value" id="commit_data">0</tspan>'
            ' | <tspan class="key">Followers</tspan>:<tspan class="cc" id="follower_data_dots"> ....... </tspan>'
            '<tspan class="value" id="follower_data">0</tspan>\n')
rows.append('<tspan x="390" y="510" class="cc">. </tspan><tspan class="key">Lines of Code on GitHub</tspan>:'
            '<tspan class="cc" id="loc_data_dots">. </tspan><tspan class="value" id="loc_data">0</tspan>'
            ' ( <tspan class="addColor" id="loc_add">0</tspan><tspan class="addColor">++</tspan>,'
            ' <tspan id="loc_del_dots"> </tspan><tspan class="delColor" id="loc_del">0</tspan>'
            '<tspan class="delColor">--</tspan> )\n')
right_inner = "".join(rows)

# ---- 3. Splice into both SVG files ----
for fname in ("dark_mode.svg", "light_mode.svg"):
    path = f"{WORK}/{fname}"
    with open(path, encoding="utf-8") as f:
        svg = f.read()
    # replace ascii block: rebuild open tag with new font-size, keep the file's fill
    def ascii_repl(m):
        open_tag = m.group(1)
        fill_m = re.search(r'fill="[^"]*"', open_tag)
        fill = fill_m.group(0) if fill_m else 'fill="#c9d1d9"'
        new_open = f'<text x="15" y="{start_y}" {fill} class="ascii" font-size="{ASCII_FS}px">'
        return new_open + ascii_inner + m.group(3)
    svg = re.sub(r'(<text x="15"[^>]*>)(.*?)(</text>)', ascii_repl, svg, count=1, flags=re.S)
    # replace right block inner, keeping lines that today.py fills (id="...")
    # so a rebuild doesn't reset Uptime/stats to placeholders
    def right_repl(m):
        live = {}
        for ln in m.group(2).splitlines(keepends=True):
            y_m = re.match(r'<tspan x="390" y="(\d+)"', ln)
            if y_m and 'id="' in ln:
                live[y_m.group(1)] = ln
        out = []
        for ln in right_inner.splitlines(keepends=True):
            y_m = re.match(r'<tspan x="390" y="(\d+)"', ln)
            out.append(live.get(y_m.group(1), ln) if y_m and 'id="' in ln else ln)
        return m.group(1) + "".join(out) + m.group(3)
    svg = re.sub(r'(<text x="390"[^>]*>)(.*?)(</text>)', right_repl, svg, count=1, flags=re.S)
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)
    print("updated", fname)
