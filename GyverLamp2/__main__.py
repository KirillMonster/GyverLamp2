import socket as _socket
from datetime import datetime as _datetime
from json import load as _jload, dump as _jdump
from random import randint as _randint
from time import time as _time
from copy import deepcopy as _deepcopy
from .gcolor import GColor as _GColor
from .config import Config as _Config
from .errors import *


class Lamp:
    def __init__(self, key: str = 'GL', ip: str | None = None, port: int | None = None, netmask: str = '255.255.255.0',
                 group_id: int = 1, json_settings_path: str = 'settings.json', log_data_request: bool = False):

        self.__key = key
        self.local_ip = _socket.gethostbyname(_socket.gethostname())
        self.netmask = netmask
        self.ip = self.__get_broadcast_addr() if ip is None else ip
        self.client_address = None
        self.__group_id = group_id
        self.port = self.__gen_port() if port is None else port
        self.__json_settings_path = json_settings_path
        self.__log_data_request = log_data_request
        self.__settings_data = _deepcopy(_Config.DEFAULT_SETTINGS_DATA)
        self.__effects_data = _deepcopy(_Config.DEFAULT_EFFECTS_DATA)

        self.__sock = _socket.socket(_socket.AF_INET, _socket.SOCK_DGRAM, _socket.IPPROTO_UDP)
        self.__sock.setsockopt(_socket.SOL_SOCKET, _socket.SO_BROADCAST, 1)
        self.__sock.bind(('', self.port))
        self.__sock.settimeout(3)

    def __get_broadcast_addr(self):
        ip = list(map(int, self.local_ip.split(".")))
        mask = list(map(int, self.netmask.split(".")))
        broadcast = [str(i | (j ^ 255)) for i, j in zip(ip, mask)]
        return '.'.join(broadcast)

    def __gen_port(self):
        port = 17
        for i in range(len(self.__key)):
            port *= ord(self.__key[i])
        port %= 65536
        port %= 15000
        port += 50000
        port += self.__group_id
        return port

    def turn_off(self, *date, **kwargs):
        """Turn off the lamp"""
        date = self.__date_proc(kwargs.get('delay'), *date)
        self.__send_request('0,0', date)

    def turn_on(self, *date, **kwargs):
        """ Turn on the lamp"""
        date = self.__date_proc(kwargs.get('delay'), *date)
        self.__send_request('0,1', date)

    def min_brightness(self):
        """ Set the minimum brightness of the lamp """
        self.__send_request('0,2')

    def max_brightness(self):
        """ Set the maximum brightness of the lamp """
        self.__send_request('0,3')

    def back_mode(self, *date, **kwargs):
        """ """
        date = self.__date_proc(kwargs.get('delay'), *date)
        self.__send_request('0,4', date)

    def next_mode(self, *date, **kwargs):
        """ Next mode """
        date = self.__date_proc(kwargs.get('delay'), *date)
        self.__send_request('0,5', date)

    def set_mode(self, mode):
        """ Set mode """
        self.__send_request(f'0,6,{mode}')

    def set_wifi_mode(self, mode):
        """ 0 - AP, 1 - Local """
        self.__send_request(f'0,7,{mode}')

    def change_role(self, role):
        """ 0 - Slave, 1 - Master """
        self.__send_request(f'0,8,{role}')

    def change_group(self, group_id):
        """ Set group"""
        self.__send_request(f'0,9,{group_id}')

    def set_wifi(self, ssid, password):
        """ Set Wi-Fi credentials """
        self.__send_request(f'0,10,{ssid},{password}')

    def restart(self):
        """ Restart the lamp"""
        self.__send_request(f'0,11')

    def firmware_update(self):
        """ Update the firmware """
        self.__send_request(f'0,12')

    def sleep_timer(self, minutes: int):
        """ 0-255 minutes"""
        self.__send_request(f'0,13,{minutes}')

    def get_settings(self):
        return self.__settings_data

    def get_param(self, name: str) -> str:
        return self.__settings_data.get(name)

    def set_auto_sync_settings(self, state: bool):
        self.__send_request(f'20,2,{int(state)}')

    def sync_settings(self, auto_sync: bool = False):
        try:
            msg, address = self.__send_request(f'20,1,{int(auto_sync)}', response=True)
            if msg is None:
                raise SyncError()
        except TimeOutError:
            raise SyncError()
        data = msg.split(',')
        count = 0
        try:
            for key_ in self.__settings_data.keys():
                self.__settings_data[key_] = data[count]
                count += 1
        except IndexError:
            raise IncorrectDataError(address, msg)

    def settings(self, default_settings: bool = False, *date, **kwargs):
        date = self.__date_proc(kwargs.get('delay'), *date)
        data = ''
        settings = _Config.DEFAULT_SETTINGS_DATA if default_settings else self.__settings_data
        for key, value in kwargs.items():
            if key not in settings:
                continue
            self.__settings_data[key] = value
            settings[key] = value
        for value in settings.values():
            data += f',{value}'
        self.__send_request(f'1{data}', date)

    def random_effects(self, count: int = 1, *date, **kwargs):
        if not 0 < count < 26:
            raise CountEffectsNotInRangeError()
        data = f'2,{count}'
        random_num = _randint(1, count)
        brightness = kwargs.get('brightness')
        if brightness:
            max_brightness, min_brightness = brightness, brightness
        else:
            min_brightness = kwargs.get('min_brightness') if kwargs.get('min_brightness') else _randint(50, 255)
            max_brightness = kwargs.get('max_brightness') if kwargs.get('max_brightness') else _randint(50, 255)
            max_brightness, min_brightness = [max_brightness, min_brightness] if max_brightness > min_brightness else [
                min_brightness, max_brightness]
        for i in range(count):
            type_effect = _randint(1, 7)
            fade_brightness = _randint(0, 1)
            brightness = _randint(min_brightness, max_brightness)
            adv_mode = kwargs.get('adv_mode') if kwargs.get('adv_mode') else _randint(1, 5)
            sound_react = kwargs.get('sound_react') if kwargs.get('sound_react') else _randint(1, 3)
            min_signal = kwargs.get('min_signal') if kwargs.get('min_signal') else _randint(1, 255)
            max_signal = kwargs.get('max_signal') if kwargs.get('max_signal') else _randint(1, 255)
            speed = _randint(50, 255)
            palette = _randint(1, 26)
            scale = _randint(50, 255)
            from_center = _randint(0, 1)
            color = _randint(0, 255)
            random_effect = _randint(0, 1)
            data += f',{type_effect},{fade_brightness},{brightness},{adv_mode},{sound_react},{min_signal},{max_signal},{speed},{palette},{scale},{from_center},{color},{random_effect}'
        data += f',{random_num}'
        date = self.__date_proc(kwargs.get('delay'), *date)
        self.__send_request(data, date)

    def color_fill(self, *date, **kwargs):
        date = self.__date_proc(kwargs.get('delay'), *date)
        hue, saturation, value = 255, 255, 255
        if kwargs.get('colour') or kwargs.get('color'):
            color = kwargs.get('colour') or kwargs.get('color')
            if color in _GColor.colours():
                hue, saturation, value = _GColor.rgb2chsv(*_GColor.hex2rgb(_GColor.colours()[color]))
        elif kwargs.get('rgb'):
            hue, saturation, value = _GColor.rgb2chsv(*kwargs.get('rgb'))
        elif kwargs.get('hex16'):
            hue, saturation, value = _GColor.rgb2chsv(*_GColor.hex2rgb(_GColor.hex16tohex24(kwargs.get('hex16'))))
        elif kwargs.get('hex'):
            hue, saturation, value = _GColor.rgb2chsv(*_GColor.hex2rgb(kwargs.get('hex')))
        elif kwargs.get('hsv'):
            hue, saturation, value = _GColor.hsv2chsv(*kwargs.get('hsv'))
        elif kwargs.get('chsv'):
            hue, saturation, value = kwargs.get('chsv')

        hue, saturation = kwargs.get('hue', hue), kwargs.get('saturation', saturation)
        value = kwargs.get('value') or kwargs.get('value') or value
        type_effect = kwargs.get('type_effect', 2)
        data = f'2,1,{type_effect},1,{value},1,1,0,255,105,2,{saturation},0,{hue},0,1'
        self.__send_request(data, date)

    def save_settings_json(self):
        with open(self.__json_settings_path, 'w') as file:
            _jdump(self.__settings_data, file)

    def load_settings_json(self):
        with open(self.__json_settings_path, 'r') as file:
            self.__settings_data = _jload(file)

    def __send_request(self, *args, **kwargs):
        if isinstance(args[0], tuple):
            args = args[0]
        delay = 0
        if len(args) > 1 and '+' in args[1]:
            delay = int(args[1].split('+')[1])

        data = []
        for i in args:
            if 'now' in i:
                i = self.__now_date(delay)
            data.append(i)
        message = f'{self.__key},{",".join(data)}'
        if self.__log_data_request:
            print(message)
            print(self.__format_request_data(message))

        for i in range(5):
            self.__sock.sendto(message.encode(), (self.ip, self.port))

        if kwargs.get('response'):
            return self.__query_handler()

    def __formate_date(self, date):
        return f'{_Config.DAYS_OF_THE_WEEK[date[0]]}, {date[1]}ч, {date[2]}м, {date[3]}с'

    def __format_request_data(self, data):
        data = data.replace('GL,', '', 1)
        data = data.split(',')
        msg = ''
        match data[0]:
            case '0':
                data = data[1:]
                msg = f'Управление: {_Config.CONTROL_TYPES[data[0]]}'
                data[0] = int(data[0])
                if data[0] in [0, 1, 4, 5]:
                    msg += f', в: {self.__formate_date(data[1:])}'
                elif data[0] == 6:
                    msg += f' №{data[2]}'
                elif data[0] == 7:
                    msg += f' на {"AP" if data[1] == 0 else "Local"}'
                elif data[0] == 8:
                    msg += f' на {"Slave" if data[1] == 0 else "Master"}'
                elif data[0] == 9:
                    msg += f' на №{data[1]}'
                elif data[0] == 10:
                    msg += f' {data[1]}, {data[2]}'
                elif data[0] == 13:
                    msg += f' на {data[1]}м.'
            case '1':
                msg = 'Настройка: '
                count_ = 0
                for i in self.__settings_data.values():
                    msg += f'{_Config.NAME_SETTINGS[count_]}: {i}, '
                    count_ += 1
            case '2':
                msg = f'Режимы: кол-во режимов: {data[1]}'
                data = data[2:]
                effects = []
                if len(data) == 19:
                    effects.append(data[1:14])
                else:
                    count = 0
                    temp_effect = []
                    for i in data:
                        count += 1
                        if count % 14 == 0:
                            effects.append(_deepcopy(temp_effect))
                            temp_effect.clear()
                            temp_effect.append(i)
                        else:
                            temp_effect.append(i)
                count = 0
                for effect in effects:
                    count += 1

                    msg += f'\nРежим #{count}, тип эффекта: {_Config.TYPE_EFFECTS[int(effect[0]) - 1]}, понизить яркость: {effect[1]},' \
                           f' яркость {effect[2]}, дополнительно: {effect[3]}, реацкия на звук: {effect[4]},' \
                           f' мин сигнал: {effect[5]}, макс сигнал: {effect[6]}, скорость {effect[7]},' \
                           f' палитра: {_Config.TYPE_PALLETES[int(effect[8]) - 1]}, масштаб: {effect[9]}, из центра: {effect[10]},' \
                           f' цвет: {effect[11]}, случайный: {effect[12]}'

        return msg

    def __now_date(self, delay=0):
        day = _datetime.fromtimestamp(int(_time() + 1 + delay))
        return f'{day.isoweekday()},{day.hour},{day.minute},{day.second}'

    def __date_proc(self, delay, *date):
        if len(date) == 0:
            return f'now+{delay}' if delay else 'now'
        return date

    def __query_handler(self, attempts: int = 15):
        try:
            result, address = self.__sock.recvfrom(8192)
            result = result.decode()
            if address[0] == self.local_ip or result.startswith('GL_ONL0'):
                if attempts > 0:
                    return self.__query_handler(attempts - 1)
                return None
            self.client_address = address
            return result, address
        except TimeoutError:
            raise TimeoutError('Вышло время получения ответа')
