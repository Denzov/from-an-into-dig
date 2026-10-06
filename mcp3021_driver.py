import time
import smbus 
import r2r_adc as r2r

class MCP3021:
    def __init__(self, dynamic_range, verbose = False):
        self.bus = smbus.SMBus(1)
        self.dynamic_range = dynamic_range
        self.address = 0x4D
        self.verbose = verbose

    def deinit(self):
        self.bus.close()

    def get_number(self):
        data = self.bus.read_word_data(self.address, 0)

        lower_data_byte = data >> 8
        upper_data_byte = data & 0xFF

        number = (upper_data_byte << 6) | (lower_data_byte >> 2)

        return number
    
    def get_voltage(self):
        return self.get_number() / 4095 * self.dynamic_range

if __name__ == "__main__":
    try:
        adc1 = MCP3021(5)
        adc2 = r2r.R2R_ADC(3.155, compare_time=0.0001)
        
        while True:
            try:
                print(adc1.get_voltage())
                time.sleep(1)

            except ValueError:
                print("Вы ввели не число. Попробуйте ещё раз\n")

    finally:
        adc.deinit()