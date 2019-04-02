def run():
    from si7021 import Si7021
    sensor = Si7021()
    print(sensor.readTemp(), sensor.readRH())
