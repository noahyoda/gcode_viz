from pygcode import *
from matplotlib import pyplot as plt

def read_file(file_name):
    line = ''
    actions = []
    with open(file_name, 'r') as f:
        for block in f.readlines():
            #print(block)
            if 'M84' in block:
                # disables steppers, means code is done
                # cont because lib doesn't handle this
                continue
            else:
                line = Line(block)
            #print(line)

            line.block.gcodes   # list of G-codes
            line.block.modal_params # list of modal parameters
            if line.comment:
                line.comment.text   # comment text
                if 'LAYER:1' in line.comment.text:
                    return actions
            
            if len(line.block.gcodes) > 0:
                #print(line.block.gcodes[0])
                try:
                    if 'G0' in line.gcodes[0].description or 'G1' in line.gcodes[0].description:
                        #print('Move found: ', line.gcodes[0].params)
                        actions.append(line.gcodes[0].params)
                except AttributeError:
                    continue
    return actions

def main():
    moves = read_file('./cube.gcode')
    print(float(str(moves[50]['X'])[1:]))
    pts = []
    for move in moves:
        x = float(str(move['X'])[1:]) if 'X' in move else 0.0
        y = float(str(move['Y'])[1:]) if 'Y' in move else 0.0
        pts.append([x, y])
    # plot pts
    x = [pt[0] for pt in pts]
    y = [pt[1] for pt in pts]
    plt.plot(x, y)
    plt.show()

if __name__ == '__main__':
    main()
