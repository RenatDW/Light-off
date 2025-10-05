#!/usr/bin/env python3
"""
Логика игры "Выключи свет" (Lights Out)
"""

import random
from config import DIFFICULTY_LEVELS, DIRECTIONS, GRID_SIZE


class Game:
    """Класс для логики игры 'Выключи свет'"""
    
    def __init__(self, difficulty='Средний'):
        self._difficulty = difficulty
        self._size = GRID_SIZE  # Фиксированный размер из конфигурации
        self._min_moves, self._max_moves = DIFFICULTY_LEVELS[difficulty]
        self._grid = [[False for _ in range(self._size)] for _ in range(self._size)]
        self._moves = 0
        
    @property
    def difficulty(self):
        """Текущий уровень сложности"""
        return self._difficulty
    
    @property
    def size(self):
        """Размер игрового поля"""
        return self._size
    
    @property
    def grid(self):
        """Состояние игрового поля"""
        return self._grid
    
    @property
    def moves(self):
        """Количество ходов"""
        return self._moves
    
    @property
    def is_solved(self):
        """Проверка, решена ли головоломка"""
        return all(not cell for row in self._grid for cell in row)
    
    def reset_game(self, difficulty=None):
        """Сброс игры с новым уровнем сложности"""
        if difficulty and difficulty in DIFFICULTY_LEVELS:
            self._difficulty = difficulty
            self._min_moves, self._max_moves = DIFFICULTY_LEVELS[difficulty]
        self._grid = [[False for _ in range(self._size)] for _ in range(self._size)]
        self._moves = 0
        self.generate_puzzle()
    
    def generate_puzzle(self):
        """Генерация случайной головоломки в зависимости от уровня сложности"""
        # Используем параметры сложности для генерации
        random_moves = random.randint(self._min_moves, self._max_moves)
        for _ in range(random_moves):
            row = random.randint(0, self._size - 1)
            col = random.randint(0, self._size - 1)
            self._toggle_lights(row, col, count_move=False)
    
    def make_move(self, row, col):
        """Совершение хода"""
        if 0 <= row < self._size and 0 <= col < self._size:
            self._toggle_lights(row, col, count_move=True)
            return True
        return False
    
    def _toggle_lights(self, row, col, count_move=True):
        """Переключение света в клетке и соседних клетках"""
        if count_move:
            self._moves += 1
            
        # Переключаем центральную клетку
        self._grid[row][col] = not self._grid[row][col]
        
        # Переключаем соседние клетки (вверх, вниз, влево, вправо)
        for dr, dc in DIRECTIONS:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < self._size and 0 <= new_col < self._size:
                self._grid[new_row][new_col] = not self._grid[new_row][new_col]
    
    @staticmethod
    def get_cell_neighbors(row, col, size):
        """Получение координат соседних клеток"""
        neighbors = [(row, col)]  # Центральная клетка
        
        for dr, dc in DIRECTIONS:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < size and 0 <= new_col < size:
                neighbors.append((new_row, new_col))
        
        return neighbors