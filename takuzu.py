# takuzu.py: Template para implementação do projeto de Inteligência Artificial 2021/2022.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 00:
# 00000 Nome1
# 00000 Nome2

import sys
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
            return(self.board_numbers[row + 1][col], None)
        elif(row + 2 > self.board_size):
            return(None, self.board_numbers[row - 1][col])
        else:
            return(self.board_numbers[row + 1][col], self.board_numbers[row - 1][col])
        
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
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        # TODO
        pass

    def actions(self, state: TakuzuState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        # TODO
        pass

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

    # TODO: outros metodos da classe


if __name__ == "__main__":
    board = Board.parse_instance_from_stdin()
    print("Initial:\n", board, sep="")
    
    print(board.adjacent_vertical_numbers(3, 3))
    print(board.adjacent_horizontal_numbers(3, 3))
    print(board.adjacent_vertical_numbers(1, 1))
    print(board.adjacent_horizontal_numbers(1, 1))

    # TODO:
    # Ler o ficheiro de input de sys.argv[1],
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    pass