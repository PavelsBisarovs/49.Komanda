
import random
import math

class Tree:
    def __init__(self, v1, v2, v3, v4, ai_points, player_points, move=None, depth=0, ai_turn=True):
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3
        self.v4 = v4
        self.ai_points = ai_points
        self.player_points = player_points
        self.move = move  # 1-6 representing different moves
        self.depth = depth
        self.ai_turn = ai_turn
        self.children = []

def generate_moves(tree, max_depth):
    """Generate all possible moves recursively up to max_depth"""
    if tree.depth >= max_depth or (tree.v1 == 0 and tree.v2 == 0 and tree.v3 == 0 and tree.v4 == 0):
        return
    
    # Generate all possible moves (1-6 as previously defined)
    moves = []
    if tree.v1 > 0:
        moves.append((1, tree.v1-1, tree.v2, tree.v3, tree.v4, 1))
    if tree.v2 > 0:
        moves.append((2, tree.v1, tree.v2-1, tree.v3, tree.v4, 2))
        moves.append((5, tree.v1+2, tree.v2-1, tree.v3, tree.v4, 0))  # Split 2
    if tree.v3 > 0:
        moves.append((3, tree.v1, tree.v2, tree.v3-1, tree.v4, 3))
    if tree.v4 > 0:
        moves.append((4, tree.v1, tree.v2, tree.v3, tree.v4-1, 4))
        moves.append((6, tree.v1, tree.v2+2, tree.v3, tree.v4-1, 1))  # Split 4
    
    for move in moves:
        move_id, new_v1, new_v2, new_v3, new_v4, points = move
        if tree.ai_turn:
            new_ai_points = tree.ai_points + points
            new_player_points = tree.player_points
        else:
            new_ai_points = tree.ai_points
            new_player_points = tree.player_points + points
        
        child = Tree(
            new_v1, new_v2, new_v3, new_v4,
            new_ai_points, new_player_points,
            move=move_id, depth=tree.depth+1,
            ai_turn=not tree.ai_turn
        )
        tree.children.append(child)
        generate_moves(child, max_depth)

def minimax(node, depth, maximizing_player):
    """Standard Minimax algorithm implementation"""
    if depth == 0 or not node.children:
        return node.ai_points - node.player_points  # Evaluation function
    
    if maximizing_player:
        value = -math.inf
        for child in node.children:
            value = max(value, minimax(child, depth-1, False))
        return value
    else:
        value = math.inf
        for child in node.children:
            value = min(value, minimax(child, depth-1, True))
        return value

def alphabeta(node, depth, alpha, beta, maximizing_player):
    """Alpha-Beta Pruning optimized Minimax"""
    if depth == 0 or not node.children:
        return node.ai_points - node.player_points
    
    if maximizing_player:
        value = -math.inf
        for child in node.children:
            value = max(value, alphabeta(child, depth-1, alpha, beta, False))
            alpha = max(alpha, value)
            if alpha >= beta:
                break  # Beta cutoff
        return value
    else:
        value = math.inf
        for child in node.children:
            value = min(value, alphabeta(child, depth-1, alpha, beta, True))
            beta = min(beta, value)
            if alpha >= beta:
                break  # Alpha cutoff
        return value

def get_best_move(tree, algorithm='minimax'):
    """Select best move using specified algorithm"""
    if not tree.children:
        return None
    
    best_move = None
    best_value = -math.inf if tree.ai_turn else math.inf
    
    for child in tree.children:
        if algorithm == 'minimax':
            value = minimax(child, max_depth - child.depth, not child.ai_turn)
        else:  # alphabeta
            value = alphabeta(child, max_depth - child.depth, -math.inf, math.inf, not child.ai_turn)
        
        if tree.ai_turn:  # Maximizing player
            if value > best_value:
                best_value = value
                best_move = child
        else:  # Minimizing player
            if value < best_value:
                best_value = value
                best_move = child
    
    return best_move

# Game setup
random.seed(42)  # For reproducible results
v1, v2, v3, v4 = [random.randint(1, 4) for _ in range(4)]
max_depth = 3  # Adjust this for deeper search

root = Tree(v1, v2, v3, v4, 0, 0, ai_turn=True)
generate_moves(root, max_depth)

# Test both algorithms
print(f"Initial board: 1's:{v1}, 2's:{v2}, 3's:{v3}, 4's:{v4}")
print(f"Max depth: {max_depth}\n")

for algo in ['minimax', 'alphabeta']:
    best_move = get_best_move(root, algo)
    if best_move:
        print(f"Using {algo}:")
        print(f"Best move: {best_move.move}")
        print(f"Projected score (AI - Player): {best_move.ai_points - best_move.player_points}")
        print(f"Resulting board: 1's:{best_move.v1}, 2's:{best_move.v2}, 3's:{best_move.v3}, 4's:{best_move.v4}\n")
    else:
        print(f"No valid moves found using {algo}")












# import random

# class Tree:
#     def __init__(self, v1, v2, v3, v4, ai_points, player_points, move=None, depth=0, ai_turn=True):
#         self.v1 = v1
#         self.v2 = v2
#         self.v3 = v3
#         self.v4 = v4
#         self.ai_points = ai_points
#         self.player_points = player_points
#         self.move = move  # 1-6 representing different moves
#         self.depth = depth  # How deep this node is in the tree
#         self.ai_turn = ai_turn  # True if it's AI's turn to move
#         self.children = []

# def generate_moves(tree, max_depth=2):
#     """Recursively generate moves up to specified depth"""
#     if tree.depth >= max_depth:
#         return
    
#     #current_player = "AI" if tree.ai_turn else "Player"
    
#     # Take moves (1-4)
#     if tree.v1 > 0:
#         points_to_add = 1
#         ai_points = tree.ai_points + (points_to_add if tree.ai_turn else 0)
#         player_points = tree.player_points + (0 if tree.ai_turn else points_to_add)
#         child = Tree(tree.v1-1, tree.v2, tree.v3, tree.v4, 
#                     ai_points, player_points, move=1, 
#                     depth=tree.depth+1, ai_turn=not tree.ai_turn)
#         tree.children.append(child)
#         generate_moves(child, max_depth)
    
#     if tree.v2 > 0:
#         points_to_add = 2
#         ai_points = tree.ai_points + (points_to_add if tree.ai_turn else 0)
#         player_points = tree.player_points + (0 if tree.ai_turn else points_to_add)
#         child = Tree(tree.v1, tree.v2-1, tree.v3, tree.v4, 
#                     ai_points, player_points, move=2, 
#                     depth=tree.depth+1, ai_turn=not tree.ai_turn)
#         tree.children.append(child)
#         generate_moves(child, max_depth)
    
#     if tree.v3 > 0:
#         points_to_add = 3
#         ai_points = tree.ai_points + (points_to_add if tree.ai_turn else 0)
#         player_points = tree.player_points + (0 if tree.ai_turn else points_to_add)
#         child = Tree(tree.v1, tree.v2, tree.v3-1, tree.v4, 
#                     ai_points, player_points, move=3, 
#                     depth=tree.depth+1, ai_turn=not tree.ai_turn)
#         tree.children.append(child)
#         generate_moves(child, max_depth)
    
#     if tree.v4 > 0:
#         points_to_add = 4
#         ai_points = tree.ai_points + (points_to_add if tree.ai_turn else 0)
#         player_points = tree.player_points + (0 if tree.ai_turn else points_to_add)
#         child = Tree(tree.v1, tree.v2, tree.v3, tree.v4-1, 
#                     ai_points, player_points, move=4, 
#                     depth=tree.depth+1, ai_turn=not tree.ai_turn)
#         tree.children.append(child)
#         generate_moves(child, max_depth)

#     # Split moves (5-6)
#     if tree.v2 > 0:
#         points_to_add = 0  # Split 2 gives no points
#         ai_points = tree.ai_points + (points_to_add if tree.ai_turn else 0)
#         player_points = tree.player_points + (0 if tree.ai_turn else points_to_add)
#         child = Tree(tree.v1+2, tree.v2-1, tree.v3, tree.v4, 
#                     ai_points, player_points, move=5, 
#                     depth=tree.depth+1, ai_turn=not tree.ai_turn)
#         tree.children.append(child)
#         generate_moves(child, max_depth)
    
#     if tree.v4 > 0:
#         points_to_add = 1  # Split 4 gives 1 point
#         ai_points = tree.ai_points + (points_to_add if tree.ai_turn else 0)
#         player_points = tree.player_points + (0 if tree.ai_turn else points_to_add)
#         child = Tree(tree.v1, tree.v2+2, tree.v3, tree.v4-1, 
#                     ai_points, player_points, move=6, 
#                     depth=tree.depth+1, ai_turn=not tree.ai_turn)
#         tree.children.append(child)
#         generate_moves(child, max_depth)

# def select_best_child(tree):
#     """Find the child with best evaluation using recursive minimax"""
#     if not tree.children:
#         return None
    
#     best_child = None
#     best_score = -float('inf') if tree.ai_turn else float('inf')
    
#     for child in tree.children:
#         child_score = evaluate_position(child)
        
#         if tree.ai_turn:  # AI wants to maximize score
#             if child_score > best_score:
#                 best_score = child_score
#                 best_child = child
#         else:  # Player wants to minimize score
#             if child_score < best_score:
#                 best_score = child_score
#                 best_child = child
    
#     return best_child

# def evaluate_position(node):
#     """Recursive evaluation using minimax"""
#     if not node.children:
#         return node.ai_points - node.player_points  # Simple point difference
    
#     if node.ai_turn:  # Maximizing level
#         return max(evaluate_position(child) for child in node.children)
#     else:  # Minimizing level
#         return min(evaluate_position(child) for child in node.children)

# # Generate random initial state
# v1 = random.randint(1, 4)
# v2 = random.randint(1, 4)
# v3 = random.randint(1, 4)
# v4 = random.randint(1, 4)

# # Create tree with AI to move first
# root = Tree(v1, v2, v3, v4, 0, 0, depth=0, ai_turn=True)

# # Generate moves with adjustable depth (try changing this value)
# generate_moves(root, max_depth=3)

# # Find and print best move
# best_move = select_best_child(root)
# if best_move:
#     print(f"Initial board: 1's:{v1}, 2's:{v2}, 3's:{v3}, 4's:{v4}")
#     print(f"Best initial move: {best_move.move}")
#     print(f"Move types: 1=Take1, 2=Take2, 3=Take3, 4=Take4, 5=Split2, 6=Split4")
#     print(f"Projected score (AI - Player): {evaluate_position(best_move)}")
#     print(f"After move - 1's:{best_move.v1}, 2's:{best_move.v2}, 3's:{best_move.v3}, 4's:{best_move.v4}")
# else:
#     print("No moves available")


















# # import random

# # class Tree:
# #     def __init__(self, v1, v2, v3, v4, ai_points, player_points, move=None):
# #         self.v1 = v1
# #         self.v2 = v2
# #         self.v3 = v3
# #         self.v4 = v4
# #         self.ai_points = ai_points
# #         self.player_points = player_points
# #         self.move = move  # 1-6 representing different moves
# #         self.children = []

# # def generate_next_move(tree):
# #     # Take moves (1-4)
# #     if tree.v1 > 0:
# #         child = Tree(tree.v1-1, tree.v2, tree.v3, tree.v4, 
# #                      tree.ai_points+1, tree.player_points, move=1)
# #         tree.children.append(child)
    
# #     if tree.v2 > 0:
# #         child = Tree(tree.v1, tree.v2-1, tree.v3, tree.v4, 
# #                      tree.ai_points+2, tree.player_points, move=2)
# #         tree.children.append(child)
    
# #     if tree.v3 > 0:
# #         child = Tree(tree.v1, tree.v2, tree.v3-1, tree.v4, 
# #                      tree.ai_points+3, tree.player_points, move=3)
# #         tree.children.append(child)
    
# #     if tree.v4 > 0:
# #         child = Tree(tree.v1, tree.v2, tree.v3, tree.v4-1, 
# #                      tree.ai_points+4, tree.player_points, move=4)
# #         tree.children.append(child)

# #     # Split moves (5-6)
# #     if tree.v2 > 0:
# #         child = Tree(tree.v1+2, tree.v2-1, tree.v3, tree.v4, 
# #                      tree.ai_points, tree.player_points, move=5)
# #         tree.children.append(child)
    
# #     if tree.v4 > 0:
# #         child = Tree(tree.v1, tree.v2+2, tree.v3, tree.v4-1, 
# #                      tree.ai_points+1, tree.player_points, move=6)
# #         tree.children.append(child)

# # # Simplified best child selection
# # def select_best_child(tree):
# #     if not tree.children:
# #         return None
# #     return max(tree.children, key=lambda child: child.ai_points)

# # # Generate random initial state
# # v1 = random.randint(1, 4)
# # v2 = random.randint(1, 4)
# # v3 = random.randint(1, 4)
# # v4 = 0

# # root = Tree(v1, v2, v3, v4, 0, 0)
# # generate_next_move(root)

# # # Example usage
# # best_move = select_best_child(root)
# # if best_move:
# #     print(f"Best move: {best_move.move} (AI points: {best_move.ai_points})")
# # else:
# #     print("No moves available")























# # # import random

# # # class Tree:
# # #     def __init__(self, v1, v2, v3, v4, ai_points, player_points):
# # #         self.v1 = v1
# # #         self.v2 = v2
# # #         self.v3 = v3
# # #         self.v4 = v4
# # #         self.ai_points = ai_points
# # #         self.player_points = player_points
# # #         self.children = []

# # #     def display_state(self):
# # #         print("\nCurrent Game State:")
# # #         print(f"Numbers: 1 (x{self.v1}) | 2 (x{self.v2}) | 3 (x{self.v3}) | 4 (x{self.v4})")
# # #         print(f"Scores -> AI: {self.ai_points} | Player: {self.player_points}")
# # #         print("Available moves:")
# # #         moves = []
# # #         if self.v1 > 0: moves.append("1 - Take a 1 (+1 point)")
# # #         if self.v2 > 0: moves.append("2 - Take a 2 (+2 points)")
# # #         if self.v3 > 0: moves.append("3 - Take a 3 (+3 points)")
# # #         if self.v4 > 0: moves.append("4 - Take a 4 (+4 points)")
# # #         if self.v2 > 0: moves.append("5 - Split a 2 (convert to two 1's)")
# # #         if self.v4 > 0: moves.append("6 - Split a 4 (convert to two 2's and +1 point)")
# # #         print("\n".join(moves))

# # # def generate_next_move(tree, is_ai_turn):
# # #     # Clear previous children
# # #     tree.children = []
    
# # #     # Generate all possible moves
# # #     if tree.v1 > 0:
# # #         new_ai = tree.ai_points + (1 if is_ai_turn else 0)
# # #         new_player = tree.player_points + (1 if not is_ai_turn else 0)
# # #         child = Tree(tree.v1-1, tree.v2, tree.v3, tree.v4, new_ai, new_player)
# # #         tree.children.append(child)
    
# # #     if tree.v2 > 0:
# # #         new_ai = tree.ai_points + (2 if is_ai_turn else 0)
# # #         new_player = tree.player_points + (2 if not is_ai_turn else 0)
# # #         child = Tree(tree.v1, tree.v2-1, tree.v3, tree.v4, new_ai, new_player)
# # #         tree.children.append(child)
    
# # #     if tree.v3 > 0:
# # #         new_ai = tree.ai_points + (3 if is_ai_turn else 0)
# # #         new_player = tree.player_points + (3 if not is_ai_turn else 0)
# # #         child = Tree(tree.v1, tree.v2, tree.v3-1, tree.v4, new_ai, new_player)
# # #         tree.children.append(child)
    
# # #     if tree.v4 > 0:
# # #         new_ai = tree.ai_points + (4 if is_ai_turn else 0)
# # #         new_player = tree.player_points + (4 if not is_ai_turn else 0)
# # #         child = Tree(tree.v1, tree.v2, tree.v3, tree.v4-1, new_ai, new_player)
# # #         tree.children.append(child)
    
# # #     if tree.v2 > 0:
# # #         # Split 2 into two 1's
# # #         child = Tree(tree.v1+2, tree.v2-1, tree.v3, tree.v4, tree.ai_points, tree.player_points)
# # #         tree.children.append(child)
    
# # #     if tree.v4 > 0:
# # #         # Split 4 into two 2's and +1 point
# # #         new_ai = tree.ai_points + (1 if is_ai_turn else 0)
# # #         new_player = tree.player_points + (1 if not is_ai_turn else 0)
# # #         child = Tree(tree.v1, tree.v2+2, tree.v3, tree.v4-1, new_ai, new_player)
# # #         tree.children.append(child)

# # # def select_best_child(tree, is_ai_turn):
# # #     if not tree.children:
# # #         return None
    
# # #     best_child = tree.children[0]
# # #     for child in tree.children[1:]:
# # #         if is_ai_turn:
# # #             if child.ai_points > best_child.ai_points:
# # #                 best_child = child
# # #         else:
# # #             if child.player_points > best_child.player_points:
# # #                 best_child = child
# # #     return best_child

# # # def player_turn(current_state):
# # #     while True:
# # #         current_state.display_state()
# # #         try:
# # #             choice = int(input("\nYour move (1-6): "))
# # #             generate_next_move(current_state, is_ai_turn=False)
            
# # #             # Find the child that matches the player's choice
# # #             valid_choices = []
# # #             if current_state.v1 > 0: valid_choices.append(1)
# # #             if current_state.v2 > 0: valid_choices.append(2)
# # #             if current_state.v3 > 0: valid_choices.append(3)
# # #             if current_state.v4 > 0: valid_choices.append(4)
# # #             if current_state.v2 > 0: valid_choices.append(5)
# # #             if current_state.v4 > 0: valid_choices.append(6)
            
# # #             if choice not in valid_choices:
# # #                 print("Invalid move! Try again.")
# # #                 continue
                
# # #             # Find the matching child
# # #             for child in current_state.children:
# # #                 if choice == 1 and child.v1 == current_state.v1 - 1:
# # #                     return child
# # #                 elif choice == 2 and child.v2 == current_state.v2 - 1:
# # #                     return child
# # #                 elif choice == 3 and child.v3 == current_state.v3 - 1:
# # #                     return child
# # #                 elif choice == 4 and child.v4 == current_state.v4 - 1:
# # #                     return child
# # #                 elif choice == 5 and child.v1 == current_state.v1 + 2 and child.v2 == current_state.v2 - 1:
# # #                     return child
# # #                 elif choice == 6 and child.v2 == current_state.v2 + 2 and child.v4 == current_state.v4 - 1:
# # #                     return child
                    
# # #         except ValueError:
# # #             print("Please enter a number!")

# # # def ai_turn(current_state):
# # #     generate_next_move(current_state, is_ai_turn=True)
# # #     best_move = select_best_child(current_state, is_ai_turn=True)
    
# # #     # Determine which move the AI chose for display purposes
# # #     move_description = ""
# # #     if best_move.v1 < current_state.v1:
# # #         move_description = f"AI took a 1 (+1 point)"
# # #     elif best_move.v2 < current_state.v2 and best_move.ai_points == current_state.ai_points + 2:
# # #         move_description = f"AI took a 2 (+2 points)"
# # #     elif best_move.v3 < current_state.v3:
# # #         move_description = f"AI took a 3 (+3 points)"
# # #     elif best_move.v4 < current_state.v4 and best_move.ai_points == current_state.ai_points + 4:
# # #         move_description = f"AI took a 4 (+4 points)"
# # #     elif best_move.v1 > current_state.v1:
# # #         move_description = f"AI split a 2 into two 1's"
# # #     else:
# # #         move_description = f"AI split a 4 into two 2's (+1 point)"
    
# # #     print(f"\nAI's move: {move_description}")
# # #     return best_move

# # # def is_game_over(state):
# # #     return state.v1 == 0 and state.v2 == 0 and state.v3 == 0 and state.v4 == 0

# # # def main():
# # #     print("Welcome to the Number Game!")
# # #     print("Rules:")
# # #     print("- Take numbers to add to your score (1=1pt, 2=2pt, 3=3pt, 4=4pt)")
# # #     print("- Or split numbers: 2→two 1's or 4→two 2's (+1pt)")
# # #     print("- Players alternate turns until all numbers are gone")
# # #     print("- Highest score wins!\n")
    
# # #     # Initialize game with random numbers
# # #     numbers = [random.randint(1, 4) for _ in range(8)] #izvēlies garumu
# # #     v1 = numbers.count(1)
# # #     v2 = numbers.count(2)
# # #     v3 = numbers.count(3)
# # #     v4 = numbers.count(4)
    
# # #     current_state = Tree(v1, v2, v3, v4, 0, 0)
    
# # #     # Randomize who starts
# # #     player_turn_first = random.choice([True, False])
# # #     if player_turn_first:
# # #         print("You go first!")
# # #     else:
# # #         print("AI goes first!")
    
# # #     while not is_game_over(current_state):
# # #         if player_turn_first:
# # #             current_state = player_turn(current_state)
# # #             if is_game_over(current_state):
# # #                 break
# # #             current_state = ai_turn(current_state)
# # #         else:
# # #             current_state = ai_turn(current_state)
# # #             if is_game_over(current_state):
# # #                 break
# # #             current_state = player_turn(current_state)
    
# # #     # Game over
# # #     print("\nFinal Scores:")
# # #     print(f"AI: {current_state.ai_points} | Player: {current_state.player_points}")
# # #     if current_state.ai_points > current_state.player_points:
# # #         print("AI wins!")
# # #     elif current_state.player_points > current_state.ai_points:
# # #         print("You win!")
# # #     else:
# # #         print("It's a tie!")

# # # if __name__ == "__main__":
# # #     main()















# # # # import random

# # # # class Tree:
# # # #     def __init__(self,v1,v2,v3,v4,ai_points,player_points):
# # # #         self.v1 =v1
# # # #         self.v2 =v2
# # # #         self.v3 =v3
# # # #         self.v4 =v4
# # # #         self.ai_points = ai_points
# # # #         self.player_points = player_points
# # # #         self.children = []


# # # # def generate_next_move(self):

# # # #     #Izveido jaunu bērnu kur izvēlas punktus pieskaitīt
# # # #     if self.v1 >0:
# # # #         new_value_v1 = self.v1 -1
# # # #         new_ai_points = self.ai_points +1
# # # #         child_v1 = Tree(new_value_v1, self.v2 ,self.v3, self.v4, new_ai_points,
# # # #                             self.player_points)
# # # #         self.children.append(child_v1)
# # # #     if self.v2 >0:
# # # #         new_value_v2 = self.v2 -1
# # # #         new_ai_points = self.ai_points +2
# # # #         child_v2 = Tree(self.v1, new_value_v2 ,self.v3, self.v4, new_ai_points,
# # # #                             self.player_points)
# # # #         self.children.append(child_v2)
# # # #     if self.v3 >0:
# # # #         new_value_v3 = self.v3 -1
# # # #         new_ai_points = self.ai_points +3
# # # #         child_v3 = Tree(self.v1, self.v2 ,new_value_v3, self.v4, new_ai_points,
# # # #                             self.player_points)
# # # #         self.children.append(child_v3)
# # # #     if self.v4 >0:
# # # #         new_value_v4 = self.v4 -1
# # # #         new_ai_points = self.ai_points +4
# # # #         child_v4 = Tree(self.v1, self.v2 ,self.v3, new_value_v4, new_ai_points,
# # # #                             self.player_points)
# # # #         self.children.append(child_v4)

# # # #     #jauni bērni split komandai
# # # #     if self.v2 >0:
# # # #         new_value_v2 = self.v2 -1
# # # #         new_value_v1 = self.v1 +2
# # # #         child_split_2 = Tree(new_value_v1, new_value_v2 ,self.v3, self.v4, self.ai_points,
# # # #                             self.player_points)
# # # #         self.children.append(child_split_2)
# # # #     if self.v4 >0:
# # # #         new_value_v4 = self.v4 -1
# # # #         new_value_v2 = self.v2 +2
# # # #         new_ai_points = self.ai_points +1
# # # #         child_split_4 = Tree(self.v1, new_value_v2 ,self.v3, new_value_v4, new_ai_points,
# # # #                             self.player_points)
# # # #         self.children.append(child_split_4)

# # # # def select_best_child(tree):
# # # #     if not tree.children:  # if no children, return None
# # # #         return None
    
# # # #     best_child = tree.children[0]  # start with first child
# # # #     for child in tree.children[1:]:  # compare with remaining children
# # # #         if child.ai_points > best_child.ai_points:
# # # #             best_child = child
# # # #     return best_child

# # # # virkne = []
# # # # garums = 4
# # # # for i in range(garums):
# # # #     virkne.append(random.randint(1,4))

# # # # v1 = virkne.count(1)
# # # # v2 = virkne.count(2)
# # # # v3 = virkne.count(3)
# # # # v4 = virkne.count(4)

# # # # root = Tree(v1,v2,v3,v4,0,0)
# # # # generate_next_move(root)
