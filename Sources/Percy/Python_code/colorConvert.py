#######################
#
# HEX to RGB converter
#
#######################

def hex_to_rgb(v):
    if v[0] == '#':
        v = v[1:]
    assert(len(v) == 6)
    return int(v[:2], 16), int(v[2:4], 16), int(v[4:6], 16)

def rgb_to_hex(v):
    assert(len(v) == 3)
    return '#%02x%02x%02x' % v