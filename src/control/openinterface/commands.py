def start():
    return bytes([128])

def baud(rate):
    VALID_RATES = {
            300:    0,
            600:    1,
            1200:   2,
            2400:   3,
            4800:   4,
            9600:   5,
            14400:  6,
            19200:  7,
            28800:  8,
            38400:  9,
            57600: 10,
            115200:11,
    }

    if rate not in VALID_RATES:
        raise ValueError("Invalid data rate")

    return bytes([129, VALID_RATE[rate]])

def mode_safe():
    return bytes([131])

def mode_full():
    return bytes([132])

def clean():
    return bytes([135])

def clean_max():
    return bytes([136])

def clean_spot():
    return bytes([134])

def seek_dock():
    return bytes([143])

def schedule(sunday=None, monday=None, tuesday=None, wednesday=None,
             thursday=None, friday=None, saturday=None):
    days = 0
    times = [ 0 ] * 14
    if sunday:
        days |= 1
        times[0] = sunday.hour
        times[1] = sunday.minute
    if monday:
        days |= 2
        times[2] = monday.hour
        times[3] = monday.minute
    if tuesday:
        days |= 4
        times[4] = tuesday.hour
        times[5] = tuesday.minute
    if wednesday:
        days |= 8
        times[6] = wednesday.hour
        times[7] = wednesday.minute
    if thursday:
        days |= 16
        times[8] = thursday.hour
        times[9] = thursday.minute
    if friday:
        days |= 32
        times[10] = friday.hour
        times[11] = friday.minute
    if saturday:
        days |= 64
        times[12] = saturday.hour
        times[13] = saturday.minute
    return bytes([167, days] + times)

def set_date(day, time):
    VALID_DAYS = {
            'sunday': 0,
            'monday': 1,
            'tuesday': 2,
            'wednesday': 3,
            'thursday': 4,
            'friday': 5,
            'saturday': 6
    }

    day = day.lower()
    if day not in VALID_DAYS:
        raise ValueError("Invalid day of week")
    return bytes([168, VALID_DAYS[day], time.hour, time.minute])

def drive(velocity, radius):
    if not (-500 <= velocity <= 500):
        raise ValueError("Invalid velocity")
    if not (-2000 <= radius <= 2000):
        raise ValueError("Invalid radius")
    v_bytes = velocity.to_bytes(2, 'big', True)
    r_bytes = radius.to_bytes(2, 'big', True)
    return bytes([137])+v_bytes+r_bytes

def drive_direct(rvelocity, lvelocity):
    if not (-500 <= rvelocity <= 500):
        raise ValueError("Invalid right velocity")
    if not (-500 <= lvelocity <= 500):
        raise ValueError("Invalid left velocity")
    r_bytes = rvelocity.to_bytes(2, 'big', True)
    l_bytes = lvelocity.to_bytes(2, 'big', True)
    return bytes([145])+r_bytes+l_bytes

def drive_pwm(rpwm, lpwm):
    if not (-255 <= rpwm <= 255):
        raise ValueError("Invalid right pwm")
    if not (-255 <= lpwm <= 255):
        raise ValueError("Invalid left pwm")
    r_bytes = rpwm.to_bytes(2, 'big', True)
    l_bytes = lpwm.to_bytes(2, 'big', True)
    return bytes([146])+r_bytes+l_bytes

def motors(side, vacuum, main, reverse_side, reverse_main):
    byte = 0
    if side:
        byte |= 1
    if vacuum:
        byte |= 2
    if main:
        byte |= 4
    if reverse_side:
        byte |= 8
    if reverse_main:
        byte |= 16
    return bytes([138, byte])

def pwm_motors(main, side, vacuum):
    if not (-127 <= main <= 127):
        raise ValueError("Invalid main pwm")
    if not (-127 <= side <= 127):
        raise ValueError("Invalid side pwm")
    if not (0 <= vacuum <= 127):
        raise ValueError("Invalid vacuum pwm")
    return bytes([144, main, side, vacuum])

def leds(check, dock, spot, debris, clean):
    bits = 0
    if check:
        bits |= 1
    if spot:
        bits |= 2
    if dock:
        bits |= 4
    if check:
        bits |= 8

    color, intensity = clean
    if not (0 <= color <= 255):
        raise ValueError("Invalid clean light color")
    if not (0 <= intensity <= 255):
        raise ValueError("Invalid clean light intensity")
    return bytes([139, bits, color, intensity])

def buttons(clock=False, schedule=False, day=False, hour=False,
            minute=False, dock=False, spot=False, clean=False):
    bits = 0
    if clean:
        bits |= 1
    if spot:
        bits |= 2
    if dock:
        bits |= 4
    if minute:
        bits |= 8
    if hour:
        bits |= 16
    if day:
        bits |= 32
    if schedule:
        bits |= 64
    if clock:
        bits |= 128
    return bytes([165, bits])

def song(slot, song):
    length = len(song)
    if not (0 <= slot <= 4):
        raise ValueError("Invalid song slot")
    if not all( [ 0 <= note <= 255 for (note, _) in song ] ):
        raise ValueError("Invalid note in song")
    if not all( [ 0 <= duraction <= 255 for (_, duration) in song ]):
        raise ValueError("Invalid duration in song")
    if not (1 <= length <= 16):
        raise ValueError("Song too long")
    return bytes([140, slot, length] + [ item for sublist in l for item in sublist ])

def play(slot):
    if not (0 <= slot <= 4):
        raise ValueError("Invalid song slot")
    return bytes([141, slot])
