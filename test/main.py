import utime
import _thread
import ujson
import comm

from ota_senko import Senko
import machine 

def threadMaqueen():
    from maqueen import Maqueen
    mq = Maqueen()

    while True:
        (temp, acc, gyro) = mq.getStatus()
        sec = round(utime.time(), 3)
        obj = {'sec': sec, 'acc': acc, 'gyro': gyro, 'temp': temp}
        mqttCli.publish(obj)

        notif = _thread.wait(1000) # 1 sec
        if notif:
            if notif == _thread.EXIT:
                return
            else:
                # command received via datacb
                type, sender, msg = _thread.getmsg()
                if msg:
                    print("COMMAND:", msg)
                pass

def threadLedDisplay():
    from led_display import LEDDisplay
    
    led = LEDDisplay()
    for i in range(1, 6):
        print (i)
        # led.setPixelHSB(i, 200, 1.0, 0.2, True)
        led.setPixelColor(i, 0, 0, 200, True)
        utime.sleep_ms(1000)
        led.setPixelColor(i, 0, 0, 0, True)
        utime.sleep_ms(1000)
        print ('clear', i)
    
    # led.rainbow(loops=2, delay=2000)    
    led.clear()

# ---------------------------------------

with open('./config.json') as fp:
    config = ujson.loads(fp.read())

OTA = Senko(user="zlatbg", repo="alphomega", working_dir="test", files=["led_display.py"])

if OTA.update():
    print("Updated to the latest version! Rebooting...")
    machine.reset()
else:
    print("OTA update done.. start the LED display!")
    led_display_thread = _thread.start_new_thread("led_display", threadLedDisplay, ())

    # print(config['mqtt'])
    print ("connect to MQTT Broker")
    mqttCli = comm.MQTTClient(config)
    if mqttCli.connect():
        mq_thread_id = _thread.start_new_thread("mq", threadMaqueen, ())
        mqttCli.setProcessingThread(mq_thread_id)

