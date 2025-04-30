"""
Header component for the Functional Requirements Agent.
"""
from PySide6.QtWidgets import QLabel, QVBoxLayout
from PySide6.QtCore import Qt

from app_styles import AppStyles

def setup_header(layout):
    """
    Set up the header with title and description.
    
    Args:
        layout: The layout to add the header components to
    """
    # Title
    title_label = QLabel("Functional Requirements Agent")
    title_label.setFont(AppStyles.get_fonts()["title"])
    title_label.setAlignment(Qt.AlignCenter)
    layout.addWidget(title_label)
    
    # Description
    description = QLabel("This agent helps define clear, complete, and validated functional requirements through structured dialogue.")
    description.setFont(AppStyles.get_fonts()["description"])
    description.setWordWrap(True)
    description.setAlignment(Qt.AlignCenter)
    layout.addWidget(description)
