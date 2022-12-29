from GyverLamp2 import Lamp

lamp = Lamp(request_delay=5000)

lamp.turn_off()  # Выключить лампу
lamp.turn_on()  # Включить лампу
lamp.max_brightness()  # Установить максимальную яркость
lamp.min_brightness()  # Установить минимальную яркость
lamp.back_mode()  # Прошлый режим
lamp.next_mode()  # Следущий режим
lamp.set_mode(1)  # Установить режим
lamp.set_wifi_mode(1)  # Установить режим WiFi, 1 - точка доступа, 2 - локальная сеть
lamp.change_role(1)  # Установить роль, 0 - младшая, 1 - Главная
lamp.change_group(1)  # Установить группу
lamp.set_wifi('ssid', 'pass')  # Установить данные WiFi
lamp.restart()  # Перезапустить лампу
lamp.firmware_update()  # Обновить прошивку если есть
lamp.sleep_timer(1)  # Выключить лампу через 1 минуту
