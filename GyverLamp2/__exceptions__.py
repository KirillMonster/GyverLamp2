class GyverLamp2Error(Exception):
    pass


class CountEffectsNotInRangeError(GyverLamp2Error):
    def __init__(self):
        super().__init__('Количество эффектов должно быть в диапозоне от 0 до 26')


class SyncError(GyverLamp2Error):
    def __init__(self):
        super().__init__('Вышло время получения ответа. Проверьте что лампа включена, \nвы находитесь в одной сети и у '
                         'лампы стоит модифицированная прошивка - \n'
                         'https://github.com/KirillMonster/GyverLamp2#sync-system')


class TimeOutError(GyverLamp2Error):
    def __init__(self):
        super().__init__('Вышло время получения ответа')


class IncorrectDataError(GyverLamp2Error):
    def __init__(self, address, data):
        super().__init__(f'Были получены неверные данные от клиента ({address[0]}:{address[1]}): {data}')
