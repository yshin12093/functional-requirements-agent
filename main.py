#!/usr/bin/env python3
"""
Functional Requirements Agent - Main Entry Point
"""

import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import FunctionalRequirementsAgent

def main():
    """Main entry point for the application"""
    app = QApplication(sys.argv)
    window = FunctionalRequirementsAgent()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
