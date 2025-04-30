import json
import os
import datetime
from typing import List, Dict, Any, Optional

class RequirementsManager:
    """
    Manages the storage, retrieval, and analysis of functional requirements.
    """
    
    def __init__(self, storage_dir: str = "requirements_data"):
        """
        Initialize the requirements manager.
        
        Args:
            storage_dir: Directory to store requirements files
        """
        self.storage_dir = storage_dir
        self.current_project = None
        self.requirements = []
        
        # Create storage directory if it doesn't exist
        if not os.path.exists(storage_dir):
            os.makedirs(storage_dir)
    
    def create_project(self, project_name: str, description: str = "") -> str:
        """
        Create a new requirements project.
        
        Args:
            project_name: Name of the project
            description: Optional project description
            
        Returns:
            project_id: Unique identifier for the project
        """
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        project_id = f"{project_name.lower().replace(' ', '_')}_{timestamp}"
        
        project_data = {
            "project_id": project_id,
            "name": project_name,
            "description": description,
            "created_at": datetime.datetime.now().isoformat(),
            "updated_at": datetime.datetime.now().isoformat(),
            "requirements": [],
            "stakeholders": [],
            "goals": [],
            "constraints": []
        }
        
        self.save_project(project_data)
        self.current_project = project_id
        self.requirements = []
        
        return project_id
    
    def load_project(self, project_id: str) -> Dict[str, Any]:
        """
        Load a project by its ID.
        
        Args:
            project_id: Project identifier
            
        Returns:
            Project data dictionary
        """
        project_path = os.path.join(self.storage_dir, f"{project_id}.json")
        
        if not os.path.exists(project_path):
            raise FileNotFoundError(f"Project {project_id} not found")
        
        with open(project_path, 'r') as f:
            project_data = json.load(f)
        
        self.current_project = project_id
        self.requirements = project_data.get("requirements", [])
        
        return project_data
    
    def save_project(self, project_data: Dict[str, Any]) -> None:
        """
        Save project data to file.
        
        Args:
            project_data: Project data dictionary
        """
        project_id = project_data["project_id"]
        project_path = os.path.join(self.storage_dir, f"{project_id}.json")
        
        with open(project_path, 'w') as f:
            json.dump(project_data, f, indent=2)
    
    def add_requirement(self, requirement_text: str, source: str = "user", metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Add a new requirement to the current project.
        
        Args:
            requirement_text: The requirement text
            source: Source of the requirement (user, system, etc.)
            metadata: Additional metadata about the requirement
            
        Returns:
            The added requirement as a dictionary
        """
        if not self.current_project:
            raise ValueError("No active project. Create or load a project first.")
        
        # Load current project data
        project_path = os.path.join(self.storage_dir, f"{self.current_project}.json")
        with open(project_path, 'r') as f:
            project_data = json.load(f)
        
        # Create requirement object
        if metadata is None:
            metadata = {}
            
        requirement_id = f"REQ-{len(project_data['requirements']) + 1:03d}"
        requirement = {
            "id": requirement_id,
            "text": requirement_text,
            "source": source,
            "created_at": datetime.datetime.now().isoformat(),
            "updated_at": datetime.datetime.now().isoformat(),
            "status": "draft",
            "metadata": metadata
        }
        
        # Add to project and save
        project_data["requirements"].append(requirement)
        project_data["updated_at"] = datetime.datetime.now().isoformat()
        
        self.save_project(project_data)
        self.requirements = project_data["requirements"]
        
        return requirement
    
    def update_requirement(self, requirement_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing requirement.
        
        Args:
            requirement_id: ID of the requirement to update
            updates: Dictionary of fields to update
            
        Returns:
            Updated requirement dictionary
        """
        if not self.current_project:
            raise ValueError("No active project. Create or load a project first.")
        
        # Load current project data
        project_path = os.path.join(self.storage_dir, f"{self.current_project}.json")
        with open(project_path, 'r') as f:
            project_data = json.load(f)
        
        # Find and update the requirement
        for i, req in enumerate(project_data["requirements"]):
            if req["id"] == requirement_id:
                for key, value in updates.items():
                    if key != "id":  # Don't allow changing the ID
                        req[key] = value
                
                req["updated_at"] = datetime.datetime.now().isoformat()
                project_data["updated_at"] = datetime.datetime.now().isoformat()
                
                self.save_project(project_data)
                self.requirements = project_data["requirements"]
                
                return req
        
        raise ValueError(f"Requirement {requirement_id} not found")
    
    def delete_requirement(self, requirement_id: str) -> None:
        """
        Delete a requirement from the current project.
        
        Args:
            requirement_id: ID of the requirement to delete
        """
        if not self.current_project:
            raise ValueError("No active project. Create or load a project first.")
        
        # Load current project data
        project_path = os.path.join(self.storage_dir, f"{self.current_project}.json")
        with open(project_path, 'r') as f:
            project_data = json.load(f)
        
        # Filter out the requirement to delete
        project_data["requirements"] = [r for r in project_data["requirements"] if r["id"] != requirement_id]
        project_data["updated_at"] = datetime.datetime.now().isoformat()
        
        self.save_project(project_data)
        self.requirements = project_data["requirements"]
    
    def get_all_requirements(self) -> List[Dict[str, Any]]:
        """
        Get all requirements for the current project.
        
        Returns:
            List of requirement dictionaries
        """
        if not self.current_project:
            return []
        
        return self.requirements
    
    def get_requirement(self, requirement_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific requirement by ID.
        
        Args:
            requirement_id: ID of the requirement
            
        Returns:
            Requirement dictionary or None if not found
        """
        for req in self.requirements:
            if req["id"] == requirement_id:
                return req
        
        return None
    
    def list_projects(self) -> List[Dict[str, Any]]:
        """
        List all available projects.
        
        Returns:
            List of project summary dictionaries
        """
        projects = []
        
        for filename in os.listdir(self.storage_dir):
            if filename.endswith(".json"):
                file_path = os.path.join(self.storage_dir, filename)
                with open(file_path, 'r') as f:
                    project_data = json.load(f)
                
                projects.append({
                    "project_id": project_data["project_id"],
                    "name": project_data["name"],
                    "description": project_data.get("description", ""),
                    "created_at": project_data["created_at"],
                    "updated_at": project_data["updated_at"],
                    "requirement_count": len(project_data.get("requirements", []))
                })
        
        return projects
    
    def add_stakeholder(self, name: str, role: str, needs: List[str] = None) -> Dict[str, Any]:
        """
        Add a stakeholder to the current project.
        
        Args:
            name: Stakeholder name
            role: Stakeholder role
            needs: List of stakeholder needs
            
        Returns:
            Added stakeholder dictionary
        """
        if not self.current_project:
            raise ValueError("No active project. Create or load a project first.")
        
        # Load current project data
        project_path = os.path.join(self.storage_dir, f"{self.current_project}.json")
        with open(project_path, 'r') as f:
            project_data = json.load(f)
        
        if needs is None:
            needs = []
            
        stakeholder = {
            "name": name,
            "role": role,
            "needs": needs,
            "added_at": datetime.datetime.now().isoformat()
        }
        
        project_data["stakeholders"].append(stakeholder)
        project_data["updated_at"] = datetime.datetime.now().isoformat()
        
        self.save_project(project_data)
        
        return stakeholder
    
    def add_goal(self, goal_text: str, priority: str = "medium") -> Dict[str, Any]:
        """
        Add a goal to the current project.
        
        Args:
            goal_text: Goal description
            priority: Goal priority (low, medium, high)
            
        Returns:
            Added goal dictionary
        """
        if not self.current_project:
            raise ValueError("No active project. Create or load a project first.")
        
        # Load current project data
        project_path = os.path.join(self.storage_dir, f"{self.current_project}.json")
        with open(project_path, 'r') as f:
            project_data = json.load(f)
        
        goal = {
            "text": goal_text,
            "priority": priority,
            "added_at": datetime.datetime.now().isoformat()
        }
        
        project_data["goals"].append(goal)
        project_data["updated_at"] = datetime.datetime.now().isoformat()
        
        self.save_project(project_data)
        
        return goal
    
    def add_constraint(self, constraint_text: str, constraint_type: str = "technical") -> Dict[str, Any]:
        """
        Add a constraint to the current project.
        
        Args:
            constraint_text: Constraint description
            constraint_type: Type of constraint (technical, regulatory, resource, etc.)
            
        Returns:
            Added constraint dictionary
        """
        if not self.current_project:
            raise ValueError("No active project. Create or load a project first.")
        
        # Load current project data
        project_path = os.path.join(self.storage_dir, f"{self.current_project}.json")
        with open(project_path, 'r') as f:
            project_data = json.load(f)
        
        constraint = {
            "text": constraint_text,
            "type": constraint_type,
            "added_at": datetime.datetime.now().isoformat()
        }
        
        project_data["constraints"].append(constraint)
        project_data["updated_at"] = datetime.datetime.now().isoformat()
        
        self.save_project(project_data)
        
        return constraint
    
    def get_project_summary(self) -> Dict[str, Any]:
        """
        Get a summary of the current project.
        
        Returns:
            Project summary dictionary
        """
        if not self.current_project:
            raise ValueError("No active project. Create or load a project first.")
        
        # Load current project data
        project_path = os.path.join(self.storage_dir, f"{self.current_project}.json")
        with open(project_path, 'r') as f:
            project_data = json.load(f)
        
        return {
            "project_id": project_data["project_id"],
            "name": project_data["name"],
            "description": project_data.get("description", ""),
            "created_at": project_data["created_at"],
            "updated_at": project_data["updated_at"],
            "requirement_count": len(project_data.get("requirements", [])),
            "stakeholder_count": len(project_data.get("stakeholders", [])),
            "goal_count": len(project_data.get("goals", [])),
            "constraint_count": len(project_data.get("constraints", []))
        }
    
    def export_requirements(self, format_type: str = "json") -> str:
        """
        Export requirements in various formats.
        
        Args:
            format_type: Export format (json, csv, text)
            
        Returns:
            Formatted string of requirements
        """
        if not self.current_project:
            raise ValueError("No active project. Create or load a project first.")
        
        if format_type == "json":
            return json.dumps(self.requirements, indent=2)
        
        elif format_type == "csv":
            if not self.requirements:
                return "id,text,status,created_at\n"
            
            csv_lines = ["id,text,status,created_at"]
            for req in self.requirements:
                # Escape commas and quotes in the text
                text = req["text"].replace('"', '""')
                csv_lines.append(f"{req['id']},\"{text}\",{req['status']},{req['created_at']}")
            
            return "\n".join(csv_lines)
        
        elif format_type == "text":
            if not self.requirements:
                return "No requirements found."
            
            text_lines = []
            for req in self.requirements:
                text_lines.append(f"{req['id']}: {req['text']}")
                text_lines.append(f"  Status: {req['status']}")
                text_lines.append(f"  Created: {req['created_at']}")
                text_lines.append("")
            
            return "\n".join(text_lines)
        
        else:
            raise ValueError(f"Unsupported export format: {format_type}")
