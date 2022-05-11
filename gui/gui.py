import tkinter as tk
import tkinter.font as tkFont
import time
import random

import sys, os
import time
import smbus

#CONFIG PATH
lib_path = '/usr/etc/scada'
config_path = '/usr/etc/scada/config'


sys.path.append(lib_path)
sys.path.append(config_path)

from drivers import driver
import config
#import redis
import utils
from utils import rtc_setup
from utils import imu_setup





class App:
    def __init__(self, root):
        
        ##########Declariing i2C Bus##############
        #bus = smbus.SMBus(3) 
        bus = smbus.SMBus(3)



        ###Local Dictionary for Sensor Period Count####
        self.SensorList = config.get('Sensors')
        last_sampled = {}
        sample_period = {}

        for key in config.get('Sensors'):
            sample_period[key] = self.SensorList.get(key).get('sample_period')
            last_sampled[key] = time.time()
        
        #setting title
        root.title("Simple SCADA")
        self.fontSize=20
        #setting window size
        fontSize=30
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        width=screenwidth
        height=screenheight
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=True, height=True)


        GLabel_829=tk.Label(root)
        ft = tkFont.Font(family='Times',size=28)
        GLabel_829["font"] = ft
        GLabel_829["fg"] = "#ff5722"
        GLabel_829["justify"] = "center"
        GLabel_829["text"] = "Simple SCADA UI"
        GLabel_829.place(x=((screenwidth) / 2)-(295/2),y=30,width=295,height=50)

#initialize the list of sensor  to display here 
        self.template(80,210,"Linear Acceleration X","")
        self.template(80,300,"Linear Acceleration Y","")
        self.template(80,410,"Linear Accekerarion Z","")

    def template(self,x_in,y_in,data_title,data_unit):
            title_width=350
            data_width=150
            unit_width=100
            sensor_title=tk.Label(root)
            ft = tkFont.Font(family='Times',size=self.fontSize)
            sensor_title["font"] = ft
            sensor_title["fg"] = "#333333"
            sensor_title["justify"] = "center"
            sensor_title["text"] = data_title
            sensor_title.place(x=x_in,y=y_in,width=title_width,height=56)


            sensor_unit=tk.Label(root)
            ft = tkFont.Font(family='Times',size=self.fontSize)
            sensor_unit["font"] = ft
            sensor_unit["fg"] = "#01aaed"
            sensor_unit["justify"] = "center"
            sensor_unit["text"] = data_unit
            sensor_unit.place(x=x_in+title_width+20+data_width+20,y=y_in,width=unit_width,height=56)


    def data_template(self,x_in,y_in,data_title,data_val):
            title_width=350
            data_width=150
            sensor_data=tk.Label(root)
            ft = tkFont.Font(family='Times',size=self.fontSize)
            sensor_data["font"] = ft
            sensor_data["fg"] = "#01aaed"
            sensor_data["justify"] = "center"
            sensor_data["text"] = data_val
            sensor_data.place(x=x_in+title_width+20,y=y_in,width=data_width,height=56) 

    def data_read(self,title):
            temp=driver.read(title)
            if(isinstance(temp,int)):
                    return str(round(temp,5))
            else:
                    return "data"

    def update(self):
#set the update  data here 
        self.data_template(80,210,"Linear Acceleration X",data_read("linacc_x"),5)
        self.data_template(80,300,"Linear Acceleration Y",data_read("linacc_y"),5)
        self.data_template(80,410,"Linear Acceleration Z",data_read("linacc_z"),5)
        root.after(500, self.update) # run itself again after 100 ms



if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    app.update()
    root.mainloop()
