#!/usr/bin/env python3
"""
Игра "Выключи свет" (Lights Out)
Реализация с использованием PyQt6
Точка входа в приложение
"""

import sys
from PyQt6.QtWidgets import QApplication

from main_window import MainWindow


def main():
    """Основная функция запуска приложения"""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()