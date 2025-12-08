import json
from colorsys import rgb_to_hls, rgb_to_hsv

fl = open('names.json')
db = json.loads(fl.read())
fl.close()

del fl

def hex2rgb(value: str):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

def rgb2hex(values):
    r, g, b = values
    return '%02x%02x%02x' % (r, g, b)

def hexbycolorname(name: str):
    if name in db.keys():
        rgb = db[name]
        hex = '%02x%02x%02x' % (rgb[0], rgb[1], rgb[2])
        return hex
    else:
        return False
    
def colornamebyhex(hex: str):
    for i in db.keys():
        rgb = hex2rgb(hex)
        rgb = (rgb[0], rgb[1], rgb[2])
        if db[i] == rgb:
            return i
    return False
    
def nearestcolor(hex: str):
    rgb = hex2rgb(hex)
    result = ['', 10000, '']
    for i in db.keys():
        diff = 0
        diff += abs(rgb[0] - db[i][0])
        diff += abs(rgb[1] - db[i][1])
        diff += abs(rgb[2] - db[i][2])
        if diff < result[1]:
            result[0] = i
            result[1] = diff
            result[2] = db[i]
        
    return result, rgb2hex(result[2])

def rgb2cmyk(r, g, b):
    if (r, g, b) == (0, 0, 0):
        return 0, 0, 0, 100

    c = 1 - r / 255
    m = 1 - g / 255
    y = 1 - b / 255

    min_cmy = min(c, m, y)
    c = (c - min_cmy) / (1 - min_cmy)
    m = (m - min_cmy) / (1 - min_cmy)
    y = (y - min_cmy) / (1 - min_cmy)
    k = min_cmy

    return c * 100, m * 100, y * 100, k * 100

def ishex(color):
    if len(color) != 6 or not all(c in "0123456789ABCDEFabcdef" for c in color):
        if len(color[1:]) != 6 or not all(c in "0123456789ABCDEFabcdef" for c in color[1:]):
            return False
        else:
            return True
    else:
        return True

def isnum(num):
    try:
        num = int(num)
        return True
    except ValueError:
        return False

def generate(color):
    name, nearestnamedhex = nearestcolor(color)

    name = name[0]

    if color != nearestnamedhex: name += f' (#<code>{nearestnamedhex}</code>)'

    rgb = hex2rgb(color)
    hsv = rgb_to_hsv(rgb[0], rgb[1], rgb[2])
    hls = rgb_to_hls(rgb[0], rgb[1], rgb[2])
    cmyk = rgb2cmyk(rgb[0], rgb[1], rgb[2])

    newhsv = []
    newhls = []
    newcmyk = []

    for i in range(len(hsv)):
        newhsv.append(round(hsv[i], 2))

    for i in range(len(hls)):
        newhls.append(round(hls[i], 2))
    
    for i in range(len(cmyk)):
        newcmyk.append(round(cmyk[i], 2))

    hsv = f"({newhsv[0]}, {newhsv[1]}, {newhsv[2]})"
    hsl = f"({newhls[0]}, {newhls[2]}%, {newhls[1]}%)"
    cmyk = f"({newcmyk[0]}%, {newcmyk[1]}%, {newcmyk[2]}%, {newcmyk[3]}%)"

    return [color, name, rgb, hsv, hsl, cmyk]

def makeresponse(values, query_text, template):
    color, name, rgb, hsv, hsl, cmyk = values
    return template.replace("<input>", query_text)\
        .replace("<hex>", f"{color}")\
        .replace("<name>", name)\
        .replace("<rgb>", f"({rgb[0]}, {rgb[1]}, {rgb[2]})")\
        .replace("<hsv>", hsv)\
        .replace("<hsl>", hsl)\
        .replace("<cmyk>", cmyk)