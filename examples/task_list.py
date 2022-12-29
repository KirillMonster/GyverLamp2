from GyverLamp2 import Lamp

lamp = Lamp(enable_task_list=True)

lamp.max_brightness()

while True:
    lamp.random_effects(delay=5000)

