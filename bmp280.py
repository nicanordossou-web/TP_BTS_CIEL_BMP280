
import time

class BMP280:
    def __init__(self, i2c, address=0x76):
        self.i2c = i2c
        self.address = address

        # Configuration du capteur
        self.i2c.writeto_mem(address, 0xF4, b'\x27')
        self.i2c.writeto_mem(address, 0xF5, b'\xA0')

        # Lecture des coefficients de calibration
        calib = self.i2c.readfrom_mem(address, 0x88, 24)

        def u16(i):
            return calib[i] | (calib[i+1] << 8)

        def s16(i):
            v = u16(i)
            return v - 65536 if v > 32767 else v

        self.T1 = u16(0)
        self.T2 = s16(2)
        self.T3 = s16(4)
        self.P1 = u16(6)
        self.P2 = s16(8)
        self.P3 = s16(10)
        self.P4 = s16(12)
        self.P5 = s16(14)
        self.P6 = s16(16)
        self.P7 = s16(18)
        self.P8 = s16(20)
        self.P9 = s16(22)

    def read(self):
        data = self.i2c.readfrom_mem(self.address, 0xF7, 6)

        adc_p = (data[0] << 12) | (data[1] << 4) | (data[2] >> 4)
        adc_t = (data[3] << 12) | (data[4] << 4) | (data[5] >> 4)

        var1 = (adc_t / 16384 - self.T1 / 1024) * self.T2
        var2 = ((adc_t / 131072 - self.T1 / 8192) ** 2) * self.T3
        t_fine = var1 + var2
        temperature = t_fine / 5120

        var1 = t_fine / 2 - 64000
        var2 = var1 * var1 * self.P6 / 32768
        var2 += var1 * self.P5 * 2
        var2 = var2 / 4 + self.P4 * 65536
        var1 = (self.P3 * var1 * var1 / 524288 + self.P2 * var1) / 524288
        var1 = (1 + var1 / 32768) * self.P1

        if var1 == 0:
            return temperature, None

        pressure = 1048576 - adc_p
        pressure = (pressure - var2 / 4096) * 6250 / var1
        var1 = self.P9 * pressure * pressure / 2147483648
        var2 = pressure * self.P8 / 32768
        pressure += (var1 + var2 + self.P7) / 16

        return temperature, pressure / 100
