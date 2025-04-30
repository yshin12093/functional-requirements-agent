"""
Dialog components for the Functional Requirements Agent.
"""

from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                              QLineEdit, QFormLayout, QComboBox, QDialogButtonBox,
                              QGroupBox, QRadioButton)
from PySide6.QtCore import Qt

import config
from requirements_manager import RequirementsManager


class LLMSettingsDialog(QDialog):
    """Dialog for configuring LLM settings"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("LLM Settings")
        self.setMinimumWidth(500)
        
        # Set up the UI
        layout = QVBoxLayout(self)
        
        # Provider selection
        provider_group = QGroupBox("LLM Provider")
        provider_layout = QVBoxLayout()
        
        self.ollama_radio = QRadioButton("Ollama (Local)")
        self.openai_radio = QRadioButton("OpenAI (GPT-4)")
        self.anthropic_radio = QRadioButton("Anthropic (Claude)")
        self.deepseek_radio = QRadioButton("Deepseek")
        
        # Set default based on config
        if config.DEFAULT_LLM_PROVIDER == "ollama":
            self.ollama_radio.setChecked(True)
        elif config.DEFAULT_LLM_PROVIDER == "openai":
            self.openai_radio.setChecked(True)
        elif config.DEFAULT_LLM_PROVIDER == "anthropic":
            self.anthropic_radio.setChecked(True)
        elif config.DEFAULT_LLM_PROVIDER == "deepseek":
            self.deepseek_radio.setChecked(True)
        else:
            self.ollama_radio.setChecked(True)
        
        provider_layout.addWidget(self.ollama_radio)
        provider_layout.addWidget(self.openai_radio)
        provider_layout.addWidget(self.anthropic_radio)
        provider_layout.addWidget(self.deepseek_radio)
        provider_group.setLayout(provider_layout)
        layout.addWidget(provider_group)
        
        # Model selection
        model_group = QGroupBox("Model Settings")
        model_layout = QFormLayout()
        
        self.model_edit = QLineEdit()
        self.model_edit.setText(config.DEFAULT_LLM_MODEL)
        model_layout.addRow("Model Name:", self.model_edit)
        
        self.api_key_edit = QLineEdit()
        self.api_key_edit.setPlaceholderText("Optional, can use environment variable")
        model_layout.addRow("API Key:", self.api_key_edit)
        
        model_group.setLayout(model_layout)
        layout.addWidget(model_group)
        
        # Connect signals to update model name based on provider
        self.ollama_radio.toggled.connect(lambda: self.update_model("ollama"))
        self.openai_radio.toggled.connect(lambda: self.update_model("openai"))
        self.anthropic_radio.toggled.connect(lambda: self.update_model("anthropic"))
        self.deepseek_radio.toggled.connect(lambda: self.update_model("deepseek"))
        
        # Buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
    
    def update_model(self, provider):
        """Update the model name based on the selected provider"""
        self.model_edit.setText(config.PROVIDER_DEFAULT_MODELS.get(provider, ""))
        
        # Show/hide API key field based on provider
        if provider == "ollama":
            self.api_key_edit.setEnabled(False)
            self.api_key_edit.setPlaceholderText("Not needed for local models")
        else:
            self.api_key_edit.setEnabled(True)
            self.api_key_edit.setPlaceholderText("Optional, can use environment variable")
    
    def get_settings(self):
        """Get the selected LLM settings"""
        provider = "ollama"  # Default
        if self.openai_radio.isChecked():
            provider = "openai"
        elif self.anthropic_radio.isChecked():
            provider = "anthropic"
        elif self.deepseek_radio.isChecked():
            provider = "deepseek"
        
        return {
            "provider": provider,
            "model": self.model_edit.text().strip(),
            "api_key": self.api_key_edit.text().strip() or None
        }


class ProjectDialog(QDialog):
    """Dialog for creating or selecting a project"""
    def __init__(self, req_manager, parent=None):
        super().__init__(parent)
        self.req_manager = req_manager
        self.setWindowTitle("Project Selection")
        self.setMinimumWidth(500)
        
        # Set up the UI
        layout = QVBoxLayout(self)
        
        # Project selection
        self.project_combo = QComboBox()
        self.refresh_projects()
        layout.addWidget(QLabel("Select Existing Project:"))
        layout.addWidget(self.project_combo)
        
        # Or create new project
        layout.addWidget(QLabel("Or Create New Project:"))
        
        form_layout = QFormLayout()
        self.name_edit = QLineEdit()
        self.description_edit = QLineEdit()
        form_layout.addRow("Project Name:", self.name_edit)
        form_layout.addRow("Description:", self.description_edit)
        layout.addLayout(form_layout)
        
        # Buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
    
    def refresh_projects(self):
        """Refresh the list of projects"""
        self.project_combo.clear()
        projects = self.req_manager.list_projects()
        
        for project in projects:
            display_text = f"{project['name']} ({project['requirement_count']} requirements)"
            self.project_combo.addItem(display_text, project['project_id'])
        
        # Add a "Create New" option
        if not projects:
            self.project_combo.addItem("No existing projects")
            self.project_combo.setEnabled(False)
    
    def get_selected_project(self):
        """Get the selected project ID or create a new one"""
        # If a new project name is provided, create it
        if self.name_edit.text().strip():
            project_name = self.name_edit.text().strip()
            description = self.description_edit.text().strip()
            return self.req_manager.create_project(project_name, description)
        
        # Otherwise return the selected existing project
        if self.project_combo.isEnabled() and self.project_combo.currentIndex() >= 0:
            return self.project_combo.currentData()
        
        return None
