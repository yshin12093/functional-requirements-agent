"""
Project handler for the Functional Requirements Agent.
"""
from PySide6.QtWidgets import QMessageBox

from ui.dialogs import ProjectDialog

class ProjectHandler:
    """Handler for project-related functionality"""
    
    def __init__(self, parent, requirements_handler, ui_components):
        """
        Initialize the project handler
        
        Args:
            parent: Parent window
            requirements_handler: Instance of RequirementsHandler
            ui_components: Dictionary containing UI components
        """
        self.parent = parent
        self.requirements_handler = requirements_handler
        self.ui_components = ui_components
    
    def select_project(self):
        """Open dialog to select or create a project"""
        dialog = ProjectDialog(self.requirements_handler.req_manager, self.parent)
        if dialog.exec():
            project_id = dialog.get_selected_project()
            if project_id:
                # Set the project in the requirements handler
                self.requirements_handler.set_project(project_id)
                
                # Load the project data
                self.load_project()
                
                # Enable buttons
                self.ui_components["action_buttons"].get_button("review").setEnabled(True)
                self.ui_components["action_buttons"].get_button("export").setEnabled(True)
                
                # Enable complete button if we have enough requirements
                if len(self.requirements_handler.get_requirements()) >= 3:
                    self.ui_components["action_buttons"].get_button("complete").setEnabled(True)
            else:
                QMessageBox.warning(self.parent, "No Project Selected", 
                                    "Please select or create a project to continue.")
    
    def load_project(self):
        """Load the current project data"""
        try:
            # Get project data
            project_data = self.requirements_handler.get_project_data()
            
            # Update status panel
            self.ui_components["status_panel"].update_status(f"Project: {project_data['name']}")
            
            # Clear chat history and add welcome message
            self.ui_components["chat_area"].chat_history.clear()
            self._add_agent_message(f"Working on project: {project_data['name']}")
            self._add_agent_message(f"Description: {project_data.get('description', 'No description provided')}")
            
            # Show existing requirements if any
            requirements = self.requirements_handler.get_requirements()
            if requirements:
                self._add_agent_message(f"Found {len(requirements)} existing requirements. "
                                       f"You can review them by clicking 'Review Requirements'.")
                self._add_agent_message("Let's continue refining these requirements. "
                                       "What would you like to discuss next?")
            else:
                self._add_agent_message("Let's start defining requirements for this project. "
                                       "Who is the system for and what is it intended to accomplish?")
                
        except Exception as e:
            QMessageBox.critical(self.parent, "Error", f"Failed to load project: {str(e)}")
    
    def _add_agent_message(self, message):
        """Add an agent message to the chat history"""
        self.ui_components["chat_area"].add_message(message, is_user=False)
