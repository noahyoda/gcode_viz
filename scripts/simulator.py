import parse

'''
This file will be used to get points from the parser and report
the shapes/points/colors to be drawn in the render.
'''


def get_points():
    '''
    This function will be used to get points from the parser
    and report the shapes/points/colors to be drawn in the render.
    '''
    # get the points from the parser
    pts = parse.get_end_points()
    # get the colors from the parser
    # [TODO] do in simulation step
    return pts