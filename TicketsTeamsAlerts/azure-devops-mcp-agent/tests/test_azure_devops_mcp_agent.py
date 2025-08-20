"""Tests for the Azure DevOps MCP Agent."""

import pytest
import asyncio
import os
from unittest.mock import Mock, AsyncMock, patch
import json

# Import the modules we want to test
try:
    from azure_devops_mcp_agent.client import AzureDevOpsClient, AzureDevOpsAuth
    from azure_devops_mcp_agent.config import Config
except ImportError:
    # Handle case where dependencies aren't installed yet
    pytest.skip("Dependencies not installed", allow_module_level=True)


class TestAzureDevOpsAuth:
    """Test Azure DevOps authentication."""
    
    def test_init_with_pat(self):
        """Test initialization with PAT."""
        auth = AzureDevOpsAuth("test-org", "test-pat")
        assert auth.organization == "test-org"
        assert auth.pat == "test-pat"
    
    def test_init_without_pat_raises_error(self):
        """Test initialization without PAT raises error."""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="Personal Access Token is required"):
                AzureDevOpsAuth("test-org")
    
    def test_get_headers(self):
        """Test getting authentication headers."""
        auth = AzureDevOpsAuth("test-org", "test-pat")
        headers = auth.get_headers()
        
        assert "Authorization" in headers
        assert headers["Authorization"].startswith("Basic ")
        assert headers["Content-Type"] == "application/json"
        assert headers["Accept"] == "application/json"


class TestConfig:
    """Test configuration management."""
    
    def test_config_with_valid_environment(self):
        """Test config with valid environment variables."""
        env_vars = {
            "AZURE_DEVOPS_ORGANIZATION": "test-org",
            "AZURE_DEVOPS_PAT": "test-pat",
            "AZURE_DEVOPS_PROJECT": "test-project"
        }
        
        with patch.dict(os.environ, env_vars):
            config = Config()
            assert config.azure_devops_organization == "test-org"
            assert config.azure_devops_pat == "test-pat"
            assert config.azure_devops_project == "test-project"
            assert config.validate() is None
    
    def test_config_missing_organization(self):
        """Test config validation with missing organization."""
        env_vars = {"AZURE_DEVOPS_PAT": "test-pat"}
        
        with patch.dict(os.environ, env_vars, clear=True):
            config = Config()
            error = config.validate()
            assert "AZURE_DEVOPS_ORGANIZATION" in error
    
    def test_config_missing_auth(self):
        """Test config validation with missing authentication."""
        env_vars = {"AZURE_DEVOPS_ORGANIZATION": "test-org"}
        
        with patch.dict(os.environ, env_vars, clear=True):
            config = Config()
            error = config.validate()
            assert "PAT or OAuth credentials" in error


@pytest.mark.asyncio
class TestAzureDevOpsClient:
    """Test Azure DevOps client functionality."""
    
    @pytest.fixture
    def mock_response(self):
        """Create a mock HTTP response."""
        response = Mock()
        response.raise_for_status = Mock()
        response.headers = {"content-type": "application/json"}
        response.json = Mock(return_value={"test": "data"})
        return response
    
    async def test_client_initialization(self):
        """Test client initialization."""
        with patch.dict(os.environ, {"AZURE_DEVOPS_PAT": "test-pat"}):
            client = AzureDevOpsClient("test-org")
            assert client.organization == "test-org"
            assert client.base_url == "https://dev.azure.com/test-org"
            await client.client.aclose()
    
    async def test_list_work_items(self):
        """Test listing work items."""
        with patch.dict(os.environ, {"AZURE_DEVOPS_PAT": "test-pat"}):
            client = AzureDevOpsClient("test-org")
            
            # Mock the WIQL query response
            wiql_response = {
                "workItems": [{"id": 1}, {"id": 2}]
            }
            
            # Mock the work items batch response
            batch_response = {
                "value": [
                    {
                        "id": 1,
                        "fields": {
                            "System.Title": "Test Item 1",
                            "System.WorkItemType": "Bug",
                            "System.State": "New"
                        }
                    },
                    {
                        "id": 2,
                        "fields": {
                            "System.Title": "Test Item 2",
                            "System.WorkItemType": "User Story",
                            "System.State": "Active"
                        }
                    }
                ]
            }
            
            with patch.object(client, '_make_request') as mock_request:
                mock_request.side_effect = [wiql_response, batch_response]
                
                result = await client.list_work_items("test-project")
                
                assert "workItems" in result
                assert len(result["workItems"]) == 2
                assert result["workItems"][0]["id"] == 1
            
            await client.client.aclose()
    
    async def test_get_work_item(self):
        """Test getting a specific work item."""
        with patch.dict(os.environ, {"AZURE_DEVOPS_PAT": "test-pat"}):
            client = AzureDevOpsClient("test-org")
            
            expected_response = {
                "id": 123,
                "fields": {
                    "System.Title": "Test Work Item",
                    "System.WorkItemType": "Bug",
                    "System.State": "New"
                }
            }
            
            with patch.object(client, '_make_request', return_value=expected_response):
                result = await client.get_work_item(123)
                
                assert result["id"] == 123
                assert result["fields"]["System.Title"] == "Test Work Item"
            
            await client.client.aclose()
    
    async def test_create_work_item(self):
        """Test creating a work item."""
        with patch.dict(os.environ, {"AZURE_DEVOPS_PAT": "test-pat"}):
            client = AzureDevOpsClient("test-org")
            
            fields = {
                "System.Title": "New Bug",
                "System.Description": "Test description"
            }
            
            expected_response = {
                "id": 456,
                "fields": fields
            }
            
            with patch.object(client, '_make_request', return_value=expected_response):
                result = await client.create_work_item("test-project", "Bug", fields)
                
                assert result["id"] == 456
                assert result["fields"]["System.Title"] == "New Bug"
            
            await client.client.aclose()


if __name__ == "__main__":
    pytest.main([__file__])
