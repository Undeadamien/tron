import pygame

from direction import Direction
from player import Player

P1 = {
    "color": "red",
    "control": {
        "up": pygame.K_w,
        "down": pygame.K_s,
        "left": pygame.K_a,
        "right": pygame.K_d,
    },
}

P2 = {
    "color": "lightpink",
    "control": {
        "up": pygame.K_UP,
        "down": pygame.K_DOWN,
        "left": pygame.K_LEFT,
        "right": pygame.K_RIGHT,
    },
}


class Game:
    def __init__(self):
        pygame.display.set_caption("War")
        self.surface = pygame.display.set_mode((800, 800))
        self.clock = pygame.time.Clock()
        self.color = pygame.Color("black")
        self.fps = 240
        self.players = []

        self.running = True
        self.paused = True
        self.over = False

    def start(self):
        pygame.init()
        self.surface.fill(self.color)

        self.p1 = Player(
            surface=self.surface,
            direction=Direction.RIGHT,
            color=P1["color"],
            grid_color=self.color,
            controls=P1["control"],
        )

        self.p2 = Player(
            surface=self.surface,
            direction=Direction.LEFT,
            color=P2["color"],
            grid_color=self.color,
            controls=P2["control"],
        )

        self.players = [self.p1, self.p2]

        self.p1.rect.midleft = self.surface.get_rect().midleft
        self.p2.rect.midright = self.surface.get_rect().midright

        for player in self.players:
            player.render()
        pygame.display.update()

        self.mainloop()
        pygame.quit()

    def handle_paused_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                self.paused = False

    def handle_game_over_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            else:
                for player in self.players:
                    player.handle_event(event)

    def update_game_logics(self):
        for player in self.players:
            player.update()
        if any(player.has_collided() for player in self.players):
            self.over = True

    def mainloop(self):
        while self.running:
            if self.paused:
                self.handle_paused_events()
                continue

            if self.over:
                self.handle_game_over_events()
                continue

            self.handle_events()
            self.update_game_logics()

            self.clock.tick(self.fps)
            pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.start()
