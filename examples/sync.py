from GyverLamp2 import Lamp


lamp = Lamp()
if not lamp.sync_settings(auto_sync=True, check_ver=True):  # Send a request to synchronize the lamp settings
    print('Произошла ошибка сихронизации. Проверьте что лампа находится с вами в одной сети')
    exit(0)
print('Лампа была синхронизирована')
lamp.save_settings_json()  # сохраняем настройки
lamp.settings(default_settings=True)

lamp.settings(brightness=255)  # Отправляем теперь свои настройки


# Чтобы лампа могла отправлять запросы на сервер, нужно скачать файл parsing.ino и архив проекта,
# дальше разархивируем архив, заходим в папку firmware, потом в папку GyverLamp2 и заменяем файл
# parsing.ino на скачанный, прошиваем. Готово!
# ССЫЛКИ
# parsing.ino - https://drive.google.com/file/d/1pnKzcrGQT6KlmFDsaizI0PsYUBRaYPh_/view?usp=sharing
# GyverLamp2 - https://codeload.github.com/AlexGyver/GyverLamp2/zip/refs/heads/main
