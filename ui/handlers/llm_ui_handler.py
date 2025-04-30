"""
LLM UI handler for the Functional Requirements Agent.
"""
from ui.dialogs import LLMSettingsDialog

class LLMUIHandler:
    """Handler for LLM UI-related functionality"""
    
    def __init__(self, parent, llm_handler):
        """
        Initialize the LLM UI handler
        
        Args:
            parent: Parent window
            llm_handler: Instance of LLMHandler
        """
        self.parent = parent
        self.llm_handler = llm_handler
    
    def configure_llm(self):
        """Open dialog to configure LLM settings"""
        dialog = LLMSettingsDialog(self.parent)
        if dialog.exec():
            # Update LLM settings
            settings = dialog.get_settings()
            self.llm_handler.update_settings(settings)
            
            # Update status bar
            self.parent.statusBar().showMessage(self.llm_handler.get_status_text())
            
            return True
        return False
