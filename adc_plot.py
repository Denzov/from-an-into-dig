
import r2r_adc as r2r
import matplotlib.pyplot as plt
import time

voltage_values = []
time_values = []
duration = 3.0

time0 = time.time()

delta = []

def plot_sampling_period_hist(time):
    plt.figure(figsize=(10,6))
    plt.hist(time)
    plt.xlim(0, 0.06)

    plt.title("Распределение периодов дискретизации")
    plt.xlabel("Период измерения")
    plt.ylabel("Количество измерений")

    plt.grid(True)

    plt.show()



if __name__ == "__main__":
    try:
        adc = r2r.R2R_ADC(3.155, compare_time=0.0001)
        
        while time.time() - time0 < duration:
            t = time.time() - time0

            time_values.append(t)
            voltage_values.append(adc.get_sc_voltage())

            t_after = time.time() - time0

            deltav = t_after - t

            delta.append(deltav)
        
        plt.figure(figsize=(10,6))
        plt.plot(time_values, voltage_values)

        plot_sampling_period_hist(delta)
        plt.show()

    except ValueError:
        print("Вы ввели не число. Попробуйте ещё раз\n")

    finally:
        adc.deinit()