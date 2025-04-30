"""
UI handler for the Functional Requirements Agent.

This module coordinates between all the specialized UI handlers.
"""

from ui.components.status_panel import StatusPanel
from ui.components.action_buttons import ActionButtons
from ui.components.chat_area import ChatArea
from ui.components.header import setup_header

from ui.handlers.message_handler import MessageHandler
from ui.handlers.project_handler import ProjectHandler
from ui.handlers.requirements_ui_handler import RequirementsUIHandler
from ui.handlers.export_ui_handler import ExportUIHandler
from ui.handlers.llm_ui_handler import LLMUIHandler

class UIHandler:
    """Coordinator for all UI-related handlers"""
    
    def __init__(self, parent, llm_handler, requirements_handler, export_handler, conversation_handler):
        """Initialize the UI handler"""
        self.parent = parent
        
        # UI components dictionary
        self.components = {}
        
        # Initialize specialized handlers
        self._initialize_handlers(
            parent, 
            llm_handler, 
            requirements_handler, 
            export_handler, 
            conversation_handler
        )
    
    def _initialize_handlers(self, parent, llm_handler, requirements_handler, export_handler, conversation_handler):
        """Initialize all specialized handlers"""
        # Create UI components first (they're needed by the handlers)
        self._setup_components()
        
        # Initialize specialized handlers
        self.llm_ui_handler = LLMUIHandler(parent, llm_handler)
        self.project_handler = ProjectHandler(parent, requirements_handler, self.components)
        self.requirements_ui_handler = RequirementsUIHandler(requirements_handler, self.components)
        self.export_ui_handler = ExportUIHandler(requirements_handler, export_handler, self.components)
        self.message_handler = MessageHandler(conversation_handler, requirements_handler, self.components)
    
    def _setup_components(self):
        """Set up UI components"""
        self.components["status_panel"] = StatusPanel()
        self.components["action_buttons"] = ActionButtons()
        self.components["chat_area"] = ChatArea(send_callback=self.send_message)
    
    def setup_ui(self, main_layout):
        """Set up the user interface"""
        # Add header
        setup_header(main_layout)
        
        # Add components to layout
        main_layout.addWidget(self.components["status_panel"].get_widget())
        main_layout.addLayout(self.components["action_buttons"].get_layout())
        main_layout.addLayout(self.components["chat_area"].get_layout())
        
        # Connect button signals
        self._connect_button_signals()
        
        # Initialize the agent
        self.message_handler.initialize_agent()
    
    def _connect_button_signals(self):
        """Connect button signals to their handlers"""
        buttons = self.components["action_buttons"]
        buttons.get_button("project").clicked.connect(self.project_handler.select_project)
        buttons.get_button("llm_settings").clicked.connect(self.llm_ui_handler.configure_llm)
        buttons.get_button("review").clicked.connect(self.requirements_ui_handler.review_requirements)
        buttons.get_button("complete").clicked.connect(self.requirements_ui_handler.complete_requirements)
        buttons.get_button("export").clicked.connect(self.export_ui_handler.export_requirements)
    
    def send_message(self):
        """Delegate message sending to the message handler"""
        self.message_handler.send_message()
