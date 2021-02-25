
# Implementation of an AI Player for Gomoku

from pa2_gomoku import Player
import time
import copy

weights = {"11111": 150000, "011110": 15000, "011100": 3000, "001110": 3000, "011010": 3000, "010110": 3000,
           "11110": 3000, "01111": 3000, "11011": 3000, "10111": 3000, "11101": 3000, "001100": 200,
           "001010": 200, "010100": 200, "000100": 20, "001000": 20}

def evaluate_line(line):
    score = 1
    for key in weights.keys():
        if key in line:
            score += weights[key]
    return score


def symbol(board_checker, my_checker):
    if board_checker == ' ':
        return '0'
    if board_checker == my_checker:
        return '1'
    return '2'

class AIPlayer(Player):
    """ a subclass of Player that looks ahead some number of moves and 
    strategically determines its best next move.
    """

    def next_move(self, board):
        """ returns the called AIPlayer's next move for a game on
            the specified Board object. 
            input: board is a Board object for the game that the called
                     Player is playing.
            return: row, col are the coordinated of a vacant location on the board 
        """
        assert(board.is_full() == False)
        self.num_moves += 1
        pos = []
        dblStart = time.process_time()
        pos = self.evaluate_board(board)
        intTime = "%.2f" % ((time.process_time() - dblStart))
        message = "Elasped Time: " + str(intTime) + " seconds"
        print(message, "\n")
        return (pos[1], pos[2])
        
    # Implementation of Minimax with alpha-beta pruning for AI player
        
    def altChecker(self, checker_val):
        if checker_val == 'X':
            return 'O'
        if checker_val == 'O':
            return 'X'
        
    
    def get_node_list(self, board, checker_val):
        node_list = []
        for i in range(board.width):
            for j in range(board.height):
                if board.slots[i][j] != ' ':
                    continue
                tmp = self.evaluate_node(i, j, board, checker_val) - self.evaluate_node(i, j, board, self.altChecker(checker_val))
                node_list.append((tmp, i, j))
        node_list.sort(reverse=True)
        return node_list

    def evaluate_node(self, r, c, board, checker_val):
        board.slots[r][c] = checker_val
        score = self.evaluate_horizontal(board, r, c, checker_val) + \
                self.evaluate_vertical(board, r, c, checker_val) + \
                self.evaluate_left_diag(board, r, c, checker_val) + \
                self.evaluate_right_diag(board, r, c, checker_val)
        board.slots[r][c] = ' '
        return score

    def evaluate_horizontal(self, board, r, c, checker_val):
        line = str()
        for offset in range(-4, 5):
            if 0 <= c + offset < board.width:
                tmp_checker = board.slots[r][c + offset]
                line += symbol(tmp_checker, checker_val)
        return evaluate_line(line)

    def evaluate_vertical(self, board, r, c, checker_val):
        line = str()
        for offset in range(-4, 5):
            if 0 <= r + offset < board.height:
                tmp_checker = board.slots[r + offset][c]
                line += symbol(tmp_checker, checker_val)
        return evaluate_line(line)

    def evaluate_left_diag(self, board, r, c, checker_val):
        line = str()
        for offset in range(-4, 5):
            if 0 <= c + offset < board.width and 0 <= r + offset < board.height:
                tmp_checker = board.slots[r + offset][c + offset]
                line += symbol(tmp_checker, checker_val)
        return evaluate_line(line)

    def evaluate_right_diag(self, board, r, c, checker_val):
        line = str()
        for offset in range(-4, 5):
            if 0 <= c + offset < board.width and 0 <= r - offset < board.height:
                tmp_checker = board.slots[r - offset][c + offset]
                line += symbol(tmp_checker, checker_val)
        return evaluate_line(line)

    def evaluate_trace(self, trace):
        value, i = 0, 1
        for node in trace:
            value += i * node[0]
            i *= -1
        return value

    def evaluate_board(self, og_board):
        board = copy.deepcopy(og_board)
        node_list = self.get_node_list(board, self.checker)
        if node_list[0][0] >= 1440:
            return node_list[0]
        best_val, best_node = -10000000, node_list[0]
        for node in node_list:
            board.slots[node[1]][node[2]] = self.checker
            value = self.minmax(board, 1, False, -10000000, 10000000, [[node[1], node[2]]])
            board.slots[node[1]][node[2]] = ' '
            if value > best_val:
                best_val, best_node = value, node
        return best_node

    def minmax(self, og_board, depth, is_max_player, alpha, beta, og_trace):
        if depth == 0:
            return self.evaluate_trace(og_trace)
        best_val = -10000000 if is_max_player else 10000000
        board = copy.deepcopy(og_board)
        trace = copy.deepcopy(og_trace)
        checker_val = self.checker if is_max_player else self.opponent_checker()
        node_list = self.get_node_list(board, checker_val)
        for node in node_list:
            trace.append(node)
            board.slots[node[1]][node[2]] = checker_val
            value = self.minmax(board, depth - 1, not is_max_player, alpha, beta, trace)
            board.slots[node[1]][node[2]] = checker_val
            trace.remove(node)
            if (is_max_player and value > best_val) or (not is_max_player and value < best_val):
                best_val = value
            if is_max_player:
                alpha = max(best_val, alpha)
            else:
                beta = min(best_val, beta)
            if beta <= alpha:
                break
        return best_val
            
            
