"""Configuration and utilities for the Azure DevOps MCP Agent."""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()


class Config:
    """Configuration settings for the Azure DevOps MCP Agent."""
    
    def __init__(self):
        self.azure_devops_organization = os.getenv("AZURE_DEVOPS_ORGANIZATION")
        self.azure_devops_pat = os.getenv("AZURE_DEVOPS_PAT")
        self.azure_devops_project = os.getenv("AZURE_DEVOPS_PROJECT")
        
        # OAuth settings (for future use)
        self.azure_devops_client_id = os.getenv("AZURE_DEVOPS_CLIENT_ID")
        self.azure_devops_client_secret = os.getenv("AZURE_DEVOPS_CLIENT_SECRET")
        self.azure_devops_tenant_id = os.getenv("AZURE_DEVOPS_TENANT_ID")
    
    def validate(self) -> Optional[str]:
        """Validate the configuration and return error message if invalid."""
        if not self.azure_devops_organization:
            return "AZURE_DEVOPS_ORGANIZATION environment variable is required"
        
        if not self.azure_devops_pat and not (self.azure_devops_client_id and self.azure_devops_client_secret):
            return "Either AZURE_DEVOPS_PAT or OAuth credentials (CLIENT_ID and CLIENT_SECRET) are required"
        
        return None


def get_config() -> Config:
    """Get validated configuration."""
    config = Config()
    error = config.validate()
    if error:
        raise ValueError(error)
    return config
