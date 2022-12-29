from GyverLamp2 import Lamp
from GyverLamp2.gcolor import *
from time import sleep

lamp = Lamp(request_delay=1500)

print('Отображение одного цвета разными кодировками цвета')
lamp.palette(colour='aqua', brightness=255)
lamp.palette(rgb=(0, 238, 255,), brightness=255)
lamp.palette(hex='00eeff', brightness=255)
lamp.palette(hsv=(0.51, 1.0, 255,), brightness=255)
lamp.palette(chsv=(130, 255, 255,), brightness=255)

sleep(5)
print('Отображение всех режимов для одного цвета')
for i in range(8):
    lamp.palette(color='aqua', brightness=255, type_effect=i + 1, delay=3000)

sleep(5)
print('Отображение разных цветов')
for color in COLORS_RGB.keys():
    lamp.palette(color=color, brightness=255)

sleep(5)
print('Отображение случайных режимов каждые 15 секунд')
while True:
    lamp.random_effects(count=1, delay=15000)
