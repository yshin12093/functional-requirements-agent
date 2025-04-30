"""
Chat area component for the Functional Requirements Agent.
"""
from PySide6.QtWidgets import QTextEdit, QVBoxLayout, QPushButton, QHBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QTextCursor

from app_styles import AppStyles

class ChatArea:
    """Chat area with history display and user input"""
    
    def __init__(self, send_callback=None, parent=None):
        """
        Initialize the chat area
        
        Args:
            send_callback: Callback function for when send button is clicked
            parent: Parent widget
        """
        self.parent = parent
        self.send_callback = send_callback
        
        # Create layout
        self.layout = QHBoxLayout()
        self.layout.setSpacing(20)  # Add more spacing between chat components
        
        self._setup_chat_history()
        self._setup_input_area()
    
    def _setup_chat_history(self):
        """Set up the chat history display"""
        self.chat_history = QTextEdit()
        self.chat_history.setReadOnly(True)
        self.chat_history.setMinimumWidth(450)
        self.chat_history.setFont(AppStyles.get_fonts()["chat"])
        
        # Set line spacing for better readability
        chat_document = self.chat_history.document()
        chat_document.setDocumentMargin(10)
        
        self.layout.addWidget(self.chat_history)
    
    def _setup_input_area(self):
        """Set up the user input area"""
        input_layout = QVBoxLayout()
        input_layout.setSpacing(15)  # Increase spacing
        
        # Text input
        self.user_input = QTextEdit()
        self.user_input.setPlaceholderText("Type your message here...")
        self.user_input.setMinimumHeight(120)  # Taller input area
        self.user_input.setFont(AppStyles.get_fonts()["chat"])
        
        # Send button
        self.send_button = QPushButton("Send")
        self.send_button.setMinimumHeight(50)  # Taller button
        self.send_button.setFont(AppStyles.get_fonts()["button"])
        self.send_button.setStyleSheet(AppStyles.get_button_styles()["send"])
        self.send_button.setCursor(Qt.PointingHandCursor)
        
        if self.send_callback:
            self.send_button.clicked.connect(self.send_callback)
        
        input_layout.addWidget(self.user_input)
        input_layout.addWidget(self.send_button)
        
        self.layout.addLayout(input_layout)
    
    def get_layout(self):
        """Get the chat area layout"""
        return self.layout
    
    def get_user_input(self):
        """Get the user input text"""
        return self.user_input.toPlainText().strip()
    
    def clear_input(self):
        """Clear the user input field"""
        self.user_input.clear()
    
    def add_message(self, message, is_user=False):
        """
        Add a message to the chat history
        
        Args:
            message: The message text to add
            is_user: Whether this is a user message (True) or agent message (False)
        """
        style = AppStyles.get_message_styles()["user" if is_user else "agent"]
        self.chat_history.append(style.format(message=message))
        # Move scroll to bottom
        self.chat_history.moveCursor(QTextCursor.End)
