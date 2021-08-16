import pygame as pg
import numpy as np
from pygame.math import Vector2
from math import sqrt, sin, cos, radians, degrees, copysign

__all__ = 'Car'


class Car:
    """Kinematic model of a car with radars for calculating distances to objects"""

    def __init__(self, *, spawn_position=(0.0, 0.0), spawn_angle=0):
        self.car_sprite = pg.image.load('sprites/car0.png')
        rect = self.car_sprite.get_rect()
        self.car_sprite_width = 0.5 * rect.width - 5
        self.car_sprite_height = 0.5 * rect.height - 10
        self.chassis_length = 0.03 * rect.height

        self.angle = spawn_angle
        self.position = Vector2(*spawn_position)
        self.velocity = Vector2(0.0, 0.0)
        self.acceleration = 0.0
        self.steering = 0.0

        self.brake_deceleration = 10.0
        self.free_deceleration = 2.0

        self.max_velocity = 30.0
        self.max_acceleration = 3.0
        self.max_steering = 1.0

        self.is_alive = True
        self.score = 0

        self.show_collision_points = False
        self.show_radars = False

    def _compute_collision_points(self):
        """Calculates collision points along the sides of the car"""
        sin_alpha = sin(radians(-self.angle))
        cos_alpha = cos(radians(-self.angle))
        old_points = np.array([
            (self.position.x + self.car_sprite_width, self.position.y + self.car_sprite_height),
            (self.position.x + self.car_sprite_width, self.position.y - self.car_sprite_height),
            (self.position.x - self.car_sprite_width, self.position.y + self.car_sprite_height),
            (self.position.x - self.car_sprite_width, self.position.y - self.car_sprite_height)
        ])

        new_points = np.empty((0, 2), np.int_)
        for x, y in old_points:
            old_x, old_y = x - self.position.x, y - self.position.y
            new_x = self.position.x + old_x * cos_alpha - old_y * sin_alpha
            new_y = self.position.y + old_x * sin_alpha + old_y * cos_alpha
            new_points = np.append(new_points, [(int(new_x), int(new_y))], axis=0)

        self.collision_points = new_points

    def _check_collision(self, screen, surface):
        """Checks for collisions and reduces score for collisions with grass and markings"""
        for point in self.collision_points:
            try:
                color = screen.get_at(point)
                if color == surface.grass_color:
                    self.score -= 100
                    self.is_alive = False
                    break
                elif color == surface.markup_color:
                    self.score -= 10
                    break
                else:
                    self.score += abs(self.velocity.x) * 0.001
            except IndexError:
                self.score -= 100
                self.is_alive = False

    def _compute_radars(self, screen, surface):
        """Calculates radars and distances from car to surface facilities"""
        x, y = 0, 0
        car_angles = np.array([radians(360 - self.angle - 45 * angle) for angle in range(9)])
        self.radars = np.empty((0, 2), np.int_)
        self.radars_data = np.empty(0, np.int_)

        for angle in car_angles:
            length = 0
            while length <= 300:
                length += 1
                x = int(self.position.x + length * cos(angle))
                y = int(self.position.y + length * sin(angle))
                try:
                    color = screen.get_at((x, y))
                    if not self.check_color(color, surface):
                        break
                except IndexError:
                    break

            self.radars = np.append(self.radars, [(x, y)], axis=0)
            self.radars_data = np.append(self.radars_data, length)

    @staticmethod
    def _color_distance(*colors):
        """Calculates distance between rgb colors"""
        return sqrt(sum(map(lambda a, b: (a - b) ** 2, *colors)))

    def check_color(self, color, surface, *, limit=60):
        """Checks that the surface color matches the colors allowed for driving"""
        return any([
            self._color_distance(color, surface.road_color) < limit,
            self._color_distance(color, surface.pointers_color) < limit,
            self._color_distance(color, surface.road_pointers_color) < limit
        ])

    def _check_params(self):
        """Checks if params are out of maximum ranges"""
        self.velocity.x = max(-self.max_velocity, min(self.velocity.x, self.max_velocity))
        self.acceleration = max(-self.max_acceleration, min(self.acceleration, self.max_acceleration))
        self.steering = max(-self.max_steering, min(self.steering, self.max_steering))

    def _update(self, movement, dt):
        """Updates motion parameters according to the kinematics laws and the input direction of the car"""
        if movement["direction"] == "forward":
            if self.velocity.x < 0:
                self.acceleration = self.brake_deceleration
            else:
                self.acceleration += dt
        elif movement["direction"] == "backward":
            if self.velocity.x > 0:
                self.acceleration = -self.brake_deceleration
            else:
                self.acceleration -= dt
        elif movement["direction"] == "neutral":
            if abs(self.velocity.x) > dt * self.free_deceleration:
                self.acceleration = -copysign(self.free_deceleration, self.velocity.x)
            elif dt:
                self.acceleration = -self.velocity.x / dt

        if movement["rotation"] == "right":
            self.steering -= self.max_steering * dt
        elif movement["rotation"] == "left":
            self.steering += self.max_steering * dt
        elif movement["rotation"] == "neutral":
            self.steering = 0

        self.velocity.x += self.acceleration * dt
        self._check_params()

        if self.steering:
            turning_radius = self.chassis_length / sin(radians(self.steering))
            angular_velocity = self.velocity.x / turning_radius
        else:
            angular_velocity = 0

        self.position += self.velocity.rotate(-self.angle) * dt
        self.angle += degrees(angular_velocity) * dt

    def move(self, movement, dt, screen, surface):
        """Moves a car model according to the kinematics laws and the input direction"""
        if self.is_alive:
            self._update(movement, dt)
            self._compute_collision_points()
            self._check_collision(screen, surface)
            self._compute_radars(screen, surface)

    def draw(self, screen):
        """Renders a car model with radars and collision points"""
        if self.show_radars:
            for coord in self.radars:
                pg.draw.line(screen, (255, 140, 0), self.position, coord, 1)
                pg.draw.circle(screen, (255, 140, 0), coord, 5)

        if self.show_collision_points:
            for coord in self.collision_points:
                if self.is_alive:
                    pg.draw.circle(screen, (15, 192, 252), coord, 5)
                else:
                    pg.draw.circle(screen, (255, 0, 0), coord, 5)

        rotated = pg.transform.rotate(self.car_sprite, self.angle)
        rect = rotated.get_rect()
        screen.blit(rotated, self.position - Vector2(rect.width / 2, rect.height / 2))
