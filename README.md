<style>
img {
	width: 100%;	
}

</style>

# Simple SCADA - User Manual

<!-- ## User Manual -->

**Authors: Tafita Rakotozandry**

---

# Introduction and Purpose

SCADA is an acronym for Supervisory Control And Data Acquisition. It is a term borrowed from industrial control applications, where a single server is often used to oversee large industrial plants such as oil refineries and assembly lines. In general, SCADA systems have three functions, they acquire data from the network of sensors connected to the plant, send control signals to the plant's other subsystems, and provide an interface for humans to interact with the plant by viewing aggregated data and issuing commands.

The Lafayette FSAE team has been working to develop a SCADA system that can be fully integrated into its electric vehicle, with the goal of performing all of the above three functions both during normal operation and throughout the various testing and maintenance procedures that it will undergo. 

There goal of the Simple SCADA is to help the future team that would work on the current SCADA to understadnd the basic of it. As the software gets more complex with different subsystems. The Simple SCADA would give a good introduction to the current system.

<div style="page-break-after: always"></div>

# Installation
To install the software, open the command line and run the following command: 

```bash
git clone git@github.com:Lafayette-FSAE/Simple-SCADA.git
cd Simple-SCADA
sudo bash install
```

<div style="page-break-after: always"></div>

# Design Overview

## CAN Network

The existence of a SCADA system implies a network. There must be communication taking place between SCADA and the other subsystems for it to successfully perform any of its responsibilities. There are a number of network protocols to choose from, but the de facto standard for automotive use is CAN (Controller Area Network) and so that is what is used in the Lafayette FSAE Car.

A good explanation of CAN can be found here:

[https://www.csselectronics.com/screen/page/simple-intro-to-can-bus/language/en](https://www.csselectronics.com/screen/page/simple-intro-to-can-bus/language/en)

At the time of writing, the CAN Network contains between 6 and 7 nodes, depending whether an external pc is needed to configure and operate the motor controller. They are:

- Motor Controller
- SCADA
- Battery Packs (1 and 2)
- TSI
- DashMan
- External Configuration PC

### CANOpen

CAN is a very low level protocol. It defines a way for a node to broadcast up to 8 bytes of data and an ID, but very few of the other things needed to perform sophisticated network operations. For this, a higher level protocol needs to be defined on top of CAN, and currently there are several competing standards. These have been described as the equivalent of something like http to the tcp/ip stack, adding an additional layer of abstraction for easier use.

While it is not the most popular, the Lafayette FSAE team has chosen the CANOpen Standard for its vehicle in order to match that of the already purchased Motor Controller, which includes a rich set of CANOpen based tools.

CANOpen can also be thought of as a subset of CAN, meaning if a node is added to the network that does not comply with the CANOpen standard, the behavior of the other nodes is undefined. For this reason, it is very important that every node added to the network, even if it does not intend to make use of the full set of CANOpen features, at least comply with a subset of the protocol.

Here are some good resources for learning more about the protocol:

[https://www.can-cia.org/canopen/](https://www.can-cia.org/canopen/)

[https://www.youtube.com/watch?v=DlbkWryzJqg](https://www.youtube.com/watch?v=DlbkWryzJqg)

As a supplement to these resources, a brief description of CANOpen is also provided here:

CANOpen can best be thought of as the sum of several communication protocols, coupled with some defined behavior for each node. Each has a different purpose, name, and associate acronym. A node can choose to implement any subset of these protocols and behaviors.

The protocol being used is determined by the function code, which is transmitted in the id part of the CAN frame. In the CANOpen standard, the message id is formed by the sum of the function code and the node id, this is to take advantage of the CAN behavior of prioritizing messages with lower ids, so protocols that are more important are given lower function codes.

**NMT**

NMT stands for Network Management. It is a master slave protocol used to manage the state of the various nodes on the bus. Any node which wishes to interact with the NMT protocol as a slave must implement the following finite state machine. 

![](https://i0.wp.com/www.byteme.org.uk/wp-content/uploads/2015/11/canopennmtstate3.png)

This determines the functional state of the node. CAN packets can be sent by the master to move the node along this state machine, allowing it to perform actions, like soft resets, emergency stops, and boot ups.

**SDO and OD**

Any node which wishes to expose internal data to the CAN network must implement a data structure know as an Object Dictionary, or OD. The Object Dictionary maps each piece of data to an address consisting of a two byte index followed by a one byte subindex. Certain addresses are reserved for general data like device name and error registers. The manufacturer of a node can publish information about the Object Dictionary in a file called an Electronic Data Sheet, or EDS, which takes the form of an INI file that is both human and machine readable.

Any node on the network can access information from the Object Dictionary of another node using the Service Data Object, or SDO protocol. The SDO packet consists of a byte of metadata followed by a three byte address and 4 bytes of data. This can be used to both read and write data, and can be used to control node behavior in real time. This is the technique used in the dyno room to spin the motor and query it for data like temperature and angular velocity.

**PDO**

Process Data Objects are a protocol meant to supplement SDO's by providing a data transfer method with a higher data rate and less overhead. They are meant to be the standard for high volume inter node data transfer during nominal operation of the network, and have the added benefit of being much simpler to implement than SDO. A node that chooses to implement only the smallest possible subset of the CANOpen protocol will most likely implement a PDO. 

PDO's work on a producer / consumer, or broadcast / subscribe model of communication, where one or more CAN packets are sent at regular intervals, each containing 8 bytes of data with a structure agreed upon beforehand. Any node on the network can subscribe to these packets and update their behavior accordingly.Both the broadcast and subscribe behavior (called the Transmit PDO and Receive PDO respectively) can be configured by dedicated addresses in the Object Dictionary.
