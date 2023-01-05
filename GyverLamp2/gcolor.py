COLORS_RGB = {
    'white': (248, 252, 248),
    'silver': (192, 192, 192),
    'gray': (128, 128, 128),
    'black': (0, 0, 0),
    'red': (248, 0, 0),
    'maroon': (128, 0, 0),
    'orange': (248, 48, 0),
    'yellow': (248, 128, 0),
    'olive': (128, 128, 0),
    'lime': (0, 252, 0),
    'green': (0, 128, 0),
    'aqua': (0, 252, 248),
    'teal': (0, 128, 128),
    'blue': (0, 0, 248),
    'navy': (0, 0, 128),
    'magenta': (248, 0, 248),
    'purple': (128, 0, 128)
}

COLORS_RU2ENG = {
    'белый': 'white',
    'серебро': 'silver',
    'серый': 'gray',
    'чёрный': 'black',
    'красный': 'red',
    'бордовый': 'maroon',
    'оранжевый': 'orange',
    'жёлтый': 'yellow',
    'олива': 'olive',
    'лайм': 'lime',
    'зелёный': 'green',
    'аква': 'aqua',
    'teal': 'teal',
    'голубой': 'blue',
    'темно-синий': 'navy',
    'розовый': 'magenta',
    'пурпурный': 'purple'
}
COLORS_ENG2RU = {}
COLORS_HEX = {}
COLORS_HSV = {}
COLORS_CHSV = {}


def hex2rgb(color: int | str) -> tuple[int, int, int]:
    if isinstance(color, str):
        color = int(color.replace('#', ''), 16)
    # https://github.com/GyverLibs/GRGB/blob/main/src/GRGB.h#L282
    return (color >> 16) & 0xFF, (color >> 8) & 0xFF, color & 0xFF


def hex16tohex24(color: int | str) -> int:
    if isinstance(color, str):
        color = int(color.replace('#', ''), 16)
    # https://github.com/GyverLibs/GRGB/blob/main/src/GRGB.h#L292
    return ((color & 0xF800) << 8) | ((color & 0x7E0) << 5) | ((color & 0x1F) << 3)


def rgb2hex(r, g, b) -> str:
    return '#%02x%02x%02x' % (r, g, b)


def rgb2hsv(r, g, b) -> tuple[int, int, int]:
    r, g, b = r / 255, g / 255, b / 255
    max_rgb = max(r, g, b)
    min_rgb = min(r, g, b)
    difference = max_rgb - min_rgb
    h = 0
    if max_rgb == min_rgb:
        h = 0
    elif max_rgb == r:
        h = (60 * ((g - b) / difference) + 360) % 360
    elif max_rgb == g:
        h = (60 * ((b - r) / difference) + 120) % 360
    elif max_rgb == b:
        h = (60 * ((r - g) / difference) + 240) % 360
    s = 0 if max_rgb == 0 else difference / max_rgb
    return round(h), round(s, 2), round(max_rgb, 2)


def hsv2chsv(h, s, v) -> tuple[int, int, int]:
    if h < 1.1:
        h = h * 255
    else:
        h = h / 360 * 255
    if s < 1.1:
        s = s * 255
    else:
        s = s / 100 * 255
    if v < 1.1:
        v = v * 255
    else:
        v = v / 100 * 255
    return round(h), round(s), round(v)


def chsv2hsv(h, s, v) -> tuple[float, float, float]:
    h = h * 360 / 255
    s = s * 100 / 255
    v = v * 100 / 255
    return round(h), round(s), round(v)


def rgb2chsv(r, g, b) -> tuple[int, int, int]:
    return hsv2chsv(*rgb2hsv(r, g, b))


for __key in COLORS_RGB.keys():
    COLORS_HEX[__key] = rgb2hex(*COLORS_RGB[__key])

for __key in COLORS_RGB.keys():
    COLORS_HSV[__key] = rgb2hsv(*COLORS_RGB[__key])

for __key in COLORS_RGB.keys():
    COLORS_CHSV[__key] = rgb2chsv(*COLORS_RGB[__key])

for __key, __value in COLORS_RU2ENG.items():
    COLORS_ENG2RU[__value] = __key
