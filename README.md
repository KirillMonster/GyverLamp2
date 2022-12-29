.. image:: https://raw.githubusercontent.com/nextcord/nextcord/master/assets/repo-banner.svg
   :alt: Nextcord

## 💡 GyverLamp2
📚 Библиотека для управления лампами GyverLamp2 на Python

### 🔗 Ссылки
 - Страница автора проекта лампы на сайте: https://alexgyver.ru/GyverLamp/

### 📋 Возможности
 - **🌐 Сихронизация настроек лампы**
   - Сохранять и загружать настройки ввиде json файла
   - Автоматическая сихронизация - лампа отправляет настройки при изменении.
 - **💥 Генерировать случайные режимы**
 - **Все функции во вкладках приложения: Управление, Конфиг, Режимы, Палитра (заливка одним цветом)**
   - Заливка цветом используя разные кодировки цвета: rgb, hex, hsv, chsv (chsv - это тот же hsv только значения от 0 до 255)
 - **Список задач, который сам добавляет функции в список и выполняет их раз в пол секунды**

### ⚙ Установка
**Python 3.9 или выше**
``` shell
# Linux/macOS
python3 -m pip install -U GyverLamp2

# Windows
py -3 -m pip install -U GyverLamp2
```

<a id="sync-system"></a>
### Установка системы синхронизации
- Cкачать файл - **[parsing.ino](https://drive.google.com/file/d/1pnKzcrGQT6KlmFDsaizI0PsYUBRaYPh_/view?usp=sharing)**
- Скачать архив с проектом **https://github.com/AlexGyver/GyverLamp2**
- Разархивировать архив
- Перейти в папку c проектом
- Потом в папку firmware, дальше в GyverLamp2
- Заменить файл parsing.ino на скачанный
- Прошиваем
- Готово!

###  Простой пример
```Python
from GyverLamp2 import Lamp
from time import sleep

lamp = Lamp()

lamp.turn_on()
sleep(0.5)
lamp.next_mode()
```

###  Список задач
```Python
from GyverLamp2 import Lamp

lamp = Lamp(enable_task_list=True)

lamp.turn_on()

while True:
    lamp.random_effects(delay=5000)
```

Все примеры - https://github.com/KirillMonster/GyverLamp2/tree/main/examples/
