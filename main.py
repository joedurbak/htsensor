# main.py -- put your code here
from si7021 import Si7021
import math
import pyb

max_temp_rise_per_sec = 1  # degrees Celsius/second
coolant_temp_drop = 10


def get_frost_point_c(t_air_c, dew_point_c):
    """Compute the frost point in degrees Celsius
    :param t_air_c: current ambient temperature in degrees Celsius
    :type t_air_c: float
    :param dew_point_c: current dew point in degrees Celsius
    :type dew_point_c: float
    :return: the frost point in degrees Celsius
    :rtype: float
    """
    dew_point_k = 273.15 + dew_point_c
    t_air_k = 273.15 + t_air_c
    frost_point_k = dew_point_k - t_air_k + 2671.02 / ((2954.61 / t_air_k) + 2.193665 * math.log(t_air_k) - 13.3448)
    return frost_point_k - 273.15


def get_dew_point_c(t_air_c, rel_humidity):
    """Compute the dew point in degrees Celsius
    :param t_air_c: current ambient temperature in degrees Celsius
    :type t_air_c: float
    :param rel_humidity: relative humidity in %
    :type rel_humidity: float
    :return: the dew point in degrees Celsius
    :rtype: float
    """
    A = 17.27
    B = 237.7
    alpha = ((A * t_air_c) / (B + t_air_c)) + math.log(rel_humidity/100.0)
    return (B * alpha) / (A - alpha)


led3 = pyb.LED(3)
led4 = pyb.LED(4)

# flashing LEDs together at 10 Hz to confirm program start
for j in range(20):
    pyb.delay(100)
    led4.toggle()
    led3.toggle()

sensor = Si7021()
i = 1
led4.on()
led3.off()

# flashing LEDs alternating at 5 Hz to confirm that sensor object was creadted successfully
for j in range(10):
    pyb.delay(200)
    led4.toggle()
    led3.toggle()

previous_temp = 1000

while True:
    humidity, temp = sensor.readRH(), sensor.readTemp()
    # humidity, temp = sensor.relative_humidity, sensor.temperature
    # humidity, temp = (43, 22)
    dew_point = get_dew_point_c(temp, humidity)
    frost_point = get_frost_point_c(temp, dew_point)

    output_dict = {
        'row': i,
        'humidity': humidity,
        'temperature': temp,
        'dew_point': dew_point,
        'frost_point': frost_point,
        'temp_change_flag': int((temp-previous_temp) > max_temp_rise_per_sec),
        'dew_flag': int(dew_point > (temp-coolant_temp_drop)),
        'frost_flag': int(frost_point > (temp-coolant_temp_drop)),
    }
    # flashing LEDs alternately at 1 Hz to confirm new row was calculated
    led4.toggle()
    led3.toggle()
    print(
        "{row},{humidity},{temperature},{dew_point},{frost_point},{temp_change_flag},{dew_flag},{frost_flag}".format(
            **output_dict
        )
    )
    previous_temp = temp
    i += 1
    pyb.delay(1000)
