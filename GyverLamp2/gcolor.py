from typing import Any

COLORS_RGB = {
    'red': (255, 0, 0,),
    'orange': (255, 165, 0,),
    'yellow': (255, 255, 0,),
    'green': (0, 214, 120,),
    'lime': (0, 255, 0,),
    'aqua': (0, 255, 255,),
    'cyan': (0, 255, 255,),
    'blue': (0, 0, 255,),
    'purple': (255, 20, 147,),
    'pink': (255, 20, 147,),
    'black': (0, 0, 0,),
    'white': (255, 255, 255,)
}
COLORS_RU2ENG = {'красный': 'red', 'оранжевый': 'orange', 'желтый': 'yellow', 'зеленый': 'green', 'лайм': 'lime', 'аква': 'aqua',
                 'циан': 'cyan', 'синий': 'blue', 'фиолетовый': 'purple', 'розовый': 'pink', 'черный': 'black',
                 'белый': 'white'}
COLORS_ENG2RU = {}
for key, value in COLORS_RU2ENG.items():
    COLORS_ENG2RU[value] = key
COLORS_HEX = {}
COLORS_HSV = {}
COLORS_CHSV = {}


def rgb2hsv(r, g, b):
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
    if max_rgb == 0:
        s = 0
    else:
        s = difference / max_rgb
    return round(h), round(s, 2), round(max_rgb, 2)


def rgb2hex(r, g, b) -> str:
    code = f'{hex(r)}{hex(g)}{hex(b)}'.replace('0x', '')
    if len(code) < 6:
        last_num = code[-1]
        for i in range(6 - len(code)):
            code += last_num
    return code


def hex2rgb(code: str) -> tuple[int, int, int]:
    code = code.replace('#', '')
    count = 0
    r, g, b = None, None, None
    len_code = len(code)
    if len_code == 0 or len_code > 6:
        return 255, 255, 255

    last_num = code[-1]
    if len_code < 6:
        for i in range(6 - len_code):
            code += last_num

    for i in code:
        count += 1
        if count % 2 != 0:
            last_num = i
        if count > 1 and count % 2 == 0:
            num = f'0x{last_num}{i}'
            if r is None:
                r = int(num, 16)
            elif g is None:
                g = int(num, 16)
            elif b is None:
                b = int(num, 16)
            else:
                break
    return r, g, b


def hsv2chsv(h, s, v) -> tuple[Any, ...]:
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
    h = round(h)
    s = round(s)
    v = round(v)
    return h, s, v


def chsv2hsv(h, s, v) -> tuple[float, float, float]:
    h = h * 360 / 255
    s = s * 100 / 255
    v = v * 100 / 255
    return round(h), round(s), round(v)


def rgb2chsv(r, g, b) -> tuple[Any, ...]:
    return hsv2chsv(*rgb2hsv(r, g, b))


for __key in COLORS_RGB.keys():
    COLORS_HEX[__key] = rgb2hex(*COLORS_RGB[__key])

for __key in COLORS_RGB.keys():
    COLORS_HSV[__key] = rgb2hsv(*COLORS_RGB[__key])

for __key in COLORS_RGB.keys():
    COLORS_CHSV[__key] = rgb2chsv(*COLORS_RGB[__key])
