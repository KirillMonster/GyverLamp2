from GyverLamp2 import Lamp
from time import sleep

lamp = Lamp(ip='192.168.1.238', log_data_request=True)
# lamp.turn_off()
# sleep(0.55)
lamp.sync_settings()
# lamp.settings(brightness=255)  # Отправляем теперь свои настройки
