
import random
import tkinter
from tkinter import *
from tkinter import messagebox

# ---------------------------------------- GLOBALIE MAINĪGIE ----------------------------------------
virkne = []
speletaja_punkti = 0
ai_punkti = 0
speletajs = True

# --------------------------------------------- SPĒLES KOKS --------------------------------------------
class Tree:
    def __init__(self, virkne, speletaja_punkti, ai_punkti, speletajs):
        self.virkne = virkne[:]
        self.speletaja_punkti = speletaja_punkti
        self.ai_punkti = ai_punkti
        self.speletajs = speletajs
        self.children = []
        self.heiristiskais_vertejums = None

    def generate_children(self):
        for i, skaitlis in enumerate(self.virkne):
            new_virkne = self.virkne[:i] + self.virkne[i + 1:]
            new_speletaja_punkti = self.speletaja_punkti
            new_ai_punkti = self.ai_punkti
            new_speletajs = not self.speletajs

            if skaitlis == 2:
                new_virkne += [1, 1]
            elif skaitlis == 4:
                new_virkne += [2, 2]
                if self.speletajs:
                    new_speletaja_punkti += 1
                else:
                    new_ai_punkti += 1
            else:
                if self.speletajs:
                    new_speletaja_punkti += skaitlis
                else:
                    new_ai_punkti += skaitlis

            child = Tree(new_virkne, new_speletaja_punkti, new_ai_punkti, new_speletajs)
            self.children.append(child)

# -------------------------------------- HEIRISTISKAIS VĒRTĒJUMS --------------------------------------
def Heiristiskais_vertejums(sequence, player_score, ai_score, maximizing_player):
    score_diff = ai_score - player_score
    f1 = sequence.count(1)
    f2 = sequence.count(2)
    f3 = sequence.count(3)
    f4 = sequence.count(4)
    heiristiskais_vertejums = ((score_diff * 10) + (f1 * 0.001) + (f2 * 0.1) + (f3 * 0.5) + (f4 * 3))
    return heiristiskais_vertejums if maximizing_player else -heiristiskais_vertejums

# -------------------------------------------- MINIMAX ALGORITMS --------------------------------------------
def minimax(node, depth, maximizing_player):
    if depth == 0 or not node.virkne:
        return Heiristiskais_vertejums(node.virkne, node.speletaja_punkti, node.ai_punkti, maximizing_player)
    node.generate_children()
    if maximizing_player:
        max_eval = float('-inf')
        for child in node.children:
            eval = minimax(child, depth - 1, False)
            max_eval = max(max_eval, eval)
        node.heiristiskais_vertejums = max_eval
        return max_eval
    else:
        min_eval = float('inf')
        for child in node.children:
            eval = minimax(child, depth - 1, True)
            min_eval = min(min_eval, eval)
        node.heiristiskais_vertejums = min_eval
        return min_eval

# ----------------------------------------- ALPHA-BETA ALGORITMS -------------------------------------------
def alpha_beta(node, depth, alpha, beta, maximizing_player):
    if depth == 0 or not node.virkne:
        return Heiristiskais_vertejums(node.virkne, node.speletaja_punkti, node.ai_punkti, maximizing_player)
    node.generate_children()
    if maximizing_player:
        max_eval = float('-inf')
        for child in node.children:
            eval = alpha_beta(child, depth - 1, alpha, beta, False)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        node.heiristiskais_vertejums = max_eval
        return max_eval
    else:
        min_eval = float('inf')
        for child in node.children:
            eval = alpha_beta(child, depth - 1, alpha, beta, True)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        node.heiristiskais_vertejums = min_eval
        return min_eval

# -------------------------------------- AI GĀJIENS --------------------------------------
def AI_gajiens():
    global virkne, speletaja_punkti, ai_punkti, speletajs

    sakums = Tree(virkne, speletaja_punkti, ai_punkti, False)
    sakums.generate_children()

    best_child = None
    best_value = float('-inf')

    if algoritms.get() == "Minmaksa":
        for child in sakums.children:
            value = minimax(child, 3, False)
            if value > best_value:
                best_value = value
                best_child = child
    elif algoritms.get() == "Alfa-beta":
        for child in sakums.children:
            value = alpha_beta(child, 3, float('-inf'), float('inf'), False)
            if value > best_value:
                best_value = value
                best_child = child

    if best_child:
        virkne[:] = best_child.virkne
        speletaja_punkti = best_child.speletaja_punkti
        ai_punkti = best_child.ai_punkti
        speletajs = True
        atjaunot_info()
        if not virkne:
            beigas()

# ----------------------------------------- INFO ATJAUNOŠANA -----------------------------------------
def atjaunot_info():
    info.config(text=f"Tavi punkti: {speletaja_punkti} | AI: {ai_punkti}")
    for widget in virkne_frame.winfo_children():
        widget.destroy()

    Label(virkne_frame, text="Izvēlies skaitli no virknes:", font=("Arial", 10, "bold")).pack()
    for skaitlis in virkne:
        btn = Button(virkne_frame, text=str(skaitlis), width=3, command=lambda s=skaitlis: speletaja_gajiens(s))
        btn.pack(side=LEFT, padx=2)

# ----------------------------------------- SPĒLĒTĀJA GĀJIENS -----------------------------------------
def speletaja_gajiens(skaitlis):
    global virkne, speletaja_punkti, speletajs

    if skaitlis in virkne and speletajs:
        virkne.remove(skaitlis)

        if skaitlis == 2:
            virkne += [1, 1]
        elif skaitlis == 4:
            virkne += [2, 2]
            speletaja_punkti += 1
        else:
            speletaja_punkti += skaitlis

        speletajs = False
        atjaunot_info()

        if not virkne:
            beigas()
        else:
            logs.after(1000, AI_gajiens)

# ----------------------------------------- BEIGU LOĢIKA -----------------------------------------
def beigas():
    if speletaja_punkti > ai_punkti:
        messagebox.showinfo("Spēles beigas", f"Tu uzvarēji! ({speletaja_punkti}:{ai_punkti})")
    elif ai_punkti > speletaja_punkti:
        messagebox.showinfo("Spēles beigas", f"AI uzvarēja! ({ai_punkti}:{speletaja_punkti})")
    else:
        messagebox.showinfo("Spēles beigas", f"Neizšķirts! ({speletaja_punkti}:{ai_punkti})")

# ----------------------------------------- SĀKUMA STĀVOKLIS -----------------------------------------
def Sakuma_stavoklis():
    global virkne, speletaja_punkti, ai_punkti, speletajs
    try:
        garums = int(lauks.get())
        if 15 <= garums <= 20:
            virkne = [random.choice([1, 2, 3, 4]) for _ in range(garums)]
            speletaja_punkti = 0
            ai_punkti = 0
            speletajs = True
            atjaunot_info()
        else:
            messagebox.showerror("Kļūda", "Lūdzu ievadiet skaitli no 15 līdz 20!")
    except ValueError:
        messagebox.showerror("Kļūda", "Lūdzu ievadiet derīgu skaitli!")

# ----------------------------------------- GRAFISKĀ SASKARNE -----------------------------------------
logs = tkinter.Tk()
logs.title("Divpersonu spēle")
logs.geometry("400x350")

Label(logs, text="Ievadiet skaitli no 15 līdz 20:", font=("Arial", 10, "bold")).pack(pady=5)
lauks = Entry(logs)
lauks.pack()

algoritms = StringVar()
algoritms.set("Minmaksa")
Label(logs, text="Izvēlies algoritmu:", font=("Arial", 10)).pack()
Radiobutton(logs, text="Minimakss", variable=algoritms, value="Minmaksa").pack()
Radiobutton(logs, text="Alfa-beta", variable=algoritms, value="Alfa-beta").pack()

Button(logs, text="Ģenerēt virkni", command=Sakuma_stavoklis).pack(pady=10)

info = Label(logs, text="", font=("Arial", 10))
info.pack(pady=10)

virkne_frame = Frame(logs)
virkne_frame.pack(pady=10)

logs.mainloop()
