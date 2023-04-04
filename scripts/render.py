import pygame, math
import numpy as np
import simulator as sim

# window settings
sc_width = 800
sc_height = 600
fps = 60
pause = False

def project(angle_x, angle_y, vertices, center_pt, scale):
    # x and y rotation axes are swapped
    rotation_matrix_y = [
        [1,0,0],
        [0, math.cos(angle_y), math.sin(angle_y)],
        [0, -math.sin(angle_y), math.cos(angle_y)],
    ]

    rotation_matrix_x = [
        [math.cos(angle_x), 0, math.sin(angle_x)],
        [0,1,0],
        [-math.sin(angle_x), 0, math.cos(angle_x)],
    ]

    rotation_matrix = np.matmul(rotation_matrix_x, rotation_matrix_y)

    z = 0.5
    # projection matrix
    proj_matrix = [
        [z, 0, 0],
        [0, z, 0]
    ]

    # compute final matrix
    proj_matrix = np.matmul(proj_matrix, rotation_matrix)
    proj_verts = []

    # project vertices to 2d coords
    for p in vertices:
        projected = np.matmul(proj_matrix, np.transpose(p))
        # apply scale
        projected = [projected[i] * scale for i in range(len(projected))]
        # apply center point
        for i in range(0,len(projected),2):
            projected[i] += center_pt['x']
            projected[i+1] += center_pt['y']
        proj_verts.append(projected)
    
    return proj_verts

def draw_tube(start, end, radius):
    # given a start point, end point, and radius draw a tube
    pass

def start_game():
    # init pygame settings
    pygame.init()
    pygame.display.set_caption("Sliced Simulator")
    screen = pygame.display.set_mode((sc_width, sc_height))
    clock = pygame.time.Clock()
    cube_center = {'y': sc_height // 2, 'x': sc_width // 2}


    # colors
    bkg = (240, 235, 240)
    shape = (255, 0, 70)
    circle_color = (255, 0, 70)

    # points
    cube_vertices = [
        [-1, -1, 1],
        [1,-1,1],
        [1, 1, 1],
        [-1, 1, 1],
        [-1, -1, -1],
        [1, -1, -1],
        [1, 1, -1],
        [-1, 1, -1]
    ]

    # cube sides, each entry is an index in cube_vertices:
    cube_sides = [
        [0, 1, 2, 3],
        [4, 5, 6, 7],
        [1, 2, 6, 5],
        [0, 3, 7, 4],
        [0, 1, 5, 4],
        [2, 3, 7, 6]
    ]

    angle_x = 0
    angle_y = 0
    running = True
    pause = False
    move_view = False
    m_pos = (0,0)
    sim_pts = sim.get_points()
    # get center of points
    ax = ay = az = 0
    for pt in sim_pts:
        ax += pt[0]
        ay += pt[1]
        az += pt[2]
    ax /= len(sim_pts)
    ay /= len(sim_pts)
    az /= len(sim_pts)
    # normalize points to be in range [-1,1]
    max_x, max_y, max_z = 1,1,1
    for pt in sim_pts:
        if pt[0] > max_x:
            max_x = pt[0]
        if pt[1] > max_y:
            max_y = pt[1]
        if pt[2] > max_z:
            max_z = pt[2]
    m = max(max_x, max_y, max_z)
    for pt in sim_pts:
        pt[0] = (pt[0] - ax) / m
        pt[1] = (pt[1] - ay) / m
        pt[2] = (pt[2] - az) / m
    
    scale = m * 10
    
    # game loop
    while running:
        clock.tick(fps)
        screen.fill(bkg)

        # process window events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pause = not pause
            # mouse events
            # zoom in/out events
            if event.type == pygame.MOUSEWHEEL:
                scale += event.y * 10
                scale = scale if scale > 10 else 10
            # moving view events
            if not move_view and event.type == pygame.MOUSEBUTTONDOWN:
                move_view = True
            elif move_view and event.type == pygame.MOUSEBUTTONUP:
                move_view = False
            if move_view:
                cm_pos = pygame.mouse.get_pos()
                angle_x += (cm_pos[0] - m_pos[0]) / 100
                angle_y += (cm_pos[1] - m_pos[1]) / 100
                m_pos = cm_pos

        # project points from 3d to 2d
        proj_verts = project(angle_x, angle_y, sim_pts, cube_center, scale)
        #proj_verts = project(angle_x, angle_y, sim_pts, proj_center, scale)

        # draw vertices as circles:
        for p in proj_verts:
            if p[0] > 0 and p[1] > 0 and p[0] < sc_width and p[1] < sc_height:
                pygame.draw.circle(screen, circle_color, (p[0], p[1]), 8)
        
        # draw cube sides:
        '''
        counter = 1
        for side in cube_sides:
            side_coords = [
                (proj_verts[side[0]][0], proj_verts[side[0]][1]),
                (proj_verts[side[1]][0], proj_verts[side[1]][1]),
                (proj_verts[side[2]][0], proj_verts[side[2]][1]),
                (proj_verts[side[3]][0], proj_verts[side[3]][1])
            ]
            pygame.draw.polygon(screen, (
                int(shape[0] * counter * 0.05), int(shape[1] * counter * 0.05),
                int(shape[2] * counter * 0.05)), side_coords)
            counter += 1
            '''
            
        # present the new image to screen:
        if not pause:
            pygame.display.update()
        

    pygame.quit()

if __name__ == "__main__":
    start_game()