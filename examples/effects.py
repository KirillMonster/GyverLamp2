from GyverLamp2 import Lamp, TYPE_EFFECTS, COLORS_RGB, COLORS_ENG2RU
from time import sleep

lamp = Lamp()

brightness = 255

print('Отображение одного цвета разными кодировками цвета')
lamp.color_fill(colour='aqua', brightness=brightness)
sleep(0.5)
lamp.color_fill(rgb=(0, 238, 255,), brightness=brightness)
sleep(0.5)
lamp.color_fill(hex='00eeff', brightness=brightness)
sleep(0.5)
lamp.color_fill(hsv=(0.51, 1.0, 255,), brightness=brightness)
sleep(0.5)
lamp.color_fill(chsv=(130, 255, 255,), brightness=brightness)

sleep(5)
print('Отображение всех режимов для одного цвета')
for i in range(1, 8):
    lamp.color_fill(color='aqua', brightness=brightness, type_effect=i)
    print(f'Эффект: {TYPE_EFFECTS[i]}, #{i}')
    sleep(5)

sleep(5)
print('Отображение разных цветов')
for color in COLORS_RGB.keys():
    lamp.color_fill(color=color, brightness=brightness)
    print(f'Цвет: {COLORS_ENG2RU[color]}')
    sleep(3)

sleep(5)
print('Отображение случайных режимов каждые 15 секунд')
while True:
    lamp.random_effects(count=1, brightness=brightness)
    sleep(15)
