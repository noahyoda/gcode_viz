import pygame, math, sys
import numpy as np
import simulator

# window settings
sc_width = 800
sc_height = 600
fps = 120
sim_delay = 2
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

def start_game(file, n):

    print("Initializing simulator...")
    sim = simulator.Sim(file, n)

    print("Starting game...")
    # init pygame settings
    pygame.init()
    pygame.display.set_caption("Sliced Simulator")
    screen = pygame.display.set_mode((sc_width, sc_height))
    clock = pygame.time.Clock()

    # colors
    bkg = (240, 235, 240)

    center, m = sim.get_center()
    scale = m * 5
    center = {'x': center[0], 'y': center[1], 'z': center[2]}
    offset = {'x': int(sc_width/2), 'y': int(sc_height/2)}
    angle_x = 0
    angle_y = 0
    running = True
    pause = False
    move_view = False
    m_pos = (0,0)
    sim_delay_counter = 0
    shapes = []
        
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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    offset['x'] += 50
                elif event.key == pygame.K_LEFT:
                    offset['x'] -= 50
                elif event.key == pygame.K_UP:
                    offset['y'] -= 50
                elif event.key == pygame.K_DOWN:
                    offset['y'] += 50

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
                dx = cm_pos[0] - m_pos[0]
                dy = cm_pos[1] - m_pos[1]
                if abs(dx) < 20 and abs(dy) < 20:
                    angle_x += (cm_pos[0] - m_pos[0]) / 100
                    angle_y += (cm_pos[1] - m_pos[1]) / 100
                m_pos = cm_pos

 
        if sim_delay_counter == sim_delay and not pause:
            sim_delay_counter = 0
            #shapes = sim.step()
            sim.multi_step()
            
        if not pause and sim.ready:
            shapes = sim.get_steps()
        
        for i in shapes:
            if not i.draw:
                continue
            # normalize points
            s_pos = [(i.start[0] - center['x']) / m, (i.start[1] - center['y']) / m, (i.start[2] - center['z']) / m]
            e_pos = [(i.end[0] - center['x']) / m, (i.end[1] - center['y']) / m, (i.end[2] - center['z']) / m]
            s_pos = project(angle_x, angle_y, [s_pos], center, scale)[0]
            e_pos = project(angle_x, angle_y, [e_pos], center, scale)[0]
            # apply screen offset
            s_pos = (s_pos[0] + offset['x'], s_pos[1] + offset['y'])
            e_pos = (e_pos[0] + offset['x'], e_pos[1] + offset['y'])
            # if points are within bounds draw
            if s_pos[0] > 0 and s_pos[1] > 0 and s_pos[0] < sc_width and s_pos[1] < sc_height and e_pos[0] > 0 and e_pos[1] > 0 and e_pos[0] < sc_width and e_pos[1] < sc_height:
                # apply screen offset
                pygame.draw.line(screen, i.color, s_pos, e_pos, 10)
                # draw for debugging
                #pygame.draw.circle(screen, (0, 255, 70), e_pos, 2)
        
        if not pause:
            sim_delay_counter += 1
 
        pygame.display.update()
        

    pygame.quit()

if __name__ == "__main__":
    n = 10
    if '-n' in sys.argv:
        n = int(sys.argv[sys.argv.index('-n') + 1])
    if '-f' in sys.argv:
        file = sys.argv[sys.argv.index('-f') + 1]
        start_game(file, n)
    else:
        #start_game('../samples/cube.gcode', n)
        path = '/home/nDev/Documents/school/sci_viz/singed_slices/samples/cube.gcode'
        start_game(path, n)
