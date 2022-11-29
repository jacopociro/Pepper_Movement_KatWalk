# Pepper_Movement_KatWalk
This repository contains the scripts to handle pepper movement for my Master Thesis.
# Additional Material
- [Unreal Projects](https://unigeit-my.sharepoint.com/:f:/g/personal/s5050695_studenti_unige_it/Err9H7kpQHlItJdDqEp7jvUBUbU8oZARRXWF8uINtnsbSA?e=RcjCUH). If the project is not available contact me.
- [Zed Camera Modified Repository](https://github.com/jacopociro/ZED-Oculus_Rift-IP)
# Prerequisites
To run these tests you need various applications, such as the Oculus app, KATIO,
Unreal Engine 4.20 with the KatWalk, the UDP and the Virtual Reality plugins,
Python2 and Steam with the SteamVR plugin.
You also need the various SDK, such as the ZED SDK, Pepper Python SDK and
the Oculus Virtual Reality(OVR) for both C plus plus and python, which uses a
wrapper.
Follow the instruction on the ZED camera Modified Repository to see how to build the applications.
# Experiment Procedure
This procedure is also explained on my [Master Thesis](https://unigeit-my.sharepoint.com/:b:/g/personal/s5050695_studenti_unige_it/EfIUiSdHC8VHr48WIcW8IxgBRkXPpD-oef2bUbKahLF1Yw?e=w8INK8), contact me for the PDF file if the the file is not available.

1. Mount the ZED mini stereocamera on Pepper's head in a stable way.
2. Start up the KatWalk Mini by connecting the cord to the power socket.
3. Turn the KatWalk Mini a full rotation.
4. Connect the KatWalk's USB cable to the computer. Be careful, to work properly the computer's USB socket must be at least a 2.0 type.
5. Turn the KatWalk Mini a full rotation in th opposite sense as before.
6. Connect the Oculus Rift S to the computer. You have two cables, a USB cable and an HDMI cable. The USB cable must be connected to a 3.0 USB port.
7. Now, on your computer start up the Oculus Application and check your device is properly connected. 
8. Start the KATIO application and press on "Start SteamVR". The treadmill should be ready to use now.
9. Step on the treadmill and wear the headset. You could be asked to setup the playable environment. After doing so, to test if the KatWalk is working properly, open up a game and walk around.
10. Now step off the treadmill and let the partecipant step on. Instruct them on how to wear the straps of the treadmill and the headset.
11. Now launch the two python scripts using Python2, legs.py and head.py, and the Unreal Project from the Unreal Engine application.
12. From the ZED camera launch the streaming sender application.
13. Back from the computer launch the ZED-Oculus application to visualize the stream on the Oculus.
14. When the partecipant is able to see the feedback of the camera, they can start moving around.

## Contact
Developer: Jacopo Ciro Soncini jacopo.ciro.soncini@edu.unige.it



