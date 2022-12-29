from GyverLamp2.gcolor import *
from GyverLamp2 import *

lamp = Lamp(enable_task_list=True)


lamp.palette(chsv=rgb2chsv(*hex2rgb('FFC0CB')))
