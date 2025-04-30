"""
Export UI handler for the Functional Requirements Agent.
"""
import config

class ExportUIHandler:
    """Handler for export UI-related functionality"""
    
    def __init__(self, requirements_handler, export_handler, ui_components):
        """
        Initialize the export UI handler
        
        Args:
            requirements_handler: Instance of RequirementsHandler
            export_handler: Instance of ExportHandler
            ui_components: Dictionary containing UI components
        """
        self.requirements_handler = requirements_handler
        self.export_handler = export_handler
        self.ui_components = ui_components
    
    def export_requirements(self):
        """Export requirements to a file"""
        if not self.requirements_handler.get_project_id():
            self._add_agent_message("Please select a project first.")
            return
            
        # Export requirements using the export handler
        result = self.export_handler.export_requirements(
            self.requirements_handler.get_project_id()
        )
        
        if result["success"]:
            self._add_agent_message(
                f"Requirements exported successfully to the '{config.EXPORTS_DIR}' directory:"
            )
            self._add_agent_message(f"- JSON: {result['json_filename']}")
            self._add_agent_message(f"- Text: {result['text_filename']}")
        else:
            self._add_agent_message(f"Error exporting requirements: {result['error']}")
    
    def _add_agent_message(self, message):
        """Add an agent message to the chat history"""
        self.ui_components["chat_area"].add_message(message, is_user=False)
