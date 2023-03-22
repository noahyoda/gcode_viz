import pygame, math
import numpy as np

# window settings
sc_width = 800
sc_height = 600
fps = 60
pause = False

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

    angle = 0
    scale = 200
    running = True
    pause = False

    # game loop
    while running:
        clock.tick(fps)
        screen.fill(bkg)
        angle += 0.02

        # process window events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pause = not pause
                    
        rotation_matrix = [
            [1,0,0],
            [0, math.cos(angle), -math.sin(angle)],
            [0, math.sin(angle), math.cos(angle)]
        ]

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
        for p in cube_vertices:
            projected = np.matmul(proj_matrix, np.transpose(p))
            x = cube_center['x'] + projected[0] * scale
            y = cube_center['y'] + projected[1] * scale
            proj_verts.append([x, y])

        # draw vertices as circles:
        for p in proj_verts:
            pygame.draw.circle(screen, circle_color, (p[0], p[1]), 8)

        # draw cube sides:
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

        # present the new image to screen:
        if not pause:
            pygame.display.update()
        

    pygame.quit()

if __name__ == "__main__":
    start_game()