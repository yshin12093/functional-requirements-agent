"""
Message handler for the Functional Requirements Agent.
"""
from PySide6.QtGui import QTextCursor
from ui.handlers.async_handler import LLMWorker

class MessageHandler:
    """Handler for message-related functionality"""
    
    def __init__(self, conversation_handler, requirements_handler, ui_components):
        """
        Initialize the message handler
        
        Args:
            conversation_handler: Instance of ConversationHandler
            requirements_handler: Instance of RequirementsHandler
            ui_components: Dictionary containing UI components
        """
        self.conversation_handler = conversation_handler
        self.requirements_handler = requirements_handler
        self.ui_components = ui_components
    
    def initialize_agent(self):
        """Initialize the agent with welcome messages"""
        self.add_agent_message("Welcome to the Functional Requirements Agent!", streaming=True)
        self.add_agent_message("I'm here to help you define clear, complete, and validated functional requirements.", streaming=True)
        self.add_agent_message("Let's start by discussing who the system is for and what it's intended to accomplish.", streaming=True)
    
    def add_agent_message(self, message, streaming=True):
        """Add an agent message to the chat history"""
        self.ui_components["chat_area"].add_message(message, is_user=False, streaming=streaming)
    
    def add_user_message(self, message):
        """Add a user message to the chat history"""
        self.ui_components["chat_area"].add_message(message, is_user=True)
        
    def _remove_last_message(self):
        """Remove the last message from the chat area"""
        # Get the chat area
        chat_area = self.ui_components["chat_area"]
        
        # Remove the last message from history if it exists
        if chat_area.message_history and len(chat_area.message_history) > 0:
            chat_area.message_history.pop()
            
            # Redraw the chat history
            chat_area._redraw_chat_history()
    
    def send_message(self):
        """Process the user's message and generate a response asynchronously"""
        user_message = self.ui_components["chat_area"].get_user_input()
        if not user_message:
            return
        
        # Add user message to chat history
        self.add_user_message(user_message)
        
        # Clear input field
        self.ui_components["chat_area"].clear_input()
        
        # Add a temporary message to indicate the agent is working
        working_message = "Working on it..."
        self.add_agent_message(working_message, streaming=False)
        
        # Disable the send button while processing
        send_button = self.ui_components["chat_area"].send_button
        send_button.setEnabled(False)
        send_button.setText("Processing...")
        
        # Create and start the worker thread
        self.worker = LLMWorker(self.conversation_handler, user_message)
        self.worker.signals.finished.connect(self._handle_response)
        self.worker.signals.error.connect(self._handle_error)
        self.worker.start()
    
    def _handle_response(self, result):
        """Handle the response from the worker thread"""
        # Remove the "working" message
        self._remove_last_message()
        
        # Re-enable the send button
        send_button = self.ui_components["chat_area"].send_button
        send_button.setEnabled(True)
        send_button.setText("Send")
        
        # Process the result
        self._process_result(result)
    
    def _handle_error(self, error_message):
        """Handle an error from the worker thread"""
        # Remove the "working" message
        self._remove_last_message()
        
        # Re-enable the send button
        send_button = self.ui_components["chat_area"].send_button
        send_button.setEnabled(True)
        send_button.setText("Send")
        
        # Add error message
        self.add_agent_message(f"An error occurred: {error_message}", streaming=False)
        self.add_agent_message("Please try again or check your settings.", streaming=False)
    
    def _process_result(self, result):
        
        # Handle the response
        if result["success"]:
            # For streaming responses, we want to combine all paragraphs into one message
            # to avoid multiple streaming messages interfering with each other
            full_response = result["message"].strip()
            
            # Check if this would be a duplicate of the last message
            is_duplicate = False
            chat_area = self.ui_components["chat_area"]
            if chat_area.message_history and len(chat_area.message_history) > 0:
                last_msg = chat_area.message_history[-1]
                if not last_msg.get("is_user", True) and last_msg.get("message") == full_response:
                    is_duplicate = True
            
            if full_response and not is_duplicate:
                self.add_agent_message(full_response, streaming=True)
            elif not full_response:
                # Fallback response if the LLM didn't return anything
                fallback_response = f"I understand you're interested in a glucose management system for type 1 diabetes patients. This is an important healthcare application. Could you tell me more about the specific requirements you're looking for? For example:\n\n1. Do you need real-time glucose monitoring?\n2. Should it integrate with insulin pumps?\n3. What kind of alerts or notifications are needed?\n4. Are there any specific reporting or data visualization needs?"
                self.add_agent_message(fallback_response, streaming=True)
                    
            # If there's a follow-up message, add it
            if "follow_up" in result:
                self.add_agent_message(result["follow_up"], streaming=True)
                
            # Enable complete button if we have a good number of requirements
            if len(self.requirements_handler.get_requirements()) >= 3:
                self.ui_components["action_buttons"].get_button("complete").setEnabled(True)
        else:
            # Handle error
            self.add_agent_message(result["message"], streaming=True)
            if "follow_up" in result:
                self.add_agent_message(result["follow_up"], streaming=True)
