from GyverLamp2 import Lamp

lamp = Lamp(ip='192.168.1.237', log_data_request=True)
lamp.sync_settings()
print('Адрес ESP:', lamp.client_address)
lamp.settings(min_brightness=100, max_brightness=255, brightness=255)  # Отправляем теперь свои настройки
