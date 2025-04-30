"""
Styles for the Functional Requirements Agent application.
This module contains all styling-related code to keep the main application clean.
"""

from PySide6.QtGui import QFont, QColor, QPalette
from PySide6.QtCore import Qt

class AppStyles:
    """Class containing all styling for the application"""
    
    @staticmethod
    def get_dark_theme_palette():
        """Get the dark theme palette for the application"""
        palette = QPalette()
        
        # Set background color to dark (black/dark gray)
        palette.setColor(QPalette.Window, QColor(18, 18, 18))  # Almost black
        palette.setColor(QPalette.WindowText, QColor(255, 255, 255))  # White text
        
        # Set text colors
        palette.setColor(QPalette.Base, QColor(30, 30, 30))  # Dark gray for input fields
        palette.setColor(QPalette.AlternateBase, QColor(45, 45, 45))
        palette.setColor(QPalette.Text, QColor(255, 255, 255))  # White text
        palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))  # White button text
        
        # Set button colors
        palette.setColor(QPalette.Button, QColor(70, 130, 180))  # Steel blue for buttons
        
        # Set highlight colors
        palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
        
        return palette
    
    @staticmethod
    def get_app_stylesheet():
        """Get the application stylesheet"""
        return """
            QTextEdit { 
                background-color: #262626; 
                color: #ffffff; 
                border: 1px solid #555555; 
                border-radius: 5px; 
            }
            QPushButton { 
                background-color: #4682b4; 
                color: white; 
                border-radius: 5px; 
                font-weight: bold; 
            }
            QPushButton:hover { 
                background-color: #5c9bd1; 
            }
            QLabel { 
                color: #ffffff; 
            }
        """
    
    @staticmethod
    def get_fonts():
        """Get the fonts used in the application"""
        return {
            "app": QFont("Helvetica", 16),
            "title": QFont("Helvetica", 28, QFont.Bold),
            "description": QFont("Helvetica", 18),
            "chat": QFont("Helvetica", 18),
            "button": QFont("Helvetica", 16)
        }
    
    @staticmethod
    def get_button_styles():
        """Get button styles for different types of buttons"""
        return {
            "project": "background-color: #9370DB; color: white; border-radius: 5px;",
            "review": "background-color: #4682b4; color: white; border-radius: 5px;",
            "complete": "background-color: #228B22; color: white; border-radius: 5px;",
            "export": "background-color: #FF8C00; color: white; border-radius: 5px;",
            "send": "background-color: #4682b4; color: white; border-radius: 5px;"
        }
    
    @staticmethod
    def get_status_styles():
        """Get styles for status labels"""
        return {
            "default": "color: #ffffff; margin-bottom: 10px;",
            "in_progress": "color: #ff9900; margin-bottom: 10px;",
            "complete": "color: #00cc00; margin-bottom: 10px;"
        }
    
    @staticmethod
    def get_message_styles():
        """Get styles for chat messages"""
        return {
            "agent": """
                <div style='background-color: #333333; padding: 15px; border-radius: 10px; margin-bottom: 15px;'>
                    <span style='color: #66ccff; font-weight: bold; font-size: 18px;'>Agent:</span> 
                    <span style='color: #ffffff; font-size: 18px;'>{message}</span>
                </div>
            """,
            "user": """
                <div style='background-color: #444444; padding: 15px; border-radius: 10px; margin-bottom: 15px; text-align: right;'>
                    <span style='color: #99ff99; font-weight: bold; font-size: 18px;'>You:</span> 
                    <span style='color: #ffffff; font-size: 18px;'>{message}</span>
                </div>
            """
        }
