from pygcode import *

'''
line.comment.text   # comment text
line.block.gcodes   # list of G-codes
line.block.modal_params # list of modal parameters
line.godes[0].description # G-code description (e.g. 'G1')
F or Feed Rate is in mm/min
'''

def read_file(file_name, n):
    line = ''
    actions = []
    z_val = 0.0
    layer_num = 0
    # check if file exists
    try:
        f = open(file_name)
        f.close()
    except FileNotFoundError:
        print("Error: File not found!")
        print("path:", file_name)
        exit()
    with open(file_name, 'r') as f:
        for block in f.readlines():
            # get gcode object
            if 'M84' in block:
                # disables steppers, means code is done
                # cont because lib doesn't handle this
                continue
            else:
                line = Line(block)

            if 'M104' in line.text:
                # set extruder temp
                e_val = float(str(line.text.split('S')[-1].split(';')[0]))
                if e_val > 0:
                    e_temp = e_val
                continue
            #line.block.gcodes   # list of G-codes
            #line.block.modal_params # list of modal parameters
            if line.comment:
                if 'LAYER:' in line.comment.text:
                    # get layer number
                    layer_num = int(line.comment.text.split(':')[-1].split(';')[0])
            
            if len(line.block.gcodes) > 0 and layer_num % n == 0:
                try:
                    if 'G0' in line.gcodes[0].description or 'G1' in line.gcodes[0].description:
                        s = line.gcodes[0].params
                        if 'E' in line.text:
                            e_pos = float(str(line.text.split('E')[-1].split(' ')[0]))
                            s['E'] = e_pos
                        if 'F' in line.text:
                            f_rate = float(str(line.text.split('F')[-1].split(' ')[0]))
                            s['F'] = f_rate

                        actions.append(s)
                        if 'Z' in s and s['Z'] != z_val:
                            z_val = s['Z']
                            layer_num += 1
                except AttributeError:
                    continue
    return actions, e_temp

def get_end_points(file_path, n):
    # currently getting every nth layer
    moves, e_temp = read_file(file_path, n)
    pts = []
    f_rate = 0.0
    e_pos = 0.0
    z_last = 0.0
    x_last = 0.0
    y_last = 0.0
    for move in moves:
        x = float(str(move['X'])[1:]) if 'X' in move else x_last
        y = float(str(move['Y'])[1:]) if 'Y' in move else y_last
        z = float(str(move['Z'])[1:]) if 'Z' in move else z_last
        # check if extruding
        e = move['E'] if 'E' in move else e_pos
        # check if speed has changed
        f = move['F'] if 'F' in move else f_rate
        # tmp only add if extruding
        ex = e_pos < e
        f_rate = f
        e_pos = e
        x_last = x
        y_last = y
        z_last = z
        pts.append([x, y, z, f, ex])
    return pts, e_temp
