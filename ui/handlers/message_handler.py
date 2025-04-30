"""
Message handler for the Functional Requirements Agent.
"""

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
        self.add_agent_message("Welcome to the Functional Requirements Agent!")
        self.add_agent_message("I'm here to help you define clear, complete, and validated functional requirements.")
        self.add_agent_message("Let's start by discussing who the system is for and what it's intended to accomplish.")
    
    def add_agent_message(self, message):
        """Add an agent message to the chat history"""
        self.ui_components["chat_area"].add_message(message, is_user=False)
    
    def add_user_message(self, message):
        """Add a user message to the chat history"""
        self.ui_components["chat_area"].add_message(message, is_user=True)
    
    def send_message(self):
        """Process the user's message and generate a response"""
        user_message = self.ui_components["chat_area"].get_user_input()
        if not user_message:
            return
        
        # Add user message to chat history
        self.add_user_message(user_message)
        
        # Clear input field
        self.ui_components["chat_area"].clear_input()
        
        # Process the message using the conversation handler
        result = self.conversation_handler.process_user_input(user_message)
        
        # Handle the response
        if result["success"]:
            # Split the response into paragraphs for better readability
            paragraphs = result["message"].split('\n\n')
            for paragraph in paragraphs:
                if paragraph.strip():
                    self.add_agent_message(paragraph.strip())
                    
            # If there's a follow-up message, add it
            if "follow_up" in result:
                self.add_agent_message(result["follow_up"])
                
            # Enable complete button if we have a good number of requirements
            if len(self.requirements_handler.get_requirements()) >= 3:
                self.ui_components["action_buttons"].get_button("complete").setEnabled(True)
        else:
            # Handle error
            self.add_agent_message(result["message"])
            if "follow_up" in result:
                self.add_agent_message(result["follow_up"])
