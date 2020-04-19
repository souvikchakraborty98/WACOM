# import subprocess, json

# out = subprocess.getoutput("PowerShell -Command \"& {Get-PnpDevice | Select-Object Status,Class,FriendlyName,InstanceId | ConvertTo-Json}\"")
# print(out)
# j = json.loads(out)
# for dev in j:
#     print(f"\nStatus: {dev['Status']} Class: {dev['Class']} Friendly Name: {dev['FriendlyName']} InstanceID: {dev['InstanceId']}\n")
import time
from serial.tools import list_ports  # pyserial

def enumerate_serial_devices():
    return set([item for item in list_ports.comports()])

def check_new_devices(old_devices):
    devices = enumerate_serial_devices()
    added = devices.difference(old_devices)
    removed = old_devices.difference(devices)
    if added:
        print(f'added: {added}')
    if removed:
        print(f'removed: {removed}')
    return devices

# Quick and dirty timing loop 
old_devices = enumerate_serial_devices()
while True:
    old_devices = check_new_devices(old_devices)
    time.sleep(0.5)