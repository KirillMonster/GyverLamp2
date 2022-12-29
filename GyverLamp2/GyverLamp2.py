from socket import AF_INET, SOCK_DGRAM, socket, SOL_SOCKET, SO_BROADCAST
from datetime import datetime
from json import load as jload, dump as jdump
from random import randint
from threading import Thread
from time import sleep, time
from copy import deepcopy
from .gcolor import *
from .config import *


class Lamp:
    def __init__(self, key: str = 'GL', ip: str | None = None, port: int | None = None, group_id: int = 1, request_delay: float = 500,
                 json_settings_path: str = 'settings.json', log_data_request: bool = False, enable_task_list: bool = False):

        self.key = key
        self.ip = '255.255.255.255' if ip is None else ip
        self.group_id = group_id
        self.port = self.gen_port() if port is None else port
        self.json_settings_path = json_settings_path
        self.request_delay = request_delay

        self.__log_data_request = log_data_request
        self.__enable_task_list = enable_task_list
        self.__task_list = []
        if self.__enable_task_list:
            self.__task_list_thread = Thread(target=self.__task_list_processing)
            self.__task_list_thread.start()

        self.__last_request_time = 0
        self.__settings_data = deepcopy(DEFAULT_SETTINGS_DATA)
        self.__effects_data = {'count_effets': '1', 'type_effect': '1', 'fade_brightness': '1', 'brightness': '255',
                               'adv_mode': '1', 'effect_react': '1', 'min_signal': '0', 'max_signal': '255',
                               'speed': '105', 'scale': '255', 'from_center': '0', 'color': '255', 'random': '0'}

        self.sock = socket(AF_INET, SOCK_DGRAM)
        self.sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        self.sock.bind(('', self.port))
        self.sock.settimeout(3)

    def gen_port(self):
        portNum = 17 # uint16_t(или % 65536)
        for i in range(len(self.key)):
            portNum *= ord(self.key[i])

        portNum %= 65536
        portNum %= 15000
        portNum += 50000
        portNum += self.group_id
        return portNum

    def turn_off(self, *date, **kwargs):
        """Turn off the lamp"""
        date = self.__date_proc(kwargs.get('delay'), *date)
        self.send_request('0,0', date)

    def turn_on(self, *date, **kwargs):
        """ Turn on the lamp"""
        date = self.__date_proc(kwargs.get('delay'), *date)
        self.send_request('0,1', date)

    def min_brightness(self):
        """ Set the minimum brightness of the lamp """
        self.send_request('0,2')

    def max_brightness(self):
        """ Set the maximum brightness of the lamp """
        self.send_request('0,3')

    def back_mode(self, *date, **kwargs):
        """ """
        date = self.__date_proc(kwargs.get('delay'), *date)
        self.send_request('0,4', date)

    def next_mode(self, *date, **kwargs):
        """ Next mode """
        date = self.__date_proc(kwargs.get('delay'), *date)
        self.send_request('0,5', date)

    def set_mode(self, mode):
        """ Set mode """
        self.send_request(f'0,6,{mode}')

    def set_wifi_mode(self, mode):
        """ 0 - AP, 1 - Local """
        self.send_request(f'0,7,{mode}')

    def change_role(self, role):
        """ 0 - Slave, 1 - Master """
        self.send_request(f'0,8,{role}')

    def change_group(self, group_id):
        """ Set group"""
        self.send_request(f'0,9,{group_id}')

    def set_wifi(self, ssid, password):
        """ Set Wi-Fi credentials """
        self.send_request(f'0,10,{ssid},{password}')

    def restart(self):
        """ Restart the lamp"""
        self.send_request(f'0,11')

    def firmware_update(self):
        """ Update the firmware """
        self.send_request(f'0,12')

    def sleep_timer(self, minutes: int):
        """ 0-255 minutes"""
        self.send_request(f'0,13,{minutes}')

    def get_settings(self):
        return self.__settings_data

    def get_param(self, name: str) -> str:
        return self.__settings_data.get(name)

    def set_auto_sync_settings(self, state: bool):
        self.send_request(f'20,2,{int(state)}')

    def sync_settings(self, auto_sync: bool = False, attempts: int = 5, check_ver: bool = True):
        data = self.send_request(f'20,1,{int(auto_sync)}', response=True)
        if data is None:
            if attempts > 0:
                sleep(0.03)
                self.sync_settings(auto_sync, attempts-1, check_ver)
            return False

        data = data.split(',')
        print(data)
        count = 0
        for key in self.__settings_data.keys():
            self.__settings_data[key] = data[count]
            count += 1
        return True

    def settings(self, default_settings: bool = False, *date, **kwargs):
        date = self.__date_proc(kwargs.get('delay'), *date)
        data = ''
        settings = DEFAULT_SETTINGS_DATA if default_settings else self.__settings_data
        for key, value in kwargs.items():
            if key not in settings:
                continue
            self.__settings_data[key] = value
            settings[key] = value
        for value in settings.values():
            data += f',{value}'
        self.send_request(f'1{data}', date)

    def random_effects(self, count: int = 3, *date, **kwargs):
        if not 0 < count < 26:
            return
        data = f'2,{count}'
        random_num = randint(1, count)
        brightness = kwargs.get('brightness')
        if brightness:
            max_brightness, min_brightness = brightness, brightness
        else:
            min_brightness = kwargs.get('min_brightness') if kwargs.get('min_brightness') else randint(50, 255)
            max_brightness = kwargs.get('max_brightness') if kwargs.get('max_brightness') else randint(50, 255)
            max_brightness, min_brightness = [max_brightness, min_brightness] if max_brightness > min_brightness else [
                min_brightness, max_brightness]
        for i in range(count):
            type_effect = randint(1, 7)
            fade_brightness = randint(0, 1)
            brightness = randint(min_brightness, max_brightness)
            adv_mode = kwargs.get('adv_mode') if kwargs.get('adv_mode') else randint(1, 5)
            sound_react = kwargs.get('sound_react') if kwargs.get('sound_react') else randint(1, 3)
            min_signal = kwargs.get('min_signal') if kwargs.get('min_signal') else randint(1, 255)
            max_signal = kwargs.get('max_signal') if kwargs.get('max_signal') else randint(1, 255)
            speed = randint(50, 255)
            palette = randint(1, 26)
            scale = randint(50, 255)
            from_center = randint(0, 1)
            color = randint(0, 255)
            random_effect = randint(0, 1)
            data += f',{type_effect},{fade_brightness},{brightness},{adv_mode},{sound_react},{min_signal},{max_signal},{speed},{palette},{scale},{from_center},{color},{random_effect}'
        data += f',{random_num}'
        date = self.__date_proc(kwargs.get('delay'), *date)
        self.send_request(data, date)

    def palette(self, *date, **kwargs):
        date = self.__date_proc(kwargs.get('delay'), *date)
        color, scale, brightness = 255, 255, kwargs.get('brightness', 255)
        if kwargs.get('colour') or kwargs.get('color') or kwargs.get('rgb'):
            color = kwargs.get('colour') or kwargs.get('color') or kwargs.get('rgb')
            if color in COLORS_RGB:
                color, scale, brightness = rgb2chsv(*COLORS_RGB[color])
            elif kwargs.get('rgb'):
                color, scale, brightness = rgb2chsv(*color)
        elif kwargs.get('hex'):
            color, scale, brightness = rgb2chsv(*hex2rgb(kwargs.get('hex').replace('#', '')))
        elif kwargs.get('hsv'):
            color, scale, brightness = hsv2chsv(*kwargs.get('hsv'))
        elif kwargs.get('chsv'):
            color, scale, brightness = kwargs.get('chsv')
        type_effect = kwargs.get('type_effect', 2)
        data = f'2,1,{type_effect},1,{brightness},1,1,0,255,105,2,{scale},0,{color},0,1'
        self.send_request(data, date)

    def save_settings_json(self):
        with open(self.json_settings_path, 'w') as file:
            jdump(self.__settings_data, file)

    def load_settings_json(self):
        with open(self.json_settings_path, 'r') as file:
            self.__settings_data = jload(file)

    def show_task_list(self):
        return self.__task_list

    def send_request(self, *args, **kwargs):
        if isinstance(args[0], tuple):
            args = args[0]
        delay = 0
        if len(args) > 1 and '+' in args[1]:
            delay = int(args[1].split('+')[1])
        current_time = int(time() * 1000)
        if not self.__check_time_to_send(current_time, delay) and kwargs.get('skip') is None:
            if self.__enable_task_list:
                self.__task_list.append(args)
            return
        data = []
        for i in args:
            if 'now' in i:
                i = self.__now_date()
            data.append(i)
        message = f'{self.key},{",".join(data)}'
        if self.__log_data_request:
            print(message)
            print(self.__format_request_data(message))

        self.__last_request_time = int(time() * 1000)
        try:
            self.sock.sendto(message.encode(), (self.ip, self.port))
            if kwargs.get('response'):
                result, addr = self.sock.recvfrom(1024)
                result = result.decode()
                if 'GL_ONL' in result:
                    return None
                return result
        except Exception as e:
            print(e)

    def __check_time_to_send(self, current_time: int, delay: int = 0):
        if delay > 0:
            delay -= self.request_delay
        return current_time - (self.__last_request_time + delay) > self.request_delay

    def __task_list_processing(self):
        while True:
            if len(self.__task_list) > 0:
                task = self.__task_list[0]
                delay = 0
                if len(task) > 1 and '+' in task[1]:
                    delay = int(task[1].split('+')[1])
                current_time = int(time() * 1000)
                if self.__check_time_to_send(current_time, delay):
                    self.__task_list.pop(0)
                    self.send_request(task, skip=1)

            sleep(0.1)

    def __formate_date(self, date):
        return f'{DAYS_OF_THE_WEEK[date[0]]}, {date[1]}ч, {date[2]}м, {date[3]}с'

    def __format_request_data(self, data):
        data = data.replace('GL,', '', 1)
        data = data.split(',')
        msg = ''
        match data[0]:
            case '0':
                data = data[1:]
                msg = f'Управление: {CONTROL_TYPES[data[0]]}'
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
                    msg += f'{NAME_SETTINGS[count_]}: {i}, '
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
                            effects.append(deepcopy(temp_effect))
                            temp_effect.clear()
                            temp_effect.append(i)
                        else:
                            temp_effect.append(i)
                count = 0
                for effect in effects:
                    count += 1

                    msg += f'\nРежим #{count}, тип эффекта: {TYPE_EFFECTS[effect[0]]}, понизить яркость: {effect[1]},' \
                           f' яркость {effect[2]}, дополнительно: {effect[3]}, реацкия на звук: {effect[4]},' \
                           f' мин сигнал: {effect[5]}, макс сигнал: {effect[6]}, скорость {effect[7]},' \
                           f' палитра: {TYPE_PALLETES[effect[8]]}, масштаб: {effect[9]}, из центра: {effect[10]},'\
                           f' цвет: {effect[11]}, случайный: {effect[12]}'

        return msg

    def __now_date(self):
        day = datetime.fromtimestamp(int(time() + 1))
        return f'{day.isoweekday()},{day.hour},{day.minute},{day.second}'

    def __date_proc(self, delay, *date):
        if len(date) == 0:
            return f'now+{delay}' if delay else 'now'
        return date