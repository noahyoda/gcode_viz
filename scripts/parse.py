import sys
from pygcode import *
from matplotlib import pyplot as plt

'''
line.comment.text   # comment text
line.block.gcodes   # list of G-codes
line.block.modal_params # list of modal parameters
line.godes[0].description # G-code description (e.g. 'G1')
F or Feed Rate is in mm/min
'''

def read_file(file_name, layer_nums):
    line = ''
    actions = []
    reading = False
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
                    if layer_num not in layer_nums and layer_nums != []:
                        reading = False
                    else:
                        reading = True
                        continue
            
            if len(line.block.gcodes) > 0 and reading:
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
                except AttributeError:
                    continue
    return actions, e_temp

def get_end_points():
    # currently getting every 5th layer, pass empty list to get all layers
    layers = [i for i in range(0, 200, 10)]
    moves, e_temp = read_file('/home/nDev/Documents/school/sci_viz/singed_slices/samples/cube.gcode', layers)
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
        #if e_pos < e:
        #    pts.append([x, y, z, f])
        ex = e_pos < e
        f_rate = f
        e_pos = e
        x_last = x
        y_last = y
        z_last = z
        pts.append([x, y, z, f, ex])
    return pts, e_temp

def main(layer):
    #layers = [i for i in range(0, 200, 10)]
    #layers = [i for i in range(1, 200, 5)]
    layers = [0]
    moves = read_file('/home/nDev/Documents/school/sci_viz/singed_slices/samples/cube.gcode', layers)
    pts = []
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
        # tmp only add if extruding
        if e_pos < e:
            pts.append([x, y, z])
        e_pos = e
        x_last = x
        y_last = y
        z_last = z
    # plot pts
    x = [pt[0] for pt in pts]
    y = [pt[1] for pt in pts]
    z = [pt[2] for pt in pts]
    print("pts count:", len(pts))
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.set_xlim(0, 200)
    ax.set_ylim(0, 200)
    ax.set_zlim(0, 40)
    ax.scatter(x, y, z)
    #plt.show()

    plt.clf()
    plt.scatter(x, y)
    plt.show()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(int(sys.argv[1]))
    else:
        main(0)
