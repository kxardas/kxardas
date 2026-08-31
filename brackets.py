COLS, ROWS = 44, 25
grid = [[" "] * COLS for _ in range(ROWS)]

def put(x, y, ch):
    if 0 <= y < ROWS and 0 <= x < COLS:
        grid[y][x] = ch

def diag(x0, y0, n, dx, ch, thick=2):
    """45-degree run of n steps starting at (x0,y0), moving dx in x and +1 in y."""
    for i in range(n + 1):
        for t in range(thick):
            put(x0 + dx * i + t, y0 + i, ch)

TOP = 3
MID = 12
N = 9  # 45-degree arms

# Left bracket  <
diag(13, TOP, N, -1, "/")          # upper arm  (down-left)
diag(4,  MID, N,  1, "\\")         # lower arm  (down-right)

# Right bracket  >
diag(29, TOP, N,  1, "\\")         # upper arm  (down-right)
diag(38, MID, N, -1, "/")          # lower arm  (down-left)

# Center slash  /   (steeper, spans full height)
for i in range(19):
    x = 26 - round(i * 10 / 18)
    for t in range(2):
        put(x + t, 3 + i, "/")

art = "\n".join("".join(r).rstrip() for r in grid)
print(art)
with open("/private/tmp/claude-501/-Users-kxardas-coding-github-readme/5bc6bcff-ad4b-4f22-a093-c17e8cd3031c/scratchpad/portrait.txt", "w") as f:
    f.write(art + "\n")
