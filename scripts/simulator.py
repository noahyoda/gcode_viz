import parse

'''
This file will be used to get points from the parser and report
the shapes/points/colors to be drawn in the render.
'''

class StepObj:
    def __init__(self, start=(0,0,0), end=(0,0,0), color=(255, 0, 70)):
        self.start = start
        self.end = end
        self.color = color

class Sim:
    def __init__(self):
        # sim vars
        self.pts = parse.get_end_points()[1:]
        self.dt = 0.1    # time step in seconds
        self.step_counter = 0    # step counter
        self.steps = []
        self.e_temp = parse.e_temp
        # step vars
        self.f_rate = self.pts[0][3]
        self.x_pos = self.pts[0][0]
        self.y_pos = self.pts[0][1]
        self.z_pos = self.pts[0][2]

    def get_color_temp(self, temp):
        return (255, 0, 70)

    def get_next_point(self, curr, next, f_rate, dt):
        '''
        This function will be used to get the next point in the simulation
        '''
        # get the distance between the current point and the next point
        dist = ((next[0] - curr[0])**2 + (next[1] - curr[1])**2 + (next[2] - curr[2])**2)**0.5
        
        # dist traveled = rate * time step
        dist_travel = f_rate * dt

        # give distance (magnitude) find next point off of curr in direction of next
        t = dist_travel / dist if dist_travel <= dist else 1
        x = (1 - t) * curr[0] + t * next[0]
        y = (1 - t) * curr[1] + t * next[1]
        z = (1 - t) * curr[2] + t * next[2]

        return [x, y, z]

    def step(self):
        '''
        This function will be used to update the simulation
        '''
        # first move to next point
        self.step_counter += 1
        next = self.pts[self.step_counter]
        # do math to get next point between current and next given f_rate and dt
        f_rate = next[3] / 60   # convert mm/min to mm/sec
        next_point = self.get_next_point([self.x_pos, self.y_pos, self.z_pos], next, f_rate, self.dt)
        
        # then create step object 
        curr = StepObj([self.x_pos, self.y_pos, self.z_pos], next_point, self.get_color_temp(self.e_temp))
        # update position vars
        self.x_pos = next_point[0]
        self.y_pos = next_point[1]
        self.z_pos = next_point[2]

        # then add step object to steps list
        self.steps.append(curr)

        # [TODO] everything below
        # then update temperatures and step colors
        # then return steps list
        return self.steps

    def get_center(self):
        # get center of points
        ax = ay = az = 0
        for pt in self.pts:
            ax += pt[0]
            ay += pt[1]
            az += pt[2]
        ax /= len(self.pts)
        ay /= len(self.pts)
        az /= len(self.pts)
        # normalize points to be in range [-1,1]
        max_x, max_y, max_z = 1,1,1
        for pt in self.pts:
            if pt[0] > max_x:
                max_x = pt[0]
            if pt[1] > max_y:
                max_y = pt[1]
            if pt[2] > max_z:
                max_z = pt[2]
        m = max(max_x, max_y, max_z)
        
        return [ax, ay, az], m

# tmp function for debugging renderer
def get_points():
    # get the points from the parser
    pts = parse.get_end_points()[1:]

    return pts