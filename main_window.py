#!/usr/bin/env python3
"""
Главное окно игры "Выключи свет"
"""

from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QGridLayout, QPushButton, QLabel, QMessageBox, QDialog)
from PyQt6.QtGui import QFont

from game_logic import Game
from ui_components import SettingsDialog, RulesDialog, LightButton, DifficultySelectionDialog
from config import DEFAULT_LIGHT_COLOR, DEFAULT_DARK_COLOR, WINDOW_WIDTH, WINDOW_HEIGHT, DIFFICULTY_LEVELS


class MainWindow(QMainWindow):
    """Главное окно игры"""
    
    def __init__(self):
        super().__init__()
        self.game = Game()  # По умолчанию средний уровень
        self.light_color = DEFAULT_LIGHT_COLOR
        self.dark_color = DEFAULT_DARK_COLOR
        self.buttons = []
        
        self.setWindowTitle("Выключи свет")
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        
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
        for difficulty in DIFFICULTY_LEVELS.keys():
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
        dialog = DifficultySelectionDialog(self, DIFFICULTY_LEVELS)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            selected_difficulty = dialog.get_selected_difficulty()
            if selected_difficulty:
                self.set_difficulty(selected_difficulty)