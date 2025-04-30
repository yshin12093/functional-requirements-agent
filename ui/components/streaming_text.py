"""
Streaming text component for the Functional Requirements Agent.
"""
from PySide6.QtCore import QTimer, Signal, QObject

class StreamingTextEmitter(QObject):
    """Signal emitter for streaming text updates"""
    text_updated = Signal(str)

class StreamingText:
    """
    Handles streaming text animation for chat responses.
    
    This class simulates a typing effect by gradually revealing
    text over time, character by character.
    """
    
    def __init__(self, callback=None, speed=30):
        """
        Initialize the streaming text handler
        
        Args:
            callback: Function to call with updated text
            speed: Characters per second for the streaming effect
        """
        self.callback = callback
        self.speed = speed  # Characters per second
        self.full_text = ""
        self.current_position = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self._update_text)
        self.emitter = StreamingTextEmitter()
        self.is_streaming = False
        
        if callback:
            self.emitter.text_updated.connect(callback)
    
    def start_streaming(self, text):
        """
        Start streaming the provided text
        
        Args:
            text: The full text to stream
        """
        self.full_text = text
        self.current_position = 0
        self.is_streaming = True
        
        # Calculate interval based on speed (ms per character)
        interval = int(1000 / self.speed)
        self.timer.start(interval)
    
    def _update_text(self):
        """Update the displayed text by adding one character"""
        if self.current_position < len(self.full_text):
            # Increment by a small chunk for smoother appearance
            chunk_size = min(3, len(self.full_text) - self.current_position)
            self.current_position += chunk_size
            current_text = self.full_text[:self.current_position]
            
            # Emit the signal with updated text
            self.emitter.text_updated.emit(current_text)
        else:
            # Stop the timer when we've displayed all text
            self.timer.stop()
            self.is_streaming = False
    
    def stop_streaming(self):
        """Stop the streaming effect and display the full text"""
        self.timer.stop()
        self.is_streaming = False
        if self.full_text and self.current_position < len(self.full_text):
            self.current_position = len(self.full_text)
            self.emitter.text_updated.emit(self.full_text)
