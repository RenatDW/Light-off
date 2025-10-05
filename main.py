#!/usr/bin/env python3
"""
Игра "Выключи свет" (Lights Out)
Реализация с использованием PyQt6
"""

import sys
import random
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QGridLayout, QPushButton, QLabel,
                            QMenuBar, QMessageBox, QDialog, QSpinBox,
                            QColorDialog, QTextEdit, QFormLayout)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QPalette, QFont


class Game:
    """Класс для логики игры 'Выключи свет'"""
    
    # Уровни сложности: (мин. ходов для генерации, макс. ходов)
    DIFFICULTY_LEVELS = {
        'Легкий': (5, 15),
        'Средний': (15, 25),
        'Сложный': (25, 40),
        'Эксперт': (40, 60)
    }
    
    def __init__(self, difficulty='Средний'):
        self._difficulty = difficulty
        self._size = 5  # Фиксированный размер 5x5
        self._min_moves, self._max_moves = self.DIFFICULTY_LEVELS[difficulty]
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
        if difficulty and difficulty in self.DIFFICULTY_LEVELS:
            self._difficulty = difficulty
            self._min_moves, self._max_moves = self.DIFFICULTY_LEVELS[difficulty]
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
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < self._size and 0 <= new_col < self._size:
                self._grid[new_row][new_col] = not self._grid[new_row][new_col]
    
    @staticmethod
    def get_cell_neighbors(row, col, size):
        """Получение координат соседних клеток"""
        neighbors = [(row, col)]  # Центральная клетка
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < size and 0 <= new_col < size:
                neighbors.append((new_row, new_col))
        
        return neighbors


class SettingsDialog(QDialog):
    """Диалог настроек игры"""
    
    def __init__(self, parent=None, light_color="#ffff00", dark_color="#808080"):
        super().__init__(parent)
        self.setWindowTitle("Настройки игры")
        self.setModal(True)
        
        self.light_color = light_color
        self.dark_color = dark_color
        
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QFormLayout()
        
        # Цвет включенной лампочки
        self.light_color_btn = QPushButton("Выбрать цвет")
        self.light_color_btn.clicked.connect(self._choose_light_color)
        self.light_color_btn.setStyleSheet(f"background-color: {self.light_color}")
        layout.addRow("Цвет включенной лампочки:", self.light_color_btn)
        
        # Цвет выключенной лампочки
        self.dark_color_btn = QPushButton("Выбрать цвет")
        self.dark_color_btn.clicked.connect(self._choose_dark_color)
        self.dark_color_btn.setStyleSheet(f"background-color: {self.dark_color}")
        layout.addRow("Цвет выключенной лампочки:", self.dark_color_btn)
        
        # Кнопки OK/Cancel
        buttons_layout = QHBoxLayout()
        ok_btn = QPushButton("OK")
        cancel_btn = QPushButton("Отмена")
        
        ok_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)
        
        buttons_layout.addWidget(ok_btn)
        buttons_layout.addWidget(cancel_btn)
        
        layout.addRow(buttons_layout)
        self.setLayout(layout)
    
    def _choose_light_color(self):
        color = QColorDialog.getColor(QColor(self.light_color), self)
        if color.isValid():
            self.light_color = color.name()
            self.light_color_btn.setStyleSheet(f"background-color: {self.light_color}")
    
    def _choose_dark_color(self):
        color = QColorDialog.getColor(QColor(self.dark_color), self)
        if color.isValid():
            self.dark_color = color.name()
            self.dark_color_btn.setStyleSheet(f"background-color: {self.dark_color}")
    
    def get_settings(self):
        """Получение настроек"""
        return {
            'light_color': self.light_color,
            'dark_color': self.dark_color
        }


class RulesDialog(QDialog):
    """Диалог с правилами игры"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Правила игры")
        self.setModal(True)
        self.resize(500, 400)
        
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout()
        
        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        text_edit.setHtml("""
        <h2>Правила игры "Выключи свет"</h2>
        
        <h3>Цель игры:</h3>
        <p>Выключить все лампочки на игровом поле.</p>
        
        <h3>Правила:</h3>
        <ul>
            <li>При нажатии на любую лампочку она меняет свое состояние (включена/выключена)</li>
            <li><b>Важно:</b> Также меняется состояние всех соседних лампочек (сверху, снизу, слева, справа)</li>
            <li>Диагональные соседи НЕ затрагиваются</li>
            <li>Игра начинается с некоторыми включенными лампочками</li>
            <li>Победа достигается, когда все лампочки выключены</li>
        </ul>
        
        <h3>Стратегия:</h3>
        <p>Это математическая головоломка. Порядок нажатий не важен - важно только 
        количество нажатий на каждую позицию (четное или нечетное).</p>
        
        <h3>Управление:</h3>
        <ul>
            <li>Нажимайте на лампочки мышью</li>
            <li>Используйте меню для новой игры и настроек</li>
            <li>Счетчик ходов показывает количество сделанных нажатий</li>
        </ul>
        """)
        
        layout.addWidget(text_edit)
        
        close_btn = QPushButton("Закрыть")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)
        
        self.setLayout(layout)


class LightButton(QPushButton):
    """Кнопка-лампочка"""
    
    clicked_with_position = pyqtSignal(int, int)
    
    def __init__(self, row, col, parent=None):
        super().__init__(parent)
        self.row = row
        self.col = col
        self.is_on = False
        self.light_color = "#ffff00"  # Желтый
        self.dark_color = "#808080"   # Серый
        
        self.setFixedSize(50, 50)
        self.clicked.connect(self._on_clicked)
        self.update_appearance()
    
    def _on_clicked(self):
        self.clicked_with_position.emit(self.row, self.col)
    
    def set_state(self, is_on, light_color="#ffff00", dark_color="#808080"):
        """Установка состояния лампочки"""
        self.is_on = is_on
        self.light_color = light_color
        self.dark_color = dark_color
        self.update_appearance()
    
    def update_appearance(self):
        """Обновление внешнего вида"""
        color = self.light_color if self.is_on else self.dark_color
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                border: 2px solid black;
                border-radius: 25px;
            }}
            QPushButton:hover {{
                border: 3px solid blue;
            }}
        """)


class MainWindow(QMainWindow):
    """Главное окно игры"""
    
    def __init__(self):
        super().__init__()
        self.game = Game()  # По умолчанию средний уровень
        self.light_color = "#ffff00"  # Желтый
        self.dark_color = "#808080"   # Серый
        self.buttons = []
        
        self.setWindowTitle("Выключи свет")
        self.setFixedSize(400, 500)
        
        self._setup_ui()
        self._setup_menu()
        self.new_game()
    
    def _setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        self.main_layout = QVBoxLayout()
        
        # Информационная панель
        info_layout = QHBoxLayout()
        self.difficulty_label = QLabel(f"Уровень: {self.game.difficulty}")
        self.difficulty_label.setFont(QFont("Arial", 10))
        self.moves_label = QLabel("Ходы: 0")
        self.moves_label.setFont(QFont("Arial", 12))
        
        info_layout.addWidget(self.difficulty_label)
        info_layout.addStretch()
        info_layout.addWidget(self.moves_label)
        
        self.main_layout.addLayout(info_layout)
        
        # Игровое поле
        self.grid_widget = QWidget()
        self.main_layout.addWidget(self.grid_widget)
        
        # Кнопка новой игры
        new_game_btn = QPushButton("Новая игра")
        new_game_btn.clicked.connect(self.new_game)
        self.main_layout.addWidget(new_game_btn)
        
        central_widget.setLayout(self.main_layout)
    
    def _setup_menu(self):
        menubar = self.menuBar()
        
        # Меню Игра
        game_menu = menubar.addMenu("Игра")
        
        new_action = game_menu.addAction("Новая игра")
        new_action.triggered.connect(self.new_game)
        
        settings_action = game_menu.addAction("Настройки")
        settings_action.triggered.connect(self.show_settings)
        
        # Меню сложности
        difficulty_menu = game_menu.addMenu("Уровень сложности")
        for difficulty in Game.DIFFICULTY_LEVELS.keys():
            action = difficulty_menu.addAction(difficulty)
            action.triggered.connect(lambda checked, d=difficulty: self.set_difficulty(d))
        
        game_menu.addSeparator()
        
        exit_action = game_menu.addAction("Выход")
        exit_action.triggered.connect(self.close)
        
        # Меню Справка
        help_menu = menubar.addMenu("Справка")
        
        rules_action = help_menu.addAction("Правила")
        rules_action.triggered.connect(self.show_rules)
    
    def _create_grid(self):
        """Создание сетки кнопок"""
        # Удаляем старый grid_widget если он есть
        if hasattr(self, 'grid_widget') and self.grid_widget is not None:
            self.main_layout.removeWidget(self.grid_widget)
            self.grid_widget.setParent(None)
            self.grid_widget.deleteLater()
        
        # Создаем новый grid_widget
        self.grid_widget = QWidget()
        
        # Вставляем его в правильное место в layout (позиция 1 - после info_layout)
        self.main_layout.insertWidget(1, self.grid_widget)
        
        # Создание новой сетки
        self.grid_layout = QGridLayout()
        self.grid_widget.setLayout(self.grid_layout)
        
        self.buttons = []
        for row in range(self.game.size):
            button_row = []
            for col in range(self.game.size):
                button = LightButton(row, col)
                button.clicked_with_position.connect(self.on_button_clicked)
                self.grid_layout.addWidget(button, row, col)
                button_row.append(button)
            self.buttons.append(button_row)
    
    def update_display(self):
        """Обновление отображения игрового поля"""
        for row in range(self.game.size):
            for col in range(self.game.size):
                is_on = self.game.grid[row][col]
                self.buttons[row][col].set_state(is_on, self.light_color, self.dark_color)
        
        self.moves_label.setText(f"Ходы: {self.game.moves}")
        self.difficulty_label.setText(f"Уровень: {self.game.difficulty}")
    
    def on_button_clicked(self, row, col):
        """Обработка нажатия на кнопку"""
        self.game.make_move(row, col)
        self.update_display()
        
        if self.game.is_solved:
            self.show_victory_dialog()
    
    def new_game(self):
        """Начало новой игры"""
        self.game.reset_game()
        self._create_grid()
        self.update_display()
    
    def show_settings(self):
        """Показ диалога настроек"""
        dialog = SettingsDialog(self, self.light_color, self.dark_color)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            settings = dialog.get_settings()
            self.light_color = settings['light_color']
            self.dark_color = settings['dark_color']
            
            # Цвета изменились, обновляем отображение
            self.update_display()
    
    def show_rules(self):
        """Показ диалога с правилами"""
        dialog = RulesDialog(self)
        dialog.exec()
    
    def set_difficulty(self, difficulty):
        """Установка уровня сложности"""
        self.game.reset_game(difficulty)
        self._create_grid()
        self.update_display()
    
    def show_victory_dialog(self):
        """Показ диалога победы с предложением новой игры"""
        msg = QMessageBox(self)
        msg.setWindowTitle("Поздравляем!")
        msg.setText(f"🎉 Вы решили головоломку за {self.game.moves} ходов!")
        msg.setInformativeText(f"Уровень сложности: {self.game.difficulty}")
        
        # Добавляем кнопки
        new_game_btn = msg.addButton("Новая игра", QMessageBox.ButtonRole.AcceptRole)
        change_difficulty_btn = msg.addButton("Изменить сложность", QMessageBox.ButtonRole.ActionRole)
        close_btn = msg.addButton("Закрыть", QMessageBox.ButtonRole.RejectRole)
        
        msg.setDefaultButton(new_game_btn)
        msg.exec()
        
        # Обработка нажатий
        if msg.clickedButton() == new_game_btn:
            self.new_game()
        elif msg.clickedButton() == change_difficulty_btn:
            self.show_difficulty_selection()
    
    def show_difficulty_selection(self):
        """Показ диалога выбора сложности"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Выбор уровня сложности")
        dialog.setModal(True)
        
        layout = QVBoxLayout()
        
        # Добавляем описание уровней
        info_label = QLabel("Выберите уровень сложности:")
        info_label.setFont(QFont("Arial", 12))
        layout.addWidget(info_label)
        
        # Создаем кнопки для каждого уровня
        for difficulty, (min_moves, max_moves) in Game.DIFFICULTY_LEVELS.items():
            btn = QPushButton(f"{difficulty} ({min_moves}-{max_moves} ходов)")
            btn.clicked.connect(lambda checked, d=difficulty: self._select_difficulty(d, dialog))
            layout.addWidget(btn)
        
        dialog.setLayout(layout)
        dialog.exec()
    
    def _select_difficulty(self, difficulty, dialog):
        """Выбор сложности и закрытие диалога"""
        self.set_difficulty(difficulty)
        dialog.accept()


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()