import pygame
import random
import time
from db import LudoDB

class LudoGame:
    def __init__(self):
        
        # Disable audio before any pygame initialization
        import os
        os.environ['SDL_AUDIODRIVER'] = 'dummy'
        os.environ['XDG_RUNTIME_DIR'] = '/tmp'

        
        # Initialize pygame
        pygame.init()
        pygame.display.set_caption("Ludo")
        self.screen = pygame.display.set_mode((800, 600))  # Increased width for player management panel

        
        # Game state variables
        self.number = 1
        self.currentPlayer = 0
        self.playerKilled = False
        self.diceRolled = False
        self.winnerRank = []
        self.show_player_manager = False
        self.player_manager_button = pygame.Rect(680, 500, 100, 30)
        
        # Initialize database
        self.db = LudoDB()
        
        # Player management variables
        self.editing_player = None
        self.player_name_input = ""
        self.input_active = False
        self.wins_input = "0"
        self.losses_input = "0"
        
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
        
        # Sound-related code has been removed

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
            [[466, 58], [418, 107], (509, 107), [466, 153]],  # Green
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
            
        # Draw player manager button
        pygame.draw.rect(self.screen, (200, 200, 200), self.player_manager_button)
        manager_text = self.font.render("Manage Players", True, (0, 0, 0))
        self.screen.blit(manager_text, (685, 505))

    def blit_all(self):
        for i in self.SAFE[4:]:
            self.screen.blit(self.star, i)

        for i in range(len(self.position)):
            for j in self.position[i]:
                self.screen.blit(self.color[i], j)

        self.screen.blit(self.DICE[self.number-1], (605, 270))
        self._render_ui()
        
        # Draw player manager if active
        if self.show_player_manager:
            self.draw_player_manager()

    def draw_player_manager(self):
        # Draw background panel
        pygame.draw.rect(self.screen, (240, 240, 240), (680, 0, 120, 600))
        pygame.draw.rect(self.screen, (180, 180, 180), (680, 0, 120, 600), 2)
        
        # Title
        title = self.FONT.render("Player Manager", True, (0, 0, 0))
        self.screen.blit(title, (685, 10))
        
        # Player list
        players = self.db.get_all_players()
        y_pos = 50
        for player in players:
            player_text = self.font.render(f"{player[1]} (W:{player[2]} L:{player[3]})", True, (0, 0, 0))
            self.screen.blit(player_text, (685, y_pos))
            
            # Edit button
            edit_btn = pygame.Rect(685, y_pos + 20, 50, 20)
            pygame.draw.rect(self.screen, (100, 100, 200), edit_btn)
            edit_text = self.font.render("Edit", True, (255, 255, 255))
            self.screen.blit(edit_text, (690, y_pos + 22))
            
            # Delete button
            delete_btn = pygame.Rect(740, y_pos + 20, 50, 20)
            pygame.draw.rect(self.screen, (200, 100, 100), delete_btn)
            delete_text = self.font.render("Delete", True, (255, 255, 255))
            self.screen.blit(delete_text, (745, y_pos + 22))
            
            y_pos += 50
        
        # Add new player form
        if y_pos < 400:
            form_title = self.font.render("Add New Player", True, (0, 0, 0))
            self.screen.blit(form_title, (685, y_pos))
            
            # Name input
            name_label = self.font.render("Name:", True, (0, 0, 0))
            self.screen.blit(name_label, (685, y_pos + 30))
            
            input_bg = pygame.Rect(685, y_pos + 50, 100, 25)
            pygame.draw.rect(self.screen, (255, 255, 255), input_bg)
            pygame.draw.rect(self.screen, (0, 0, 0) if self.input_active else (100, 100, 100), input_bg, 1)
            
            name_text = self.font.render(self.player_name_input, True, (0, 0, 0))
            self.screen.blit(name_text, (690, y_pos + 53))
            
            # Add button
            add_btn = pygame.Rect(685, y_pos + 85, 50, 25)
            pygame.draw.rect(self.screen, (100, 200, 100), add_btn)
            add_text = self.font.render("Add", True, (0, 0, 0))
            self.screen.blit(add_text, (695, y_pos + 88))
            
            # Close button
            close_btn = pygame.Rect(685, 550, 50, 25)
            pygame.draw.rect(self.screen, (200, 100, 100), close_btn)
            close_text = self.font.render("Close", True, (0, 0, 0))
            self.screen.blit(close_text, (690, 553))

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
                            self.currentPlayer = (self.currentPlayer + 3) % 4

    def check_winner(self):
        if self.currentPlayer not in self.winnerRank:
            for i in self.position[self.currentPlayer]:
                if i not in self.WINNER:
                    return
            self.winnerRank.append(self.currentPlayer)
            
            # Update database with win
            player_name = f"Player {self.currentPlayer + 1}"
            self.db.update_score(player_name, won=True)
        else:
            self.currentPlayer = (self.currentPlayer + 1) % 4

    def handle_player_manager_click(self, pos):
        if not self.show_player_manager:
            if self.player_manager_button.collidepoint(pos):
                self.show_player_manager = True
                return True
            return False
        
        # Check if click is in player manager area
        if pos[0] < 680:
            self.show_player_manager = False
            self.input_active = False
            return True
            
        players = self.db.get_all_players()
        y_pos = 50
        
        # Check player edit/delete buttons
        for i, player in enumerate(players):
            edit_btn = pygame.Rect(685, y_pos + 20, 50, 20)
            delete_btn = pygame.Rect(740, y_pos + 20, 50, 20)
            
            if edit_btn.collidepoint(pos):
                self.editing_player = player
                self.player_name_input = player[1]
                self.wins_input = str(player[2])
                self.losses_input = str(player[3])
                self.input_active = True
                return True
                
            if delete_btn.collidepoint(pos):
                self.db.delete_player(player[1])
                return True
                
            y_pos += 50
        
        # Check add player form
        if y_pos < 400:
            input_bg = pygame.Rect(685, y_pos + 50, 100, 25)
            if input_bg.collidepoint(pos):
                self.input_active = True
                return True
                
            add_btn = pygame.Rect(685, y_pos + 85, 50, 25)
            if add_btn.collidepoint(pos):
                if self.player_name_input:
                    try:
                        if self.editing_player:
                            # Update existing player
                            self.db.delete_player(self.editing_player[1])
                        self.db.create_player(self.player_name_input)
                        
                        # Update wins and losses
                        wins = int(self.wins_input) if self.wins_input else 0
                        losses = int(self.losses_input) if self.losses_input else 0
                        
                        for _ in range(wins):
                            self.db.update_score(self.player_name_input, won=True)
                        for _ in range(losses):
                            self.db.update_score(self.player_name_input, won=False)
                            
                        self.player_name_input = ""
                        self.wins_input = "0"
                        self.losses_input = "0"
                        self.editing_player = None
                    except Exception as e:
                        print(f"Error adding player: {e}")
                return True
                
        # Check close button
        close_btn = pygame.Rect(685, 550, 50, 25)
        if close_btn.collidepoint(pos):
            self.show_player_manager = False
            self.input_active = False
            self.editing_player = None
            return True
            
        return False

    def handle_keydown(self, event):
        if not self.input_active:
            return
            
        if event.key == pygame.K_BACKSPACE:
            if self.player_name_input:
                self.player_name_input = self.player_name_input[:-1]
        elif event.key == pygame.K_RETURN:
            self.input_active = False
        else:
            # Only allow alphanumeric characters for player names
            if event.unicode.isalnum() or event.unicode == ' ':
                self.player_name_input += event.unicode

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
                    
                    # Handle player manager clicks first
                    if self.handle_player_manager_click(coordinate):
                        continue
                    
                    # Rolling Dice
                    if not self.diceRolled and (605 <= coordinate[0] <= 669) and (270 <= coordinate[1] <= 334):
                        self.number = random.randint(1, 6)
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
                elif event.type == pygame.KEYDOWN:
                    self.handle_keydown(event)

            self.blit_all()
            pygame.display.update()


if __name__ == "__main__":
    game = LudoGame()
    game.run()