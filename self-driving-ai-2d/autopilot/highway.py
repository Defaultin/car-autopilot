import numpy as np
import pygame as pg
from math import pi, sin, cos, sqrt, acos, degrees
from scipy.interpolate import splprep, splev

__all__ = "Highway"


class Highway:
    """Highway based on a random-generated curve"""
    def __init__(self, position, spread=(250, 350), complexity=3, width=30):
        self.grass_color = 63, 155, 11, 255
        self.markup_color = 255, 255, 255, 255
        self.road_color = 80, 80, 80, 255
        self.pointers_color = 242, 188, 10, 255
        self.road_pointers_color = 161, 134, 45, 255

        self.x, self.y = position
        self.min_uniform, self.max_uniform = spread
        self.complexity = complexity
        self.width = width
        self.highway_curve = None
        self.highway_markup = None
        self.start_position = 0, 0
        self.start_angle = 0
        self.generate()

    def generate(self, points_num=1000):
        """Generates a random curve using random circle polarization and B-spline"""
        # random curve interpolation
        rho = np.random.uniform(self.min_uniform, self.max_uniform, size=2 * self.complexity)
        phi = np.arange(0, 2 * pi, pi / self.complexity)
        points = np.array([(self.x + r * cos(p), self.y + r * sin(p)) for r, p in zip(rho, phi)])
        tck, u = splprep(points.T, s=0.0, per=1)

        # highway curve and markup generation
        self.highway_curve = np.c_[splev(np.linspace(u.min(), u.max(), points_num), tck, der=0)].T
        self.highway_markup = np.array_split(self.highway_curve, 5 * points_num // self.width)[::2]

        # start car position and angle computation
        idx = points_num // 10
        (x1, y1), (x2, y2) = self.highway_curve[idx], self.highway_curve[idx + self.width]
        self.start_position = x1, y1
        self.start_angle = 180 - degrees(acos((x2 - x1) / sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)))

    def draw(self, screen):
        """Renders highway curve and its markup"""
        screen.fill(self.grass_color)
        for coord in self.highway_curve:
            pg.draw.circle(screen, self.markup_color, coord, 1.1 * self.width)
        for coord in self.highway_curve:
            pg.draw.circle(screen, self.road_color, coord, self.width)
        for pts in self.highway_markup:
            pg.draw.aalines(screen, self.pointers_color, False, pts)
