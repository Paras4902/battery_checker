"""Script to check battery percentage using python module"""
import psutil  # pip install psutil
import time
import pyttsx3    # pip install pyttsx3
from win10toast import ToastNotifier    # pip install win10toast # also need to install win32api
import threading

toaster = ToastNotifier()
x = pyttsx3.init()
x.setProperty('rate', 130)
x.setProperty('volume', 8)
count = 0


def show_notification(show_text):
    """Function to notify about battery percentage"""
    toaster.show_toast(show_text,
                       icon_path='battery_indicator.ico',
                       duration=10)
    # loop the toaster over some period of time
    while toaster.notification_active():
        time.sleep(0.1)


def monitor():
    """Function to monitor battery percentage"""
    global count
    while True:
        time.sleep(10)
        battery = psutil.sensors_battery()
        plugged = battery.power_plugged
        percent = int(battery.percent)

        if percent < 40:
            if not plugged:
                process_thread = threading.Thread(target=show_notification, args=("Your Battery at "+str(percent)+"% Please plug the cable",))  # <- note extra ','
                process_thread.start()
                x.say("Your battery is getting low so charge it right now")
                x.runAndWait()
                count = 0
        elif percent == 100:
            if plugged:
                process_thread = threading.Thread(target=show_notification, args=("Charging is getting complete",))  # <- note extra ','
                process_thread.start()
                x.say("Charging is getting complete")
                x.runAndWait()
        elif percent == 90:
            if plugged:
                if count == 0:
                    process_thread = threading.Thread(target=show_notification, args=("Your Battery at 90% Please plug out the cable",))  # <- note extra ','
                    process_thread.start()
                    x.say("Your battery at 90% ")
                    x.runAndWait()
                    count = count + 1


if __name__ == "__main__":
    monitor()
