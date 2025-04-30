"""
Chat area component for the Functional Requirements Agent.
"""
from PySide6.QtWidgets import QTextEdit, QVBoxLayout, QPushButton, QHBoxLayout, QLabel
from PySide6.QtCore import Qt, QTimer
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
        
        # Chat message history
        self.message_history = []
        
        # For streaming effect
        self.streaming_timer = QTimer()
        self.streaming_timer.timeout.connect(self._update_streaming_text)
        self.streaming_text = ""
        self.full_text = ""
        self.current_position = 0
        self.streaming_speed = 40  # characters per second
        self.is_streaming = False
        
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
    
    def clear_chat_history(self):
        """
        Clear the entire chat history
        """
        # Clear the UI
        self.chat_history.clear()
        
        # Clear the message history
        self.message_history = []
        
        # Stop any ongoing streaming
        if self.streaming_timer.isActive():
            self.streaming_timer.stop()
            self.is_streaming = False
    
    def add_message(self, message, is_user=False, streaming=False):
        """
        Add a message to the chat history
        
        Args:
            message: The message text to add
            is_user: Whether this is a user message (True) or agent message (False)
            streaming: Whether to stream the text (only for agent messages)
        """
        # Stop any ongoing streaming
        if self.streaming_timer.isActive():
            self.streaming_timer.stop()
            self.is_streaming = False
        
        # Check for duplicate message
        is_duplicate = False
        if not is_user and self.message_history:
            # Check the last few messages for duplicates
            for i in range(min(3, len(self.message_history))):
                if i >= len(self.message_history):
                    break
                idx = len(self.message_history) - 1 - i
                if idx < 0:
                    break
                msg = self.message_history[idx]
                if not msg.get("is_user", True) and msg.get("message") == message:
                    is_duplicate = True
                    break
        
        # Don't add duplicate messages
        if is_duplicate:
            return
        
        # Get the appropriate style
        style = AppStyles.get_message_styles()["user" if is_user else "agent"]
        
        if is_user or not streaming:
            # Regular non-streaming message
            formatted_message = style.format(message=message)
            self.chat_history.append(formatted_message)
            
            # Store in message history
            self.message_history.append({
                "is_user": is_user,
                "message": message
            })
            
            # Move scroll to bottom
            self.chat_history.moveCursor(QTextCursor.End)
        else:
            # For streaming, start with empty content
            self.full_text = message
            self.streaming_text = ""
            self.current_position = 0
            self.is_streaming = True
            
            # Add a placeholder to message history (will be updated when streaming completes)
            self.message_history.append({
                "is_user": is_user,
                "message": "",  # Will be updated when streaming completes
                "streaming": True
            })
            
            # Start the streaming timer
            interval = int(1000 / self.streaming_speed)  # ms between updates
            self.streaming_timer.start(interval)
    
    def _update_streaming_text(self):
        """
        Update the streaming text by adding characters
        """
        if self.current_position < len(self.full_text):
            # Add a few characters at a time for smoother appearance
            chars_to_add = min(3, len(self.full_text) - self.current_position)
            self.current_position += chars_to_add
            self.streaming_text = self.full_text[:self.current_position]
            
            # Redraw the entire chat history with updated streaming text
            self._redraw_chat_history()
        else:
            # Done streaming
            self.streaming_timer.stop()
            self.is_streaming = False
            
            # Update the message in history
            for msg in self.message_history:
                if msg.get("streaming", False):
                    msg["message"] = self.full_text
                    msg["streaming"] = False
                    break
    
    def _redraw_chat_history(self):
        """
        Redraw the entire chat history with current messages
        """
        # Store scroll position
        scroll_bar = self.chat_history.verticalScrollBar()
        scroll_position = scroll_bar.value()
        
        # Clear the text edit
        self.chat_history.clear()
        
        # Redraw all messages
        for msg in self.message_history:
            is_user = msg.get("is_user", False)
            message = msg.get("message", "")
            
            # If this is the streaming message, use the current streaming text
            if msg.get("streaming", False):
                message = self.streaming_text
            
            # Get the style and format the message
            style = AppStyles.get_message_styles()["user" if is_user else "agent"]
            formatted_message = style.format(message=message)
            
            # Add to chat history
            self.chat_history.append(formatted_message)
        
        # Restore scroll position if needed
        if self.is_streaming:
            self.chat_history.moveCursor(QTextCursor.End)
        else:
            scroll_bar.setValue(scroll_position)
