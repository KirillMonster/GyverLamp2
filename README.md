## 💡 GyverLamp2
📚 Библиотека для управления лампами GyverLamp2 на Python

### 🔗 Ссылки
 - Страница проекта на сайте: https://alexgyver.ru/GyverLamp/ <br />
 - GyverLamp2 - https://github.com/AlexGyver/GyverLamp2 <br />
 - **[parsing.ino](https://drive.google.com/file/d/1pnKzcrGQT6KlmFDsaizI0PsYUBRaYPh_/view?usp=sharing)** - Этот файл нужен для сихронизации настроек, скачайте прошивку и замените файл parsing.ino на этот, лампой можно управлять без этого


### 📋 Возможности
 - **🌐 Сихронизация настроек лампы**
   - Сохранять и загружать настройки ввиде json файла
   - Автоматическая сихронизация - лампа отправляет настройки при изменении.
 - **💥 Генерировать случайные режимы**
 - **Все функции во вкладках приложения: Управление, Конфиг, Режимы, Палитра (заливка одним цветом)**
   - Заливка цветом используя разные кодировки цвета: rgb, hex, hsv, chsv (chsv - это hsv только значения от 0 до 255)
 - **Есть список задач, который сам добавляет функции в список и выполняет их раз в пол секунды**

### ⚙ Установка
**Python 3.9 или выше**
``` shell
# Linux/macOS
python3 -m pip install -U GyverLamp2

# Windows
py -3 -m pip install -U GyverLamp2
```

###  Простой пример
```Python
from GyverLamp2 import Lamp
from time import sleep

lamp = Lamp()

lamp.turn_on()
sleep(0.5)
lamp.next_mode()
```

Все примеры - https://github.com/KirillMonster/GyverLamp2/tree/main/examples/
