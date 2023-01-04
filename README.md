![](https://github.com/KirillMonster/GyverLamp2/blob/master/assets/banner.png)
![pypi](https://img.shields.io/pypi/v/gyverlamp2.svg)
## 💡 GyverLamp2
📚 Библиотека для управления лампами GyverLamp2 на Python

### 🔗 Ссылки
 - PyPi - https://pypi.org/project/GyverLamp2/
 - Страница проекта автора лампы: https://alexgyver.ru/GyverLamp/

### 📋 Возможности
 - **🌐 Синхронизация настроек лампы**
   - Сохранять и загружать настройки ввиде json файла
   - Автоматическая синхронизация - лампа отправляет настройки на локальный сервер при изменении их.
 - 💥 **Генерировать случайные режимы**
 - 📱 **Все функции во вкладках приложения: Управление, Конфиг, Режимы, Палитра (заливка одним цветом)**
   - Заливка цветом используя разные кодировки цвета: rgb, hex, hsv, chsv (chsv - это тот же hsv только значения от 0 до 255)

### ⚙ Установка
**Python 3.9 или выше**
``` shell
# Linux/macOS
python3 -m pip install -U GyverLamp2

# Windows
py -3 -m pip install -U GyverLamp2
```

<a id="sync-system"></a>
### Установка синхронизации
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

Все примеры - https://github.com/KirillMonster/GyverLamp2/tree/main/examples
