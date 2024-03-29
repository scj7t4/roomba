from . import packets

def validate_sensor_packet(pkt_id):
    if 0 <= pkt_id <= 58 or 100 <= pkt_id <= 107:
        return True
    return False

def sensors(packet):
    if not validate_sensor_packet(packet):
        raise ValueError("Invalid sensor packet")
    return bytes([142, packet])

def query_list(packets):
    if not all([ validate_sensor_packet(p) for p in packets ]):
        raise ValueError("Invalid sensor packet")
    return bytes([149, len(packets)]) + bytes(packets)

def stream(packets):
    if not all([ validate_sensor_packet(p) for p in packets ]):
        raise ValueError("Invalid sensor packet")
    return bytes([148, len(packets)]) + bytes(packets)

def pause_resume(reset):
    return bytes([150, 1 if reset else 0])

def validate_packet(data):
    if data[0] != 19:
        raise ValueError("Data does not contain a packet stream")
    if len(data)+3 < data[1]:
        raise BufferError("Data does not contain full packet")
    if sum(data[1:]) & 0xFF != 0:
        raise IOError("Checksum is invalid")
    return (data[0:data[1]+3], data[data[1]+3:])

class PacketStreamer:
    def __init__(self, serial_conn, pkts):
        self.ser = serial_conn
        self.packets = pkts
        self.state = 'new'
        self.buffer = bytes([])
        self.last_pkt = None
        self.factory = packets.SensorPacketFactory()

    def start(self):
        self.freshen()
        cmd = stream(self.packets)
        self.ser.write(cmd)
        state = 'streaming'

    def pause(self):
        if self.state == 'streaming':
            cmd = pause_resume(False)
            self.ser.write(cmd)
            state = 'paused'

    def resume(self):
        if self.state == 'paused':
            self.freshen()
            cmd = pause_resume(True)
            self.ser.write(cmd)
            state = 'streaming'

    def read_raw(self):
        aligned = False
        while not aligned:
            tmp = self.ser.read(64)
            if not tmp:
                return None
            self.buffer += tmp
            try:
                (pkt, rem) = validate_packet(self.buffer)
                self.buffer = rem
                aligned = True
                self.last_pkt = pkt
            except (ValueError, IOError):
                while self.buffer and self.buffer[0] != 19:
                    self.buffer = self.buffer[1:]
            except BufferError:
                continue
        return self.last_pkt

    def read(self):
        pkt = self.read_raw()
        if pkt:
            return self.factory.parse(pkt)
        else:
            return pkt

    def freshen(self):
        self.ser.reset_input_buffer()
        self.buffer = []
