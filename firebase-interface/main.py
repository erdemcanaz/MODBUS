import datetime,time
import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate("firebase_credentials.json")
firebase_admin.initialize_app(cred, {'databaseURL': "https://iot-project-2b9fb-default-rtdb.europe-west1.firebasedatabase.app/"})


import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from collections import deque
import easygui

# define function to update data
def update_data(frame):
    # get data
    for i, var_name in enumerate(selected_vars):
        var_data[var_name].popleft()
        var_data[var_name].append(var_values[var_name])
        # clear axis
        axs[i].cla()
        # plot data
        axs[i].plot(var_data[var_name])
        axs[i].scatter(len(var_data[var_name])-1, var_data[var_name][-1])
        axs[i].text(len(var_data[var_name])-1, var_data[var_name][-1]+2, "{}".format(var_data[var_name][-1]))
        # set y-axis limits based on the min and max values of the data
        var_min = np.min(var_data[var_name])
        var_max = np.max(var_data[var_name])
        var_range = var_max - var_min
        ylim_min = var_min - var_range*0.1  # add 10% padding to the y-axis limits
        ylim_max = var_max + var_range*0.1
        axs[i].set_ylim(ylim_min, ylim_max)
        axs[i].set_title(var_name)

# define variables to plot and start collections with zeros
var_values = {'BESS-voltage': 53.1, 'calculated-BESS-current': -0.1318267419962335, 
              'calculated-BESS-power': -7.0, 'grid-power': 0.0, 'humidity': 29.88, 
              'load-power': 9.0, 'pv-power': 0.0, 'temperature': 24.19}


var_names = list(var_values.keys())

# create a dialog box to select variables to plot
selected_vars = easygui.multchoicebox(msg='Select variables to plot', title='Plot Variables', choices=var_names)

# get number of data points as numeric input
n_data_points_str = easygui.enterbox(msg='Enter number of data points', title='Data Points')
n_data_points = int(n_data_points_str)
var_data = {var_name: deque(np.zeros(n_data_points)) for var_name in var_names}

# define and adjust figure
fig, axs = plt.subplots(nrows=len(selected_vars), figsize=(12,6*len(selected_vars)), facecolor='#DEDEDE')
if len(selected_vars) == 1:
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
            if key in selected_vars:
                var_values[key] = value

        # start animation
        ani.event_source.start()      
        plt.pause(1)
        ani.event_source.stop()
        


    except KeyboardInterrupt:
        break
