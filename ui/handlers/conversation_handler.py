"""
Conversation handler for the Functional Requirements Agent.
"""
from llm_interface import get_default_system_prompt

class ConversationHandler:
    """Handler for conversation management and LLM interactions"""
    
    def __init__(self, llm_handler, requirements_handler):
        """
        Initialize the conversation handler
        
        Args:
            llm_handler: Instance of LLMHandler
            requirements_handler: Instance of RequirementsHandler
        """
        self.llm_handler = llm_handler
        self.requirements_handler = requirements_handler
        self.conversation_history = []
    
    def add_user_message(self, message):
        """
        Add a user message to the conversation history
        
        Args:
            message: The message text
        """
        self.conversation_history.append({"role": "user", "content": message})
    
    def add_assistant_message(self, message):
        """
        Add an assistant message to the conversation history
        
        Args:
            message: The message text
        """
        self.conversation_history.append({"role": "assistant", "content": message})
    
    def get_conversation_history(self):
        """Get the full conversation history"""
        return self.conversation_history
    
    def process_user_input(self, user_message):
        """
        Process user input and generate responses using the configured LLM
        
        Args:
            user_message: The user's message text
            
        Returns:
            Dictionary with response and any extracted requirements
        """
        try:
            # Store message in conversation history
            self.add_user_message(user_message)
            
            # Check if we need to select a project first
            if not self.requirements_handler.get_project_id():
                return {
                    "success": False,
                    "message": "Please select a project first by clicking the 'Select Project' button."
                }
                
            # Handle special case for restarting requirements
            if (self.requirements_handler.is_complete() and 
                "restart" in user_message.lower()):
                self.requirements_handler.requirements_complete = False
                return {
                    "success": True,
                    "message": "I've reset the requirements gathering process. Let's continue refining the requirements.",
                    "follow_up": "What aspect of the requirements would you like to focus on?"
                }
                
            # Get the system prompt
            system_prompt = get_default_system_prompt()
            
            # Prepare context from existing requirements
            requirements_context = ""
            existing_reqs = self.requirements_handler.get_requirements()
            if existing_reqs:
                requirements_context = "Current requirements:\n"
                for req in existing_reqs:
                    requirements_context += f"- {req['id']}: {req['text']}\n"
            
            # Get project data for context
            project_data = self.requirements_handler.get_project_data()
            project_context = f"Project: {project_data['name']}\nDescription: {project_data.get('description', '')}\n"
            
            # Combine all context
            full_context = f"{project_context}\n{requirements_context}\n\nUser message: {user_message}"
            
            # Prepare messages for the LLM
            messages = [
                {"role": "system", "content": system_prompt}
            ]
            
            # Add the last few conversation turns for context (limited to avoid token limits)
            max_history = 5  # Limit history to last 5 exchanges
            for msg in self.conversation_history[-max_history*2:]:
                messages.append(msg)
                
            # Add the current message with full context
            messages.append({"role": "user", "content": full_context})
            
            # Generate response using the configured LLM provider
            llm = self.llm_handler.get_llm()
            try:
                response = llm.chat(messages=messages)
            except Exception as e:
                return {
                    "success": False,
                    "message": f"Error communicating with {llm.get_name()}: {str(e)}",
                    "follow_up": "Please check your LLM settings and try again."
                }
            
            # Extract the response content
            ai_response = response['message']['content']
            
            # Check if this response is a duplicate of the last assistant message
            is_duplicate = False
            if self.conversation_history and len(self.conversation_history) >= 2:
                last_msg = self.conversation_history[-1]
                if last_msg.get('role') == 'assistant' and last_msg.get('content') == ai_response:
                    is_duplicate = True
            
            # Extract and save requirements from both user message and AI response
            saved_user_reqs = self.requirements_handler.extract_requirements(user_message)
            saved_ai_reqs = self.requirements_handler.extract_requirements(ai_response)
            
            # Only store AI response if it's not a duplicate
            if not is_duplicate:
                self.add_assistant_message(ai_response)
            
            return {
                "success": True,
                "message": ai_response,
                "saved_requirements": saved_user_reqs + saved_ai_reqs
            }
                
        except Exception as e:
            # Handle any errors that might occur
            return {
                "success": False,
                "message": f"An error occurred: {str(e)}",
                "follow_up": "Please try again or check your settings."
            }
