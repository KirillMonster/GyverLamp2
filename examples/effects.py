from GyverLamp2 import Lamp
from GyverLamp2.config import Config
from GyverLamp2.gcolor import GColor
from time import sleep

lamp = Lamp()
brightness = 255
sleep(0.5)
print('Отображение одного цвета разными кодировками цвета')
sleep(2)
print('rgb')
lamp.color_fill(rgb=(0, 238, 255,), brightness=brightness)
sleep(1)
print('hex')
lamp.color_fill(hex='00eeff', brightness=brightness)
sleep(1)
print('hsv')
lamp.color_fill(hsv=(0.51, 1.0, 1.0,), brightness=brightness)
sleep(1)
print('chsv')
lamp.color_fill(chsv=(130, 255, 255,), brightness=brightness)

sleep(5)
print('Отображение всех режимов для одного цвета')
for i in range(7):
    lamp.color_fill(color='aqua', brightness=brightness, type_effect=i)
    print(f'Эффект #{i+1}: {Config.TYPE_EFFECTS[i]}')
    sleep(5)

sleep(5)
print('Отображение разных цветов')
for color in GColor.colours().keys():
    lamp.color_fill(color=color, brightness=brightness)
    print(f'Цвет: {GColor.colours_eng2ru()[color]}')
    sleep(3)

sleep(5)
print('Отображение случайных режимов каждые 15 секунд')
while True:
    lamp.random_effects(count=1, brightness=brightness)
    sleep(15)
