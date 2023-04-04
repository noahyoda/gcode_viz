import parse

'''
This file will be used to get points from the parser and report
the shapes/points/colors to be drawn in the render.
'''
class step:
    def __init__(self, start=(0,0,0), end=(0,0,0), color=(255, 0, 70)):
        self.start = start
        self.end = end
        self.color = color
    

def get_shapes():
    # tmp function to draw lines between points
    pass


def get_points():
    '''
    This function will be used to get points from the parser
    and report the shapes/points/colors to be drawn in the render.
    '''
    # get the points from the parser
    pts = parse.get_end_points()[1:]

    # get the colors from the parser
    # [TODO] do in simulation step
    return pts