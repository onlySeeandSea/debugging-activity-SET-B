# ==========================================================================
#  qrcode.py - OFFLINE QR CODE MODULE                    (DO NOT EDIT)
# ==========================================================================
#  This file is NOT part of the bugs. It is a small, offline copy of the
#  "qrcode" module we used in the qr-code lesson, written in plain Python,
#  so the activity works WITHOUT internet and WITHOUT "pip install".
#
#  Because this file is named qrcode.py, the line
#
#       import qrcode
#
#  inside SET-A, SET-B and SET-C loads THIS file (Python looks for modules
#  in the program's own folder first). This is a custom module, exactly
#  like the "you can also create your own modules" part of lesson 13.
#
#  It supports the same commands as the real module:
#       qrcode.make(data)
#       qrcode.QRCode(version, error_correction, box_size, border)
#       qr.add_data(...), qr.make(fit=True)
#       qr.make_image(fill_color=..., back_color=...)
#       img.save("name.png")
# ==========================================================================

import os
import struct
import zlib


class constants:
    ERROR_CORRECT_L = 1
    ERROR_CORRECT_M = 0
    ERROR_CORRECT_Q = 3
    ERROR_CORRECT_H = 2


# --------------------------------------------------------------------------
#  QR code tables (versions 1-40)
# --------------------------------------------------------------------------
_LEVEL_INDEX = {constants.ERROR_CORRECT_L: 0, constants.ERROR_CORRECT_M: 1,
                constants.ERROR_CORRECT_Q: 2, constants.ERROR_CORRECT_H: 3}
_FORMAT_BITS = {0: 1, 1: 0, 2: 3, 3: 2}   # level index -> format bits

_ECC_PER_BLOCK = (
    (-1, 7, 10, 15, 20, 26, 18, 20, 24, 30, 18, 20, 24, 26, 30, 22, 24, 28, 30, 28, 28, 28, 28, 30, 30, 26, 28, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30),
    (-1, 10, 16, 26, 18, 24, 16, 18, 22, 22, 26, 30, 22, 22, 24, 24, 28, 28, 26, 26, 26, 26, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28),
    (-1, 13, 22, 18, 26, 18, 24, 18, 22, 20, 24, 28, 26, 24, 20, 30, 24, 28, 28, 26, 30, 28, 30, 30, 30, 30, 28, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30),
    (-1, 17, 28, 22, 16, 22, 28, 26, 26, 24, 28, 24, 28, 22, 24, 24, 30, 28, 28, 26, 28, 30, 24, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30),
)
_NUM_BLOCKS = (
    (-1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 4, 4, 4, 4, 4, 6, 6, 6, 6, 7, 8, 8, 9, 9, 10, 12, 12, 12, 13, 14, 15, 16, 17, 18, 19, 19, 20, 21, 22, 24, 25),
    (-1, 1, 1, 1, 2, 2, 4, 4, 4, 5, 5, 5, 8, 9, 9, 10, 10, 11, 13, 14, 16, 17, 17, 18, 20, 21, 23, 25, 26, 28, 29, 31, 33, 35, 37, 38, 40, 43, 45, 47, 49),
    (-1, 1, 1, 2, 2, 4, 4, 6, 6, 8, 8, 8, 10, 12, 16, 12, 17, 16, 18, 21, 20, 23, 23, 25, 27, 29, 34, 34, 35, 38, 40, 43, 45, 48, 51, 53, 56, 59, 62, 65, 68),
    (-1, 1, 1, 2, 4, 4, 4, 5, 6, 8, 8, 11, 11, 16, 16, 18, 16, 19, 21, 25, 25, 25, 34, 30, 32, 35, 37, 40, 42, 45, 48, 51, 54, 57, 60, 63, 66, 70, 74, 77, 81),
)


def _raw_modules(ver):
    result = (16 * ver + 128) * ver + 64
    if ver >= 2:
        num_align = ver // 7 + 2
        result -= (25 * num_align - 10) * num_align - 55
        if ver >= 7:
            result -= 36
    return result


def _data_codewords(ver, lvl):
    return (_raw_modules(ver) // 8
            - _ECC_PER_BLOCK[lvl][ver] * _NUM_BLOCKS[lvl][ver])


# --------------------------------------------------------------------------
#  Reed-Solomon error correction
# --------------------------------------------------------------------------
def _gf_mul(x, y):
    z = 0
    for i in range(7, -1, -1):
        z = (z << 1) ^ ((z >> 7) * 0x11D)
        z ^= ((y >> i) & 1) * x
    return z


def _rs_divisor(degree):
    result = [0] * (degree - 1) + [1]
    root = 1
    for _ in range(degree):
        for j in range(len(result)):
            result[j] = _gf_mul(result[j], root)
            if j + 1 < len(result):
                result[j] ^= result[j + 1]
        root = _gf_mul(root, 0x02)
    return result


def _rs_remainder(data, divisor):
    result = [0] * len(divisor)
    for b in data:
        factor = b ^ result.pop(0)
        result.append(0)
        for i, coef in enumerate(divisor):
            result[i] ^= _gf_mul(coef, factor)
    return result


# --------------------------------------------------------------------------
#  Building the symbol
# --------------------------------------------------------------------------
def _alignment_positions(ver):
    if ver == 1:
        return []
    num_align = ver // 7 + 2
    step = 26 if ver == 32 else (ver * 4 + num_align * 2 + 1) // (num_align * 2 - 2) * 2
    result = [6]
    pos = ver * 4 + 10
    for _ in range(num_align - 1):
        result.insert(1, pos)
        pos -= step
    return result


class _Symbol:
    def __init__(self, ver, lvl, codewords):
        self.ver = ver
        self.lvl = lvl
        self.size = ver * 4 + 17
        n = self.size
        self.modules = [[False] * n for _ in range(n)]
        self.is_function = [[False] * n for _ in range(n)]
        self._draw_function_patterns()
        self._draw_codewords(self._add_ecc(codewords))
        best, best_penalty = 0, None
        for mask in range(8):
            self._apply_mask(mask)
            self._draw_format(mask)
            penalty = self._penalty()
            if best_penalty is None or penalty < best_penalty:
                best, best_penalty = mask, penalty
            self._apply_mask(mask)
        self._apply_mask(best)
        self._draw_format(best)

    def _set(self, x, y, dark):
        self.modules[y][x] = dark
        self.is_function[y][x] = True

    def _draw_function_patterns(self):
        n = self.size
        for i in range(n):
            self._set(6, i, i % 2 == 0)
            self._set(i, 6, i % 2 == 0)
        for cx, cy in ((3, 3), (n - 4, 3), (3, n - 4)):
            for dy in range(-4, 5):
                for dx in range(-4, 5):
                    x, y = cx + dx, cy + dy
                    if 0 <= x < n and 0 <= y < n:
                        dist = max(abs(dx), abs(dy))
                        self._set(x, y, dist not in (2, 4))
        pos = _alignment_positions(self.ver)
        last = len(pos) - 1
        for i, ax in enumerate(pos):
            for j, ay in enumerate(pos):
                if (i == 0 and j == 0) or (i == 0 and j == last) or (i == last and j == 0):
                    continue
                for dy in range(-2, 3):
                    for dx in range(-2, 3):
                        self._set(ax + dx, ay + dy, max(abs(dx), abs(dy)) != 1)
        self._draw_format(0)
        self._draw_version()

    def _draw_format(self, mask):
        n = self.size
        data = _FORMAT_BITS[self.lvl] << 3 | mask
        rem = data
        for _ in range(10):
            rem = (rem << 1) ^ ((rem >> 9) * 0x537)
        bits = (data << 10 | rem) ^ 0x5412
        bit = lambda i: (bits >> i) & 1 != 0
        for i in range(0, 6):
            self._set(8, i, bit(i))
        self._set(8, 7, bit(6))
        self._set(8, 8, bit(7))
        self._set(7, 8, bit(8))
        for i in range(9, 15):
            self._set(14 - i, 8, bit(i))
        for i in range(0, 8):
            self._set(n - 1 - i, 8, bit(i))
        for i in range(8, 15):
            self._set(8, n - 15 + i, bit(i))
        self._set(8, n - 8, True)

    def _draw_version(self):
        if self.ver < 7:
            return
        rem = self.ver
        for _ in range(12):
            rem = (rem << 1) ^ ((rem >> 11) * 0x1F25)
        bits = self.ver << 12 | rem
        for i in range(18):
            dark = (bits >> i) & 1 != 0
            a, b = self.size - 11 + i % 3, i // 3
            self._set(a, b, dark)
            self._set(b, a, dark)

    def _add_ecc(self, data):
        ver, lvl = self.ver, self.lvl
        num_blocks = _NUM_BLOCKS[lvl][ver]
        ecc_len = _ECC_PER_BLOCK[lvl][ver]
        raw = _raw_modules(ver) // 8
        num_short = num_blocks - raw % num_blocks
        short_len = raw // num_blocks
        divisor = _rs_divisor(ecc_len)
        blocks, k = [], 0
        for i in range(num_blocks):
            length = short_len - ecc_len + (0 if i < num_short else 1)
            dat = data[k:k + length]
            k += length
            ecc = _rs_remainder(dat, divisor)
            if i < num_short:
                dat = dat + [0]
            blocks.append(dat + ecc)
        result = []
        for i in range(len(blocks[0])):
            for j, blk in enumerate(blocks):
                if i != short_len - ecc_len or j >= num_short:
                    result.append(blk[i])
        return result

    def _draw_codewords(self, data):
        n = self.size
        i = 0
        right = n - 1
        while right >= 1:
            if right == 6:
                right = 5
            for vert in range(n):
                for j in range(2):
                    x = right - j
                    upward = ((right + 1) & 2) == 0
                    y = n - 1 - vert if upward else vert
                    if not self.is_function[y][x] and i < len(data) * 8:
                        self.modules[y][x] = (data[i >> 3] >> (7 - (i & 7))) & 1 != 0
                        i += 1
            right -= 2

    def _apply_mask(self, mask):
        rules = (
            lambda x, y: (x + y) % 2 == 0,
            lambda x, y: y % 2 == 0,
            lambda x, y: x % 3 == 0,
            lambda x, y: (x + y) % 3 == 0,
            lambda x, y: (x // 3 + y // 2) % 2 == 0,
            lambda x, y: x * y % 2 + x * y % 3 == 0,
            lambda x, y: (x * y % 2 + x * y % 3) % 2 == 0,
            lambda x, y: ((x + y) % 2 + x * y % 3) % 2 == 0,
        )
        rule = rules[mask]
        for y in range(self.size):
            for x in range(self.size):
                if not self.is_function[y][x] and rule(x, y):
                    self.modules[y][x] = not self.modules[y][x]

    def _penalty(self):
        n, m = self.size, self.modules
        result = 0
        lines = [m[y] for y in range(n)] + [[m[y][x] for y in range(n)] for x in range(n)]
        for line in lines:
            run = 1
            for i in range(1, n + 1):
                if i < n and line[i] == line[i - 1]:
                    run += 1
                else:
                    if run >= 5:
                        result += run - 2
                    run = 1
            padded = [False] * 4 + line + [False] * 4
            for i in range(len(padded) - 10):
                seg = padded[i:i + 11]
                if seg == [True, False, True, True, True, False, True, False, False, False, False] or \
                   seg == [False, False, False, False, True, False, True, True, True, False, True]:
                    result += 40
        for y in range(n - 1):
            for x in range(n - 1):
                c = m[y][x]
                if c == m[y][x + 1] == m[y + 1][x] == m[y + 1][x + 1]:
                    result += 3
        dark = sum(row.count(True) for row in m)
        total = n * n
        k = (abs(dark * 20 - total * 10) + total - 1) // total - 1
        result += k * 10
        return result


# --------------------------------------------------------------------------
#  Image + PNG writer (no outside libraries)
# --------------------------------------------------------------------------
_COLORS = {
    "black": (0, 0, 0), "white": (255, 255, 255), "red": (255, 0, 0),
    "green": (0, 128, 0), "blue": (0, 0, 255), "yellow": (255, 255, 0),
    "gray": (128, 128, 128), "grey": (128, 128, 128), "navy": (0, 0, 128),
    "orange": (255, 165, 0), "purple": (128, 0, 128), "pink": (255, 192, 203),
}


def _color(value):
    if isinstance(value, tuple):
        return tuple(value[:3])
    if isinstance(value, str) and value.lower() in _COLORS:
        return _COLORS[value.lower()]
    raise ValueError("unknown color specifier: " + repr(value))


class QRImage:
    def __init__(self, modules, box_size, border, fill_color, back_color):
        self.modules = modules
        self.box_size = box_size
        self.border = border
        self.fill = _color(fill_color)
        self.back = _color(back_color)
        self.size = (len(modules) + 2 * border) * box_size

    def save(self, filename):
        extension = os.path.splitext(str(filename))[1]
        if extension.lower() != ".png":
            raise ValueError("unknown file extension: " + extension)
        count = len(self.modules)
        rows = []
        for py in range(self.size):
            my = py // self.box_size - self.border
            row = bytearray([0])
            for px in range(self.size):
                mx = px // self.box_size - self.border
                dark = 0 <= mx < count and 0 <= my < count and self.modules[my][mx]
                row.extend(self.fill if dark else self.back)
            rows.append(bytes(row))

        def chunk(tag, data):
            body = tag + data
            return struct.pack(">I", len(data)) + body + struct.pack(">I", zlib.crc32(body) & 0xFFFFFFFF)

        png = b"\x89PNG\r\n\x1a\n"
        png += chunk(b"IHDR", struct.pack(">IIBBBBB", self.size, self.size, 8, 2, 0, 0, 0))
        png += chunk(b"IDAT", zlib.compress(b"".join(rows), 9))
        png += chunk(b"IEND", b"")
        with open(filename, "wb") as file:
            file.write(png)


class QRCode:
    def __init__(self, version=None, error_correction=constants.ERROR_CORRECT_M,
                 box_size=10, border=4):
        self.version = version
        self.error_correction = error_correction
        self.box_size = int(box_size)
        self.border = int(border)
        self.data = b""
        self.modules = None

    def add_data(self, data):
        if isinstance(data, str):
            data = data.encode("utf-8")
        elif not isinstance(data, bytes):
            data = str(data).encode("utf-8")
        self.data += data
        self.modules = None

    def make(self, fit=True):
        lvl = _LEVEL_INDEX[self.error_correction]
        length = len(self.data)
        versions = range(1, 41) if (fit or self.version is None) else [self.version]
        chosen = None
        for ver in versions:
            count_bits = 8 if ver <= 9 else 16
            if 4 + count_bits + length * 8 <= _data_codewords(ver, lvl) * 8:
                chosen = ver
                break
        if chosen is None:
            raise ValueError("data is too long for a QR code")
        self.version = chosen
        capacity = _data_codewords(chosen, lvl) * 8
        bits = []

        def append(value, n):
            for i in range(n - 1, -1, -1):
                bits.append((value >> i) & 1)

        append(0b0100, 4)
        append(length, 8 if chosen <= 9 else 16)
        for b in self.data:
            append(b, 8)
        append(0, min(4, capacity - len(bits)))
        append(0, (-len(bits)) % 8)
        codewords = [int("".join(map(str, bits[i:i + 8])), 2) for i in range(0, len(bits), 8)]
        pad = 0xEC
        while len(codewords) < capacity // 8:
            codewords.append(pad)
            pad ^= 0xEC ^ 0x11
        self.modules = _Symbol(chosen, lvl, codewords).modules

    def make_image(self, fill_color="black", back_color="white"):
        if self.modules is None:
            self.make()
        return QRImage(self.modules, self.box_size, self.border, fill_color, back_color)


def make(data):
    qr = QRCode()
    qr.add_data(data)
    return qr.make_image()
