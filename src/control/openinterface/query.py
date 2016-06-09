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

class PacketStream:
    def __init__(data):
        if data[0] != 19:
            raise ValueError("Data does not contain a packet stream")
        if len(data)+3 != data[1]:
            raise BufferError("Data does not contain full packet")
        if sum(data[1:]) & 0xFF != 0:
            raise IOError("Checksum is invalid")



