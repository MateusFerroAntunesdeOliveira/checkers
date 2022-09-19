from copy import deepcopy
import time
import math

# Definindo cores utilizadas
ansi_black = "\u001b[30m"
ansi_red = "\u001b[31m"
ansi_green = "\u001b[32m"
ansi_yellow = "\u001b[33m"
ansi_blue = "\u001b[34m"
ansi_magenta = "\u001b[35m"
ansi_cyan = "\u001b[36m"
ansi_white = "\u001b[37m"
ansi_reset = "\u001b[0m"

# Definindo indicadores das peças e suas Damas
BLACK_PIECE = "p"
WHITE_PIECE = "b"
BLACK_PIECE_CHECK = "P"
WHITE_PIECE_CHECK = "B"

# Definindo outras condições
BOARD_SIZE = 10
EXIT_CONDITION = "-1"
SURRENDER_CONDITION = "s"
BLANK_SPACE = "---"

class Node:
    # Construtor da classe Nó
    def __init__(self, board, move=None, parent=None, value=None):
        self.board = board
        self.value = value
        self.move = move
        self.parent = parent

    # Checa e determina possíveis jogadas (em listas)
    def get_children(self, minimizing_player):
        current_state = deepcopy(self.board)
        available_moves = []
        children_states = []
        big_letter = ""
        queen_row = 0
        if minimizing_player is True:
            available_moves = Checkers.find_available_moves(current_state)
            big_letter = BLACK_PIECE_CHECK
            queen_row = BOARD_SIZE - 1
        else:
            available_moves = Checkers.find_player_available_moves(current_state)
            big_letter = WHITE_PIECE_CHECK
            queen_row = 0
        for i in range(len(available_moves)):
            old_i = available_moves[i][0]
            old_j = available_moves[i][1]
            new_i = available_moves[i][2]
            new_j = available_moves[i][3]
            state = deepcopy(current_state)
            Checkers.make_a_move(state, old_i, old_j, new_i, new_j, big_letter, queen_row)
            children_states.append(Node(state, [old_i, old_j, new_i, new_j]))
        return children_states

    def set_value(self, value):
        self.value = value

    def get_board(self):
        return self.board


class Checkers:
    # Construtor do Tabuleiro
    def __init__(self):
        self.matrix = [[], [], [], [], [], [], [], [], [], []]
        self.player_turn = True
        self.computer_pieces = 20
        self.player_pieces = 20
        self.available_moves = []

        for row in self.matrix:
            for i in range(BOARD_SIZE):
                row.append(BLANK_SPACE)
        self.position_computer()
        self.position_player()

    # Define posições do computador (3 primeiras linhas - peças pretas)
    def position_computer(self):
        for i in range(4):
            for j in range(BOARD_SIZE):
                if (i + j) % 2 == 1:
                    self.matrix[i][j] = (BLACK_PIECE + str(i) + str(j))

    # Define posições do jogador (3 últimas linhas - peças brancas)
    def position_player(self):
        for i in range(6, BOARD_SIZE, 1):
            for j in range(BOARD_SIZE):
                if (i + j) % 2 == 1:
                    self.matrix[i][j] = (WHITE_PIECE + str(i) + str(j))

    # Define e apresenta tabuleiro
    def print_matrix(self):
        i = 0
        print("\n")
        print("                    TABULEIRO                ")
        print("    _________________________________________")
        print("   |                                         |")
        for row in self.matrix:
            print(i, end="  | ")
            i += 1
            for elem in row:
                print(elem, end=" ")
            print("|")
        print("   |_________________________________________|")
        for j in range(BOARD_SIZE):
            if j == 0:
                j = "      0"
            print(j, end="   ")
        print("\n")

    # Recebe Input do Jogador
    def get_player_input(self):
        available_moves = Checkers.find_player_available_moves(self.matrix)
        if len(available_moves) == 0:
            if self.computer_pieces > self.player_pieces:
                print(
                    ansi_red + "Você não possui movimentos disponíveis, e tem menos peças que o adversário. Você Perdeu!" + ansi_reset)
            else:
                print(ansi_yellow + "Você não tem movimentos disponíveis.\nJogo Terminado!" + ansi_reset)
            exit()
        self.player_pieces = 0
        self.computer_pieces = 0
        while True:    
            old = ""
            coord1 = input("Escolha a peca [i,j]: ")
            if coord1 == EXIT_CONDITION:
                print(ansi_cyan + "Jogo Acabou!" + ansi_reset)
                exit()
            elif coord1 == SURRENDER_CONDITION:
                print(ansi_cyan + "Você se rendeu!" + ansi_reset)
                exit()
            coord2 = input("Para onde [i,j]: ")
            if coord2 == WHITE_PIECE_CHECK:                         #//FIXME rever esse ponto...
                print(ansi_cyan + "Jogo Acabou!" + ansi_reset)
                exit()
            elif coord2 == SURRENDER_CONDITION:
                print(ansi_cyan + "Você se rendeu!" + ansi_reset)
                exit()
            old = coord1.split(",")
            new = coord2.split(",")

            if len(old) != 2 or len(new) != 2 or not old[0].isdigit() or not old[1].isdigit() or not new[0].isdigit() or not new[1].isdigit():
                print(ansi_red + "Entrada Inválida!" + ansi_reset)
            else:
                old_i = old[0]
                old_j = old[1]
                new_i = new[0]
                new_j = new[1]
                move = [int(old_i), int(old_j), int(new_i), int(new_j)]
                if move not in available_moves:
                    print(ansi_red + "Movimentação Inválida!" + ansi_reset)
                # Define que pode mover e move
                else:
                    Checkers.make_a_move(self.matrix, int(old_i), int(old_j), int(new_i), int(new_j), WHITE_PIECE_CHECK, 0)
                    for m in range(BOARD_SIZE):
                        for n in range(BOARD_SIZE):
                            if self.matrix[m][n][0] == BLACK_PIECE or self.matrix[m][n][0] == BLACK_PIECE_CHECK:
                                self.computer_pieces += 1
                            elif self.matrix[m][n][0] == WHITE_PIECE or self.matrix[m][n][0] == WHITE_PIECE_CHECK:
                                self.player_pieces += 1
                    break

    # Checa se é possível pular a peça - Computador
    @staticmethod
    def check_jumps(board, old_i, old_j, via_i, via_j, new_i, new_j):
        if new_i > (BOARD_SIZE - 1) or new_i < 0:
            return False
        if new_j > (BOARD_SIZE - 1) or new_j < 0:
            return False
        if board[via_i][via_j] == BLANK_SPACE:
            return False
        if board[via_i][via_j][0] == BLACK_PIECE_CHECK or board[via_i][via_j][0] == BLACK_PIECE:
            return False
        if board[new_i][new_j] != BLANK_SPACE:
            return False
        if board[old_i][old_j] == BLANK_SPACE:
            return False
        if board[old_i][old_j][0] == WHITE_PIECE or board[old_i][old_j][0] == WHITE_PIECE_CHECK:
            return False
        return True

    # Checa se é possível pular a peça - Jogador
    @staticmethod
    def check_player_jumps(board, old_i, old_j, via_i, via_j, new_i, new_j):
        if new_i > (BOARD_SIZE - 1) or new_i < 0:
            return False
        if new_j > (BOARD_SIZE - 1) or new_j < 0:
            return False
        if board[via_i][via_j] == BLANK_SPACE:
            return False
        if board[via_i][via_j][0] == WHITE_PIECE_CHECK or board[via_i][via_j][0] == WHITE_PIECE:
            return False
        if board[new_i][new_j] != BLANK_SPACE:
            return False
        if board[old_i][old_j] == BLANK_SPACE:
            return False
        if board[old_i][old_j][0] == BLACK_PIECE or board[old_i][old_j][0] == BLACK_PIECE_CHECK:
            return False
        return True

    # Checa se é possível mover a peça - Computador
    @staticmethod
    def check_moves(board, old_i, old_j, new_i, new_j):
        if new_i > (BOARD_SIZE - 1) or new_i < 0:
            return False
        if new_j > (BOARD_SIZE - 1) or new_j < 0:
            return False
        if board[old_i][old_j] == BLANK_SPACE:
            return False
        if board[new_i][new_j] != BLANK_SPACE:
            return False
        if board[old_i][old_j][0] == WHITE_PIECE or board[old_i][old_j][0] == WHITE_PIECE_CHECK:
            return False
        if board[new_i][new_j] == BLANK_SPACE:
            return True

    # Checa se é possível mover a peça - Jogador
    @staticmethod
    def check_player_moves(board, old_i, old_j, new_i, new_j):
        if new_i > (BOARD_SIZE - 1) or new_i < 0:
            return False
        if new_j > (BOARD_SIZE - 1) or new_j < 0:
            return False
        if board[old_i][old_j] == BLANK_SPACE:
            return False
        if board[new_i][new_j] != BLANK_SPACE:
            return False
        if board[old_i][old_j][0] == BLACK_PIECE or board[old_i][old_j][0] == BLACK_PIECE_CHECK:
            return False
        if board[new_i][new_j] == BLANK_SPACE:
            return True

    # Encontra movimentos possíveis a partir das listas de movimentos e pulos - Computador
    @staticmethod
    def find_available_moves(board):
        available_moves = []
        available_jumps = []
        for m in range(BOARD_SIZE):
            for n in range(BOARD_SIZE):
                if board[m][n][0] == BLACK_PIECE:
                    if Checkers.check_moves(board, m, n, m + 1, n + 1):
                        available_moves.append([m, n, m + 1, n + 1])
                    if Checkers.check_moves(board, m, n, m + 1, n - 1):
                        available_moves.append([m, n, m + 1, n - 1])
                    if Checkers.check_jumps(board, m, n, m + 1, n - 1, m + 2, n - 2):
                        available_jumps.append([m, n, m + 2, n - 2])
                    if Checkers.check_jumps(board, m, n, m + 1, n + 1, m + 2, n + 2):
                        available_jumps.append([m, n, m + 2, n + 2])
                elif board[m][n][0] == BLACK_PIECE_CHECK:
                    if Checkers.check_moves(board, m, n, m + 1, n + 1):
                        available_moves.append([m, n, m + 1, n + 1])
                    if Checkers.check_moves(board, m, n, m + 1, n - 1):
                        available_moves.append([m, n, m + 1, n - 1])
                    if Checkers.check_moves(board, m, n, m - 1, n - 1):
                        available_moves.append([m, n, m - 1, n - 1])
                    if Checkers.check_moves(board, m, n, m - 1, n + 1):
                        available_moves.append([m, n, m - 1, n + 1])
                    if Checkers.check_jumps(board, m, n, m + 1, n - 1, m + 2, n - 2):
                        available_jumps.append([m, n, m + 2, n - 2])
                    if Checkers.check_jumps(board, m, n, m - 1, n - 1, m - 2, n - 2):
                        available_jumps.append([m, n, m - 2, n - 2])
                    if Checkers.check_jumps(board, m, n, m - 1, n + 1, m - 2, n + 2):
                        available_jumps.append([m, n, m - 2, n + 2])
                    if Checkers.check_jumps(board, m, n, m + 1, n + 1, m + 2, n + 2):
                        available_jumps.append([m, n, m + 2, n + 2])
        return (available_jumps, available_moves)[len(available_jumps) == 0]

    # Encontra movimentos possíveis a partir das listas de movimentos e pulos - Jogador
    @staticmethod
    def find_player_available_moves(board):
        available_moves = []
        available_jumps = []
        for m in range(BOARD_SIZE):
            for n in range(BOARD_SIZE):
                if board[m][n][0] == WHITE_PIECE:
                    if Checkers.check_player_moves(board, m, n, m - 1, n - 1):
                        available_moves.append([m, n, m - 1, n - 1])
                    if Checkers.check_player_moves(board, m, n, m - 1, n + 1):
                        available_moves.append([m, n, m - 1, n + 1])
                    if Checkers.check_player_jumps(board, m, n, m - 1, n - 1, m - 2, n - 2):
                        available_jumps.append([m, n, m - 2, n - 2])
                    if Checkers.check_player_jumps(board, m, n, m - 1, n + 1, m - 2, n + 2):
                        available_jumps.append([m, n, m - 2, n + 2])
                elif board[m][n][0] == WHITE_PIECE_CHECK:
                    if Checkers.check_player_moves(board, m, n, m - 1, n - 1):
                        available_moves.append([m, n, m - 1, n - 1])
                    if Checkers.check_player_moves(board, m, n, m - 1, n + 1):
                        available_moves.append([m, n, m - 1, n + 1])
                    if Checkers.check_player_jumps(board, m, n, m - 1, n - 1, m - 2, n - 2):
                        available_jumps.append([m, n, m - 2, n - 2])
                    if Checkers.check_player_jumps(board, m, n, m - 1, n + 1, m - 2, n + 2):
                        available_jumps.append([m, n, m - 2, n + 2])
                    if Checkers.check_player_moves(board, m, n, m + 1, n - 1):
                        available_moves.append([m, n, m + 1, n - 1])
                    if Checkers.check_player_jumps(board, m, n, m + 1, n - 1, m + 2, n - 2):
                        available_jumps.append([m, n, m + 2, n - 2])
                    if Checkers.check_player_moves(board, m, n, m + 1, n + 1):
                        available_moves.append([m, n, m + 1, n + 1])
                    if Checkers.check_player_jumps(board, m, n, m + 1, n + 1, m + 2, n + 2):
                        available_jumps.append([m, n, m + 2, n + 2])
        return (available_jumps, available_moves)[len(available_jumps) == 0]

    # Calcula heurística das jogadas possíveis, avaliando o que é 'melhor'
    @staticmethod
    def calculate_heuristics(board):
        result = 0
        mine = 0
        opp = 0
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if board[i][j][0] == BLACK_PIECE or board[i][j][0] == BLACK_PIECE_CHECK:
                    mine += 1
                    if board[i][j][0] == BLACK_PIECE:
                        result += 5
                    if board[i][j][0] == BLACK_PIECE_CHECK:
                        result += 10
                    if i == 0 or j == 0 or i == (BOARD_SIZE - 1) or j == (BOARD_SIZE - 1):
                        result += (BOARD_SIZE - 1)
                    if i + 1 > (BOARD_SIZE - 1) or j - 1 < 0 or i - 1 < 0 or j + 1 > (BOARD_SIZE - 1):
                        continue
                    if (board[i + 1][j - 1][0] == WHITE_PIECE or board[i + 1][j - 1][0] == WHITE_PIECE_CHECK) and board[i - 1][
                        j + 1] == BLANK_SPACE:
                        result -= 3
                    if (board[i + 1][j + 1][0] == WHITE_PIECE or board[i + 1][j + 1] == WHITE_PIECE_CHECK) and board[i - 1][j - 1] == BLANK_SPACE:
                        result -= 3
                    if board[i - 1][j - 1][0] == WHITE_PIECE_CHECK and board[i + 1][j + 1] == BLANK_SPACE:
                        result -= 3

                    if board[i - 1][j + 1][0] == WHITE_PIECE_CHECK and board[i + 1][j - 1] == BLANK_SPACE:
                        result -= 3
                    if i + 2 > (BOARD_SIZE - 1) or i - 2 < 0:
                        continue
                    if (board[i + 1][j - 1][0] == WHITE_PIECE_CHECK or board[i + 1][j - 1][0] == WHITE_PIECE) and board[i + 2][
                        j - 2] == BLANK_SPACE:
                        result += 6
                    if i + 2 > (BOARD_SIZE - 1) or j + 2 > (BOARD_SIZE - 1):
                        continue
                    if (board[i + 1][j + 1][0] == WHITE_PIECE_CHECK or board[i + 1][j + 1][0] == WHITE_PIECE) and board[i + 2][
                        j + 2] == BLANK_SPACE:
                        result += 6

                elif board[i][j][0] == WHITE_PIECE or board[i][j][0] == WHITE_PIECE_CHECK:
                    opp += 1

        return result + (mine - opp) * 1000

    # Avalia jogadas a partir do calculado acima
    def evaluate_states(self):
        tempoInicial = time.time()
        current_state = Node(deepcopy(self.matrix))

        first_computer_moves = current_state.get_children(True)
        if len(first_computer_moves) == 0:
            if self.player_pieces > self.computer_pieces:
                print(ansi_yellow + "Computador não tem mais movimentos disponíveis, e você tem peças sobrando." + ansi_reset)
                print("=-"*BOARD_SIZE+"=")
                print(ansi_green + "VOCÊ GANHOU!" + ansi_reset)
                print("=-"*BOARD_SIZE+"=")
                exit()
            else:
                print(ansi_yellow + "Computador não tem mais movimentos disponíveis." + ansi_reset)
                print("=-"*BOARD_SIZE+"=")
                print(ansi_green + "JOGO ACABOU!" + ansi_reset)
                print("=-"*BOARD_SIZE+"=")
                exit()
        dict = {}
        for i in range(len(first_computer_moves)):
            child = first_computer_moves[i]
            value = Checkers.minimax(child.get_board(), 4, -math.inf, math.inf, False)
            dict[value] = child
        if len(dict.keys()) == 0:
            print(ansi_green + "Computador está encurralado." + ansi_reset)
            print("=-"*BOARD_SIZE+"=")
            print(ansi_green + "VOCÊ GANHOU!" + ansi_reset)
            print("=-"*BOARD_SIZE+"=")
            exit()
        new_board = dict[max(dict)].get_board()
        move = dict[max(dict)].move
        self.matrix = new_board
        tempoFinal = time.time()
        print("Computador moveu peça da (" + str(move[0]) + "," + str(move[1]) + ") para a posição (" + str(move[2]) + "," + str(move[3]) + ").")
        print("Levou " + str(tempoFinal - tempoInicial) + " segundos para pensar e jogar")

    # Calculo minimax - Alphabeta
    @staticmethod
    def minimax(board, depth, alpha, beta, maximizing_player):
        if depth == 0:
            return Checkers.calculate_heuristics(board)
        current_state = Node(deepcopy(board))
        if maximizing_player is True:
            max_eval = -math.inf
            for child in current_state.get_children(True):
                ev = Checkers.minimax(child.get_board(), depth - 1, alpha, beta, False)
                max_eval = max(max_eval, ev)
                alpha = max(alpha, ev)
                if beta <= alpha:
                    break
            current_state.set_value(max_eval)
            return max_eval
        else:
            min_eval = math.inf
            for child in current_state.get_children(False):
                ev = Checkers.minimax(child.get_board(), depth - 1, alpha, beta, True)
                min_eval = min(min_eval, ev)
                beta = min(beta, ev)
                if beta <= alpha:
                    break
            current_state.set_value(min_eval)
            return min_eval

    # Realiza jogada
    @staticmethod
    def make_a_move(board, old_i, old_j, new_i, new_j, big_letter, queen_row):
        letter = board[old_i][old_j][0]
        i_difference = old_i - new_i
        j_difference = old_j - new_j
        if i_difference == -2 and j_difference == 2:
            board[old_i + 1][old_j - 1] = BLANK_SPACE

        elif i_difference == 2 and j_difference == 2:
            board[old_i - 1][old_j - 1] = BLANK_SPACE

        elif i_difference == 2 and j_difference == -2:
            board[old_i - 1][old_j + 1] = BLANK_SPACE

        elif i_difference == -2 and j_difference == -2:
            board[old_i + 1][old_j + 1] = BLANK_SPACE

        if new_i == queen_row:
            letter = big_letter
        
        board[old_i][old_j] = BLANK_SPACE
        board[new_i][new_j] = letter + str(new_i) + str(new_j)

    def play(self):
        print("\n\n")
        print("|=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=|")
        print("|              REGRAS IMPORTANTES DO JOGO:              |")
        print("|                                                       |")
        print("| 1. As entradas são feitas no formato \"linha,coluna\".  |")
        print("| 2. O jogo pode ser finalizado digitando \"-1\"          |")
        print(f"| 3. Você pode desistir digitando \"s\".                  |")
        print("|                                                       |")
        print("|                                 Desenvolvido por:     |")
        print("|                            Mateus Ferro               |")
        print("|                            Tasi Pasin                 |")
        print("|                            João Gabriel               |")
        print("|                            Gabriel Skorei             |")
        print("|                                                       |")
        print("|                   Tenha um Bom Jogo!                  |")
        print("|=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=|")
        while True:
            self.print_matrix()
            if self.player_turn is True:
                print(ansi_cyan + "\nTurno do Jogador" + ansi_reset)
                self.get_player_input()
            else:
                print(ansi_cyan + "Turno do Computador..." + ansi_reset)
                self.evaluate_states()

            if self.player_pieces == 0:
                self.print_matrix()
                print(ansi_red + "Sem peças disponíveis.\nVocê perdeu!" + ansi_reset)
                exit()
            elif self.computer_pieces == 0:
                self.print_matrix()
                print(ansi_green + "O computador não tem mais peças.\nVocê ganhou!" + ansi_reset)
                exit()
            self.player_turn = not self.player_turn

if __name__ == '__main__':
    checkers = Checkers()
    checkers.play()
