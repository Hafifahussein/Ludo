import pygame
from pygame import mixer
import random
import time

class LudoGame:
    def __init__(self):
        # Initialize pygame
        pygame.init()
        pygame.display.set_caption("Ludo")
        self.screen = pygame.display.set_mode((680, 600))
        
        # Game state variables
        self.number = 1
        self.currentPlayer = 0
        self.playerKilled = False
        self.diceRolled = False
        self.winnerRank = []
        
        # Load assets
        self._load_assets()
        
        # Define constants
        self._define_constants()
        
        # Initialize fonts
        self.font = pygame.font.Font('freesansbold.ttf', 11)
        self.FONT = pygame.font.Font('freesansbold.ttf', 16)
        self.currentPlayerText = self.font.render('Current Player', True, (0, 0, 0))
        self.line = self.font.render('------------------------------------', True, (0, 0, 0))

    def _load_assets(self):
        # Load images
        self.board = pygame.image.load('asset/Board.jpg')
        self.star = pygame.image.load('asset/star.png')
        self.DICE = [
            pygame.image.load('asset/1.png'),
            pygame.image.load('asset/2.png'),
            pygame.image.load('asset/3.png'),
            pygame.image.load('asset/4.png'),
            pygame.image.load('asset/5.png'),
            pygame.image.load('asset/6.png')
        ]
        self.color = [
            pygame.image.load('asset/red.png'),
            pygame.image.load('asset/green.png'),
            pygame.image.load('asset/yellow.png'),
            pygame.image.load('asset/blue.png')
        ]
        
        # Load sounds
        self.killSound = mixer.Sound("asset/Killed.wav")
        self.tokenSound = mixer.Sound("asset/Token Movement.wav")
        self.diceSound = mixer.Sound("asset/Dice Roll.wav")
        self.winnerSound = mixer.Sound("asset/Reached Star.wav")

    def _define_constants(self):
        self.HOME = [
            [(110, 58), (61, 107), (152, 107), (110, 152)],  # Red
            [(466, 58), (418, 107), (509, 107), (466, 153)],  # Green
            [(466, 415), (418, 464), (509, 464), (466, 510)],  # Yellow
            [(110, 415), (61, 464), (152, 464), (110, 510)]   # Blue
        ]
        
        self.SAFE = [
            (50, 240), (328, 50), (520, 328), (240, 520),
            (88, 328), (240, 88), (482, 240), (328, 482)
        ]
        
        self.position = [
            [[110, 58], [61, 107], [152, 107], [110, 152]],  # Red
            [[466, 58], [418, 107], [509, 107], [466, 153]],  # Green
            [[466, 415], [418, 464], [509, 464], [466, 510]],  # Yellow
            [[110, 415], [61, 464], [152, 464], [110, 510]]   # Blue
        ]
        
        self.jump = {
            (202, 240): (240, 202),  # R1 -> G3
            (328, 202): (368, 240),  # G1 -> Y3
            (368, 328): (328, 368),  # Y1 -> B3
            (240, 368): (202, 328)   # B1 -> R3
        }
        
        self.WINNER = [
            [240, 284],  # Red
            [284, 240],  # Green
            [330, 284],  # Yellow
            [284, 330]   # Blue
        ]

    def show_token(self, x, y):
        self.screen.fill((255, 255, 255))
        self.screen.blit(self.board, (0, 0))

        for i in self.SAFE[4:]:
            self.screen.blit(self.star, i)

        for i in range(len(self.position)):
            for j in self.position[i]:
                self.screen.blit(self.color[i], j)

        self.screen.blit(self.DICE[self.number-1], (605, 270))

        if self.position[x][y] in self.WINNER:
            self.winnerSound.play()
        else:
            self.tokenSound.play()

        self._render_ui()

        pygame.display.update()
        time.sleep(0.5)

    def _render_ui(self):
        self.screen.blit(self.color[self.currentPlayer], (620, 28))
        self.screen.blit(self.currentPlayerText, (600, 10))
        self.screen.blit(self.line, (592, 59))

        for i in range(len(self.winnerRank)):
            rank = self.FONT.render(f'{i+1}.', True, (0, 0, 0))
            self.screen.blit(rank, (600, 85 + (40*i)))
            self.screen.blit(self.color[self.winnerRank[i]], (620, 75 + (40*i)))

    def blit_all(self):
        for i in self.SAFE[4:]:
            self.screen.blit(self.star, i)

        for i in range(len(self.position)):
            for j in self.position[i]:
                self.screen.blit(self.color[i], j)

        self.screen.blit(self.DICE[self.number-1], (605, 270))
        self._render_ui()

    def to_home(self, x, y):
        # R2
        if (self.position[x][y][1] == 284 and self.position[x][y][0] <= 202 and x == 0) \
                and (self.position[x][y][0] + 38*self.number > self.WINNER[x][0]):
            return False
        # Y2
        elif (self.position[x][y][1] == 284 and 368 < self.position[x][y][0] and x == 2) \
                and (self.position[x][y][0] - 38*self.number < self.WINNER[x][0]):
            return False
        # G2
        elif (self.position[x][y][0] == 284 and self.position[x][y][1] <= 202 and x == 1) \
                and (self.position[x][y][1] + 38*self.number > self.WINNER[x][1]):
            return False
        # B2
        elif (self.position[x][y][0] == 284 and self.position[x][y][1] >= 368 and x == 3) \
                and (self.position[x][y][1] - 38*self.number < self.WINNER[x][1]):
            return False
        return True

    def move_token(self, x, y):
        # Taking Token out of HOME
        if tuple(self.position[x][y]) in self.HOME[self.currentPlayer] and self.number == 6:
            self.position[x][y] = list(self.SAFE[self.currentPlayer])
            self.tokenSound.play()
            self.diceRolled = False
        # Moving token which is not in HOME
        elif tuple(self.position[x][y]) not in self.HOME[self.currentPlayer]:
            self.diceRolled = False
            if not self.number == 6:
                self.currentPlayer = (self.currentPlayer + 1) % 4

            # Way to WINNER position
            if (self.position[x][y][1] == 284 and self.position[x][y][0] <= 202 and x == 0) \
                    and (self.position[x][y][0] + 38*self.number <= self.WINNER[x][0]):
                for i in range(self.number):
                    self.position[x][y][0] += 38
                    self.show_token(x, y)
            elif (self.position[x][y][1] == 284 and 368 < self.position[x][y][0] and x == 2) \
                    and (self.position[x][y][0] - 38*self.number >= self.WINNER[x][0]):
                for i in range(self.number):
                    self.position[x][y][0] -= 38
                    self.show_token(x, y)
            elif (self.position[x][y][0] == 284 and self.position[x][y][1] <= 202 and x == 1) \
                    and (self.position[x][y][1] + 38*self.number <= self.WINNER[x][1]):
                for i in range(self.number):
                    self.position[x][y][1] += 38
                    self.show_token(x, y)
            elif (self.position[x][y][0] == 284 and self.position[x][y][1] >= 368 and x == 3) \
                    and (self.position[x][y][1] - 38*self.number >= self.WINNER[x][1]):
                for i in range(self.number):
                    self.position[x][y][1] -= 38
                    self.show_token(x, y)
            else:
                for _ in range(self.number):
                    # R1, Y3
                    if (self.position[x][y][1] == 240 and self.position[x][y][0] < 202) \
                            or (self.position[x][y][1] == 240 and 368 <= self.position[x][y][0] < 558):
                        self.position[x][y][0] += 38
                    # R3 -> R2 -> R1
                    elif (self.position[x][y][0] == 12 and self.position[x][y][1] > 240):
                        self.position[x][y][1] -= 44
                    # R3, Y1
                    elif (self.position[x][y][1] == 328 and 12 < self.position[x][y][0] <= 202) \
                            or (self.position[x][y][1] == 328 and 368 < self.position[x][y][0]):
                        self.position[x][y][0] -= 38
                    # Y3 -> Y2 -> Y1
                    elif (self.position[x][y][0] == 558 and self.position[x][y][1] < 328):
                        self.position[x][y][1] += 44
                    # G3, B1
                    elif (self.position[x][y][0] == 240 and 12 < self.position[x][y][1] <= 202) \
                            or (self.position[x][y][0] == 240 and 368 < self.position[x][y][1]):
                        self.position[x][y][1] -= 38
                    # G3 -> G2 -> G1
                    elif (self.position[x][y][1] == 12 and 240 <= self.position[x][y][0] < 328):
                        self.position[x][y][0] += 44
                    # B3, G1
                    elif (self.position[x][y][0] == 328 and self.position[x][y][1] < 202) \
                            or (self.position[x][y][0] == 328 and 368 <= self.position[x][y][1] < 558):
                        self.position[x][y][1] += 38
                    # B3 -> B2 -> B1
                    elif (self.position[x][y][1] == 558 and self.position[x][y][0] > 240):
                        self.position[x][y][0] -= 44
                    else:
                        for i in self.jump:
                            if self.position[x][y] == list(i):
                                self.position[x][y] = list(self.jump[i])
                                break
                    self.show_token(x, y)

            # Killing Player
            if tuple(self.position[x][y]) not in self.SAFE:
                for i in range(len(self.position)):
                    for j in range(len(self.position[i])):
                        if self.position[i][j] == self.position[x][y] and i != x:
                            self.position[i][j] = list(self.HOME[i][j])
                            self.killSound.play()
                            self.currentPlayer = (self.currentPlayer + 3) % 4

    def check_winner(self):
        if self.currentPlayer not in self.winnerRank:
            for i in self.position[self.currentPlayer]:
                if i not in self.WINNER:
                    return
            self.winnerRank.append(self.currentPlayer)
        else:
            self.currentPlayer = (self.currentPlayer + 1) % 4

    def run(self):
        running = True
        while running:
            self.screen.fill((255, 255, 255))
            self.screen.blit(self.board, (0, 0))
            
            self.check_winner()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONUP:
                    coordinate = pygame.mouse.get_pos()
                    # Rolling Dice
                    if not self.diceRolled and (605 <= coordinate[0] <= 669) and (270 <= coordinate[1] <= 334):
                        self.number = random.randint(1, 6)
                        self.diceSound.play()
                        flag = True
                        for i in range(len(self.position[self.currentPlayer])):
                            if tuple(self.position[self.currentPlayer][i]) not in self.HOME[self.currentPlayer] and self.to_home(self.currentPlayer, i):
                                flag = False
                        if (flag and self.number == 6) or not flag:
                            self.diceRolled = True
                        else:
                            self.currentPlayer = (self.currentPlayer + 1) % 4
                    # Moving Player
                    elif self.diceRolled:
                        for j in range(len(self.position[self.currentPlayer])):
                            if self.position[self.currentPlayer][j][0] <= coordinate[0] <= self.position[self.currentPlayer][j][0] + 31 \
                                    and self.position[self.currentPlayer][j][1] <= coordinate[1] <= self.position[self.currentPlayer][j][1] + 31:
                                self.move_token(self.currentPlayer, j)
                                break

            self.blit_all()
            pygame.display.update()

if __name__ == "__main__":
    game = LudoGame()
    game.run()