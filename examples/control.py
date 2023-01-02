from GyverLamp2 import Lamp
from time import sleep

lamp = Lamp()

lamp.turn_off()  # Выключить лампу
sleep(0.5)
lamp.turn_on()  # Включить лампу
sleep(0.5)
lamp.max_brightness()  # Установить максимальную яркость
sleep(0.5)
lamp.min_brightness()  # Установить минимальную яркость
sleep(0.5)
lamp.back_mode()  # Прошлый режим
sleep(0.5)
lamp.next_mode()  # Следущий режим
sleep(0.5)
lamp.set_mode(1)  # Установить режим
sleep(0.5)
lamp.set_wifi_mode(1)  # Установить режим WiFi, 1 - точка доступа, 2 - локальная сеть
sleep(0.5)
lamp.change_role(1)  # Установить роль, 0 - младшая, 1 - Главная
sleep(0.5)
lamp.change_group(1)  # Установить группу
sleep(0.5)
lamp.set_wifi('Lola', '123456')  # Установить данные WiFi
sleep(0.5)
lamp.restart()  # Перезапустить лампу
sleep(0.5)
lamp.firmware_update()  # Обновить прошивку если есть
sleep(0.5)
lamp.sleep_timer(1)  # Выключить лампу через 1 минуту
