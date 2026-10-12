"""Generates the original pixel-art icon set used by index.html.
Run: python3 tools/make_icons.py  -> writes tools/icons.js (PIX32 / PIX16 / GLYPHS)"""
import math, json

N = 32
class Canvas:
    def __init__(s, n=32):
        s.n = n; s.p = [['.'] * n for _ in range(n)]
    def set(s, x, y, c):
        if 0 <= x < s.n and 0 <= y < s.n: s.p[y][x] = c
    def get(s, x, y): return s.p[y][x] if 0 <= x < s.n and 0 <= y < s.n else '.'
    def rect(s, x, y, w, h, c):
        for j in range(y, y + h):
            for i in range(x, x + w): s.set(i, j, c)
    def bevel(s, x, y, w, h, face='g', hi='W', lo='G'):
        s.rect(x, y, w, h, face)
        s.rect(x, y, w, 1, hi); s.rect(x, y, 1, h, hi)
        s.rect(x, y + h - 1, w, 1, lo); s.rect(x + w - 1, y, 1, h, lo)
    def sunk(s, x, y, w, h, face='W'):
        s.rect(x, y, w, h, face)
        s.rect(x, y, w, 1, 'G'); s.rect(x, y, 1, h, 'G')
        s.rect(x, y + h - 1, w, 1, 'W'); s.rect(x + w - 1, y, 1, h, 'W')
    def disc(s, cx, cy, r, c):
        for y in range(s.n):
            for x in range(s.n):
                if (x - cx) ** 2 + (y - cy) ** 2 <= r * r + r * 0.6: s.set(x, y, c)
    def line(s, x0, y0, x1, y1, c):
        n = max(abs(x1 - x0), abs(y1 - y0), 1)
        for i in range(n + 1):
            s.set(round(x0 + (x1 - x0) * i / n), round(y0 + (y1 - y0) * i / n), c)
    def outline(s):
        add = []
        for y in range(s.n):
            for x in range(s.n):
                if s.p[y][x] == '.' and any(s.get(x + dx, y + dy) not in ('.',) for dx, dy in ((1,0),(-1,0),(0,1),(0,-1))):
                    add.append((x, y))
        for x, y in add: s.p[y][x] = 'K'
    def text(s, x, y, word, c, font):
        for ch in word:
            g = font[ch]
            for j, row in enumerate(g):
                for i, v in enumerate(row):
                    if v == 'X': s.set(x + i, y + j, c)
            x += len(g[0]) + 1
    def rows(s): return [''.join(r) for r in s.p]

FONT = {
 'P': ['XXX','X.X','XXX','X..','X..'], 'D': ['XX.','X.X','X.X','X.X','XX.'], 'F': ['XXX','X..','XX.','X..','X..'],
 'C': ['XXX','X..','X..','X..','XXX'], ':': ['.','X','.','X','.'], '\\': ['X..','X..','.X.','..X','..X'],
 '_': ['XXXX']}

icons = {}

def folder():
    c = Canvas()
    c.rect(3, 8, 25, 19, 'Y'); c.rect(3, 6, 11, 3, 'Y')
    c.rect(3, 6, 11, 1, 'W'); c.rect(3, 8, 25, 1, 'W'); c.rect(3, 6, 1, 21, 'W')
    c.rect(3, 12, 25, 1, 'W')
    c.rect(27, 8, 1, 19, 'y'); c.rect(3, 26, 25, 1, 'y'); c.rect(13, 6, 1, 2, 'y')
    for x in range(5, 27, 2): c.set(x, 14, 'y') if False else None
    c.outline(); return c
icons['folder'] = folder()

def computer():
    c = Canvas()
    c.bevel(4, 3, 24, 18); c.sunk(7, 6, 18, 12, 't')
    for i in range(4): c.set(9 + i, 8 + i, 'C') if False else None
    c.line(9, 12, 12, 9, 'C'); c.line(9, 14, 14, 9, 'C')
    c.set(22, 19, 'L'); c.set(23, 19, 'L')
    c.bevel(12, 21, 8, 2); c.bevel(8, 23, 16, 4)
    c.rect(10, 25, 12, 1, 'G')
    c.outline(); return c
icons['computer'] = computer()

def bin_():
    c = Canvas()
    for y in range(12, 28):
        inset = (y - 12) // 5
        c.rect(8 + inset, y, 16 - 2 * inset, 1, 'g')
    for y in range(12, 28):
        inset = (y - 12) // 5
        c.set(8 + inset, y, 'W'); c.set(23 - inset, y, 'G'); c.set(22 - inset, y, 'G')
    for x in (12, 16, 20):
        c.rect(x, 14, 1, 11, 'G'); c.rect(x + 1, 14, 1, 11, 'W')
    c.bevel(5, 8, 22, 4, 'l', 'W', 'G')
    c.bevel(12, 5, 8, 3, 'g')
    c.outline(); return c
icons['bin'] = bin_()

def page(c, fold=True):
    c.rect(7, 3, 18, 26, 'W')
    c.rect(24, 3, 1, 26, 'G'); c.rect(7, 28, 18, 1, 'G')
    if fold:
        for y in range(3, 10):
            for x in range(18, 25):
                if (x - 18) >= (y - 3): c.set(x, y, '.')
                else: c.set(x, y, 'g')
        for i in range(7): c.set(18 + i, 3 + i, 'K') if False else None
        c.line(18, 3, 18, 9, 'G'); c.line(18, 9, 24, 9, 'G')
def textdoc():
    c = Canvas(); page(c)
    for i, y in enumerate((12, 15, 18, 21, 24)):
        c.rect(10, y, 12 if i < 4 else 7, 1, 'b')
    c.outline(); return c
icons['text'] = textdoc()

def pdf():
    c = Canvas(); page(c)
    for y in (7, 10, 13): c.rect(10, y, 11 if y < 13 else 6, 1, 'G')
    c.rect(7, 16, 18, 9, 'R'); c.rect(7, 16, 18, 1, 'r'); c.rect(7, 24, 18, 1, 'r')
    c.text(9, 18, 'PDF', 'W', FONT)
    c.outline(); return c
icons['pdf'] = pdf()

def app():
    c = Canvas()
    c.bevel(3, 5, 26, 22); c.rect(5, 7, 22, 4, 'b'); c.rect(23, 8, 3, 2, 'g')
    c.sunk(5, 12, 22, 13, 'W')
    c.line(9, 15, 12, 18, 'b'); c.line(12, 18, 9, 21, 'b'); c.rect(14, 21, 6, 1, 'b')
    c.rect(17, 15, 6, 1, 'G')
    c.outline(); return c
icons['app'] = app()

def dos():
    c = Canvas()
    c.rect(3, 5, 26, 22, 'K'); c.rect(3, 5, 26, 1, 'G'); c.rect(3, 5, 1, 22, 'G')
    c.rect(4, 6, 24, 3, 'g')
    c.text(6, 13, 'C:\\', 'g', FONT); c.rect(17, 18, 4, 1, 'g'); c.rect(17, 17, 4, 1, 'g')
    c.rect(28, 5, 1, 22, 'G') if False else None
    c.outline(); return c
icons['dos'] = dos()

def mine():
    c = Canvas()
    c.disc(16, 16, 8, 'K')
    for a in range(0, 360, 45):
        dx, dy = round(math.cos(math.radians(a)) * 12), round(math.sin(math.radians(a)) * 12)
        c.line(16, 16, 16 + dx, 16 + dy, 'K'); c.line(17, 16, 17 + dx, 16 + dy, 'K') if a in (0, 180) else None
        c.line(16, 17, 16 + dx, 17 + dy, 'K') if a in (90, 270) else None
    c.rect(12, 12, 3, 3, 'W')
    return c
icons['mine'] = mine()

def globe():
    c = Canvas()
    c.disc(16, 16, 12, 'B')
    land = [(10,8,6,2),(9,10,8,3),(11,13,4,2),(8,16,4,3),(10,19,5,4),(12,23,3,2),(19,9,5,3),(21,12,6,4),(19,16,4,3),(22,20,3,3)]
    for x, y, w, h in land:
        for j in range(h):
            for i in range(w):
                if (x + i - 16) ** 2 + (y + j - 16) ** 2 < 11 ** 2: c.set(x + i, y + j, 'e')
    for x, y, w, h in [(10,9,2,1),(21,13,2,1),(19,10,2,1)]:
        c.rect(x, y, w, h, 'L')
    for i in range(5): c.set(8 + i, 9 - i // 2 - 1, 'C') if False else None
    c.line(8, 12, 11, 7, 'C'); c.line(9, 12, 12, 8, 'C') if False else None
    for y in range(22, 28):
        for x in range(N):
            if c.get(x, y) == 'B' and (x - 16) ** 2 + (y - 16) ** 2 > 8 ** 2 and x > 14: c.set(x, y, 'b')
    c.outline(); return c
icons['globe'] = globe()

def floppy():
    c = Canvas()
    c.rect(4, 4, 24, 24, 'G')
    c.set(27, 4, '.'); c.set(26, 4, '.'); c.set(27, 5, '.')
    c.rect(10, 4, 13, 9, 'l'); c.rect(11, 4, 1, 9, 'W')
    c.rect(17, 6, 4, 5, 'G')
    c.rect(7, 16, 18, 12, 'W'); c.rect(7, 16, 18, 1, 'g')
    for y in (19, 22, 25): c.rect(9, y, 14, 1, 'b' if y == 19 else 'G')
    c.outline(); return c
icons['floppy'] = floppy()

def cd():
    c = Canvas()
    c.disc(16, 16, 12, 'l'); c.disc(16, 16, 9, 'g'); c.disc(16, 16, 6, 'l')
    c.disc(16, 16, 3, '.')
    for i, col in enumerate(('M', 'C', 'Y')): c.set(8 + i, 9 - i, col); c.set(9 + i, 9 - i, col)
    c.rect(6, 13, 3, 1, 'W'); c.rect(7, 12, 1, 2, 'W')
    c.outline(); return c
icons['cd'] = cd()

def drive():
    c = Canvas()
    c.bevel(3, 11, 26, 13)
    c.rect(6, 16, 14, 2, 'K'); c.rect(6, 18, 14, 1, 'W')
    c.rect(23, 16, 3, 2, 'L'); c.rect(23, 18, 3, 1, 'e')
    c.rect(5, 24, 3, 2, 'G'); c.rect(24, 24, 3, 2, 'G')
    c.outline(); return c
icons['drive'] = drive()

def warn():
    c = Canvas()
    for y in range(4, 28):
        half = int((y - 3) * 0.53)
        c.rect(16 - half, y, 2 * half + 1, 1, 'Y')
    c.rect(2, 27, 29, 1, 'Y')
    c.rect(15, 12, 3, 9, 'K'); c.rect(15, 23, 3, 3, 'K')
    c.outline(); return c
icons['warn'] = warn()

def info():
    c = Canvas()
    c.disc(16, 16, 13, 'W'); c.disc(16, 16, 11, 'B')
    c.rect(14, 8, 4, 4, 'W'); c.rect(14, 14, 4, 10, 'W'); c.rect(12, 14, 2, 2, 'W'); c.rect(12, 23, 8, 2, 'W')
    c.outline(); return c
icons['info'] = info()

def error():
    c = Canvas()
    c.disc(16, 16, 13, 'W'); c.disc(16, 16, 11, 'R')
    for d in range(-1, 2):
        c.line(10 + d, 10, 22 + d, 22, 'W'); c.line(22 + d, 10, 10 + d, 22, 'W')
    c.outline(); return c
icons['error'] = error()

def bulb():
    c = Canvas()
    c.disc(16, 12, 9, 'Y')
    for y in range(18, 22):
        c.rect(16 - (9 - (y - 18) * 1), y, 2 * (9 - (y - 18)) + 1, 1, 'Y') if False else None
    c.rect(11, 18, 11, 3, 'Y')
    c.rect(10, 6, 3, 3, 'W'); c.rect(9, 8, 2, 3, 'W')
    c.rect(12, 21, 9, 2, 'g'); c.rect(12, 24, 9, 2, 'g'); c.rect(14, 27, 5, 2, 'G')
    c.rect(12, 21, 9, 1, 'W'); c.rect(12, 25, 9, 1, 'G')
    c.line(13, 13, 15, 16, 'y'); c.line(15, 16, 17, 13, 'y'); c.line(17, 13, 19, 16, 'y')
    c.outline(); return c
icons['bulb'] = bulb()

def logo():
    c = Canvas()
    def pane(x0, y0, col, shade):
        for x in range(10):
            off = int(round(math.sin((x0 + x) * 0.55) * 1.2))
            for y in range(9):
                c.set(x0 + x, y0 + y + off, col)
            c.set(x0 + x, y0 + 8 + off, shade)
    pane(5, 6, 'R', 'r'); pane(16, 6, 'L', 'e'); pane(5, 16, 'B', 'b'); pane(16, 16, 'Y', 'y')
    return c
icons['logo'] = logo()

def down16(rows):
    out = []
    for by in range(16):
        line = ''
        for bx in range(16):
            blk = [rows[by*2][bx*2], rows[by*2][bx*2+1], rows[by*2+1][bx*2], rows[by*2+1][bx*2+1]]
            solid = [b for b in blk if b != '.']
            if len(solid) < 2: line += '.'; continue
            ks = blk.count('K')
            non = [b for b in solid if b != 'K']
            if ks >= 2 or not non: line += 'K'
            else:
                pick = max(set(non), key=non.count)
                line += pick if ks < 2 else 'K'
        out.append(line)
    return out


S16 = {}
def f16():
    c = Canvas(16)
    c.rect(1, 5, 14, 9, 'Y'); c.rect(1, 3, 6, 3, 'Y')
    c.rect(1, 3, 6, 1, 'W'); c.rect(1, 5, 14, 1, 'W'); c.rect(1, 3, 1, 11, 'W')
    c.rect(14, 5, 1, 9, 'y'); c.rect(1, 13, 14, 1, 'y')
    c.outline(); return c
S16['folder'] = f16()
def c16():
    c = Canvas(16)
    c.bevel(2, 1, 12, 9); c.sunk(4, 3, 8, 5, 't'); c.set(5, 6, 'C'); c.set(6, 5, 'C')
    c.rect(6, 10, 4, 1, 'g'); c.bevel(4, 11, 8, 2); c.set(11, 9, 'L')
    c.outline(); return c
S16['computer'] = c16()
def b16():
    c = Canvas(16)
    for y in range(5, 14):
        ins = (y - 5) // 4
        c.rect(3 + ins, y, 10 - 2 * ins, 1, 'g'); c.set(3 + ins, y, 'W'); c.set(12 - ins, y, 'G')
    for x in (6, 9): c.rect(x, 6, 1, 6, 'G')
    c.bevel(2, 3, 12, 2, 'l', 'W', 'G'); c.rect(6, 1, 4, 2, 'g')
    c.outline(); return c
S16['bin'] = b16()
def page16(c):
    c.rect(3, 1, 10, 14, 'W'); c.rect(12, 1, 1, 14, 'G'); c.rect(3, 14, 10, 1, 'G')
    for y in range(1, 5):
        for x in range(9, 13):
            c.set(x, y, '.' if (x - 9) >= (y - 1) else 'g')
    c.line(9, 1, 9, 4, 'G'); c.line(9, 4, 12, 4, 'G')
def t16():
    c = Canvas(16); page16(c)
    for y, w in ((7, 6), (9, 6), (11, 6), (13, 4)): c.rect(5, y, w, 1, 'b')
    c.outline(); return c
S16['text'] = t16()
def p16():
    c = Canvas(16); page16(c)
    c.rect(5, 6, 5, 1, 'G'); c.rect(3, 8, 10, 5, 'R'); c.rect(3, 8, 10, 1, 'r')
    for x in (5, 8, 10): c.set(x, 10, 'W'); c.set(x, 11, 'W')
    c.outline(); return c
S16['pdf'] = p16()
def a16():
    c = Canvas(16)
    c.bevel(1, 2, 14, 12); c.rect(3, 4, 10, 2, 'b'); c.sunk(3, 7, 10, 6, 'W')
    c.set(5, 9, 'b'); c.set(6, 10, 'b'); c.set(5, 11, 'b'); c.rect(8, 11, 3, 1, 'b')
    c.outline(); return c
S16['app'] = a16()
def d16():
    c = Canvas(16)
    c.rect(1, 2, 14, 12, 'K'); c.rect(1, 2, 14, 1, 'G'); c.rect(1, 2, 1, 12, 'G'); c.rect(2, 3, 12, 2, 'g')
    c.set(3, 7, 'g'); c.set(4, 8, 'g'); c.set(3, 9, 'g'); c.rect(6, 10, 3, 1, 'g')
    return c
S16['dos'] = d16()
def m16():
    c = Canvas(16)
    c.disc(8, 8, 4, 'K')
    for dx, dy in ((7,0),(-7,0),(0,7),(0,-7),(5,5),(-5,5),(5,-5),(-5,-5)): c.line(8, 8, 8 + dx, 8 + dy, 'K')
    c.rect(6, 6, 2, 2, 'W')
    return c
S16['mine'] = m16()
def dr16():
    c = Canvas(16)
    c.bevel(1, 5, 14, 7); c.rect(3, 8, 7, 1, 'K'); c.rect(12, 8, 2, 1, 'L'); c.rect(2, 12, 2, 1, 'G'); c.rect(12, 12, 2, 1, 'G')
    c.outline(); return c
S16['drive'] = dr16()
def g16():
    c = Canvas(16)
    c.disc(8, 8, 6, 'B')
    for x, y, w, h in ((5,4,3,2),(4,6,3,2),(9,4,3,3),(8,9,3,2),(5,10,2,2)):
        for j in range(h):
            for i in range(w):
                if (x + i - 8) ** 2 + (y + j - 8) ** 2 < 5.3 ** 2: c.set(x + i, y + j, 'e')
    c.set(4, 5, 'C'); c.set(5, 4, 'C')
    c.outline(); return c
S16['globe'] = g16()
def l16():
    c = Canvas(16)
    def pane(x0, y0, col, sh):
        for x in range(6):
            off = int(round(math.sin((x0 + x) * 0.9) * 0.9))
            for y in range(5): c.set(x0 + x, y0 + y + off, col)
            c.set(x0 + x, y0 + 4 + off, sh)
    pane(2, 3, 'R', 'r'); pane(8, 3, 'L', 'e'); pane(2, 8, 'B', 'b'); pane(8, 8, 'Y', 'y')
    return c
S16['logo'] = l16()

# ---- per-app icons -------------------------------------------------------
def poly(c, pts, col):
    ys = [p[1] for p in pts]
    for y in range(min(ys), max(ys) + 1):
        xs = []
        for i in range(len(pts)):
            (x0, y0), (x1, y1) = pts[i], pts[(i + 1) % len(pts)]
            if y0 == y1: continue
            if min(y0, y1) <= y + 0.5 < max(y0, y1):
                xs.append(x0 + (y + 0.5 - y0) * (x1 - x0) / (y1 - y0))
        xs.sort()
        for i in range(0, len(xs) - 1, 2):
            for x in range(int(round(xs[i])), int(round(xs[i + 1]))): c.set(x, y, col)
def big(c, x, y, ch, col, k=2):
    g = FONT[ch]
    for j, row in enumerate(g):
        for i, v in enumerate(row):
            if v == 'X': c.rect(x + i * k, y + j * k, k, k, col)
FONT['R'] = ['XX.', 'X.X', 'XX.', 'X.X', 'X.X']
FONT['?'] = ['XX.', '..X', '.X.', '...', '.X.']

A32, A16 = {}, {}

def forg3d32():
    c = Canvas()
    poly(c, [(16,4),(27,10),(16,16),(5,10)], 'C')
    poly(c, [(5,10),(16,16),(16,28),(5,22)], 'B')
    poly(c, [(16,16),(27,10),(27,22),(16,28)], 'b')
    c.line(16,16,16,28,'K'); c.line(5,10,16,16,'K'); c.line(16,16,27,10,'K')
    c.rect(14, 9, 4, 6, 'W'); c.rect(15, 15, 2, 1, 'W')  # tiny mic body on top face
    c.outline(); return c
def forg3d16():
    c = Canvas(16)
    poly(c, [(8,2),(14,5),(8,8),(2,5)], 'C')
    poly(c, [(2,5),(8,8),(8,14),(2,11)], 'B')
    poly(c, [(8,8),(14,5),(14,11),(8,14)], 'b')
    c.outline(); return c
A32['forg3d'], A16['forg3d'] = forg3d32(), forg3d16()

def ghst32():
    c = Canvas()
    c.disc(14, 12, 8, 'W'); c.rect(6, 12, 17, 13, 'W')
    for x in range(6, 23):
        c.set(x, 25 + (1 if (x // 3) % 2 == 0 else 0), 'W'); c.set(x, 26 if (x // 3) % 2 == 0 else 25, 'W')
    c.rect(6, 12, 1, 14, 'g'); c.rect(22, 12, 1, 14, 'g')
    c.rect(10, 10, 2, 4, 'K'); c.rect(17, 10, 2, 4, 'K'); c.rect(13, 16, 3, 2, 'K')
    c.line(30, 3, 20, 20, 'b'); c.line(29, 3, 19, 20, 'b'); c.set(18, 21, 'K'); c.set(19, 21, 'K')
    c.outline(); return c
def ghst16():
    c = Canvas(16)
    c.disc(7, 6, 4, 'W'); c.rect(3, 6, 9, 7, 'W'); c.set(3,13,'.'); c.set(6,13,'.'); c.set(9,13,'.')
    c.rect(5, 5, 1, 2, 'K'); c.rect(9, 5, 1, 2, 'K'); c.rect(7, 8, 2, 1, 'K')
    c.line(15, 1, 10, 10, 'b')
    c.outline(); return c
A32['ghstwrtr'], A16['ghstwrtr'] = ghst32(), ghst16()

def motion32():
    c = Canvas()
    c.rect(3, 6, 26, 20, 'K'); c.rect(4, 7, 24, 18, 'b')
    for x in range(5, 27, 4): c.rect(x, 8, 2, 2, 'W'); c.rect(x, 22, 2, 2, 'W')
    c.rect(5, 11, 22, 10, 'M'); c.rect(5, 11, 22, 3, 'p')
    poly(c, [(13,13),(13,20),(20,16.5)], 'W')
    c.outline(); return c
def motion16():
    c = Canvas(16)
    c.rect(1, 3, 14, 10, 'b')
    for x in (2, 5, 8, 11): c.set(x, 4, 'W'); c.set(x, 11, 'W')
    c.rect(2, 5, 12, 5, 'M'); poly(c, [(6,6),(6,10),(10,8)], 'W')
    c.outline(); return c
A32['motiondeckstudio'], A16['motiondeckstudio'] = motion32(), motion16()

def backlog32():
    c = Canvas()
    c.rect(1, 1, 30, 30, '.') 
    c.disc(16, 8, 5, 'Y'); c.rect(11, 8, 11, 5, 'M')   # synthwave sun
    for y in (10, 12): c.rect(11, y, 11, 1, 'p')
    c.rect(3, 13, 26, 11, 'p'); c.rect(2, 15, 28, 8, 'p'); c.rect(4, 24, 6, 4, 'p'); c.rect(22, 24, 6, 4, 'p')
    c.rect(4, 14, 24, 1, 'M')
    c.rect(7, 17, 6, 2, 'W'); c.rect(9, 15, 2, 6, 'W')
    c.rect(20, 16, 2, 2, 'C'); c.rect(24, 18, 2, 2, 'Y'); c.rect(22, 20, 2, 2, 'L'); c.rect(18, 19, 2, 2, 'R')
    c.outline(); return c
def backlog16():
    c = Canvas(16)
    c.disc(8, 4, 3, 'Y')
    c.rect(1, 6, 14, 6, 'p'); c.rect(2, 12, 3, 2, 'p'); c.rect(11, 12, 3, 2, 'p'); c.rect(2, 6, 12, 1, 'M')
    c.rect(3, 8, 4, 1, 'W'); c.rect(4, 7, 1, 3, 'W'); c.set(10, 8, 'C'); c.set(12, 9, 'Y')
    c.outline(); return c
A32['neverendingbacklog'], A16['neverendingbacklog'] = backlog32(), backlog16()

def stud32():
    c = Canvas()
    for x in (6, 13, 20):
        c.rect(x, 8, 6, 4, 'R'); c.rect(x, 8, 6, 1, 'W'); c.rect(x + 5, 9, 1, 3, 'r')
    c.rect(3, 12, 26, 14, 'R'); c.rect(3, 12, 26, 1, 'W'); c.rect(3, 12, 1, 14, 'W')
    c.rect(28, 12, 1, 14, 'r'); c.rect(3, 25, 26, 1, 'r'); c.rect(4, 24, 24, 1, 'r')
    c.outline(); return c
def stud16():
    c = Canvas(16)
    for x in (3, 7, 11): c.rect(x, 3, 3, 2, 'R'); c.rect(x, 3, 3, 1, 'W')
    c.rect(1, 5, 14, 8, 'R'); c.rect(1, 5, 14, 1, 'W'); c.rect(14, 5, 1, 8, 'r'); c.rect(1, 12, 14, 1, 'r')
    c.outline(); return c
A32['studworkz'], A16['studworkz'] = stud32(), stud16()

def nerd32():
    c = Canvas()
    c.rect(4, 8, 24, 20, 'p'); c.rect(4, 8, 24, 1, 'M'); c.rect(4, 8, 1, 20, 'M'); c.rect(27, 8, 1, 20, 'b'); c.rect(4, 27, 24, 1, 'b')
    c.rect(7, 11, 18, 3, 'Y')
    c.bevel(9, 15, 12, 12, 'W', 'W', 'G')
    for x, y in ((11,17),(17,17),(14,20),(11,23),(17,23)): c.rect(x, y, 2, 2, 'K')
    c.rect(22, 16, 4, 4, 'C'); c.rect(22, 16, 4, 1, 'W')
    c.outline(); return c
def nerd16():
    c = Canvas(16)
    c.rect(1, 3, 14, 11, 'p'); c.rect(1, 3, 14, 1, 'M'); c.rect(2, 5, 12, 2, 'Y')
    c.bevel(4, 7, 7, 7, 'W', 'W', 'G'); c.set(5, 8, 'K'); c.set(9, 8, 'K'); c.set(7, 10, 'K'); c.set(5, 12, 'K'); c.set(9, 12, 'K')
    c.outline(); return c
A32['nerdroom'], A16['nerdroom'] = nerd32(), nerd16()

def nmotg32():
    c = Canvas()
    c.rect(6, 3, 21, 26, 'b'); c.rect(6, 3, 21, 1, 'B'); c.rect(6, 3, 1, 26, 'B'); c.rect(26, 3, 1, 26, 'K')
    c.rect(9, 6, 16, 20, 'W')
    for y in (8, 12, 16): c.rect(11, y, 4, 1, 'G'); c.rect(16, y, 7, 1, 'G')
    for y in (4, 9, 14, 19, 24): c.rect(3, y, 5, 2, 'g'); c.rect(3, y, 5, 1, 'W')
    big(c, 13, 17, '?', 'R', 2)
    c.outline(); return c
def nmotg16():
    c = Canvas(16)
    c.rect(3, 1, 11, 14, 'b'); c.rect(5, 3, 8, 10, 'W')
    for y in (2, 6, 10): c.rect(1, y, 3, 1, 'G')
    c.rect(7, 5, 3, 1, 'R'); c.set(9, 6, 'R'); c.set(8, 7, 'R'); c.set(8, 9, 'R')
    c.outline(); return c
A32['nmotg'], A16['nmotg'] = nmotg32(), nmotg16()

def pass32():
    c = Canvas()
    c.rect(5, 4, 22, 24, 'Y'); c.rect(5, 4, 22, 1, 'W'); c.rect(5, 4, 1, 24, 'W'); c.rect(26, 4, 1, 24, 'y'); c.rect(5, 27, 22, 1, 'y')
    poly(c, [(21,28),(27,22),(27,28)], 'g')
    c.rect(9, 9, 14, 2, 'R'); c.rect(9, 14, 10, 2, 'B'); c.rect(9, 19, 12, 2, 'e'); c.rect(9, 23, 6, 2, 'M')
    c.outline(); return c
def pass16():
    c = Canvas(16)
    c.rect(2, 1, 12, 13, 'Y'); c.rect(2, 1, 12, 1, 'W'); c.rect(13, 1, 1, 13, 'y'); c.rect(2, 13, 12, 1, 'y')
    c.rect(4, 4, 8, 1, 'R'); c.rect(4, 7, 6, 1, 'B'); c.rect(4, 10, 7, 1, 'e')
    c.outline(); return c
A32['passinote'], A16['passinote'] = pass32(), pass16()

def fate32():
    c = Canvas()
    for y, (x0, x1) in enumerate([(15,17),(14,18),(13,19),(12,20),(11,21),(10,22),(9,23),(9,23),(8,24),(8,24),(8,24),(9,23),(10,22),(11,21)]):
        c.rect(x0, 5 + y, x1 - x0, 1, 'R')
    for y, (x0, x1) in enumerate([(15,17),(14,18),(13,19),(12,20),(12,20),(11,21),(11,21),(12,20)]):
        c.rect(x0, 11 + y, x1 - x0, 1, 'Y')
    c.rect(14, 15, 4, 3, 'W')
    c.rect(15, 1, 2, 14, 'g'); c.rect(15, 1, 1, 14, 'W'); c.rect(12, 14, 8, 2, 'G') ; c.rect(15, 16, 2, 8, 'y')
    c.rect(4, 22, 24, 4, 'y'); c.rect(4, 22, 24, 1, 'Y'); c.rect(6, 26, 20, 3, 'r')
    c.outline(); return c
def fate16():
    c = Canvas(16)
    for y, (x0, x1) in enumerate([(7,9),(6,10),(5,11),(4,12),(4,12),(5,11),(6,10)]): c.rect(x0, 3 + y, x1 - x0, 1, 'R')
    for y, (x0, x1) in enumerate([(7,9),(6,10),(6,10)]): c.rect(x0, 6 + y, x1 - x0, 1, 'Y')
    c.rect(7, 0, 2, 8, 'g'); c.rect(5, 7, 6, 1, 'G')
    c.rect(2, 11, 12, 2, 'y'); c.rect(3, 13, 10, 2, 'r')
    c.outline(); return c
A32['fatemold'], A16['fatemold'] = fate32(), fate16()

def speed32():
    c = Canvas()
    c.bevel(2, 6, 28, 20); c.sunk(4, 8, 24, 16, 'W')
    c.rect(15, 8, 2, 3, 'R'); c.rect(15, 21, 2, 3, 'R')
    big(c, 14, 11, 'R', 'R', 2) if False else None
    c.rect(13, 12, 2, 8, 'K'); c.rect(15, 12, 3, 2, 'K'); c.rect(17, 14, 2, 2, 'K'); c.rect(15, 16, 3, 2, 'K'); c.rect(17, 18, 2, 2, 'K')
    c.rect(14, 12, 2, 8, 'R') if False else None
    for y in (13, 16, 19): c.rect(5, y, 5 - (y % 3), 1, 'G')
    c.rect(22, 15, 5, 1, 'G'); c.rect(22, 18, 4, 1, 'G')
    c.outline(); return c
def speed16():
    c = Canvas(16)
    c.bevel(1, 3, 14, 10); c.sunk(2, 4, 12, 8, 'W')
    c.rect(7, 4, 1, 2, 'R'); c.rect(7, 10, 1, 2, 'R'); c.rect(6, 6, 3, 4, 'K'); c.rect(7, 7, 1, 2, 'W')
    c.rect(3, 7, 2, 1, 'G'); c.rect(11, 8, 2, 1, 'G')
    c.outline(); return c
A32['speedr'], A16['speedr'] = speed32(), speed16()

def line32():
    c = Canvas()
    c.sunk(3, 3, 26, 26, 'W')
    pts = [(7,22),(8,12),(13,8),(19,9),(22,14),(18,18),(12,16),(11,23),(17,25),(24,22)]
    for a, b in zip(pts, pts[1:]): c.line(a[0], a[1], b[0], b[1], 'K')
    c.line(24, 22, 25, 8, 'K')
    c.rect(24, 6, 4, 2, 'R')
    c.outline(); return c
def line16():
    c = Canvas(16)
    c.sunk(1, 1, 14, 14, 'W')
    pts = [(3,11),(4,5),(8,3),(11,6),(8,9),(6,8),(6,12),(12,12)]
    for a, b in zip(pts, pts[1:]): c.line(a[0], a[1], b[0], b[1], 'K')
    c.outline(); return c
A32['onlyline'], A16['onlyline'] = line32(), line16()

def aian32():
    c = Canvas()
    nodes = [(6,7),(26,7),(5,25),(27,25)]
    for n in nodes: c.line(n[0], n[1], 16, 16, 'G'); c.line(n[0]+1, n[1], 17, 16, 'G')
    for x, y in nodes: c.disc(x, y, 3, 'B'); c.set(x - 1, y - 1, 'C')
    c.disc(16, 15, 6, 'Y'); c.rect(14, 21, 5, 3, 'G'); c.rect(14, 21, 5, 1, 'g')
    c.rect(12, 12, 2, 2, 'W'); c.rect(13, 10, 3, 1, 'W')
    c.outline(); return c
def aian16():
    c = Canvas(16)
    nodes = [(3,3),(13,3),(3,13),(13,13)]
    for n in nodes: c.line(n[0], n[1], 8, 8, 'G')
    for x, y in nodes: c.disc(x, y, 1, 'B')
    c.disc(8, 7, 3, 'Y'); c.rect(7, 10, 3, 1, 'G')
    c.outline(); return c
A32['aiadoptionnetwork'], A16['aiadoptionnetwork'] = aian32(), aian16()
for k in A32: icons['app_' + k] = A32[k]; S16['app_' + k] = A16[k]

def doom32():
    c = Canvas()
    c.rect(1, 1, 30, 30, 'K'); c.rect(1, 1, 30, 1, 'r'); c.rect(1, 1, 1, 30, 'r'); c.rect(30, 1, 1, 30, 'R'); c.rect(1, 30, 30, 1, 'R')
    poly(c, [(6,12),(4,3),(11,8)], 'R'); poly(c, [(26,12),(28,3),(21,8)], 'R')
    c.disc(16, 14, 8, 'W'); c.rect(11, 19, 10, 8, 'W'); c.rect(11, 19, 1, 8, 'g'); c.rect(20, 19, 1, 8, 'g')
    c.rect(10, 12, 4, 5, 'K'); c.rect(18, 12, 4, 5, 'K'); c.rect(11, 14, 2, 2, 'R'); c.rect(19, 14, 2, 2, 'R')
    c.rect(15, 18, 2, 2, 'K')
    for x in (12, 14, 17, 19): c.rect(x, 23, 1, 4, 'K')
    c.rect(12, 23, 8, 1, 'K')
    return c
def doom16():
    c = Canvas(16)
    c.rect(0, 0, 16, 16, 'K'); c.rect(0, 0, 16, 1, 'r'); c.rect(0, 0, 1, 16, 'r'); c.rect(15, 0, 1, 16, 'R'); c.rect(0, 15, 16, 1, 'R')
    c.set(3, 2, 'R'); c.set(2, 1, 'R'); c.set(12, 2, 'R'); c.set(13, 1, 'R')
    c.disc(8, 7, 4, 'W'); c.rect(5, 10, 6, 3, 'W')
    c.rect(5, 6, 2, 2, 'K'); c.rect(9, 6, 2, 2, 'K'); c.set(6, 7, 'R'); c.set(9, 7, 'R'); c.set(7, 9, 'K'); c.set(8, 9, 'K')
    for x in (6, 8, 10): c.set(x, 11, 'K')
    return c
icons['doom'] = doom32(); S16['doom'] = doom16()

def disky(blink=False, wave=False):
    c = Canvas()
    # disk body
    c.rect(5, 4, 22, 24, 'b'); c.rect(5, 4, 22, 1, 'B'); c.rect(5, 4, 1, 24, 'B'); c.rect(26, 4, 1, 24, 'K'); c.rect(5, 27, 22, 1, 'K')
    c.set(5, 4, '.'); c.set(26, 4, '.')
    poly(c, [(22,4),(27,4),(27,9)], '.')
    # metal shutter
    c.rect(10, 4, 12, 8, 'g'); c.rect(10, 4, 12, 1, 'W'); c.rect(10, 4, 1, 8, 'W'); c.rect(21, 4, 1, 8, 'G'); c.rect(10, 11, 12, 1, 'G')
    c.rect(18, 6, 3, 4, 'K')
    # label with face
    c.rect(8, 15, 16, 12, 'W'); c.rect(8, 15, 16, 1, 'l')
    if blink:
        c.rect(11, 19, 3, 1, 'K'); c.rect(18, 19, 3, 1, 'K')
    else:
        c.rect(11, 17, 3, 4, 'K'); c.rect(18, 17, 3, 4, 'K'); c.set(11, 17, 'W'); c.set(18, 17, 'W')
    c.rect(11, 15, 4, 1, 'G'); c.rect(18, 15, 4, 1, 'G')  # eyebrows
    c.rect(12, 23, 8, 1, 'R'); c.set(11, 22, 'R'); c.set(20, 22, 'R'); c.rect(13, 24, 6, 1, 'r')
    # little arms and feet
    c.rect(2, 19, 3, 2, 'K'); c.rect(27, 17 if wave else 19, 3, 2, 'K')
    if wave: c.rect(29, 14, 2, 3, 'K')
    c.rect(9, 28, 4, 2, 'K'); c.rect(19, 28, 4, 2, 'K')
    c.outline(); return c
icons['disky'] = disky(); icons['disky_blink'] = disky(blink=True); icons['disky_wave'] = disky(wave=True)
def disky16():
    c = Canvas(16)
    c.rect(2, 1, 12, 13, 'b'); c.rect(2, 1, 12, 1, 'B'); c.rect(2, 1, 1, 13, 'B'); c.rect(13, 1, 1, 13, 'K'); c.rect(2, 13, 12, 1, 'K')
    c.rect(5, 1, 6, 4, 'g'); c.rect(5, 1, 6, 1, 'W'); c.rect(9, 2, 1, 2, 'K')
    c.rect(4, 7, 8, 6, 'W'); c.rect(5, 8, 1, 2, 'K'); c.rect(9, 8, 1, 2, 'K'); c.rect(6, 11, 4, 1, 'R'); c.set(5, 10, 'R'); c.set(10, 10, 'R')
    c.outline(); return c
S16['disky'] = disky16()

pix32 = {k: v.rows() for k, v in icons.items()}
pix16 = {k: v.rows() for k, v in S16.items()}

def glyph(rows): return rows
glyphs = {
 'min': ['.........','.........','.........','.........','.........','.........','.KKKKKK..','.KKKKKK..'][:8],
 'max': ['KKKKKKKKK','KKKKKKKKK','K.......K','K.......K','K.......K','K.......K','K.......K','KKKKKKKKK'],
 'restore': ['..KKKKKKK','..KKKKKKK','..K.....K','KKKKKKK.K','KKKKKKK.K','K.....K.K','K.....KKK','K.....K..','KKKKKKK..'],
 'close': ['KK....KK','.KK..KK.','..KKKK..','...KK...','..KKKK..','.KK..KK.','KK....KK'],
}
js = 'const PIX32 = ' + json.dumps(pix32, separators=(',', ':')) + ';\nconst PIX16 = ' + json.dumps(pix16, separators=(',', ':')) + ';\nconst GLYPHS = ' + json.dumps(glyphs, separators=(',', ':')) + ';\n'
open('/home/claude/zachofalltrade/tools/icons.js', 'w').write(js)

PAL = {'K':'#000000','W':'#ffffff','g':'#c0c0c0','G':'#808080','l':'#dfdfdf','R':'#ff0000','r':'#800000','Y':'#ffff00','y':'#808000','L':'#00ff00','e':'#008000','C':'#00ffff','t':'#008080','B':'#0000ff','b':'#000080','M':'#ff00ff','p':'#800080'}
def svg(rows, z):
    n = len(rows); parts = []
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch != '.': parts.append(f'<rect x="{x}" y="{y}" width="1" height="1" fill="{PAL[ch]}"/>')
    return f'<svg width="{n*z}" height="{n*z}" viewBox="0 0 {n} {n}" shape-rendering="crispEdges">' + ''.join(parts) + '</svg>'
html = '<body style="background:#008080;margin:10px;font:12px Arial;color:#fff"><div style="display:flex;flex-wrap:wrap;gap:14px">'
for k in pix32:
    html += f'<div style="text-align:center">{svg(pix32[k],5)}<br>{svg(pix16[k],5) if k in pix16 else ''}<br><span style="background:#c0c0c0;color:#000;padding:2px">{svg(pix32[k],1)}{svg(pix16[k],1) if k in pix16 else ''}</span><br>{k}</div>'
html += '</div></body>'
open('/tmp/claude-0/-home-claude-zachofalltrade/32b4901b-1ee5-50b4-b0bd-357c7d3a8bfa/scratchpad/preview.html', 'w').write(html)
print('icons:', len(pix32))
