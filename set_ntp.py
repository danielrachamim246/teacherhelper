import socket
import struct
import sys
import time
import datetime
import win32api
import ctypes

def gettime_ntp(addr='time.windows.com'):
    # http://code.activestate.com/recipes/117211-simple-very-sntp-client/
    TIME1970 = 2208988800      # Thanks to F.Lundh
    client = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
    data = '\x1b' + 47 * '\0'
    try:
        # Timing out the connection after 5 seconds, if no response received
        client.settimeout(5.0)
        client.sendto( data, (addr, 123))
        data, address = client.recvfrom( 1024 )
        if data:
            epoch_time = struct.unpack( '!12I', data )[10]
            epoch_time -= TIME1970
            return epoch_time
    except socket.timeout:
        return None

def settime_ntp():
    while True:
        epoch_time = gettime_ntp()
        if epoch_time is not None:
            # Set Windows time
            utcTime = datetime.datetime.utcfromtimestamp(epoch_time)
            win32api.SetSystemTime(utcTime.year, utcTime.month, utcTime.weekday(), utcTime.day, utcTime.hour, utcTime.minute, utcTime.second, 0)
            # Local time is obtained using fromtimestamp()
            localTime = datetime.datetime.fromtimestamp(epoch_time)
            return

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def sync_ntp_as_admin():
    if is_admin():
        while True:
            settime_ntp()
            time.sleep(0.5)
        return

    else:
        ctypes.windll.shell32.ShellExecuteW(None, u"runas", unicode(sys.executable), unicode(__file__), None, 0)
        if is_admin():
            settime_ntp()
            return
        else:
            return

sync_ntp_as_admin()