# takuzu.py: Template para implementação do projeto de Inteligência Artificial 2021/2022.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 00:
# 00000 Nome1
# 00000 Nome2

import sys
from typing import Tuple
import numpy as np

from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)


class TakuzuState:
    state_id = 0

    
    def __init__(self, board):
        self.board = board
        self.id = TakuzuState.state_id
        TakuzuState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id

    # TODO: outros metodos da classe


class Board:
    """Representação interna de um tabuleiro de Takuzu."""
    board_size = 0
    board_numbers = np.array([])

    def get_number(self, row: int, col: int) -> int:
        return(self.board_numbers[row][col])

    def adjacent_vertical_numbers(self, row: int, col: int) -> (int, int):
        if(row - 1 < 0 and row + 2 > self.board_size):
            return(None, None)
        elif(row - 1 < 0):
            return(None, self.board_numbers[row + 1][col])
        elif(row + 2 > self.board_size):
            return(self.board_numbers[row - 1][col], None)
        else:
            return(self.board_numbers[row - 1][col], self.board_numbers[row + 1][col])
        
    def adjacent_horizontal_numbers(self, row: int, col: int) -> (int, int):
        if(col - 1 < 0 and col + 2 > self.board_size):
            return(None, None)
        elif(col - 1 < 0):
            return(None, self.board_numbers[row][col + 1])
        elif(col + 2 > self.board_size):
            return(self.board_numbers[row][col - 1], None)
        else:
            return(self.board_numbers[row][col - 1], self.board_numbers[row][col + 1])
        

    @staticmethod
    def parse_instance_from_stdin():
        from sys import stdin
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.
        """
        board = Board()
        array1 = np.array([])
        
        s = stdin.readline()
        board.board_size = int(s)
        
        for i in range(board.board_size):
            str1 = stdin.readline()
            
            for num in str1:
                if(num != '\t' and num != '\n' and num != " "):
                    array1 = np.append(array1, [int(num)])
        
        array1 = array1.reshape(board.board_size, board.board_size)
        array1 = array1.astype(int)
        board.board_numbers = array1

        return board
    
    def __str__(self) -> str:
        str_ret = ""
        for arr in self.board_numbers:
            for i in range(len(arr) - 1):
                str_ret += str(arr[i]) + " "
            str_ret += (str(arr[len(arr) - 1]) + '\n')
        return str_ret

    # TODO: outros metodos da classe


class Takuzu(Problem):
    board = Board()
    
    def __init__(self, board: Board):
        self.board = board

    def actions(self, state: TakuzuState):
        list1 = []
        board = state.board
        obg_move = self.get_obligatory_move(board) 
        if(obg_move != None):
            list1.append(obg_move)
            return list1
        for row in range(board.board_size):
            for col in range(board.board_size):
                if board.get_number(row, col) == 2:
                    if self.valid_action(row, col, board, 0):
                        list1.append((row, col, 0))
                    if self.valid_action(row, col, board, 1):
                        list1.append((row, col, 1))
        return list1
        

    def result(self, state: TakuzuState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        # TODO
        pass

    def goal_test(self, state: TakuzuState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas com uma sequência de números adjacentes."""
        # TODO
        pass

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass
    
    def valid_action(self, row : int, col : int, board : Board, num : int) -> bool:
        adj_vert = board.adjacent_vertical_numbers(row, col)
        adj_hor = board.adjacent_horizontal_numbers(row, col)
        
        if adj_vert[0] == num:
            if board.adjacent_vertical_numbers(row - 1, col)[0] == num:
                return False
        if adj_vert[1] == num:
            if board.adjacent_vertical_numbers(row + 1, col)[1] == num:
                return False
        if adj_hor[0] == num:
            if board.adjacent_horizontal_numbers(row, col - 1)[0] == num:
                return False
        if adj_hor[1] == num:
            if board.adjacent_horizontal_numbers(row, col + 1)[1] == num:
                return False
        
        row = self.get_row(row, board)
        col = self.get_col(col, board)
        
        count_row, count_col = 0
        
        for i in range(board.board_size):
            if(row[i] == num):
                count_row += 1
            if(col[i] == num):
                count_col += 1
                
        max_num = (board.board_size // 2) + (board.board_size % 2)

        if(count_row >= max_num or count_col >= max_num):
            return False
        
        return True
    
    def get_row(self, row : int, board : Board):
        return(board.board_numbers[row])
        
    def get_col(self, col : int, board : Board):
        list1 = []
        for i in range(board.board_size):
            list1.append(board.board_numbers[i][col])
        return np.array(list1)
    
    def get_obligatory_move(self, board : Board) -> Tuple:
        """
        for row in board.board_numbers:
            count = 0
            for num in row:
                if num == 2:
                    count += 1
            if count == 1:
        """
        for i in range(board.board_size):
            row = self.get_row(i, board)
            print("row: ", row)
            move = self.get_obligatory_move_aux(row, board.board_size, i)
            
            if move != None:
               return move 
            
            col = self.get_col(i, board)
            print("col: ", col)
            move = self.get_obligatory_move_aux(col, board.board_size, i)
            
            if move != None:
                return (move[1], move[0], move[2])
        
        return None
    
    def get_obligatory_move_aux(self, line, board_size, n_line):
        count = 0
        other_coord = 0
        
        print("yeet: ", line)
        for pos in range(board_size):
            if line[pos] == 2:
                count += 1
                other_coord = pos
        if count == 1:
            return(n_line, other_coord, self.find_number_obligatory_move(line, n_line, other_coord, board))
        return None
            
    def find_number_obligatory_move(self, line, row_pos, col_pos, board):
        count_0 = 0
        count_1 = 0
        for num in line:
            if num == 0:
                count_0 += 1
            elif num == 1:
                count_1 += 1
        
        if count_0 > count_1:
            return 1
        elif count_1 > count_0:
            return 0
        else:
            if self.valid_action(row_pos, col_pos, board, 0):
                return 0
            elif self.valid_action(row_pos, col_pos, board, 1):
                return 1
            
        return None
        
    # TODO: outros metodos da classe


if __name__ == "__main__":
    board = Board.parse_instance_from_stdin()
    
    problem = Takuzu(board)
    
    s0 = TakuzuState(board)
    print("Initial:\n", s0.board, sep="")
    
    print(problem.actions(s0))

    
    # TODO:
    # Ler o ficheiro de input de sys.argv[1],
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    pass