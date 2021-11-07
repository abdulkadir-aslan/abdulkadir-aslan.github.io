import os
import subprocess
from time import sleep
y=(1)
subprocess.Popen(["python", 'alarm.py'])
sleep(y)
subprocess.Popen(["python", 'temp.py'])
sleep(y)
subprocess.Popen(["python", 'gyrotime.py'])
sleep(y)
subprocess.Popen(["python", 'example.py'])
sleep(y)
# **********************************************
# # ALARM BUTONU VE MAİL GÖNDERME İÇİN KOD (ALARM.PY)
# **********************************************
import subprocess
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)#Button to GPIO23
GPIO.setup(24, GPIO.OUT)  #LED to GPIO24
try:
    while True:
         button_state = GPIO.input(23)
         if button_state == False:
             GPIO.output(24, True)
             print('Butona basildi...')
             print('mail gonderiliyor...')
             time.sleep(0.5)
             subprocess.Popen(["python", 'mail.py'])
             time.sleep(0.5)
             print('mail gonderildi')
             time.sleep(0.2)
         else:
             GPIO.output(24, False)
except:
    GPIO.cleanup()
# *******************************************************
# JİROSKOP SÜREKLİ ÇALIŞTIRMA VE DÜŞTÜĞÜNÜ ALGILAYAN VE MAİL GÖNDEREN KOD (GYROTİME.PY)
# *******************************************************
#!/usr/bin/python
import smbus
import math
import time
import subprocess
# Register
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c
def read_byte(reg):
    return bus.read_byte_data(address, reg)
def read_word(reg):
    h = bus.read_byte_data(address, reg)
    l = bus.read_byte_data(address, reg+1)
    value = (h << 8) + l
    return value
def read_word_2c(reg):
    val = read_word(reg)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val
def dist(a,b):
    return math.sqrt((a*a)+(b*b))
def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)
def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)
bus = smbus.SMBus(1) # bus = smbus.SMBus(0) fuer Revision 1
address = 0x68       # via i2cdetect
# MPU6050 ilk calistiginda uyku modunda oldugundan, calistirmak icin asagidaki komutu veriyoruz:
bus.write_byte_data(address, power_mgmt_1, 0)
print "Jiroskop"
print "--------"
while True:
 time.sleep(0.1)
 gyroskop_xout = read_word_2c(0x43)
 gyroskop_yout = read_word_2c(0x45)
 gyroskop_zout = read_word_2c(0x47)
 print "jiroskop x: ", ("%5d" % gyroskop_xout)
 print "jiroskop y: ", ("%5d" % gyroskop_yout)
 print "jiroskop z: ", ("%5d" % gyroskop_zout)
 beschleunigung_xout = read_word_2c(0x3b)
 beschleunigung_yout = read_word_2c(0x3d)
 beschleunigung_zout = read_word_2c(0x3f)
 beschleunigung_xout_skaliert = beschleunigung_xout / 16384.0
 beschleunigung_yout_skaliert = beschleunigung_yout / 16384.0
 beschleunigung_zout_skaliert = beschleunigung_zout / 16384.0
 time.sleep(2)
 if (read_word_2c(0x3f)<= -15000):
         print "hasta dustu ailesine mail gonderiliyor..."
         subprocess.Popen(["python", 'mail.py'])
         print "gonderildi"
         time.sleep(3)
# **************************************************************
# MAİL GÖNDERME KODU (MAİL.PY)
# **************************************************************
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
email_user = 'hastabilekligi@gmail.com'
email_password = 'raspberrypi'
email_send = 'hastabilekligi@gmail.com'
subject = 'HASTA BILEKLIGINDEN  MESAJINIZ VAR'
msg = MIMEMultipart()
msg['From'] = email_user
msg['To'] = email_send
msg['Subject'] = subject
body = 'HASTA YERE DUSTU !!'
msg.attach(MIMEText(body,'plain'))
filename='filename'
attachment  =open(filename,'rb')
part = MIMEBase('application','octet-stream')
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition',"attachment; filename= "+filename)
msg.attach(part)
text = msg.as_string()
server = smtplib.SMTP('smtp.gmail.com',587)
server.starttls()
server.login(email_user,email_password)
server.sendmail(email_user,email_send,text)
server.quit()
# *****************************************************************
# JİROSKOP İÇİN MPU6050 KODU (MPU6050.PY)
# ******************************************************************
#!/usr/bin/python
import smbus
import math
import time
# Guc yonetim register'lari
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c
def read_byte(adr):
 return bus.read_byte_data(address, adr)
def read_word(adr):
 high = bus.read_byte_data(address, adr)
 low = bus.read_byte_data(address, adr+1)
 val = (high << 8) + low
 return val
def read_word_2c(adr):
 val = read_word(adr)
 if (val >= 0x8000):
 return -((65535 - val) + 1)
 else:
 return val
def dist(a,b):
 return math.sqrt((a*a)+(b*b))
def get_y_rotation(x,y,z):
 radians = math.atan2(x, dist(y,z))
 return -math.degrees(radians)
def get_x_rotation(x,y,z):
 radians = math.atan2(y, dist(x,z))
 return math.degrees(radians)
bus = smbus.SMBus(1)
address = 0x68 #MPU6050 I2C adresi
#MPU6050 ilk calistiginda uyku modunda oldugundan, calistirmak icin asagidaki komutu veriyoruz:
bus.write_byte_data(address, power_mgmt_1, 0)
while True:
 time.sleep(0.1)
 #Jiroskop register'larini oku
 gyro_xout = read_word_2c(0x43)
 gyro_yout = read_word_2c(0x45)
 gyro_zout = read_word_2c(0x47)
 print "Jiroskop X : ", gyro_xout, " olcekli: ", (gyro_xout / 131)
 print "Jiroskop Y : ", gyro_yout, " olcekli: ", (gyro_yout / 131)
 print "Jiroskop Z: ", gyro_zout, " olcekli: ", (gyro_zout / 131)
 #Ivmeolcer register'larini oku
 accel_xout = read_word_2c(0x3b)
 accel_yout = read_word_2c(0x3d)
 accel_zout = read_word_2c(0x3f)
 accel_xout_scaled = accel_xout / 16384.0
 accel_yout_scaled = accel_yout / 16384.0
 accel_zout_scaled = accel_zout / 16384.0
 print "Ivmeolcer X: ", accel_xout, " olcekli: ", accel_xout_scaled
 print "Ivmeolcer Y: ", accel_yout, " olcekli: ", accel_yout_scaled
 print "Ivmeolcer Z: ", accel_zout, " olcekli: ", accel_zout_scaled
 print "X dondurme: " , get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
 print "Y dondurme: " , get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
 time.sleep(0.5)
# ****************************************************************************************
# MCP3008 ADC KODU NABIZ ÖLÇER İÇİN (MCP3008.PY)
# ***************************************************************************************
from spidev import SpiDev
class MCP3008:
    def __init__(self, bus = 0, device = 0):
        self.bus, self.device = bus, device
        self.spi = SpiDev()
        self.open()
    def open(self):
        self.spi.open(self.bus, self.device)
    def read(self, channel = 0):
        self.spi.max_speed_hz = 1000000
        adc = self.spi.xfer2([1, (8 + channel) << 4, 0])
        data = ((adc[1] & 3) << 8) + adc[2]
        return data
    def close(self):
        self.spi.close()
# *****************************************************************************
# NABIZ ÖLÇERİ DİJİTALE DÖNÜŞTÜREN ALGORİTMA (PULSESENSOR.PY)
# ******************************************************************************
import time
import threading
from MCP3008 import MCP3008
class Pulsesensor:
    def __init__(self, channel = 0, bus = 0, device = 0):
        self.channel = channel
        self.BPM = 0
        self.adc = MCP3008(bus, device)
    def getBPMLoop(self):
        # init variables
        rate = [0] * 10         # array to hold last 10 IBI values
        sampleCounter = 0       # used to determine pulse timing
        lastBeatTime = 0        # used to find IBI
        P = 512                 # used to find peak in pulse wave, seeded
        T = 512                 # used to find trough in pulse wave, seeded
        thresh = 525            # used to find instant moment of heart beat, seeded
        amp = 100               # used to hold amplitude of pulse waveform, seeded
        firstBeat = True        # used to seed rate array so we startup with reasonable BPM
        secondBeat = False      # used to seed rate array so we startup with reasonable BPM
        IBI = 600               # int that holds the time interval between beats! Must be seeded!
        Pulse = False           # "True" when User's live heartbeat is detected. "False" when not a "live beat".
        lastTime = int(time.time()*1000)
        while not self.thread.stopped:
            Signal = self.adc.read(self.channel)
            currentTime = int(time.time()*1000)
            sampleCounter += currentTime - lastTime
            lastTime = currentTime
            N = sampleCounter - lastBeatTime
            # find the peak and trough of the pulse wave
            if Signal < thresh and N > (IBI/5.0)*3:     # avoid dichrotic noise by waiting 3/5 of last IBI
                if Signal < T:                          # T is the trough
                    T = Signal                          # keep track of lowest point in pulse wave
            if Signal > thresh and Signal > P:
                P = Signal
            # signal surges up in value every time there is a pulse
            if N > 250:                                 # avoid high frequency noise
                if Signal > thresh and Pulse == False and N > (IBI/5.0)*3:
                    Pulse = True                        # set the Pulse flag when we think there is a pulse
                    IBI = sampleCounter - lastBeatTime  # measure time between beats in mS
                    lastBeatTime = sampleCounter        # keep track of time for next pulse
                    if secondBeat:                      # if this is the second beat, if secondBeat == TRUE
                        secondBeat = False;             # clear secondBeat flag
                        for i in range(len(rate)):      # seed the running total to get a realisitic BPM at startup
                          rate[i] = IBI
                    if firstBeat:                       # if it's the first time we found a beat, if firstBeat == TRUE
                        firstBeat = False;              # clear firstBeat flag
                        secondBeat = True;              # set the second beat flag
                        continue
                    # keep a running total of the last 10 IBI values
                    rate[:-1] = rate[1:]                # shift data in the rate array
                    rate[-1] = IBI                      # add the latest IBI to the rate array
                    runningTotal = sum(rate)            # add upp oldest IBI values
                    runningTotal /= len(rate)           # average the IBI values
                    self.BPM = 60000/runningTotal       # how many beats can fit into a minute? that's BPM!
            if Signal < thresh and Pulse == True:       # when the values are going down, the beat is over
                Pulse = False                           # reset the Pulse flag so we can do it again
                amp = P - T                             # get amplitude of the pulse wave
                thresh = amp/2 + T                      # set thresh at 50% of the amplitude
                P = thresh                              # reset these for next time
                T = thresh
            if N > 2500:                                # if 2.5 seconds go by without a beat
                thresh = 512                            # set thresh default
                P = 512                                 # set P default
                T = 512                                 # set T default
                lastBeatTime = sampleCounter            # bring the lastBeatTime up to date
                firstBeat = True                        # set these to avoid noise
                secondBeat = False                      # when we get the heartbeat back
                self.BPM = 0
            time.sleep(0.005)
    # Start getBPMLoop routine which saves the BPM in its variable
    def startAsyncBPM(self):
        self.thread = threading.Thread(target=self.getBPMLoop)
        self.thread.stopped = False
        self.thread.start()
        return
    # Stop the routine
    def stopAsyncBPM(self):
        self.thread.stopped = True
        self.BPM = 0
        return
# ***************************************************************************************************
# NABIZ SENSÖRÜNDEKİ BİLGİYİ TERMİNALDE GÖSTEREN KOD (EXAMPLE.PY)
# ********************************************************************************************
from pulsesensor import Pulsesensor
import time
import subprocess
p = Pulsesensor()
p.startAsyncBPM()
try:
    while True:
        bpm = p.BPM
        if bpm > 0:
            print("BPM: %d" % bpm)
        else:
            print("No Heartbeat found")
        time.sleep(1)
except:
    p.stopAsyncBPM()
