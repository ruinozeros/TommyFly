import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import serial

fig, ax = plt.subplots()

max_x = 5
max_rand = 10

length = 100

ar = [0]*length

x = np.arange(0, length)
ax.set_ylim(-2,3)
line1, = ax.plot(x, color='g', label="sensor data")
line2, = ax.plot(x, color='r', label="average", linestyle='--')
line3, = ax.plot(x, color='y', label="average points")

dd_ar = [0]*length

plt.grid(b=True, which='both', color='0.65', linestyle='-')

ser = serial.Serial(
        port='/dev/ttyUSB0',\
        baudrate=9600,\
        parity=serial.PARITY_NONE,\
        stopbits=serial.STOPBITS_ONE,\
        bytesize=serial.EIGHTBITS,\
            timeout=0)

def init():  # give a clean slate to start
    line1.set_ydata([np.nan] * len(x))
    line2.set_ydata([np.nan] * len(x))
    line3.set_ydata([np.nan] * len(x))
    
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('Variometer')
    plt.ylabel('Height (m)')
    plt.xlabel('Time (ms)')
    ax.legend()
    return [line1,line2,line3]

def animate(i):  # update the y values (every 1000ms)
    
    
    l = ser.readline()
    str = l.decode("utf-8").rstrip()
    if len(str):
        value = float(str)
    else:
        return [line1,line2]
        
    ar.append(value)
    
    # derivation
#    dd_ar.append(value - dd_ar[-1])
#    np_dd = np.array(dd_ar[-length:])
    
    # last data points
    np_ar = np.array(ar[-length:])
    
    # average
    avg_range = 50
    np_sum = np.sum(np_ar[-avg_range:])
    np_avg = np.array([np_sum / avg_range] * len(x))
    
    dd_ar.append(np_sum / avg_range)
    np_dd = np.array(dd_ar[-length:])
    

    
    line1.set_ydata(np_ar)
    line2.set_ydata(np_avg)
    line3.set_ydata(np_dd)
    #line.set_ydata([1] * length)
    return [line1,line2,line3]

ani = animation.FuncAnimation(
    fig, animate, init_func=init, interval=10, blit=True, save_count=10)

plt.show()