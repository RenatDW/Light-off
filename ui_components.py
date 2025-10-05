#!/usr/bin/env python3
"""
UI компоненты для игры "Выключи свет"
"""

from PyQt6.QtWidgets import (QPushButton, QDialog, QVBoxLayout, QHBoxLayout, 
                            QFormLayout, QColorDialog, QTextEdit, QLabel)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QFont

from config import DEFAULT_LIGHT_COLOR, DEFAULT_DARK_COLOR, BUTTON_SIZE, BUTTON_STYLE, RULES_HTML


class SettingsDialog(QDialog):
    """Диалог настроек игры"""
    
    def __init__(self, parent=None, light_color=DEFAULT_LIGHT_COLOR, dark_color=DEFAULT_DARK_COLOR):
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
        text_edit.setHtml(RULES_HTML)
        
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
        self.light_color = DEFAULT_LIGHT_COLOR
        self.dark_color = DEFAULT_DARK_COLOR
        
        self.setFixedSize(BUTTON_SIZE, BUTTON_SIZE)
        self.clicked.connect(self._on_clicked)
        self.update_appearance()
    
    def _on_clicked(self):
        self.clicked_with_position.emit(self.row, self.col)
    
    def set_state(self, is_on, light_color=DEFAULT_LIGHT_COLOR, dark_color=DEFAULT_DARK_COLOR):
        """Установка состояния лампочки"""
        self.is_on = is_on
        self.light_color = light_color
        self.dark_color = dark_color
        self.update_appearance()
    
    def update_appearance(self):
        """Обновление внешнего вида"""
        color = self.light_color if self.is_on else self.dark_color
        self.setStyleSheet(BUTTON_STYLE.format(color=color))


class DifficultySelectionDialog(QDialog):
    """Диалог выбора уровня сложности"""
    
    def __init__(self, parent=None, difficulty_levels=None):
        super().__init__(parent)
        self.setWindowTitle("Выбор уровня сложности")
        self.setModal(True)
        self.selected_difficulty = None
        self.difficulty_levels = difficulty_levels or {}
        
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout()
        
        # Добавляем описание уровней
        info_label = QLabel("Выберите уровень сложности:")
        info_label.setFont(QFont("Arial", 12))
        layout.addWidget(info_label)
        
        # Создаем кнопки для каждого уровня
        for difficulty, (min_moves, max_moves) in self.difficulty_levels.items():
            btn = QPushButton(f"{difficulty} ({min_moves}-{max_moves} ходов)")
            btn.clicked.connect(lambda checked, d=difficulty: self._select_difficulty(d))
            layout.addWidget(btn)
        
        self.setLayout(layout)
    
    def _select_difficulty(self, difficulty):
        """Выбор сложности и закрытие диалога"""
        self.selected_difficulty = difficulty
        self.accept()
    
    def get_selected_difficulty(self):
        """Получение выбранного уровня сложности"""
        return self.selected_difficulty