class GColour:
    @classmethod
    def colours(cls):
        return {
            'white': 0xF8FCF8,
            'silver': 0xC0C0C0,
            'gray': 0x808080,
            'black': 0x000000,
            'red': 0xF80000,
            'maroon': 0x800000,
            'orange': 0xF83000,
            'yellow': 0xF88000,
            'olive': 0x808000,
            'lime': 0x00FC00,
            'green': 0x008000,
            'aqua': 0x00FCF8,
            'teal': 0x008080,
            'blue': 0x0000F8,
            'navy': 0x000080,
            'magenta': 0xF800F8,
            'purple': 0x800080
        }

    @classmethod
    def colours_ru2eng(cls):
        return {
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

    @classmethod
    def colours_eng2ru(cls):
        colours_ = {}
        for key, value in cls.colours_ru2eng().items():
            colours_[value] = key
        return colours_

    @classmethod
    def hex2rgb(cls, color: int | str) -> tuple[int, int, int]:
        if isinstance(color, str):
            color = int(color.replace('#', ''), 16)
        # https://github.com/GyverLibs/GRGB/blob/main/src/GRGB.h#L282
        return (color >> 16) & 0xFF, (color >> 8) & 0xFF, color & 0xFF

    @classmethod
    def hex16tohex24(cls, color: int | str) -> int:
        if isinstance(color, str):
            color = int(color.replace('#', ''), 16)
        # https://github.com/GyverLibs/GRGB/blob/main/src/GRGB.h#L292
        return ((color & 0xF800) << 8) | ((color & 0x7E0) << 5) | ((color & 0x1F) << 3)

    @classmethod
    def rgb2hex(cls, r, g, b) -> str:
        return '#%02x%02x%02x' % (r, g, b)

    @classmethod
    def rgb2hsv(cls, r, g, b) -> tuple[int, int, int]:
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

    @classmethod
    def hsv2chsv(cls, h, s, v) -> tuple[int, int, int]:
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

    @classmethod
    def chsv2hsv(cls, h, s, v) -> tuple[float, float, float]:
        h = h * 360 / 255
        s = s * 100 / 255
        v = v * 100 / 255
        return round(h), round(s), round(v)

    @classmethod
    def rgb2chsv(cls, r, g, b) -> tuple[int, int, int]:
        return cls.hsv2chsv(*cls.rgb2hsv(r, g, b))


GColor = GColour
