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

# Define as cores das peças de cada jogador
COMPUTER_COLOR_PIECES = ansi_blue
PLAYER_COLOR_PIECES = ansi_magenta

class Node:
    # Construtor da classe Nó
    def __init__(self, board, move=None, parent=None, value=None):
        self.board = board
        self.value = value
        self.move = move
        self.parent = parent

    # Checa e determina possíveis jogadas (em listas)
    def get_children(self, minimizing_player, computer_pieces, player_pieces, player_pieces_qtd):

        current_state = deepcopy(self.board)
        available_moves = []
        children_states = []
        turn_pieces = computer_pieces
        adversary_pieces = player_pieces
        if minimizing_player is True:
            available_moves = Checkers.find_available_moves(current_state, computer_pieces)
        # Verifica para o jogador
        else:
            available_moves = Checkers.find_available_moves(current_state, player_pieces)
            turn_pieces = player_pieces
            adversary_pieces = computer_pieces
        queen_row = (BOARD_SIZE - 1, 0)[turn_pieces[1] == BLACK_PIECE_CHECK]
        for i in range(len(available_moves)):
            old_i = available_moves[i][0]
            old_j = available_moves[i][1]
            new_i = available_moves[i][2]
            new_j = available_moves[i][3]
            state = deepcopy(current_state)
            Checkers.make_a_move(state, old_i, old_j, new_i, new_j, turn_pieces, queen_row, adversary_pieces)
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
        self.player_pieces_txt = None
        self.computer_pieces_txt = None

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
                    # TESTE
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
                color = ansi_reset
                if elem[0] in self.computer_pieces_txt:
                    color = COMPUTER_COLOR_PIECES
                elif elem[0] in self.player_pieces_txt:
                    color = PLAYER_COLOR_PIECES
                print(color + elem + ansi_reset, end=" ",)
            print("|")
        print("   |_________________________________________|")
        for j in range(BOARD_SIZE):
            if j == 0:
                j = "      0"
            print(j, end="   ")
        print("\n")
        
    @staticmethod
    def get_play_input(message):
        # Inicializa as coordenadas de retorno
        coordinate_i = None
        coordinate_j = None
        # Executa loop enquanto as entradas não estiverem corretas
        while None is coordinate_i or None is coordinate_j:
            # Requisita entrada do usuário
            entry = input(f"{message} [i,j]: ")
            # Verifica se entrou com condição de finalizar o jogo
            if entry == EXIT_CONDITION:
                print(ansi_cyan + "Jogo Acabou!" + ansi_reset)
                exit()
            # Verifica se entrou com condição de rendição
            elif entry == SURRENDER_CONDITION:
                print(ansi_cyan + "Você se rendeu!" + ansi_reset)
                exit()
            # Divide os valores
            coordinates = entry.split(",")
            # Verifica se as coordenadas é vetor com tamanho 2
            # Verifica se os valores entrados são inteiros e pertencem ao tabuleiro
            if len(coordinates) == 2 and Checkers.is_value_inside_board(coordinates[0]) and Checkers.is_value_inside_board(coordinates[1]):
                coordinate_i = int(coordinates[0])
                coordinate_j = int(coordinates[1])
            else:
                print(ansi_red + "Entrada Inválida!" + ansi_reset)
        return coordinate_i, coordinate_j
        
        
    @staticmethod
    def is_value_inside_board(value):
        return (isinstance(value, int) or value.isdigit()) and int(value) >= 0 and int(value) < BOARD_SIZE

    # Recebe Input do Jogador
    def get_player_input(self):
        available_moves = Checkers.find_available_moves(self.matrix, self.player_pieces_txt)
        print(f"movimentos do jogador {len(available_moves)}")
        print(available_moves)
        while len(available_moves) > 0:   
            if len(available_moves) == 0:
                if self.computer_pieces > self.player_pieces:
                    print(
                        ansi_red + "Você não possui movimentos disponíveis, e tem menos peças que o adversário. Você Perdeu!" + ansi_reset)
                else:
                    print(ansi_yellow + "Você não tem movimentos disponíveis.\nJogo Terminado!" + ansi_reset)
                exit()
            
            old_i, old_j = Checkers.get_play_input("Escolha a peca")
            new_i, new_j = Checkers.get_play_input("Para onde")
            move = [int(old_i), int(old_j), int(new_i), int(new_j)]
            if move not in available_moves:
                print(ansi_red + "Movimentação Inválida!" + ansi_reset)
            # Define que pode mover e move
            else:
                killed = Checkers.make_a_move(self.matrix, int(old_i), int(old_j), int(new_i), int(new_j), self.player_pieces_txt, 0, self.computer_pieces_txt)
                available_moves.clear()
                if killed:
                    self.computer_pieces -= 1
                    available_moves = Checkers.find_available_jumps(self.matrix, int(new_i), int(new_j),  self.player_pieces_txt, self.computer_pieces_txt)
                    if len(available_moves) > 0:
                        self.print_matrix()

    # Encontra os possíveis movimentos para o jogador
    @staticmethod
    def find_available_moves(board, player):
        # Indica que deve caminhar para baixo no tabuleiro
        multiplier = 1
        # Inicializa peças do adversário como sendo as brandas
        adversary_pieces = (WHITE_PIECE, WHITE_PIECE_CHECK)
        # Verifica se é peça branca
        if player[0] == WHITE_PIECE:
            # Indica que deve caminhar para cima do tabuleiro
            multiplier = -1
            # Altera as peças do adversário para as pretas
            adversary_pieces = (BLACK_PIECE, BLACK_PIECE_CHECK)
        available_moves = list()
        available_jumps = list()
        for m in range(BOARD_SIZE):
            for n in range(BOARD_SIZE):
                available_jumps.extend(Checkers.find_available_jumps(board, m, n, player,adversary_pieces))
                available_moves.extend(Checkers.find_player_available_moves(board, m, n, player, adversary_pieces, multiplier))
        return (available_jumps, available_moves)[len(available_jumps) == 0]

    @staticmethod
    def find_available_jumps(board, m, n, player, adversary_pieces):        
        available_jumps = list()
        for i in range(1, BOARD_SIZE + 1):
            if i == 1 or (i > 1 and board[m][n][0] == player[1]):
                if Checkers.check_jump(board, m, n, m + i, n + i, m + (i+1), n + (i+1), player, adversary_pieces): #Direita baixo
                    available_jumps.append([m, n, m + (i+1), n + (i+1)])
                if Checkers.check_jump(board, m, n, m - i, n - i, m - (i+1), n - (i+1), player, adversary_pieces): #Esquerda cima
                    available_jumps.append([m, n, m - (i+1), n - (i+1)])
                if Checkers.check_jump(board, m, n, m + i, n - i, m + (i+1), n - (i+1), player, adversary_pieces): #Esquerda baixo
                    available_jumps.append([m, n, m + (i+1), n - (i+1)])
                if Checkers.check_jump(board, m, n, m - i, n + i, m - (i+1), n + (i+1), player, adversary_pieces): #Direita cima
                    available_jumps.append([m, n, m - (i+1), n + (i+1)])
        return available_jumps
    
    # Checa se é possível pular a peça
    @staticmethod
    def check_jump(board, old_i, old_j, via_i, via_j, new_i, new_j, player, adversary_pieces):
        if board[old_i][old_j][0] == player[1]: # 7, 4 // 5,2 
            diff = abs(old_i - new_i) # 2
            iMultiplier = 1
            jMultiplier = 1
            if (old_i < new_i): # False
                iMultiplier = -1
            if (old_j < new_j): # False
                jMultiplier = -1
            for i in range(1, diff):
                forI = new_i + i * iMultiplier # 5 + (1 *  1) = 6 // 5 + (2 *  1) = 7 // 2 + (3 *  1) = 5 // 2 + (4 *  1) = 6
                forJ = new_j + i * jMultiplier # 2 + (1 *  1) = 3 // 2 + (2 *  1) = 4 // 7 + (3 * -1) = 4 // 7 + (4 * -1) = 3
                if (Checkers.is_value_inside_board(forI) and Checkers.is_value_inside_board(forJ) and board[forI][forJ][0].lower() == player[0]):
                    return False
        if new_i > (BOARD_SIZE - 1) or new_i < 0:
            return False
        if new_j > (BOARD_SIZE - 1) or new_j < 0:
            return False
        if board[via_i][via_j] == BLANK_SPACE:
            return False
        if board[via_i][via_j][0].lower() == player[0]:
            return False
        if board[new_i][new_j] != BLANK_SPACE:
            return False
        if board[old_i][old_j] == BLANK_SPACE:
            return False
        if board[old_i][old_j][0].lower() == adversary_pieces[0]:
            return False
        return True
    
    # Busca movimentos possíveis para o jogador levando em consideração para onde pode mover (multiplier)
    @staticmethod
    def find_player_available_moves(board, m, n, player, adversary_pieces, multiplier):
        result = list()
        if Checkers.check_player_moves(board, m, n, m + (1 * multiplier), n - 1, player, adversary_pieces):
            result.append([m, n, m + (1 * multiplier), n - 1])
        if Checkers.check_player_moves(board, m, n, m + (1 * multiplier), n + 1, player, adversary_pieces):
            result.append([m, n, m + (1 * multiplier), n + 1])
        if board[m][n][0] == player[1]:
            for i in range(BOARD_SIZE):
                if Checkers.check_player_moves(board, m, n, m - (i * multiplier), n + i, player, adversary_pieces):
                    result.append([m, n, m - (i * multiplier), n + i])
                if Checkers.check_player_moves(board, m, n, m - (i * multiplier), n - i, player, adversary_pieces):
                    result.append([m, n, m - (i * multiplier), n - i])
                if Checkers.check_player_moves(board, m, n, m + (i * multiplier), n + i, player, adversary_pieces):
                    result.append([m, n, m + (i * multiplier), n + i])
                if Checkers.check_player_moves(board, m, n, m + (i * multiplier), n - i, player, adversary_pieces):
                    result.append([m, n, m + (i * multiplier), n - i])
        return result
        
    # Checa se é possível mover a peça
    @staticmethod
    def check_player_moves(board, old_i, old_j, new_i, new_j, player, adversary_pieces):
        diff = abs(old_i - new_i)
        if diff > 1:
            iMultiplier = 1
            jMultiplier = 1
            if (old_i > new_i):
                iMultiplier = -1
            if (old_j > new_j):
                jMultiplier = -1
            for i in range(1, diff - 1):
                forI = old_i + i * iMultiplier
                forJ = old_j + i * jMultiplier
                if (Checkers.is_value_inside_board(forI) and Checkers.is_value_inside_board(forJ) and not board[forI][forJ] == BLANK_SPACE):
                    return False
        if new_i > (BOARD_SIZE - 1) or new_i < 0:
            return False
        if new_j > (BOARD_SIZE - 1) or new_j < 0:
            return False
        if board[old_i][old_j] == BLANK_SPACE:
            return False
        if board[new_i][new_j] != BLANK_SPACE:
            return False
        if board[old_i][old_j][0].lower() == adversary_pieces[0]:
            return False
        if board[new_i][new_j] == BLANK_SPACE:
            return True

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

        first_computer_moves = current_state.get_children(True, self.computer_pieces_txt, self.player_pieces_txt, self.player_pieces)
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
            value = Checkers.minimax(child.get_board(), 4, -math.inf, math.inf, False, self.computer_pieces_txt, self.player_pieces_txt, self.player_pieces)
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
    def minimax(board, depth, alpha, beta, maximizing_player, computer_pieces, player_pieces, player_pieces_qtd):
        if depth == 0:
            return Checkers.calculate_heuristics(board)
        current_state = Node(deepcopy(board))
        if maximizing_player is True:
            max_eval = -math.inf
            for child in current_state.get_children(True, computer_pieces, player_pieces, player_pieces_qtd):
                ev = Checkers.minimax(child.get_board(), depth - 1, alpha, beta, False, computer_pieces, player_pieces, player_pieces_qtd)
                max_eval = max(max_eval, ev)
                alpha = max(alpha, ev)
                if beta <= alpha:
                    break
            current_state.set_value(max_eval)
            return max_eval
        else:
            min_eval = math.inf
            for child in current_state.get_children(False, computer_pieces, player_pieces, player_pieces_qtd):
                ev = Checkers.minimax(child.get_board(), depth - 1, alpha, beta, True, computer_pieces, player_pieces, player_pieces_qtd)
                min_eval = min(min_eval, ev)
                beta = min(beta, ev)
                if beta <= alpha:
                    break
            current_state.set_value(min_eval)
            return min_eval

    # Realiza jogada
    @staticmethod
    def make_a_move(board, old_i, old_j, new_i, new_j, turn_pieces, queen_row, adversary_pieces):
        killed = True
        letter = board[old_i][old_j][0]
        i_difference = old_i - new_i
        j_difference = old_j - new_j
        i_multiplier = int(i_difference / abs(i_difference))
        j_multiplier = int(j_difference / abs(j_difference))
        
        if abs(i_difference) >= 2:
            capture_i = new_i + (1 * i_multiplier)
            capture_j = new_j + (1 * j_multiplier)
            if Checkers.is_value_inside_board(capture_i) and Checkers.is_value_inside_board(capture_j):
                board[capture_i][capture_j] = BLANK_SPACE
        else:
            killed = False        
        if new_i == queen_row:
            letter = turn_pieces[1]
        board[old_i][old_j] = BLANK_SPACE
        board[new_i][new_j] = letter + str(new_i) + str(new_j)
        return killed

    def get_player_turn(self):
        while self.player_pieces_txt is None:
            print("Insira o número da opção do jogador que deve iniciar:")
            print("1. Jogador")
            print("2. Computador")
            try:
                entry = int(input())
                if entry == 1:
                    self.player_pieces_txt = (WHITE_PIECE, WHITE_PIECE_CHECK)
                    self.computer_pieces_txt = (BLACK_PIECE, BLACK_PIECE_CHECK)    
                elif entry == 2:
                    self.player_pieces_txt = (BLACK_PIECE, BLACK_PIECE_CHECK)
                    self.computer_pieces_txt = (WHITE_PIECE, WHITE_PIECE_CHECK)
                    self.player_turn = False 
            except:
                print("Valor inserido incorreto")

    def play(self):
        print("\n\n")
        print("|=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=|")
        print("|              REGRAS IMPORTANTES DO JOGO:              |")
        print("|                                                       |")
        print("| 1. As entradas são feitas no formato \"linha,coluna\".  |")
        print("| 2. O jogo pode ser finalizado digitando \"-1\"          |")
        print("| 3. Você pode desistir digitando \"s\".                  |")
        print("|                                                       |")
        print("|                                 Desenvolvido por:     |")
        print("|                            Mateus Ferro               |")
        print("|                            Tasi Pasin                 |")
        print("|                            João Gabriel               |")
        print("|                            Gabriel Skorei             |")
        print("|                                                       |")
        print("|                   Tenha um Bom Jogo!                  |")
        print("|=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=|")
        
        self.get_player_turn()
        
        game_over = False
        while not game_over:
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
                game_over = True
            elif self.computer_pieces == 0:
                self.print_matrix()
                print(ansi_green + "O computador não tem mais peças.\nVocê ganhou!" + ansi_reset)
                game_over = True
            self.player_turn = not self.player_turn

if __name__ == '__main__':
    checkers = Checkers()
    checkers.play()
