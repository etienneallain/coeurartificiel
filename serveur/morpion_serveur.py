from flask import Flask, request, jsonify
import math
from flask_cors import CORS

#Création de notre serveur en utilisant la bibliothèque Flask.
app = Flask(__name__)
#Utilisation de CORS pour résoudre le problème de Cross-Origin Resource Sharing.
CORS(app)


def check_victoire(board):
    combos_gagnant = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
    for combo in combos_gagnant:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] != '':
            return board[combo[0]]
    if '' not in board:
        return 'Egalite'
    return None

#L'implémentation de l'algorithme min-max
def minimax(board, profondeur, maximise):
    scores = {'X': -1, 'O': 1, 'Egalite': 0}
    gagnant = check_victoire(board)
    
    if gagnant:
        return scores[gagnant]
    
    if maximise:
        max_eval = -math.inf
        for i in range(9):
            if board[i] == '':
                board[i] = 'O'
                eval = minimax(board, profondeur + 1, False)
                board[i] = ''
                max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = math.inf
        for i in range(9):
            if board[i] == '':
                board[i] = 'X'
                eval = minimax(board, profondeur + 1, True)
                board[i] = ''
                min_eval = min(min_eval, eval)
        return min_eval

def mouvement_ia(board):
    meilleur_mouvement = None
    best_eval = -math.inf
    for i in range(9):
        if board[i] == '':
            board[i] = 'O'
            eval = minimax(board, 0, False)
            board[i] = ''
            if eval > best_eval:
                best_eval = eval
                meilleur_mouvement = i
    return meilleur_mouvement



@app.route('/play_move', methods=['POST'])
def play_move():
    
    global game_board

    if request.method == 'POST':
        data = request.get_json()
        board_recu = data.get('game_board')
        
        if board_recu:
            game_board = board_recu
            print("Board Reçu:", game_board)  
            #On stocke la position choisit par l'IA dans ai_mouvement
            ai_mouvement = mouvement_ia(game_board)
            print("Mouvement IA:", ai_mouvement) 
            #On met à jour la game_board avec la case ou l'IA joue
            game_board[ai_mouvement] = 'O'  
            print("Board mis a jour:", game_board)  
            return jsonify({'game_board':game_board})

    
    return 'Invalid request', 400


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
