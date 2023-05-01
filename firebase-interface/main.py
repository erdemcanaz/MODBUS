import datetime
import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate("firebase_credentials.json")
firebase_admin.initialize_app(cred, {'databaseURL': "https://iot-project-2b9fb-default-rtdb.europe-west1.firebasedatabase.app/"})


import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from collections import deque
import psutil

# define function to update data
def update_data(frame):
    # get data
    for i, var_name in enumerate(var_names):
        var_data[var_name].popleft()
        var_data[var_name].append(var_values[var_name])
        # clear axis
        axs[i].cla()
        # plot data
        axs[i].plot(var_data[var_name])
        axs[i].scatter(len(var_data[var_name])-1, var_data[var_name][-1])
        axs[i].text(len(var_data[var_name])-1, var_data[var_name][-1]+2, "{}".format(var_data[var_name][-1]))
        axs[i].set_ylim(0,100)
        axs[i].set_title(var_name)

# define variables to plot and start collections with zeros
var_values = {'BESS-voltage': 53.1, 'calculated-BESS-current': -0.1318267419962335, 
              'calculated-BESS-power': -7.0, 'grid-power': 0.0, 'humidity': 29.88, 
              'load-power': 9.0, 'pv-power': 0.0, 'temperature': 24.19}


var_names = list(var_values.keys())
var_data = {var_name: deque(np.zeros(100)) for var_name in var_names}

# define and adjust figure
fig, axs = plt.subplots(nrows=len(var_names), figsize=(12,6*len(var_names)), facecolor='#DEDEDE')
if len(var_names) == 1:
    axs = [axs]
for ax in axs:
    ax.set_facecolor('#DEDEDE')

# define animation
ani = FuncAnimation(fig, update_data, interval=1000)

# start loop to continuously update the plot with new data
while True:
    try:
        # update var_values
        ref = db.reference("monibostan_ODTU")
        data = ref.get()
        for key, value in data.items():
            if key in var_names:
                var_values[key] = value

       
        # start animation
        ani.event_source.start()
        plt.pause(5)
        ani.event_source.stop()
    except KeyboardInterrupt:
        break
