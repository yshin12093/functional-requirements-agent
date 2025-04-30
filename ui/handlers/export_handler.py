"""
Export handler for the Functional Requirements Agent.
"""
import os
import datetime
import config

class ExportHandler:
    """Handler for exporting requirements"""
    
    def __init__(self, req_manager):
        """
        Initialize the export handler
        
        Args:
            req_manager: Instance of RequirementsManager
        """
        self.req_manager = req_manager
    
    def export_requirements(self, project_id):
        """
        Export requirements to files
        
        Args:
            project_id: ID of the project to export
            
        Returns:
            Dictionary with export paths and status
        """
        if not project_id:
            return {"success": False, "error": "No project selected"}
            
        try:
            # Get project data
            project_data = self.req_manager.load_project(project_id)
            project_name = project_data['name']
            
            # Create export directory if it doesn't exist
            if not os.path.exists(config.EXPORTS_DIR):
                os.makedirs(config.EXPORTS_DIR)
            
            # Export in different formats
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # JSON export
            json_path = os.path.join(config.EXPORTS_DIR, f"{project_name.replace(' ', '_')}_{timestamp}.json")
            with open(json_path, 'w') as f:
                f.write(self.req_manager.export_requirements("json"))
            
            # Text export
            text_path = os.path.join(config.EXPORTS_DIR, f"{project_name.replace(' ', '_')}_{timestamp}.txt")
            with open(text_path, 'w') as f:
                f.write(self.req_manager.export_requirements("text"))
            
            return {
                "success": True,
                "json_path": json_path,
                "text_path": text_path,
                "json_filename": os.path.basename(json_path),
                "text_filename": os.path.basename(text_path)
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
