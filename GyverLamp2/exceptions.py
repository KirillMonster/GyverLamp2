class GyverLamp2Error(Exception):
    """ Basic exception when working with the Club House """
    pass


class CountEffectsNotInRangeError(GyverLamp2Error):
    def __init__(self):
        super().__init__('Количество эффектов должно быть в диапозоне 0 и 26')


class SyncError(GyverLamp2Error):
    def __init__(self):
        super().__init__('Ошибка синхронизации лампы. Проверьте что вы находитесь в одной сети и у лампы стоит '
                         'модифицированная прошивка https://github.com/AlexGyver/GyverLamp#chapter-0')
