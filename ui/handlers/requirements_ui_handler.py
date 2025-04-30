"""
Requirements UI handler for the Functional Requirements Agent.
"""

class RequirementsUIHandler:
    """Handler for requirements UI-related functionality"""
    
    def __init__(self, requirements_handler, ui_components):
        """
        Initialize the requirements UI handler
        
        Args:
            requirements_handler: Instance of RequirementsHandler
            ui_components: Dictionary containing UI components
        """
        self.requirements_handler = requirements_handler
        self.ui_components = ui_components
    
    def review_requirements(self):
        """Review the collected requirements"""
        if not self.requirements_handler.get_project_id():
            self._add_agent_message("Please select a project first.")
            return
            
        requirements = self.requirements_handler.get_requirements()
        if not requirements:
            self._add_agent_message("No requirements have been collected yet. "
                                   "Let's continue our discussion to identify some requirements.")
            return
            
        self._add_agent_message("Here are the functional requirements we've collected so far:")
        for i, req in enumerate(requirements, 1):
            self._add_agent_message(f"{i}. {req['id']}: {req['text']}")
            
        self._add_agent_message("Are these requirements complete and accurate? "
                               "Would you like to add, modify, or remove any requirements?")
    
    def complete_requirements(self):
        """Mark the requirements gathering process as complete"""
        if not self.requirements_handler.get_project_id():
            self._add_agent_message("Please select a project first.")
            return
            
        # Mark requirements as complete
        self.requirements_handler.mark_complete()
        
        # Update status panel
        project_data = self.requirements_handler.get_project_data()
        self.ui_components["status_panel"].update_status(
            f"Project: {project_data['name']} (Complete)",
            "complete"
        )
        
        # Display completion message
        self._add_agent_message("Great! We have completed the requirements gathering process. "
                               "Here is the final list of functional requirements:")
        for i, req in enumerate(self.requirements_handler.get_requirements(), 1):
            self._add_agent_message(f"{i}. {req['id']}: {req['text']}")
            
        self._add_agent_message("These requirements should provide a solid foundation for your system development. "
                               "If you need to revisit or refine these requirements in the future, "
                               "you can always return to this conversation.")
    
    def _add_agent_message(self, message):
        """Add an agent message to the chat history"""
        self.ui_components["chat_area"].add_message(message, is_user=False)
