import pygame as pg
import numpy as np
from pygame.math import Vector2
from math import sqrt, sin, cos, radians, degrees, copysign

__all__ = "Car"


class Car:
    """Kinematic model of a car with radars for calculating distances to objects"""

    def __init__(self, spawn_position=(0.0, 0.0), spawn_angle=0, scale=1,
                 show_collision=False, show_radars=False, show_score=False):
        sprite = pg.image.load(f"autopilot/sprites/car0.png")
        rect = sprite.get_rect()
        w, h = round(rect.width * scale), round(rect.height * scale)
        self.car_sprite = pg.transform.scale(sprite, (w, h))
        self.car_sprite_width = 0.5 * w - 5
        self.car_sprite_height = 0.5 * h - 10
        self.chassis_length = 0.03 * h

        self.angle = spawn_angle
        self.position = Vector2(*spawn_position)
        self.velocity = Vector2(0.0, 0.0)
        self.acceleration = 0.0
        self.steering = 0.0

        self.brake_deceleration = 10.0 * scale
        self.free_deceleration = 2.0 * scale

        self.max_velocity = 50.0 * scale
        self.max_acceleration = 3.0 * scale
        self.max_steering = 1.5 * scale
        self.max_radar_len = int(300 * scale)

        self.is_alive = True
        self.parked = False
        self.scale = scale
        self.radars_data = np.zeros(8, np.int_)

        self.target_distance = 0
        self.start_distance = 0
        self.distance_score = 0
        self.movement_score = 0
        self.score = 0

        self.show_collision_points = show_collision
        self.show_radars = show_radars
        self.show_score = show_score

    def _update(self, movement, dt):
        """Updates motion parameters according to the kinematics laws and the input direction of the car"""
        # update acceleration
        if movement["direction"] in {1, "forward"}:
            if self.velocity.x < 0:
                self.acceleration = self.brake_deceleration
            else:
                self.acceleration += dt
        elif movement["direction"] in {-1, "backward"}:
            if self.velocity.x > 0:
                self.acceleration = -self.brake_deceleration
            else:
                self.acceleration -= dt
        elif movement["direction"] in {0, "neutral"}:
            if abs(self.velocity.x) > dt * self.free_deceleration:
                self.acceleration = -copysign(self.free_deceleration, self.velocity.x)
            elif dt:
                self.acceleration = -self.velocity.x / dt

        # update steering
        if movement["rotation"] in {1, "right"}:
            self.steering -= self.max_steering * dt
        elif movement["rotation"] in {-1, "left"}:
            self.steering += self.max_steering * dt
        elif movement["rotation"] in {0, "neutral"}:
            self.steering = 0

        # update velocity
        self.velocity.x += self.acceleration * dt
        self._check_params()

        # update position and angle
        if self.steering:
            turning_radius = self.chassis_length / sin(radians(self.steering))
            angular_velocity = self.velocity.x / turning_radius
        else:
            angular_velocity = 0

        self.position += self.velocity.rotate(-self.angle) * dt
        self.angle += degrees(angular_velocity) * dt

    def _check_params(self):
        """Checks if params are out of maximum ranges"""
        self.velocity.x = max(-self.max_velocity, min(self.velocity.x, self.max_velocity))
        self.acceleration = max(-self.max_acceleration, min(self.acceleration, self.max_acceleration))
        self.steering = max(-self.max_steering, min(self.steering, self.max_steering))

    def _stop(self):
        """Stops a car model"""
        self.is_alive = False
        self.acceleration = 0
        self.velocity.x = 0
        self.steering = 0

    def _compute_collision_points(self):
        """Calculates collision points along the sides of the car"""
        sin_alpha = sin(radians(-self.angle))
        cos_alpha = cos(radians(-self.angle))

        left, right = self.position.x - self.car_sprite_width, self.position.x + self.car_sprite_width
        bottom, top = self.position.y - self.car_sprite_height, self.position.y + self.car_sprite_height

        old_points = np.array([(right, top), (right, bottom), (left, top), (left, bottom)])
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
            if not self._safe_position(point, screen, surface):
                self.movement_score -= 10
                self._stop()
                break

    def _compute_radars(self, screen, surface):
        """Calculates radars and distances from car to surface facilities"""
        car_angles = np.array([radians(90 - self.angle - 45 * angle) for angle in range(8)])
        self.radars = np.empty((0, 2), np.int_)
        self.radars_data = np.empty(0, np.int_)

        for angle in car_angles:
            for length in range(1, self.max_radar_len + 1):
                x = int(self.position.x + length * cos(angle))
                y = int(self.position.y + length * sin(angle))
                if not self._safe_position((x, y), screen, surface):
                    self.radars = np.append(self.radars, [(x, y)], axis=0)
                    self.radars_data = np.append(self.radars_data, length / self.max_radar_len)
                    break

    def _safe_position(self, position, screen, surface, *, limit=60):
        """Checks that the color on surface matches the colors allowed for safe driving"""
        try:
            color = screen.get_at(position)
            return any([
                self._compute_distance(color, surface.road_color) < limit,
                self._compute_distance(color, surface.pointers_color) < limit,
                self._compute_distance(color, surface.road_pointers_color) < limit
            ])
        except IndexError:
            return False

    @staticmethod
    def _compute_distance(*points):
        """Calculates distance between points"""
        return sqrt(sum(map(lambda a, b: (a - b) ** 2, *points)))

    def _compute_target_distance(self, surface):
        """Calculates distance ratio depending on the proximity to the target"""
        distance = self._compute_distance(self.position, surface.get_target_position())
        if not self.start_distance:
            self.start_distance = distance
        ratio = -distance / self.start_distance + 1
        self.target_distance = ratio if ratio > 0 else 0

    def _compute_score(self):
        """Charges score points according to driving quality and target distance"""
        self.movement_score -= 0.1 if abs(self.velocity.x) < 1 else 0.01
        self.distance_score = 100 * self.target_distance
        if self.distance_score > 99:
            self.distance_score = 1000
            self._stop()
            self.parked = True
        self.score = self.distance_score + self.movement_score

    def move(self, movement, dt, screen, surface):
        """Moves a car model according to the kinematics laws and the input direction"""
        if self.is_alive:
            self._update(movement, dt)
            self._compute_collision_points()
            self._check_collision(screen, surface)
            self._compute_radars(screen, surface)
            self._compute_target_distance(surface)
            self._compute_score()

    def draw(self, screen):
        """Renders a car model with radars and collision points"""
        if self.is_alive and self.show_radars:
            for coord in self.radars:
                pg.draw.aaline(screen, (255, 140, 0), self.position, coord, 1)
                pg.draw.circle(screen, (255, 140, 0), coord, 5)

        if self.show_collision_points:
            for coord in self.collision_points:
                if self.is_alive:
                    pg.draw.circle(screen, (15, 192, 252), coord, 5)
                elif self.parked:
                    pg.draw.circle(screen, (0, 255, 0), coord, 5)
                else:
                    pg.draw.circle(screen, (255, 0, 0), coord, 5)

        rotated = pg.transform.rotate(self.car_sprite, self.angle)
        rect = rotated.get_rect()
        screen.blit(rotated, self.position - Vector2(rect.width / 2, rect.height / 2))

        if self.show_score:
            font = pg.font.SysFont("Comic Sans MS", int(20 * self.scale))
            label = font.render(str(round(self.score)), True, (0, 0, 0))
            label_rect = label.get_rect()
            label_rect.center = self.position
            screen.blit(label, label_rect)
