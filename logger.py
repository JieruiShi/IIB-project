import numpy as np
import pickle
import time
from datetime import date
import matplotlib.pyplot as plt
from nidaqmx.constants import TerminalConfiguration
from nidaqmx.task import Task
import keyboard

plot_info = {
    "pH": True,
    "conductance": True,
    "temperature": True,
    "temperature2": False,
    "no": 7,
    "date": date.today().strftime("%m%d")
}

class Logger(object):

    def __init__(self):
        self.ai_task = Task("ai_task")
        self.ai_task.ai_channels.add_ai_voltage_chan("Dev2/ai0", terminal_config=TerminalConfiguration.RSE) # conductance
        self.ai_task.ai_channels.add_ai_voltage_chan("Dev2/ai1", terminal_config=TerminalConfiguration.RSE) # temperature center
        self.ai_task.ai_channels.add_ai_voltage_chan("Dev2/ai2", terminal_config=TerminalConfiguration.RSE) # pH input
        self.ai_task.ai_channels.add_ai_voltage_chan("Dev2/ai3", terminal_config=TerminalConfiguration.RSE) # 5V
        self.ai_task.ai_channels.add_ai_voltage_chan("Dev2/ai8", terminal_config=TerminalConfiguration.RSE) # temperature 2 side
        self.ai_task.ai_channels.add_ai_voltage_chan("Dev2/ai9", terminal_config=TerminalConfiguration.RSE) # pH V_ref

        time.sleep(2)

        self.dataTrim = [plot_info["conductance"], plot_info["temperature"], plot_info["pH"], True, plot_info["temperature2"], plot_info["pH"]]
        self.savePath = "Data/" + plot_info["date"] + "-" + str(plot_info["no"]) + "--pH"*plot_info["pH"] + "--G"*plot_info["conductance"] + "--T"*plot_info["temperature"] + "x2"*plot_info["temperature2"]
        self.dataBuffer = []

        try:
            with open(self.savePath + '.pickle', 'rb') as handle:
                if input("resume previous log? Y/n") == "Y":
                    plot_info_loaded = pickle.load(handle)
                    self.startTime = plot_info_loaded["startTime"]
                else:
                    exit()
        except:
            self.startTime = time.time()
            self.saveRecordDetails()

    def saveRecordDetails(self):
        plot_info["startTime"] = self.startTime
        with open(self.savePath + '.pickle', 'wb') as handle:
            pickle.dump(plot_info, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def saveBufferToFile(self, writeLine = 100):
        """When the buffer reaches 1000 records or cooking terminates, call this function, and writes the first 1000 lines in dataBuffer into output file, in npy format"""
        if len(self.dataBuffer) < writeLine:
            toBuffer = self.dataBuffer
            self.dataBuffer = []
        else:
            toBuffer = self.dataBuffer[:writeLine]
            self.dataBuffer = self.dataBuffer[writeLine:] # removes first 1000/writeLine worth data from the buffer

        appendData = np.array(toBuffer, dtype=float)

        try:
            loadedData = np.load("{}.npy".format(self.savePath))
            appendedData = np.append(loadedData,appendData, axis = 0)
        except:
            appendedData = appendData

        np.save(self.savePath, appendedData)
        print("successfully saved data, file currently holds {} records".format(str(len(appendedData))))

    def step(self):
        data = self.ai_task.read()
        dataToSave = [time.time()-self.startTime] + [data[index]*obj for index,obj in enumerate(self.dataTrim)] #Make values zero if the recorded are not relevant
        self.dataBuffer.append(dataToSave)
        print(dataToSave)

        if len(self.dataBuffer) > 100:
            self.saveBufferToFile()




if __name__ == '__main__':
    logger = Logger()
    while True:
        logger.step()
        time.sleep(0.1)
        if keyboard.is_pressed("q"):
            logger.saveBufferToFile()
            break


