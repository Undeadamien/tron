import pygame

from direction import Direction


class Player:
    def __init__(self, surface, direction, color, grid_color, controls):
        self.surface = surface
        self.rect = pygame.rect.Rect(0, 0, 10, 10)
        self.direction = direction
        self.color = pygame.Color(color)
        self.grid_color = pygame.Color(grid_color)
        self.collided = False
        self.controls = controls

    def rotate(self, direction):
        # return if vectors act on the same direction (0,-1) and (0,1)
        if self.direction.value[0] == direction.value[0]:
            return
        if self.direction.value[1] == direction.value[1]:
            return
        self.direction = direction

    def move(self):
        self.rect.move_ip(self.direction.value)

    def render(self):
        pygame.draw.rect(self.surface, self.color, self.rect)
        if self.collided:
            pygame.draw.circle(
                self.surface,
                self.color,
                self.rect.center,
                self.rect.width * 1.5,
            )

    def check_collision(self):
        # determine the collision points for the next position
        if self.direction == Direction.LEFT:
            new_rect = self.rect.move(-1, 0)
            points = [new_rect.topleft, new_rect.bottomleft]
        elif self.direction == Direction.RIGHT:
            new_rect = self.rect.move(1, 0)
            points = [new_rect.topright, new_rect.bottomright]
        elif self.direction == Direction.UP:
            new_rect = self.rect.move(0, -1)
            points = [new_rect.topleft, new_rect.topright]
        elif self.direction == Direction.DOWN:
            new_rect = self.rect.move(0, 1)
            points = [new_rect.bottomleft, new_rect.bottomright]

        # check the color at those points
        def check_point(point):
            return self.surface.get_at(point) != self.grid_color

        try:
            if any(filter(check_point, points)):
                self.collided = True
        except IndexError:  # error when points are out of bound
            self.collided = True

    def has_collided(self):
        return self.collided

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == self.controls.get("up"):
                self.rotate(Direction.UP)
            elif event.key == self.controls.get("down"):
                self.rotate(Direction.DOWN)
            elif event.key == self.controls.get("left"):
                self.rotate(Direction.LEFT)
            elif event.key == self.controls.get("right"):
                self.rotate(Direction.RIGHT)

    def update(self):
        self.move()
        self.check_collision()
        self.render()
