import random
import tkinter as tk
from tkinter import messagebox

# ==== Spēles loģika (paliek tā pati) ====

def generate_sequence(length):
    return [random.choice([1, 2, 3, 4]) for _ in range(length)]

def is_game_over(numbers):
    return len(numbers) == 0

def evaluate(human_score, ai_score):
    return ai_score - human_score

def generate_all_moves(state):
    (numbers, human_score, ai_score, current_player) = state
    next_states = []

    for i, num in enumerate(numbers):
        # Take number
        new_numbers = numbers[:i] + numbers[i+1:]
        if current_player == 'ai':
            new_state = (new_numbers, human_score, ai_score + num, 'human')
        else:
            new_state = (new_numbers, human_score + num, ai_score, 'ai')
        next_states.append(new_state)

        # Split 2 -> 1, 1 (no points)
        if num == 2:
            new_numbers = numbers[:i] + [1, 1] + numbers[i+1:]
            new_state = (new_numbers, human_score, ai_score, 'human' if current_player == 'ai' else 'ai')
            next_states.append(new_state)

        # Split 4 -> 2, 2 (+1 point)
        if num == 4:
            new_numbers = numbers[:i] + [2, 2] + numbers[i+1:]
            if current_player == 'ai':
                new_state = (new_numbers, human_score, ai_score + 1, 'human')
            else:
                new_state = (new_numbers, human_score + 1, ai_score, 'ai')
            next_states.append(new_state)

    return next_states

def minimax(state, depth, maximizing_player):
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

# ==== Tkinter GUI ====

class GameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Skaitļu spēle ar AI")
        self.start_screen()

    def start_screen(self):
        self.clear_window()

        tk.Label(self.root, text="Virknes garums (15-20):").pack()
        self.length_var = tk.IntVar(value=15)
        tk.Spinbox(self.root, from_=15, to=20, textvariable=self.length_var).pack()

        tk.Label(self.root, text="Kurš sāk?").pack()
        self.starter_var = tk.StringVar(value='human')
        tk.Radiobutton(self.root, text="Cilvēks", variable=self.starter_var, value='human').pack()
        tk.Radiobutton(self.root, text="AI", variable=self.starter_var, value='ai').pack()

        tk.Label(self.root, text="AI algoritms:").pack()
        self.algo_var = tk.StringVar(value='minimax')
        tk.Radiobutton(self.root, text="Minimax", variable=self.algo_var, value='minimax').pack()
        tk.Radiobutton(self.root, text="Alpha-Beta", variable=self.algo_var, value='alpha-beta').pack()

        tk.Button(self.root, text="Sākt spēli", command=self.start_game).pack(pady=10)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def start_game(self):
        self.numbers = generate_sequence(self.length_var.get())
        self.human_score = 0
        self.ai_score = 0
        self.current_player = self.starter_var.get()
        self.algorithm = self.algo_var.get()
        self.update_game_screen()

    def update_game_screen(self):
        self.clear_window()

        tk.Label(self.root, text=f"Cilvēks: {self.human_score}    AI: {self.ai_score}").pack()

        frame = tk.Frame(self.root)
        frame.pack(pady=10)
        for i, num in enumerate(self.numbers):
            btn = tk.Button(frame, text=str(num), width=4,
                            command=lambda i=i: self.human_move(i))
            btn.grid(row=0, column=i)

        if self.current_player == 'ai':
            self.root.after(1000, self.ai_move)

    def human_move(self, index):
        num = self.numbers[index]
        action = None

        if num in [2, 4]:
            action = messagebox.askquestion("Darbība", f"Sadalīt {num}? (Jā = Sadalīt, Nē = Paņemt)")
        else:
            action = 'no'

        if action == 'yes' and num == 2:
            self.numbers = self.numbers[:index] + [1,1] + self.numbers[index+1:]
        elif action == 'yes' and num == 4:
            self.numbers = self.numbers[:index] + [2,2] + self.numbers[index+1:]
            self.human_score += 1
        else:
            self.human_score += num
            self.numbers.pop(index)

        self.current_player = 'ai'
        self.check_game_over()
        self.update_game_screen()

    def ai_move(self):
        state = (self.numbers, self.human_score, self.ai_score, 'ai')
        if self.algorithm == 'minimax':
            _, best_state = minimax(state, 4, True)
        else:
            _, best_state = alpha_beta(state, 4, -999999, 999999, True)

        self.numbers, self.human_score, self.ai_score, self.current_player = best_state
        self.check_game_over()
        self.update_game_screen()

    def check_game_over(self):
        if is_game_over(self.numbers):
            result = f"Cilvēks: {self.human_score} | AI: {self.ai_score}\n"
            if self.human_score > self.ai_score:
                result += "Tu uzvarēji!"
            elif self.human_score < self.ai_score:
                result += "AI uzvarēja!"
            else:
                result += "Neizšķirts!"
            messagebox.showinfo("Spēles beigas", result)
            self.start_screen()

if __name__ == '__main__':
    root = tk.Tk()
    app = GameApp(root)
    root.mainloop()
