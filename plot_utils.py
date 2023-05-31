from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import numpy as np
import math

TITLE_FONT = {'fontname': 'Arial', 'fontsize': 12, 'fontweight': 'normal'}
# plt.title('Plot Title', **TITLE_FONT)

def load_raw_data(fileName):
    data = np.load(fileName)
    time = data[:, 0]
    G = data[:,1]
    RTD1 = data[:, 2]
    pH = data[:,3]
    VCC = data[:,4]
    RTD2 = data[:, 5]
    Vref = data[:,6]
    
    return time, G, pH, RTD1, RTD2, VCC, Vref, data

def find_segment(G, G_threshold = 4.7, padding = 2):
    G_up = True
    start = 0
    end = 0
    segments = []

    for index, datum in enumerate(G):
        if G_up and datum < G_threshold:
            G_up = False
            start = index + padding

        elif not G_up and datum > G_threshold:
            G_up = True
            end = index - padding
            segments.append((start, end))
            
    return segments

def find_segment2(start_t = 15, t_gap = 30, t_window = 15, t_end = 750):
    segments = []
    while start_t + t_window < t_end:
        segments.append((start_t, start_t + t_window))
        start_t += t_gap
    
    return segments
    

def calculate_data_points(data, segments, RTD_constant = 0.27, T_backwards = 5, G_forwards = 5):
    time = data[:, 0]
    G = data[:,1]
    RTD1 = data[:, 2]
    pH = data[:,3]
    VCC = data[:,4]
    Vref = data[:,6]
    with np.errstate(divide='ignore', invalid='ignore'):
        T_value = np.log(RTD1/(VCC - RTD1)*1.1)/np.log(1 + RTD_constant/100)
        G_value = (VCC - G) / (G *100) * 1000
        pH_value = (pH - Vref)/-0.058 + 7
        
    t_point = np.array([np.average(time[segment[0]:segment[1]]) for segment in segments])
    
    T_point = np.array([np.average(T_value[segment[1] - T_backwards:segment[1]]) for segment in segments])
    G_point = np.array([np.average(G_value[segment[0]:segment[0] + G_forwards]) for segment in segments])
    pH_point = np.array([np.average(pH_value[segment[0]:segment[1]]) for segment in segments])
    if T_backwards == -1:
        T_point = np.array([np.average(T_value[segment[0]:segment[1]]) for segment in segments])
    
    if G_forwards == -1:
        G_point = np.array([np.average(G_value[segment[0]:segment[1]]) for segment in segments])
    
    return t_point, T_point, G_point, pH_point


def analyse_and_plot(fileName, showPlot = True, G_threshold = 4.7, RTD_constant = 0.27, T_backwards = 5, G_forwards = 5):
    time, G, pH, RTD1, RTD2, VCC, Vref, data = load_raw_data(fileName)
    segments = find_segment(G, G_threshold)
    t_point, T_point, G_point, pH_point = calculate_data_points(data, segments, RTD_constant, T_backwards = T_backwards, G_forwards = G_forwards)
    
    if showPlot:
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18,4))
        ax1.plot(t_point, T_point)
        ax1.set_title("Temperature")
        ax2.plot(t_point, G_point)
        ax2.set_title("Conductance")
        ax3.plot(t_point, pH_point)
        ax3.set_title("pH")
    
    return t_point, T_point, G_point, pH_point
    
    
    

    