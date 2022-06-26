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
from utils import print_table


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
                str_ret += str(arr[i]) + '\t'
            if(not np.array_equal(arr,self.board_numbers[self.board_size - 1])):
                str_ret += (str(arr[len(arr) - 1]) + '\n')
            else:
                str_ret += (str(arr[len(arr) - 1]))
        return str_ret

    # TODO: outros metodos da classe


class Takuzu(Problem):
    #todo: exitem mais movimentos obrigatorios; nos nao obrigatorios apenas dar uma posicao; goal_test apenas ver se nao tem dois
    board = Board()
    initial = TakuzuState(board)
    
    #def goal_test(self, state: TakuzuState) -> bool:
    
    # def goal_test(self, state: TakuzuState) -> bool:
    #     board = state.board
    #     for row in range(board.board_size):
    #         for col in range(board.board_size):
    #             if board.get_number(row, col) == 2:
    #                 return False
    #     return True

    def __init__(self, board: Board):
        self.board = board
        self.initial = TakuzuState(board)

    def actions(self, state: TakuzuState):
        list1 = []
        board = state.board
        obg_move = self.get_obligatory_move(state)
        if(obg_move != None):
            #print(obg_move)
            list1.append(obg_move)
            return list1
        for row in range(board.board_size):
            for col in range(board.board_size):
                if board.get_number(row, col) == 2:
                    if self.valid_action(row, col, state, 0) and self.valid_action(row, col, state, 1):
                        list1.append((row, col, 0))
                        list1.append((row, col, 1))
                        #print(list1)
                        return list1
        return list1

    def result(self, state: TakuzuState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
    
        actionList = self.actions(state)
        new_board = Board()
        new_board.board_numbers = np.copy(state.board.board_numbers)
        new_board.board_size = state.board.board_size
        new_state = TakuzuState(new_board)
        
        for act in actionList:
            if act == action:
                #print(act)
                new_state.board.board_numbers[action[0]][action[1]] = action[2]
                return new_state

    def goal_test(self, state: TakuzuState):
        board = state.board
        for row in board.board_numbers:
            for num in row:
                if num == 2:
                    return False
        return True

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass
    
    def valid_action(self, row : int, col : int, state : TakuzuState, num : int) -> bool:
        board = state.board
        
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
        
        count_row = 0
        count_col = 0
        
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
    
    def get_obligatory_move(self, state : TakuzuState) -> Tuple:
        board = state.board
        for row_num in range(board.board_size):
            row = self.get_row(row_num, board)
            col = self.get_col(row_num, board)
            for col_num in range(board.board_size):
                if board.get_number(row_num, col_num) == 2:
                    adj_hori_numbers = board.adjacent_horizontal_numbers(row_num, col_num)
                    adj_vert_numbers = board.adjacent_vertical_numbers(row_num, col_num)
                    
                    if adj_hori_numbers[0] == adj_hori_numbers[1] and adj_hori_numbers[0] != 2:
                        num = abs(adj_hori_numbers[0] - 1)
                        if self.valid_action(row_num, col_num, state, num):
                            return (row_num, col_num, num)
                    
                    if adj_vert_numbers[0] == adj_vert_numbers[1] and adj_vert_numbers[0] != 2:
                        num = abs(adj_vert_numbers[0] - 1)
                        if self.valid_action(row_num, col_num, state, num):
                            return (row_num, col_num, num)

                if col_num != board.board_size - 1:
                    if(row[col_num] == row[col_num + 1] and row[col_num] != 2):
                        if col_num + 2 < board.board_size:
                            if row[col_num + 2] == 2:
                                if self.valid_action(row_num, col_num + 2, state, abs(row[col_num] - 1)):
                                    return(row_num, col_num + 2, abs(row[col_num] - 1))
                        if col_num - 1 >= 0:
                            if row[col_num - 1] == 2:
                                if self.valid_action(row_num, col_num - 1, state, abs(row[col_num] - 1)):
                                    return (row_num, col_num - 1, abs(row[col_num] - 1))
                                
                
                if col_num != board.board_size - 1:
                    if(col[col_num] == col[col_num + 1] and col[col_num] != 2):
                        if col_num + 2 < board.board_size:
                            if col[col_num + 2] == 2:
                                if self.valid_action(col_num + 2, row_num, state, abs(col[col_num] - 1)):
                                    return(col_num + 2, row_num, abs(col[col_num] - 1))
                        if col_num - 1 >= 0:
                            if col[col_num - 1] == 2:
                                if self.valid_action(col_num - 1, row_num, state, abs(col[col_num] - 1)):
                                    return (col_num - 1, row_num, abs(col[col_num] - 1))
                                
            count_0 = 0
            count_1 = 0
            first_2 = 0
            check = True
            
            for pos in range(board.board_size):
                if row[pos] == 0:
                    count_0 += 1
                elif row[pos] == 1:
                    count_1 += 1
                elif check == True:
                    first_2 = pos
                    check = False
            
            max_num = (board.board_size // 2) + (board.board_size % 2)
            
            if not check:
                if(count_0 == max_num):
                    if self.valid_action(row_num, first_2, state, 1):
                        return (row_num, first_2, 1)
                elif(count_1 == max_num):
                    if self.valid_action(row_num, first_2, state, 0):
                        return (row_num, first_2, 0)
                               
                    
            count_0 = 0
            count_1 = 0
            first_2 = 0
            check = True
            
            for pos in range(board.board_size):
                if col[pos] == 0:
                    count_0 += 1
                elif col[pos] == 1:
                    count_1 += 1
                elif check == True:
                    first_2 = pos
                    check = False
            
            if not check:
                if(count_0 == max_num):
                    if self.valid_action(first_2, row_num, state, 1):
                        return (first_2, row_num, 1)
                elif(count_1 == max_num):
                    if self.valid_action(first_2, row_num, state, 0):
                        return (first_2, row_num, 0)
                                    
                    
        return None

    
    # def get_obligatory_move_aux(self, line, board_size, n_line):
    #     count = 0
    #     other_coord = 0
        
    #     for pos in range(board_size):
    #         if line[pos] == 2:
    #             count += 1
    #             other_coord = pos
    #     if count == 1:
    #         return(n_line, other_coord, self.find_number_obligatory_move(line, n_line, other_coord, board))
    #     return None
            
    # def find_number_obligatory_move(self, line, row_pos, col_pos, board):
    #     count_0 = 0
    #     count_1 = 0
    #     for num in line:
    #         if num == 0:
    #             count_0 += 1
    #         elif num == 1:
    #             count_1 += 1
        
    #     if count_0 > count_1:
    #         return 1
    #     elif count_1 > count_0:
    #         return 0
    #     else:
    #         if self.valid_action(row_pos, col_pos, board, 0):
    #             return 0
    #         elif self.valid_action(row_pos, col_pos, board, 1):
    #             return 1
            
    #     return None
        
    # TODO: outros metodos da classe


if __name__ == "__main__":
    board = Board.parse_instance_from_stdin()

    # Ler tabuleiro do ficheiro 'i1.txt' (Figura 1):
    # $ python3 takuzu < i1.txt
    # Criar uma instância de Takuzu:
    problem = Takuzu(board)
    # Obter o nó solução usando a procura em profundidade:
    goal_node = depth_first_tree_search(problem)
    # Verificar se foi atingida a solução
    if(problem.goal_test(goal_node.state)):
        print(goal_node.state.board)
    pass