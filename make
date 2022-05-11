#!/bin/bash


#############################################################################################
## Company: FSAE Lafayette College                                                               
## Engineers: Tafita Rakotozandry                                    
## Last Updated : 05/24/2022                   
## Project Name: SCADA FSAE 2022                                 
## Module Name: make                                               
## Description: This file is the make file for the scada system. 
##              This file does not install anything, but it does enable execution of certain
##              files in the system before copying all files down to a defined, arbitrary 
##              folder (either /usr/etc or /usr/bin or /etc/systemd) so that they can be run
##              by system level commands. This file must be run after modifying the Git
##              repository folder for changes to apply.
##              In to run this file the user must run sudo bash make in the terminal from 
##              the SCADA_2021 folder.                 
#############################################################################################

# # make sure can bus is set up for testing
modprobe can
# ip link set can0 down
# ip link set can0 up type can bitrate 125000

# # make sure virtual can bus is set up for testing
# modprobe vcan
# ip link add dev vcan0 type vcan
# ip link set up vcan0

# make binary files executable, these are the looping files run by our services
chmod +x install
chmod +x make
chmod +x scada
chmod +x sorter/sorter.py
chmod +x gui/gui.py


# copy binary files to /usr/bin
cp scada /usr/bin/simple-scada

#Copying down i2c sorter 
# cp drivers/i2c_sorter.py /usr/bin/i2c_sorter.py
# #copying down can sorter
# cp drivers/can_driver.py /usr/bin/can_driver.py

cp sorter/sorter.py /usr/bin/scada_sorter.py
cp gui/gui.py /usr/bin/scada_gui.py
cp rtc_setup.py /usr/bin/scadartc_setup.py

# create a workspace and copy important files into it
mkdir -p /usr/etc/scada-gui
rm -rf /usr/etc/scada/config
cp -r config /usr/etc/scada/config
cp ./install /usr/etc/scada
cp ./make /usr/etc/scada
rm -rf /usr/etc/scada/gui
cp -r GUI /usr/etc/scada/gui
rm -rf /usr/etc/scada/drivers
cp -r drivers /usr/etc/scada/drivers

echo 'MAKE COMPLETE'

# /usr/bin/scada_gui.py