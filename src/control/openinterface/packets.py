class SensorPacket:
    packet_id = -1
    size = None
    def __init__(self, data):
        self.raw = data
    
    @property
    def uint(self):
        return int.from_bytes(self.raw)

    @property
    def int(self):
        return int.from_bytes(self.raw, signed=True)

class BumpAndWheelDrop(SensorPacket):
    packet_id = 7
    size = 1
    def __init__(self,data):
        super().__init__(data)
    
    @property
    def bumper_right(self):
        return bool(0x01 & self.uint)

    @property
    def bumper_left(self):
        return bool(0x02 & self.uint)

    @property
    def wheel_drop_right(self):
        return bool(0x04 & self.uint)

    @property
    def wheel_drop_left(self):
        return bool(0x08 & self.uint)


class Wall(SensorPacket):
    packet_id = 8
    size = 1
    def __init__(self,data):
        super().__init__(data)

    def __nonzero__(self):
        return bool(self.raw)

class Cliff(SensorPacket):
    def __init__(self,data):
        super().__init__(data)

    def __nonzero__(self):
        return bool(self.raw)

class CliffLeft(Cliff):
    packet_id = 9
    size = 1
    def __init__(self,data):
        super().__init__(data)

class CliffFrontLeft(Cliff):
    packet_id = 10
    size = 1
    def __init__(self,data):
        super().__init__(data)

class CliffFrontRight(Cliff):
    packet_id = 11
    size = 1
    def __init__(self,data):
        super().__init__(data)

class CliffRight(Cliff):
    packet_id = 12
    size = 1
    def __init__(self,data):
        super().__init__(data)

class VirtualWall(SensorPacket):
    packet_id = 13
    size = 1
    def __init__(self,data):
        super().__init__(data)

class WheelOvercurrents(SensorPacket):
    packet_id = 14
    size = 1
    def __init__(self,data):
        super().__init__(data)

    @property
    def side_brush(self):
        return bool(self.uint & 1)
    
    @property
    def main_brush(self):
        return bool(self.uint & 4)
    
    @property
    def right_wheel(self):
        return bool(self.uint & 8)

    @property
    def right_wheel(self):
        return bool(self.uint & 16)

class DirtDetect(SensorPacket):
    packet_id = 15
    size = 1
    def __init__(self,data):
        super().__init__(data)

    @property
    def dirt_level(self):
        return self.uint

class InfraredCharacter(SensorPacket):
    def __init__(self,data):
        super().__init__(data)

class InfraredCharacterOmni(InfraredCharacter):
    packet_id = 17
    size = 1
    def __init__(self,data):
        super().__init__(data)

class InfraredCharacterLeft(InfraredCharacter):
    packet_id = 52
    size = 1
    def __init__(self,data):
        super().__init__(data)

class InfraredCharacterRight(InfraredCharacter):
    packet_id = 53
    size = 1
    def __init__(self,data):
        super().__init__(data)

class Buttons(SensorPacket):
    packet_id = 18
    size = 1
    def __init__(self,data):
        super().__init__(data)

    @property
    def clean(self):
        return bool(self.uint & 1)
    
    @property
    def spot(self):
        return bool(self.uint & 2)
    
    @property
    def dock(self):
        return bool(self.uint & 4)
    
    @property
    def minute(self):
        return bool(self.uint & 8)
    
    @property
    def hour(self):
        return bool(self.uint & 16)
    
    @property
    def day(self):
        return bool(self.uint & 32)
    
    @property
    def schedule(self):
        return bool(self.uint & 64)
    
    @property
    def clock(self):
        return bool(self.uint & 128)

class Distance(SensorPacket):
    packet_id = 19
    size = 2
    def __init__(self,data):
        super().__init__(data)

    @property
    def millimeters(self):
        return self.int

class Angle(SensorPacket):
    packet_id = 20
    size = 2
    def __init__(self,data):
        super().__init__(data)

    @property
    def degrees(self):
        return self.int

class ChargingState(SensorPacket):
    packet_id = 21
    size = 1
    def __init__(self,data):
        super().__init__(data)

    @property
    def mode(self):
        modes = [
                'Not Charging',
                'Reconditioning Charging',
                'Full Charging',
                'Trickle Charging',
                'Waiting',
                'Charging Fault Condition',
                ]
        return modes[self.uint]

    @property
    def code(self):
        return self.uint

class Voltage(SensorPacket):
    packet_id = 22
    size = 2
    def __init__(self,data):
        super().__init__(data)

    @property
    def millivolts(self):
        return self.uint

class Current(SensorPacket):
    packet_id = 23
    size = 2
    def __init__(self,data):
        super().__init__(data)

    @property
    def milliamps(self):
        return self.int

class Temperature(SensorPacket):
    packet_id = 24
    size = 1
    def __init__(self,data):
        super().__init__(data)
    
    @property
    def celsius(self):
        return self.int

class BatteryCharge(SensorPacket):
    packet_id = 25
    size = 2
    def __init__(self,data):
        super().__init__(data)

    @property
    def level(self):
        return self.uint

class BatteryCapacity(SensorPacket):
    packet_id = 26
    size = 2
    def __init__(self,data):
        super().__init__(data)

    @property
    def capacity(self):
        return self.uint

class WallSignal(SensorPacket):
    packet_id = 27
    size = 2
    def __init__(self,data):
        super().__init__(data)

    @property
    def strength(self):
        return self.uint

class CliffSignal(SensorPacket):
    size = 2 
    def __init__(self,data):
        super().__init__(data)

    @property
    def strength(self):
        return self.uint

class CliffLeftSignal(CliffSignal):
    packet_id = 28
    def __init__(self,data):
        super().__init__(data)

class CliffFrontLeftSignal(CliffSignal):
    packet_id = 29
    def __init__(self,data):
        super().__init__(data)

class CliffFrontRightSignal(CliffSignal):
    packet_id = 30
    def __init__(self,data):
        super().__init__(data)

class CliffRightSignal(CliffSignal):
    packet_id = 31
    def __init__(self,data):
        super().__init__(data)

class ChargingSourcesAvailable(SensorPacket):
    packet_id = 34
    size = 1
    def __init__(self,data):
        super().__init__(data)

    @property
    def home(self):
        return bool(self.uint & 2)

    @property
    def charger(self):
        return bool(self.uint & 1)

class OIMode(SensorPacket):
    packet_id = 35
    size = 1
    def __init__(self,data):
        super().__init__(data)

    @property
    def mode(self):
        modes = [
                'Off',
                'Passive',
                'Safe',
                'Full',
                ]
        return modes[self.uint]

    @property
    def code(self):
        return self.uint

class SongNumber(SensorPacket):
    packet_id = 36
    size = 1
    def __init__(self,data):
        super().__init__(data)

    @property
    def number(self):
        return self.uint

class SongPlaying(SensorPacket):
    packet_id = 37
    size = 1
    def __init__(self,data):
        super().__init__(data)

    def __nonzero__(self):
        return bool(self.uint)

class NumberOfStreamPackets(SensorPacket):
    packet_id = 38
    size = 1
    def __init__(self,data):
        super().__init__(data)
    
    @property
    def packets(self):
        return self.uint

class RequestedVelocity(SensorPacket):
    packet_id = 39
    size = 2
    def __init__(self,data):
        super().__init__(data)

    @property
    def mmps(self):
        return self.int

class RequestedRadius(SensorPacket):
    packet_id = 40
    size = 2
    def __init__(self,data):
        super().__init__(data)

    @property
    def millimeters(self):
        return self.int

class RequestedRightVelocity(SensorPacket):
    packet_id = 41
    size = 2
    def __init__(self,data):
        super().__init__(data)
    
    @property
    def mmps(self):
        return self.int

class RequestedLeftVelocity(SensorPacket):
    packet_id = 42
    size = 2
    def __init__(self,data):
        super().__init__(data)
    
    @property
    def mmps(self):
        return self.int

class RightEncoderCounts(SensorPacket):
    packet_id = 43
    size = 2
    def __init__(self,data):
        super().__init__(data)

    @property
    def counts(self):
        return self.uint

class LeftEncoderCounts(SensorPacket):
    packet_id = 44
    size = 2
    def __init__(self,data):
        super().__init__(data)
    
    @property
    def counts(self):
        return self.uint

class LightBumper(SensorPacket):
    packet_id = 45
    size = 1
    def __init__(self,data):
        super().__init__(data)

    @property
    def bumper_left(self):
        return bool(self.uint & 1)
    
    @property
    def bumper_front_left(self):
        return bool(self.uint & 2)
    
    @property
    def bumper_center_left(self):
        return bool(self.uint & 4)
    
    @property
    def bumper_center_right(self):
        return bool(self.uint & 8)
    
    @property
    def bumper_front_right(self):
        return bool(self.uint & 16)
    
    @property
    def bumper_right(self):
        return bool(self.uint & 32)

class BumpSignal(SensorPacket):
    size = 2
    def __init__(self,data):
        super().__init__(data)

    def strength(self):
        return bool(self.uint)

class LightBumpLeftSignal(BumpSignal):
    packet_id = 46
    def __init__(self,data):
        super().__init__(data)

class LightBumpFrontLeftSignal(BumpSignal):
    packet_id = 47
    def __init__(self,data):
        super().__init__(data)

class LightBumpCenterLeftSignal(BumpSignal):
    packet_id = 48
    def __init__(self,data):
        super().__init__(data)

class LightBumpCenterRightSignal(BumpSignal):
    packet_id = 49
    def __init__(self,data):
        super().__init__(data)

class LightBumpFrontRightSignal(BumpSignal):
    packet_id = 50
    def __init__(self,data):
        super().__init__(data)

class LightBumpRightSignal(BumpSignal):
    packet_id = 51
    def __init__(self,data):
        super().__init__(data)

class MotorCurrent(SensorPacket):
    size = 2
    def __init__(self,data):
        super().__init__(data)

    @property
    def milliamps(self):
        return self.int

class LeftMotorCurrent(MotorCurrent):
    packet_id = 54
    def __init__(self,data):
        super().__init__(data)

class RightMotorCurrent(MotorCurrent):
    packet_id = 55
    def __init__(self,data):
        super().__init__(data)

class MainBrushMotorCurrent(MotorCurrent):
    packet_id = 56
    def __init__(self,data):
        super().__init__(data)

class SideBrushMotorCurrent(MotorCurrent):
    packet_id = 57
    def __init__(self,data):
        super().__init__(data)

class Stasis(SensorPacket):
    size = 1
    packet_id = 58
    def __init__(self,data):
        super().__init__(data)

    def __nonzero__(self):
        return bool(self.uint)

class Unused1(SensorPacket):
    size = 1
    packet_id = 16
    def __init__(self,data):
        super().__init__(data)

class Unused2(SensorPacket):
    size = 1
    packet_id = 32
    def __init__(self,data):
        super().__init__(data)

class Unused3(SensorPacket):
    size = 2
    packet_id = 33
    def __init__(self,data):
        super().__init__(data)


import sys, inspect

class SensorPacketFactory:
    def __init__(self):
        classes = inspect.getmembers(sys.modules[__name__], inspect.isclass)
        self.classes = list(
                filter(lambda x: issubclass(x[1], SensorPacket) and x[1].packet_id != -1,
                classes))
        self.conv = {}
        for ctype in self.classes:
            self.conv[ctype[1].packet_id] = ctype
    def parse(self, data, output):
        c = 0
        objs = {}
        while c < len(data):
            ptype = data[c]
            c += 1
            try:
                stype, otype = self.conv[ptype]
            except KeyError:
                raise ValueError("Invalid sensor packet type")
            nc = c + otype.size
            obj = otype(data[c:nc])
            c += nc
            objs[stype] = obj
        return objs

