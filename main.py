# main.py -- put your code here
import pyb

led3 = pyb.LED(3)
led4 = pyb.LED(4)
led4.on()
led3.on()

for j in range(5):
    pyb.delay(100)
    led4.toggle()
    led3.toggle()

i = 1
led4.on()
led3.off()
while True:
    output_dict = {
        'humidity': 43,
        'temperature': 22,
        'dew_point': 24,
        'row': i,
    }
    led4.toggle()
    led3.toggle()
    print("{row},{humidity},{temperature},{dew_point}".format(**output_dict))
    i += 1
    pyb.delay(1000)
