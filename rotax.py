import serial
import time


class ez_comm:
    def __init__(self, device: str):
        self.serial = serial.Serial(device, 115200)

    def get_pos(self):
        self.serial.flush()

        self.serial.write(bytes("AZ EL\n", encoding="ascii"))
        time.sleep(0.01)
        buffer = self.serial.read_all()
        buffer = buffer.strip()
        split = buffer.split(b" ")
        azimuth = float(split[0][2:])
        elevation = float(split[1][2:])

        return (azimuth, elevation)


    def set_pos(self, azimuth: float, elevation: float):
        msg = "AZ{:.1f} El{:.1f}\n".format(azimuth, elevation)
        self.serial.write(bytes(msg, encoding="ascii"))
        pass


if __name__ == "__main__":
    TARM = ez_comm("/dev/ttyUSB0")
    while(True):
        TARM.set_pos(90, 0)
        time.sleep(2)
        TARM.set_pos(0, 0)
        time.sleep(2)