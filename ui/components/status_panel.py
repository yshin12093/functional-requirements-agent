"""
Status panel component for the Functional Requirements Agent.
"""
from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt

from app_styles import AppStyles

class StatusPanel:
    """Status panel to display the current requirements status"""
    
    def __init__(self, parent=None):
        """Initialize the status panel"""
        self.status_label = QLabel("Requirements Status: Not Started")
        self.status_label.setFont(AppStyles.get_fonts()["button"])
        self.status_label.setStyleSheet(AppStyles.get_status_styles()["in_progress"])
        self.status_label.setAlignment(Qt.AlignCenter)
    
    def get_widget(self):
        """Get the status label widget"""
        return self.status_label
    
    def update_status(self, status_text, status_type="default"):
        """
        Update the status panel text and style
        
        Args:
            status_text: The text to display in the status panel
            status_type: The type of status (default, in_progress, complete)
        """
        self.status_label.setText(status_text)
        self.status_label.setStyleSheet(AppStyles.get_status_styles()[status_type])
