import pyaudio
from msvcrt import getch
p = pyaudio.PyAudio()
c=1
for i in range(p.get_device_count()):
  if p.get_device_count()!=0:
    if p.get_device_info_by_index(i).get('maxInputChannels')>0 and '@' not in p.get_device_info_by_index(i).get('name') and int(p.get_device_info_by_index(i).get('hostApi'))==0 and p.get_device_info_by_index(i).get('name')!="Microsoft Sound Mapper - Input":
      print(str(c)+") "+str(p.get_device_info_by_index(i)))
      c+=1
      print("\n")
  else:
    print("No IP Devices found")
    getch()
    exit()

print("press any key to exit")
junk=getch()