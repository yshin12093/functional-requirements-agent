"""
Main application window for the Functional Requirements Agent.

This module integrates all the UI components and handlers to create the main application window.
"""

from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget
from PySide6.QtCore import Qt

import config
from app_styles import AppStyles

# Import handlers
from ui.handlers.llm_handler import LLMHandler
from ui.handlers.requirements_handler import RequirementsHandler
from ui.handlers.export_handler import ExportHandler
from ui.handlers.conversation_handler import ConversationHandler
from ui.handlers.ui_handler import UIHandler


class FunctionalRequirementsAgent(QMainWindow):
    """
    Main application window for the Functional Requirements Agent.
    
    This class serves as the main window and coordinates between different handlers.
    All specific functionality is delegated to specialized handlers.
    """
    
    def __init__(self):
        """Initialize the application window and components"""
        super().__init__()
        
        # Configure window properties
        self.setWindowTitle(config.UI_TITLE)
        self.setMinimumSize(config.UI_WIDTH, config.UI_HEIGHT)
        
        # Initialize handlers
        self._initialize_handlers()
        
        # Apply styles
        self._apply_styles()
        
        # Set up UI
        self._setup_ui()
        
        # Initialize status bar
        self.statusBar().showMessage(self.llm_handler.get_status_text())
        
        # Show project selection dialog on startup
        self.ui_handler.project_handler.select_project()
    
    def _initialize_handlers(self):
        """Initialize all handlers"""
        # Initialize core handlers
        self.llm_handler = LLMHandler()
        self.requirements_handler = RequirementsHandler()
        self.export_handler = ExportHandler(self.requirements_handler.req_manager)
        self.conversation_handler = ConversationHandler(
            self.llm_handler,
            self.requirements_handler
        )
        
        # Initialize UI handler (coordinates all UI-related functionality)
        self.ui_handler = UIHandler(
            self,
            self.llm_handler,
            self.requirements_handler,
            self.export_handler,
            self.conversation_handler
        )
    
    def _setup_ui(self):
        """Set up the user interface"""
        # Main widget and layout
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)  # Add more padding
        main_layout.setSpacing(15)  # Increase spacing between widgets
        
        # Set up UI components using the UI handler
        self.ui_handler.setup_ui(main_layout)
        
        # Set the central widget
        self.setCentralWidget(main_widget)
    
    def _apply_styles(self):
        """Apply application styles"""
        # Set application-wide stylesheet
        self.setStyleSheet(AppStyles.get_app_stylesheet())
        
        # Apply dark theme palette
        self.setPalette(AppStyles.get_dark_theme_palette())
