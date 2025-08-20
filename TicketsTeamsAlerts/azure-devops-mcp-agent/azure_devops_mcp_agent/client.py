"""Azure DevOps API client for authentication and API calls."""

import os
import base64
from typing import Optional, Dict, Any, List
import httpx
from urllib.parse import quote


class AzureDevOpsAuth:
    """Handle Azure DevOps authentication."""
    
    def __init__(self, organization: str, pat: Optional[str] = None):
        self.organization = organization
        self.pat = pat or os.getenv("AZURE_DEVOPS_PAT")
        
        if not self.pat:
            raise ValueError("Azure DevOps Personal Access Token is required")
    
    def get_headers(self) -> Dict[str, str]:
        """Get authentication headers for API requests."""
        # Encode PAT for basic auth (username can be empty for PAT)
        auth_string = f":{self.pat}"
        encoded_auth = base64.b64encode(auth_string.encode()).decode()
        
        return {
            "Authorization": f"Basic {encoded_auth}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }


class AzureDevOpsClient:
    """Azure DevOps API client."""
    
    def __init__(self, organization: str, pat: Optional[str] = None):
        self.organization = organization
        self.auth = AzureDevOpsAuth(organization, pat)
        self.base_url = f"https://dev.azure.com/{organization}"
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()
    
    async def _make_request(self, method: str, url: str, **kwargs) -> Dict[str, Any]:
        """Make an authenticated request to Azure DevOps API."""
        headers = self.auth.get_headers()
        if "headers" in kwargs:
            headers.update(kwargs["headers"])
        kwargs["headers"] = headers
        
        response = await self.client.request(method, url, **kwargs)
        response.raise_for_status()
        
        if response.headers.get("content-type", "").startswith("application/json"):
            return response.json()
        return {"content": response.text}
    
    # Work Items API
    async def list_work_items(self, project: str, wiql: Optional[str] = None, top: int = 200) -> Dict[str, Any]:
        """List work items from a project using WIQL query."""
        if not wiql:
            # Default query to get recent work items
            wiql = f"""
            SELECT [System.Id], [System.Title], [System.State], [System.AssignedTo], 
                   [System.WorkItemType], [System.CreatedDate]
            FROM WorkItems 
            WHERE [System.TeamProject] = '{project}'
            ORDER BY [System.ChangedDate] DESC
            """
        
        url = f"{self.base_url}/{quote(project)}/_apis/wit/wiql"
        params = {"api-version": "7.1"}
        
        data = {
            "query": wiql
        }
        
        # Get work item IDs first
        wiql_result = await self._make_request("POST", url, json=data, params=params)
        
        if not wiql_result.get("workItems"):
            return {"workItems": []}
        
        # Extract IDs and get detailed work items
        work_item_ids = [item["id"] for item in wiql_result["workItems"][:top]]
        
        if work_item_ids:
            return await self.get_work_items_batch(work_item_ids)
        
        return {"workItems": []}
    
    async def get_work_item(self, work_item_id: int, expand: str = "All") -> Dict[str, Any]:
        """Get a specific work item by ID."""
        url = f"{self.base_url}/_apis/wit/workitems/{work_item_id}"
        params = {
            "api-version": "7.1",
            "$expand": expand
        }
        
        return await self._make_request("GET", url, params=params)
    
    async def get_work_items_batch(self, work_item_ids: List[int], fields: Optional[List[str]] = None) -> Dict[str, Any]:
        """Get multiple work items by IDs."""
        if not work_item_ids:
            return {"workItems": []}
        
        ids_str = ",".join(map(str, work_item_ids))
        url = f"{self.base_url}/_apis/wit/workitems"
        params = {
            "ids": ids_str,
            "api-version": "7.1",
            "$expand": "All"
        }
        
        if fields:
            params["fields"] = ",".join(fields)
        
        result = await self._make_request("GET", url, params=params)
        return {"workItems": result.get("value", [])}
    
    async def create_work_item(self, project: str, work_item_type: str, fields: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new work item."""
        url = f"{self.base_url}/{quote(project)}/_apis/wit/workitems/${work_item_type}"
        params = {"api-version": "7.1"}
        
        # Convert fields to JSON Patch format
        patch_document = []
        for field, value in fields.items():
            patch_document.append({
                "op": "add",
                "path": f"/fields/{field}",
                "value": value
            })
        
        headers = {"Content-Type": "application/json-patch+json"}
        
        return await self._make_request("POST", url, json=patch_document, params=params, headers=headers)
    
    async def update_work_item(self, work_item_id: int, fields: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing work item."""
        url = f"{self.base_url}/_apis/wit/workitems/{work_item_id}"
        params = {"api-version": "7.1"}
        
        # Convert fields to JSON Patch format
        patch_document = []
        for field, value in fields.items():
            patch_document.append({
                "op": "replace",
                "path": f"/fields/{field}",
                "value": value
            })
        
        headers = {"Content-Type": "application/json-patch+json"}
        
        return await self._make_request("PATCH", url, json=patch_document, params=params, headers=headers)
    
    # Repository API
    async def list_repositories(self, project: str) -> Dict[str, Any]:
        """List repositories in a project."""
        url = f"{self.base_url}/{quote(project)}/_apis/git/repositories"
        params = {"api-version": "7.1"}
        
        result = await self._make_request("GET", url, params=params)
        return {"repositories": result.get("value", [])}
    
    async def get_repository(self, project: str, repository: str) -> Dict[str, Any]:
        """Get detailed repository information."""
        url = f"{self.base_url}/{quote(project)}/_apis/git/repositories/{quote(repository)}"
        params = {"api-version": "7.1"}
        
        return await self._make_request("GET", url, params=params)
    
    # Build API
    async def list_builds(self, project: str, definition_id: Optional[int] = None, top: int = 50) -> Dict[str, Any]:
        """List builds in a project."""
        url = f"{self.base_url}/{quote(project)}/_apis/build/builds"
        params = {
            "api-version": "7.1",
            "$top": top
        }
        
        if definition_id:
            params["definitions"] = definition_id
        
        result = await self._make_request("GET", url, params=params)
        return {"builds": result.get("value", [])}
    
    async def get_build(self, project: str, build_id: int) -> Dict[str, Any]:
        """Get detailed build information."""
        url = f"{self.base_url}/{quote(project)}/_apis/build/builds/{build_id}"
        params = {"api-version": "7.1"}
        
        return await self._make_request("GET", url, params=params)
    
    # Team API
    async def list_teams(self, project: str) -> Dict[str, Any]:
        """List teams in a project."""
        url = f"{self.base_url}/_apis/projects/{quote(project)}/teams"
        params = {"api-version": "7.1"}
        
        result = await self._make_request("GET", url, params=params)
        return {"teams": result.get("value", [])}
    
    async def get_team(self, project: str, team: str) -> Dict[str, Any]:
        """Get detailed team information."""
        url = f"{self.base_url}/_apis/projects/{quote(project)}/teams/{quote(team)}"
        params = {"api-version": "7.1"}
        
        return await self._make_request("GET", url, params=params)
    
    # Projects API
    async def list_projects(self) -> Dict[str, Any]:
        """List all projects in the organization."""
        url = f"{self.base_url}/_apis/projects"
        params = {"api-version": "7.1"}
        
        result = await self._make_request("GET", url, params=params)
        return {"projects": result.get("value", [])}
    
    async def get_project(self, project: str) -> Dict[str, Any]:
        """Get detailed project information."""
        url = f"{self.base_url}/_apis/projects/{quote(project)}"
        params = {"api-version": "7.1"}
        
        return await self._make_request("GET", url, params=params)
