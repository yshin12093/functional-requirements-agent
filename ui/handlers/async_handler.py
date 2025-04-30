"""
Asynchronous handler for the Functional Requirements Agent.

This module provides threading support for non-blocking LLM operations.
"""
from PySide6.QtCore import QObject, Signal, QThread

class WorkerSignals(QObject):
    """Signals for the worker thread"""
    finished = Signal(dict)
    error = Signal(str)

class LLMWorker(QThread):
    """Worker thread for LLM operations"""
    
    def __init__(self, conversation_handler, user_message):
        """
        Initialize the worker thread
        
        Args:
            conversation_handler: Instance of ConversationHandler
            user_message: The user's message text
        """
        super().__init__()
        self.conversation_handler = conversation_handler
        self.user_message = user_message
        self.signals = WorkerSignals()
    
    def run(self):
        """Run the worker thread"""
        try:
            # Process the message using the conversation handler
            result = self.conversation_handler.process_user_input(self.user_message)
            
            # Emit the result
            self.signals.finished.emit(result)
        except Exception as e:
            # Emit the error
            self.signals.error.emit(str(e))
