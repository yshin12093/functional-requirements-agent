"""
Requirements handler for the Functional Requirements Agent.
"""
import config
from requirements_manager import RequirementsManager

class RequirementsHandler:
    """Handler for requirements-related functionality"""
    
    def __init__(self):
        """Initialize the requirements handler"""
        self.req_manager = RequirementsManager(storage_dir=config.REQUIREMENTS_DATA_DIR)
        self.current_project_id = None
        self.requirements_complete = False
    
    def set_project(self, project_id):
        """
        Set the current project
        
        Args:
            project_id: The ID of the project to set as current
        """
        self.current_project_id = project_id
        self.requirements_complete = False
    
    def get_project_id(self):
        """Get the current project ID"""
        return self.current_project_id
    
    def get_project_data(self):
        """
        Get the current project data
        
        Returns:
            Dictionary with project data or None if no project is selected
        """
        if not self.current_project_id:
            return None
        
        return self.req_manager.load_project(self.current_project_id)
    
    def get_requirements(self):
        """
        Get all requirements for the current project
        
        Returns:
            List of requirements or empty list if no project is selected
        """
        if not self.current_project_id:
            return []
        
        return self.req_manager.get_all_requirements()
    
    def extract_requirements(self, text):
        """
        Extract potential requirements from text and save to project
        
        Args:
            text: Text to extract requirements from
            
        Returns:
            List of saved requirements
        """
        if not self.current_project_id:
            return []
            
        lines = text.split('\n')
        potential_reqs = []
        
        for line in lines:
            line = line.strip()
            # Look for lines that might be requirements
            if line.lower().startswith(('the system shall', 'system must', 'system should', 'requirement:', 'fr-')):
                potential_reqs.append(line)
            elif 'shall' in line.lower() and len(line) < 200:  # Reasonable length for a requirement
                potential_reqs.append(line)
        
        # Save new requirements to the project
        saved_reqs = []
        for req_text in potential_reqs:
            # Check if this requirement text already exists
            existing_reqs = self.req_manager.get_all_requirements()
            if not any(req['text'].lower() == req_text.lower() for req in existing_reqs):
                # Add to project
                saved_req = self.req_manager.add_requirement(req_text)
                saved_reqs.append(saved_req)
                
        return saved_reqs
    
    def mark_complete(self):
        """Mark the requirements as complete"""
        if not self.current_project_id:
            return False
            
        self.requirements_complete = True
        
        # Update requirements status to 'approved'
        requirements = self.req_manager.get_all_requirements()
        for req in requirements:
            self.req_manager.update_requirement(req['id'], {"status": "approved"})
            
        return True
    
    def is_complete(self):
        """Check if requirements are marked as complete"""
        return self.requirements_complete
