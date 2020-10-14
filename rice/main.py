
import psutil
import time
from datetime import datetime
import sys

import pipes
import os
import subprocess
import re
import errno
import bluetooth
import sys


def send(sock, message):
    sock.send(b"\r\n" + message + b"\r\n")


def getATCommand(sock, line, device):
    blevel = -1

    if b"BRSF" in line:
        send(sock, b"+BRSF: 1024")
        send(sock, b"OK")
    elif b"CIND=" in line:
        send(sock, b"+CIND: (\"battchg\",(0-5))")
        send(sock, b"OK")
    elif b"CIND?" in line:
        send(sock, b"+CIND: 5")
        send(sock, b"OK")
    elif b"BIND=?" in line:
        # Announce that we support the battery level HF indicator
        # https://www.bluetooth.com/specifications/assigned-numbers/hands-free-profile/
        send(sock, b"+BIND: (2)")
        send(sock, b"OK")
    elif b"BIND?" in line:
        # Enable battery level HF indicator
        send(sock, b"+BIND: 2,1")
        send(sock, b"OK")
    elif b"XAPL=" in line:
        send(sock, b"+XAPL: iPhone,7")
        send(sock, b"OK")
    elif b"IPHONEACCEV" in line:
        parts = line.strip().split(b',')[1:]
        if len(parts) > 1 and (len(parts) % 2) == 0:
            parts = iter(parts)
            params = dict(zip(parts, parts))
            if b'1' in params:
                blevel = (int(params[b'1']) + 1) * 10
    elif b"BIEV=" in line:
        params = line.strip().split(b"=")[1].split(b",")
        if params[0] == b"2":
            blevel = int(params[1])
    else:
        send(sock, b"OK")

    if blevel != -1:
        return blevel

    return None

def find_rfcomm_port(device):
    uuid="0000111e-0000-1000-8000-00805f9b34fb"
    proto = bluetooth.find_service(address=device, uuid=uuid)
    if len(proto) == 0:
        print("Couldn't find the RFCOMM port number")
        return 4
    else:
        for j in range(len(proto)):
            if 'protocol' in proto[j] and proto[j]['protocol'] == 'RFCOMM':
                port = proto[j]['port']
                return port

def bluetooth_bat(arg):
    device = arg
    i = device.find('.')
    if i == -1:
        port = find_rfcomm_port(device)
    else:
        port = int(device[i+1:])
        device = device[:i]
    try:
        s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        s.connect((device, port))
        atcommand = getATCommand(s, s.recv(127), device)
        while atcommand is None:
            atcommand = getATCommand(s, s.recv(127), device)
            if atcommand is not None:
                return atcommand
        s.close()
    except OSError as e:
        return None


def convert_to_gbit(value):
    return round(value / 1024. / 1024. * 8)


def readTemp():
    temp = open("/sys/class/thermal/thermal_zone0/temp")
    temp = temp.read()
    return str(int(round(int(temp) / 1000)))


def readMem():
    return psutil.virtual_memory()


def readTime():
    now = datetime.now()
    return now.strftime("%a %d %b %I:%M%P")




def mediaa():
    status = subprocess.run(["playerctl", "status"], stdout=subprocess.PIPE).stdout.decode('utf-8')
    if status == "Playing\n" or status == "Paused\n":
        metadata = subprocess.run(["playerctl", "metadata"], stdout=subprocess.PIPE).stdout.decode('utf-8')
        artist = re.search(r":artist\s+(.+)", metadata).group(1)
        track = re.search(r":title\s+(.+)", metadata).group(1)
        o = "^#DBD89e^"
        if status == "Playing\n":
            o += " "
        else:
            o += " "
        o += track + " - " + artist
        return o

blueon = False
def volume():
    regex = r"Sink #(\d)\n\s+State: (.+)\n\s+Name: (.+)(?:\n|.)*?Mute: (\w+)(?:\n|.)*?Volume: .*? \d+ \/\s+(\d{1,3})"

    test_str = subprocess.run(["pactl", "list", "sinks"], stdout=subprocess.PIPE).stdout.decode('utf-8')
    matches = re.finditer(regex, test_str)
    sinks = []
    for matchNum, match in enumerate(matches, start=1):
        sink = {}
        sink["num"] = match.group(1)
        sink["status"] = match.group(2)
        sink["name"] = match.group(3)
        sink["mute"] = match.group(4)
        sink["volume"] = match.group(5)
        sinks.append(sink)

    for sink in sinks:
        if (re.match(r"alsa_output.usb", sink["name"]) is not None) or (
                re.match(r"bluez_sink", sink["name"]) is not None):
            if re.match(r"bluez_sink",sink["name"]) is not None:
                blueon = True
            o = ""
            volume = int(sink["volume"])
            if sink["mute"] == "yes":
                o += " "
            else:
                if volume > 65:
                    o += " "
                elif volume > 45:
                    o += " "
                elif volume < 45:
                    o += " "
            o += str(volume) + "% "

            return o
# file descriptors r, w for reading and writing
def bluetooth():
    if blueon == False:
        return None
    bat = bluetooth_bat("CC:98:8B:F5:60:77")
    bluetoothbat = bat
    if bat is not None:
        bluecol = "6FB379"
        if bluetoothbat < 15:
            bluecol = "FF4B39"

        bluetoothbat = str(20 - ((20 / 100) * bluetoothbat) + 3) + ",5," + str((20 / 100) * bluetoothbat)

        return "^c#B8ECFF^^r0,7,2,4^^r2,4,22,10^^c#000000^^r3,5,20,8^^c#" + bluecol + "^^r" + bluetoothbat + ",8^^d^^f24^"


def merge(sep=" :: "):
    sections = []
    audio = []
    media = mediaa()
    if media is not None:
        audio.append(media)
    blue = bluetooth()
    if blue is not None:
        audio.append(blue)
    vol = volume()
    if vol is not None:
        audio.append("^c#9ecbdb^" + vol)
    if len(audio) > 0:
        sections.append(" ".join(audio))
    sections.append("^c#51edd5^" + str(psutil.cpu_percent()) + "%")
    sections.append("^c#2fa18f^" + readTemp() + "c")
    sections.append("::^c#6d5ced^ " + str(
        round(mem.used * 100 / mem.total)) + "% (" + str(round(mem.used / 1000000000,
                                                               2)) + "GiB)")
    sections.append("^c#ed6887^ " + str(
        convert_to_gbit(psutil.net_io_counters().bytes_recv)) + "KB/s  " + str(
        convert_to_gbit(psutil.net_io_counters().bytes_sent)) + "KB/s")
    sections.append("^c#ffd1dc^ " + readTime() + "\n")
    return sep.join(sections)


while True:
    mem = readMem()

    sys.stdout.write(" " + merge())
    sys.stdout.flush()
    time.sleep(1)

