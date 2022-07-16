import machine, time

# https://github.com/loboris/MicroPython_ESP32_psRAM_LoBo/blob/fff2e193d064effe36a7d456050faa78fe6280a8/MicroPython_BUILD/components/micropython/esp32/machine_neopixel.c

class LEDDisplay:

    def __init__(self):
        self.np = machine.Neopixel(machine.Pin(13), 25)

    def __del__(self):
        self.np.deinit()

    def clear(self):
        self.np.clear()

    def show(self):
        self.np.show()

    def HSBtoRGB(self, hue, sat, bri):
        return self.np.HSBtoRGB(hue, sat, bri)

    def RGBtoHSB(self, color):
        return self.np.RGBtoHSB(color)

    def setPixelHSB(self, pos, hue, sat, bri, update=False): # pos = 1-25
        self.np.setHSB(pos, hue, sat, bri, 1, update)
        
    def setPixelColor(self, pos, red, green, blue, update=False): # pos = 1-25
        rgb_color_int = red << 16 | green << 8 | blue
        hue, sat, bri = self.np.RGBtoHSB(rgb_color_int)
        self.np.setHSB(pos, hue, sat, bri, 1, update)

    def rainbow(self, loops=10, delay=1000, sat=1.0, bri=0.2):
        for pos in range(0, loops):
            for i in range(1, 26):
                dHue = 360.0/25*(pos+i);
                hue = dHue % 360;
                self.np.setHSB(i, hue, sat, bri, 1, False)
            self.np.show()
            if delay > 0:
                time.sleep_ms(delay)
                self.clear()
                time.sleep_ms(200)



