import pygame
import math
import numpy as np


class Projection:
    def __init__(self):
        self.update_projection_matrix()

    def update_projection_matrix(self):
        self.projection_matrix = [[1,0,0],
                            [0,1,0],
                            [0,0,1]]
        
    def get_rotation_x(self, angle_x) -> list:
        rotation_x = [[1, 0, 0],
                    [0, math.cos(angle_x), -math.sin(angle_x)],
                    [0, math.sin(angle_x), math.cos(angle_x)]]
        return rotation_x

    def get_rotation_y(self, angle_y) -> list:
        rotation_y = [[math.cos(angle_y), 0, math.sin(angle_y)],
                        [0, 1, 0],
                        [-math.sin(angle_y), 0, math.cos(angle_y)]]
        return rotation_y

    def get_rotation_z(self, angle_z) -> list:
        rotation_z = [[math.cos(angle_z), -math.sin(angle_z), 0],
                        [math.sin(angle_z), math.cos(angle_z), 0],
                        [0, 0, 1]]
        return rotation_z
    

class Cube:
    
    def __init__(self):
        self.ROTATE_SPEED = 0.02
        self.projection = Projection()
        
        print(self.projection.projection_matrix)

        self.cube_points = [n for n in range(8)]
        self.cube_points[0] = [[-1], [-1], [1]]
        self.cube_points[1] = [[1],[-1],[1]]
        self.cube_points[2] = [[1],[1],[1]]
        self.cube_points[3] = [[-1],[1],[1]]
        self.cube_points[4] = [[-1],[-1],[-1]]
        self.cube_points[5] = [[1],[-1],[-1]]
        self.cube_points[6] = [[1],[1],[-1]]
        self.cube_points[7] = [[-1],[1],[-1]]

    def connect_points(self, surf, i, j, points) -> None:
        pygame.draw.line(surf, (255, 255, 255), (points[i][0], points[i][1]) , (points[j][0], points[j][1]))

    def fill_faces(self, points : np, surf, color=(255, 255, 255)):
        faces =[[0, 1, 2, 3],
                [0, 4, 5, 1],
                [4, 5, 6, 7],
                [3, 7, 6, 2],
                [0, 3, 7, 4],
                [1, 2, 6, 5]]
        for face in faces:
            face_points = []
            for point in face:
                face_points.append(points[point])
            pygame.draw.polygon(surf, color, face_points)

    def render(self, surf, angle_x=0, angle_y=0, angle_z=0, scale=30, offset=(0,0), fill_color=None):    
        points = [0 for _ in range(len(self.cube_points))]
        i = 0

        for point in self.cube_points:
            rotate_x = np.dot(self.projection.get_rotation_x(angle_x), point)
            rotate_y = np.dot(self.projection.get_rotation_y(angle_y), rotate_x)
            rotate_z = np.dot(self.projection.get_rotation_z(angle_z), rotate_y)
            point_2d = np.dot(self.projection.projection_matrix, rotate_z)
            
            x = (point_2d[0][0] * scale) + offset[0]
            y = (point_2d[1][0] * scale) + offset[1]

            points[i] = (x,y)
            i += 1

        if fill_color:
            self.fill_faces(points, surf, fill_color)

        self.connect_points(surf, 0, 1, points)
        self.connect_points(surf, 0, 3, points)
        self.connect_points(surf, 0, 4, points)
        
        self.connect_points(surf, 1, 2, points)
        self.connect_points(surf, 1, 5, points)
        
        self.connect_points(surf, 2, 6, points)
        self.connect_points(surf, 2, 3, points)
        
        self.connect_points(surf, 3, 7, points)
        
        self.connect_points(surf, 4, 5, points)
        self.connect_points(surf, 4, 7, points)
        
        self.connect_points(surf,6, 5, points)
        self.connect_points(surf,6, 7, points)