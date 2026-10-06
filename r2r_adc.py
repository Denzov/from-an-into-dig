import RPi.GPIO as GPIO
import time

class R2R_ADC:
    def __init__(self, dynamic_range, compare_time = 0.001, verbose = False):
        self.dynamic_range = dynamic_range
        self.verbose = verbose
        self.compare_time = compare_time

        self.bits_gpio = [26, 20, 19, 16, 13, 12, 25, 11][::-1]
        self.comp_gpio = 21

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.bits_gpio, GPIO.OUT, initial = 0)
        GPIO.setup(self.comp_gpio, GPIO.IN)

    def deinit(self):
        GPIO.output(self.bits_gpio, 0)
        GPIO.cleanup()

    def number_to_dac(self, cnt):
        for i in range(len(self.bits_gpio)):
            led_st = int(bool(cnt & (0b1 << i)))
            GPIO.output(self.bits_gpio[i], led_st)

    def sequential_counting_adc(self):
        last = 0
        for i in range(256):
            last = i
            self.number_to_dac(i)
            time.sleep(self.compare_time)
            if(GPIO.input(self.comp_gpio)):
                break
        return last

    def successive_approximation_adc(self):
        step = 255 // 2
        base = 255

        base -= step
        while step > 0:
            self.number_to_dac(base)
            time.sleep(self.compare_time)
            state = GPIO.input(self.comp_gpio)

            step //= 2
            if(state):
                base -= step
            else:
                base += step
        
        return base
    
    def get_sc_voltage(self):
        number = self.sequential_counting_adc()
        return number / 255 * self.dynamic_range
    def get_sar_voltage(self):
        number = self.successive_approximation_adc()
        return number / 255 * self.dynamic_range

if __name__ == "__main__":
    try:
        adc = R2R_ADC(3.294)
        
        while True:
            try:
                print(adc.get_sc_voltage())
                # time.sleep(0.5)

            except ValueError:
                print("Вы ввели не число. Попробуйте ещё раз\n")

    finally:
        adc.deinit()


    