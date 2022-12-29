class GyverLamp2Error(Exception):
    pass


class CountEffectsNotInRangeError(GyverLamp2Error):
    def __init__(self):
        super().__init__('Количество эффектов должно быть в диапозоне от 0 до 26')


class SyncError(GyverLamp2Error):
    def __init__(self):
        super().__init__('Ошибка синхронизации лампы. Проверьте что вы находитесь в одной сети и у лампы стоит '
                         'модифицированная прошивка - https://github.com/KirillMonster/GyverLamp2#sync-system')
