#######################################################################
# plot_sensor_data.py
#
#######################################################################

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import serial

fig, ax = plt.subplots()

# serial settings
serial_port = "/dev/ttyUSB1"
serial_bdrate = 9600

# set view range of y axis (meters)
ax.set_ylim(-2,3)

# set view and calculation range of x axis
length = 100

# allocate buffer
ar_sensor      = [0]*length
ar_avg         = [0]*length
ar_grad        = [0]*length


x = np.arange(0, length)
line_sensor, = ax.plot(x, color='g', label="sensor data")
line_avg, = ax.plot(x, color='r', label="moving average", linestyle='--')
line_grad, = ax.plot(x, color='y', label="gradient")


plt.grid(b=True, which='both', color='0.65', linestyle='-')


ser = serial.Serial(
        port=serial_port,\
        baudrate=serial_bdrate,\
        parity=serial.PARITY_NONE,\
        stopbits=serial.STOPBITS_ONE,\
        bytesize=serial.EIGHTBITS,\
            timeout=0)

def init():  # give a clean slate to start
    line_sensor.set_ydata([np.nan] * len(x))
    line_avg.set_ydata([np.nan] * len(x))
    line_grad.set_ydata([np.nan] * len(x))
    
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('Variometer')
    plt.ylabel('Height (m)')
    plt.xlabel('Time (ms)')
    ax.legend()
    return [line_sensor, line_avg, line_grad]

class mvg_avg_old:
    def __init__(self, avg):
        self.avg = avg
        
avg_old = mvg_avg_old(0)

def animate(i):
    l = ser.readline()
    try:
        flt = l.decode("utf-8").rstrip()
        sensor_float = float(flt)
    except (UnicodeDecodeError, ValueError):
        return [line_sensor, line_avg, line_grad]
        
    ar_sensor.append(sensor_float)
        
    # sensor data
    np_sensor = np.array(ar_sensor[-length:])
    
    # moving average
    avg_window = 100
    mov_avg = np.sum(np_sensor[-avg_window:]) / avg_window
    ar_avg.append(mov_avg)
    np_avg = np.array(ar_avg[-length:])
    
    ravg = old_avg + (n-1)/n + sensor_float / n
    
    # draw lines
    line_sensor.set_ydata(np_sensor)
    line_avg.set_ydata(np_avg)
    
    # vertical speed
    if not i % 100:
        print(str(round(mov_avg - avg_old.avg, 2)) + "m/s")
        avg_old.avg = mov_avg
    
    return [line_sensor, line_avg, line_grad]



ani = animation.FuncAnimation(
    fig, animate, init_func=init, interval=10, blit=True, save_count=10)

plt.show()