"""
Action buttons component for the Functional Requirements Agent.
"""
from PySide6.QtWidgets import QPushButton, QHBoxLayout
from PySide6.QtCore import Qt

from app_styles import AppStyles

class ActionButtons:
    """Action buttons for requirements management"""
    
    def __init__(self, parent=None):
        """Initialize the action buttons"""
        self.parent = parent
        self.buttons = {}
        self.layout = QHBoxLayout()
        
        self._create_buttons()
        self._setup_layout()
    
    def _create_buttons(self):
        """Create all action buttons"""
        button_styles = AppStyles.get_button_styles()
        button_font = AppStyles.get_fonts()["button"]
        
        # Project button
        self.buttons["project"] = QPushButton("Select Project")
        self.buttons["project"].setFont(button_font)
        self.buttons["project"].setMinimumHeight(40)
        self.buttons["project"].setStyleSheet(button_styles["project"])
        
        # LLM Settings button
        self.buttons["llm_settings"] = QPushButton("LLM Settings")
        self.buttons["llm_settings"].setFont(button_font)
        self.buttons["llm_settings"].setMinimumHeight(40)
        self.buttons["llm_settings"].setStyleSheet(button_styles["project"])
        
        # Review button
        self.buttons["review"] = QPushButton("Review Requirements")
        self.buttons["review"].setFont(button_font)
        self.buttons["review"].setMinimumHeight(40)
        self.buttons["review"].setStyleSheet(button_styles["review"])
        self.buttons["review"].setEnabled(False)
        
        # Complete button
        self.buttons["complete"] = QPushButton("Complete Requirements")
        self.buttons["complete"].setFont(button_font)
        self.buttons["complete"].setMinimumHeight(40)
        self.buttons["complete"].setStyleSheet(button_styles["complete"])
        self.buttons["complete"].setEnabled(False)
        
        # Export button
        self.buttons["export"] = QPushButton("Export Requirements")
        self.buttons["export"].setFont(button_font)
        self.buttons["export"].setMinimumHeight(40)
        self.buttons["export"].setStyleSheet(button_styles["export"])
        self.buttons["export"].setEnabled(False)
    
    def _setup_layout(self):
        """Add buttons to the layout"""
        self.layout.addWidget(self.buttons["project"])
        self.layout.addWidget(self.buttons["llm_settings"])
        self.layout.addWidget(self.buttons["review"])
        self.layout.addWidget(self.buttons["complete"])
        self.layout.addWidget(self.buttons["export"])
    
    def get_layout(self):
        """Get the buttons layout"""
        return self.layout
    
    def get_button(self, button_name):
        """Get a specific button by name"""
        return self.buttons.get(button_name)
