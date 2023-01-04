from GyverLamp2 import Lamp

lamp = Lamp(ip='192.168.1.237', log_data_request=True)
print(lamp.ip, lamp.port, lamp.local_ip)
lamp.sync_settings()
print('SUCCESSFULLY')
print('Client address', lamp.client_address)
# lamp.settings(brightness=255)  # Отправляем теперь свои настройки
