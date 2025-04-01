import pygame
import sys
import random

pygame.init()

# -----------------------------
# Konstantes
# -----------------------------
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY  = (200, 200, 200)
RED   = (255, 0, 0)

FONT = pygame.font.SysFont(None, 30)
BIG_FONT = pygame.font.SysFont(None, 50)

# Spēles stāvokļi
STATE_MENU = "MENU"
STATE_GAME = "GAME"
STATE_END  = "END"

# Spēlētāji
HUMAN = 0
AI = 1

# Atļautais virknes garums
MIN_LEN = 15
MAX_LEN = 20

# -----------------------------
# Loģikas funkcijas
# -----------------------------

def is_game_over(numbers):
    """Pārbaudām, vai virkne ir tukša (vai spēle ir beigusies)."""
    return len(numbers) == 0

def evaluate(human_score, ai_score):
    """
    Novērtējuma funkcija: atgriež (ai_score - human_score).
    Jo lielāka vērtība, jo labāk Datoram.
    """
    return ai_score - human_score

def generate_all_moves(state):
    """
    Ģenerē visus iespējamos nākamos stāvokļus (pēc viena gājiena).
    state = (numbers, human_score, ai_score, current_player)
    """
    (numbers, human_score, ai_score, current_player) = state
    
    # Nosakām, kuru spēlētāju punkti tiks mainīti
    if current_player == HUMAN:
        current_score = human_score
        opp_score = ai_score
        next_player = AI
    else:
        current_score = ai_score
        opp_score = human_score
        next_player = HUMAN

    next_states = []
    numbers_list = list(numbers)

    for i, val in enumerate(numbers_list):
        # 1) Paņemt skaitli (to noņem no virknes un pieskaita saviem punktiem)
        new_nums = list(numbers_list)
        del new_nums[i]
        new_score = current_score + val
        if current_player == HUMAN:
            new_state = (tuple(new_nums), new_score, opp_score, next_player)
        else:
            new_state = (tuple(new_nums), opp_score, new_score, next_player)
        next_states.append(new_state)

        # 2) Ja val == 2, var sadalīt 2 -> (1,1) un punkti nemainās
        if val == 2:
            new_nums2 = list(numbers_list)
            new_nums2[i] = 1
            new_nums2.insert(i+1, 1)
            if current_player == HUMAN:
                new_state2 = (tuple(new_nums2), current_score, opp_score, next_player)
            else:
                new_state2 = (tuple(new_nums2), opp_score, current_score, next_player)
            next_states.append(new_state2)

        # 3) Ja val == 4, var sadalīt 4 -> (2,2) un +1 punkts
        if val == 4:
            new_nums4 = list(numbers_list)
            new_nums4[i] = 2
            new_nums4.insert(i+1, 2)
            new_score4 = current_score + 1  # +1 punkts par sadalīšanu
            if current_player == HUMAN:
                new_state4 = (tuple(new_nums4), new_score4, opp_score, next_player)
            else:
                new_state4 = (tuple(new_nums4), opp_score, new_score4, next_player)
            next_states.append(new_state4)
    
    return next_states

def minimax(state, depth, maximizing_player):
    """
    Minimax algoritms (bez alpha-beta).
    Atgriež (labākā_vērtība, labākais_stāvoklis).
    """
    (numbers, human_score, ai_score, current_player) = state

    if is_game_over(numbers) or depth == 0:
        return evaluate(human_score, ai_score), state

    if maximizing_player:
        best_value = -999999
        best_state = None
        for nxt in generate_all_moves(state):
            val, _ = minimax(nxt, depth - 1, False)
            if val > best_value:
                best_value = val
                best_state = nxt
        return best_value, best_state
    else:
        best_value = 999999
        best_state = None
        for nxt in generate_all_moves(state):
            val, _ = minimax(nxt, depth - 1, True)
            if val < best_value:
                best_value = val
                best_state = nxt
        return best_value, best_state

def alpha_beta(state, depth, alpha, beta, maximizing_player):
    """
    Minimax ar alfa-beta griešanu.
    Atgriež (labākā_vērtība, labākais_stāvoklis).
    """
    (numbers, human_score, ai_score, current_player) = state

    if is_game_over(numbers) or depth == 0:
        return evaluate(human_score, ai_score), state

    if maximizing_player:
        best_value = -999999
        best_state = None
        for nxt in generate_all_moves(state):
            val, _ = alpha_beta(nxt, depth - 1, alpha, beta, False)
            if val > best_value:
                best_value = val
                best_state = nxt
            alpha = max(alpha, best_value)
            if beta <= alpha:
                break
        return best_value, best_state
    else:
        best_value = 999999
        best_state = None
        for nxt in generate_all_moves(state):
            val, _ = alpha_beta(nxt, depth - 1, alpha, beta, True)
            if val < best_value:
                best_value = val
                best_state = nxt
            beta = min(beta, best_value)
            if beta <= alpha:
                break
        return best_value, best_state

# -----------------------------
# Galvenais kontrolieris
# -----------------------------
class GameController:
    def __init__(self):
        self.state = STATE_MENU
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Spēle ar Minimax un Alpha-Beta")
        
        # Parametri, ko izvēlamies izvēlnē
        self.seq_length = 15
        self.use_alpha_beta = False  # False -> Minimax, True -> Alpha-Beta
        self.first_move_choice = 1   # 1=Cilvēks, 2=Dators, 3=Nejauši

        # Spēles dati
        self.numbers = []
        self.human_score = 0
        self.ai_score = 0
        self.current_player = HUMAN

        # Lai zinātu, kuru skaitli cilvēks ir izvēlējies
        self.selected_index = None

        # Meklēšanas dziļums (koku dziļums)
        self.search_depth = 3  # Var mainīt pēc vajadzības

    def run(self):
        clock = pygame.time.Clock()

        running = True
        while running:
            clock.tick(30)  # FPS
            if self.state == STATE_MENU:
                self.handle_menu_events()
                self.draw_menu()
            elif self.state == STATE_GAME:
                self.handle_game_events()
                self.draw_game()
            elif self.state == STATE_END:
                self.handle_end_events()
                self.draw_end()
            else:
                running = False

            pygame.display.flip()

        pygame.quit()
        sys.exit()

    # -----------------------------
    # Izvēlne (MENU)
    # -----------------------------
    def handle_menu_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # Bultiņas augšup/lejup maina virknes garumu
                if event.key == pygame.K_UP:
                    self.seq_length = min(self.seq_length + 1, MAX_LEN)
                elif event.key == pygame.K_DOWN:
                    self.seq_length = max(self.seq_length - 1, MIN_LEN)
                # Skaitlis 1 vai 2 -> Minimax/Alpha-Beta
                if event.key == pygame.K_1:
                    self.use_alpha_beta = False
                elif event.key == pygame.K_2:
                    self.use_alpha_beta = True
                # F taustiņi (F1/F2/F3) lai izvēlētos, kurš iet pirmais
                if event.key == pygame.K_F1:
                    self.first_move_choice = 1  # Cilvēks
                elif event.key == pygame.K_F2:
                    self.first_move_choice = 2  # Dators
                elif event.key == pygame.K_F3:
                    self.first_move_choice = 3  # Nejauši
                # Enter -> sākt spēli
                if event.key == pygame.K_RETURN:
                    self.start_game()

    def draw_menu(self):
        self.screen.fill(WHITE)
        title = BIG_FONT.render("Parametru izvēle", True, BLACK)
        self.screen.blit(title, (250, 50))

        txt1 = FONT.render(f"Virknes garums: {self.seq_length}  (UP/DOWN taustiņi)", True, BLACK)
        self.screen.blit(txt1, (250, 120))

        algo_str = "Alpha-Beta" if self.use_alpha_beta else "Minimax"
        txt2 = FONT.render(f"Algoritms: {algo_str}  (1=Minimax, 2=Alpha-Beta)", True, BLACK)
        self.screen.blit(txt2, (250, 160))

        # Kurš gājiens pirmais
        if self.first_move_choice == 1:
            mover_text = "Cilvēks"
        elif self.first_move_choice == 2:
            mover_text = "Dators"
        else:
            mover_text = "Nejauši"
        txt3 = FONT.render(
            f"Pirmais gājiens: {mover_text}  (F1=Cilvēks, F2=Dators, F3=Nejauši)",
            True, BLACK
        )
        self.screen.blit(txt3, (250, 200))

        txt4 = FONT.render("Nospiediet ENTER, lai sāktu", True, RED)
        self.screen.blit(txt4, (250, 280))

    def start_game(self):
        # Ģenerējam sākotnējo virkni
        self.numbers = [random.randint(1,4) for _ in range(self.seq_length)]
        self.human_score = 0
        self.ai_score = 0

        # Nosakām, kurš iet pirmais
        if self.first_move_choice == 1:
            self.current_player = HUMAN
        elif self.first_move_choice == 2:
            self.current_player = AI
        else:
            # Nejaušs
            self.current_player = random.choice([HUMAN, AI])

        self.selected_index = None
        self.state = STATE_GAME

    # -----------------------------
    # Spēles stāvoklis (GAME)
    # -----------------------------
    def handle_game_events(self):
        if self.current_player == AI:
            # Datora gājiens
            pygame.time.wait(500)  # neliela pauze
            self.ai_move()
            # Pārbaudām, vai beigusies spēle
            if is_game_over(self.numbers):
                self.state = STATE_END
            else:
                self.current_player = HUMAN
            return

        # Cilvēka gājiens: gaidām peles klikšķus
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                # Noskaidrojam, vai cilvēks noklikšķināja uz kāda skaitļa
                index_clicked = self.get_number_index_by_pos(mx, my)
                if index_clicked is not None:
                    # Iezīmējam vai noņemam iezīmējumu
                    if self.selected_index == index_clicked:
                        self.selected_index = None
                    else:
                        self.selected_index = index_clicked
                else:
                    # Varbūt noklikšķināja uz pogas?
                    action = self.check_action_buttons(mx, my)
                    if action and self.selected_index is not None:
                        # Izpildām darbību
                        self.player_action(action, self.selected_index)
                        # Pārbaudām beigas
                        if is_game_over(self.numbers):
                            self.state = STATE_END
                        else:
                            self.current_player = AI  # dodam gājienu datoram
                        self.selected_index = None
                        return

    def draw_game(self):
        self.screen.fill(WHITE)

        # Punkti
        score_text = FONT.render(
            f"Punkti: Cilvēks={self.human_score} | Dators={self.ai_score}",
            True, BLACK
        )
        self.screen.blit(score_text, (20, 20))

        # Kurš gājiens?
        if self.current_player == HUMAN:
            turn_text = FONT.render("Cilvēka gājiens", True, BLACK)
        else:
            turn_text = FONT.render("Datora gājiens (lūdzu, uzgaidiet...)", True, BLACK)
        self.screen.blit(turn_text, (20, 60))

        # Zīmējam virkni (skaitļus)
        self.draw_sequence()

        # Zīmējam darbību pogas
        self.draw_action_buttons()

    def draw_sequence(self):
        """
        Uzzīmē skaitļu virkni.
        Katrs skaitlis ir taisnstūris (40x40), atstarpe ~10px.
        """
        x_start = 50
        y = 120
        for i, val in enumerate(self.numbers):
            rect = pygame.Rect(x_start, y, 40, 40)
            color = GRAY
            if i == self.selected_index:
                color = (180, 180, 255)  # izcelts
            pygame.draw.rect(self.screen, color, rect)
            num_text = FONT.render(str(val), True, BLACK)
            text_rect = num_text.get_rect(center=rect.center)
            self.screen.blit(num_text, text_rect)
            x_start += 50

    def get_number_index_by_pos(self, mx, my):
        """
        Noskaidro, kura skaitļa taisnstūrī ir klikšķis.
        Ja nav trāpīts, atgriež None.
        """
        x_start = 50
        y = 120
        for i, val in enumerate(self.numbers):
            rect = pygame.Rect(x_start, y, 40, 40)
            if rect.collidepoint(mx, my):
                return i
            x_start += 50
        return None

    def draw_action_buttons(self):
        """
        Uzzīmē 3 pogas: "Paņemt", "Split 2", "Split 4".
        """
        self.btn_take = pygame.Rect(50, 500, 100, 40)
        self.btn_s2   = pygame.Rect(200, 500, 120, 40)
        self.btn_s4   = pygame.Rect(350, 500, 120, 40)

        pygame.draw.rect(self.screen, GRAY, self.btn_take)
        pygame.draw.rect(self.screen, GRAY, self.btn_s2)
        pygame.draw.rect(self.screen, GRAY, self.btn_s4)

        take_txt = FONT.render("Paņemt", True, BLACK)
        s2_txt   = FONT.render("Split 2", True, BLACK)
        s4_txt   = FONT.render("Split 4", True, BLACK)

        self.screen.blit(take_txt, take_txt.get_rect(center=self.btn_take.center))
        self.screen.blit(s2_txt,   s2_txt.get_rect(center=self.btn_s2.center))
        self.screen.blit(s4_txt,   s4_txt.get_rect(center=self.btn_s4.center))

    def check_action_buttons(self, mx, my):
        """
        Atgriež darbības virkni "take"/"split2"/"split4" vai None.
        """
        if self.btn_take.collidepoint(mx, my):
            return "take"
        if self.btn_s2.collidepoint(mx, my):
            return "split2"
        if self.btn_s4.collidepoint(mx, my):
            return "split4"
        return None

    def player_action(self, action, index):
        """
        Piemēro izvēlēto darbību (take/split2/split4) pie skaitļa ar norādīto indeksu.
        """
        val = self.numbers[index]
        nums = list(self.numbers)

        if action == "take":
            # Paņemam skaitli => +val cilvēka punktiem, noņemam to no virknes
            self.human_score += val
            del nums[index]

        elif action == "split2":
            # Sadalām 2 -> (1,1) bez papildu punktiem
            if val == 2:
                nums[index] = 1
                nums.insert(index+1, 1)
            else:
                return

        elif action == "split4":
            # Sadalām 4 -> (2,2) un +1 punkts
            if val == 4:
                nums[index] = 2
                nums.insert(index+1, 2)
                self.human_score += 1
            else:
                return

        self.numbers = tuple(nums)

    def ai_move(self):
        """
        Datora gājiens, izmantojot Minimax vai Alpha-Beta (atkarībā no izvēles).
        """
        state = (tuple(self.numbers), self.human_score, self.ai_score, AI)
        if self.use_alpha_beta:
            _, best_state = alpha_beta(state, self.search_depth, -999999, 999999, True)
        else:
            _, best_state = minimax(state, self.search_depth, True)

        if best_state is None:
            return
        (numbers, h_score, a_score, next_player) = best_state
        self.numbers = numbers
        self.human_score = h_score
        self.ai_score = a_score

    # -----------------------------
    # Spēles beigu ekrāns
    # -----------------------------
    def handle_end_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # Jebkurš taustiņš -> atpakaļ uz izvēlni
                self.state = STATE_MENU

    def draw_end(self):
        self.screen.fill(WHITE)
        # Gala rezultāts
        result_text = "Neizšķirts!"
        if self.human_score > self.ai_score:
            result_text = "Uzvar Cilvēks!"
        elif self.ai_score > self.human_score:
            result_text = "Uzvar Dators!"

        t1 = BIG_FONT.render("Spēle beigusies", True, RED)
        t2 = FONT.render(f"Punkti: Cilvēks={self.human_score} | Dators={self.ai_score}", True, BLACK)
        t3 = FONT.render(result_text, True, BLACK)
        t4 = FONT.render("Nospiediet jebkuru taustiņu, lai atgrieztos izvēlnē", True, GRAY)

        self.screen.blit(t1, (250, 100))
        self.screen.blit(t2, (250, 200))
        self.screen.blit(t3, (250, 250))
        self.screen.blit(t4, (100, 400))

def main():
    game = GameController()
    game.run()

if __name__ == "__main__":
    main()

