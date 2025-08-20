"""MCP Server implementation for Azure DevOps integration."""

import os
import json
import logging
from typing import Any, Dict, List, Optional
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
    LoggingLevel
)
from .client import AzureDevOpsClient

# Configure logging to stderr to avoid interfering with MCP stdio transport
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

class AzureDevOpsMCPServer:
    """MCP Server for Azure DevOps integration."""
    
    def __init__(self):
        self.server = Server("azure-devops-mcp-agent")
        self.organization = os.getenv("AZURE_DEVOPS_ORGANIZATION")
        self.default_project = os.getenv("AZURE_DEVOPS_PROJECT")
        
        if not self.organization:
            raise ValueError("AZURE_DEVOPS_ORGANIZATION environment variable is required")
        
        # Register tools
        self._register_tools()
        
        # Register resources (optional)
        self._register_resources()
    
    def _register_tools(self):
        """Register all available tools."""
        
        @self.server.list_tools()
        async def list_tools() -> List[Tool]:
            """List all available Azure DevOps tools."""
            return [
                Tool(
                    name="list_work_items",
                    description="List work items from an Azure DevOps project with optional WIQL query",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "project": {
                                "type": "string",
                                "description": "The Azure DevOps project name"
                            },
                            "wiql": {
                                "type": "string",
                                "description": "Optional WIQL query to filter work items"
                            },
                            "top": {
                                "type": "integer",
                                "description": "Maximum number of work items to return (default: 50)",
                                "minimum": 1,
                                "maximum": 200,
                                "default": 50
                            }
                        },
                        "required": ["project"]
                    }
                ),
                Tool(
                    name="get_work_item",
                    description="Get detailed information about a specific work item",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "work_item_id": {
                                "type": "integer",
                                "description": "The work item ID"
                            },
                            "expand": {
                                "type": "string",
                                "description": "Fields to expand (All, Relations, Fields, Links, etc.)",
                                "default": "All"
                            }
                        },
                        "required": ["work_item_id"]
                    }
                ),
                Tool(
                    name="create_work_item",
                    description="Create a new work item in Azure DevOps",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "project": {
                                "type": "string",
                                "description": "The Azure DevOps project name"
                            },
                            "work_item_type": {
                                "type": "string",
                                "description": "Type of work item (Bug, User Story, Task, Feature, Epic, etc.)"
                            },
                            "title": {
                                "type": "string",
                                "description": "The work item title"
                            },
                            "description": {
                                "type": "string",
                                "description": "The work item description"
                            },
                            "assigned_to": {
                                "type": "string",
                                "description": "Email of the person to assign the work item to"
                            },
                            "priority": {
                                "type": "integer",
                                "description": "Priority level (1-4)"
                            },
                            "tags": {
                                "type": "string",
                                "description": "Semicolon-separated tags"
                            }
                        },
                        "required": ["project", "work_item_type", "title"]
                    }
                ),
                Tool(
                    name="update_work_item",
                    description="Update an existing work item",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "work_item_id": {
                                "type": "integer",
                                "description": "The work item ID to update"
                            },
                            "title": {
                                "type": "string",
                                "description": "Updated title"
                            },
                            "description": {
                                "type": "string",
                                "description": "Updated description"
                            },
                            "state": {
                                "type": "string",
                                "description": "Updated state (New, Active, Resolved, Closed, etc.)"
                            },
                            "assigned_to": {
                                "type": "string",
                                "description": "Email of the person to assign the work item to"
                            },
                            "priority": {
                                "type": "integer",
                                "description": "Priority level (1-4)"
                            },
                            "tags": {
                                "type": "string",
                                "description": "Semicolon-separated tags"
                            }
                        },
                        "required": ["work_item_id"]
                    }
                ),
                Tool(
                    name="list_repositories",
                    description="List repositories in an Azure DevOps project",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "project": {
                                "type": "string",
                                "description": "The Azure DevOps project name"
                            }
                        },
                        "required": ["project"]
                    }
                ),
                Tool(
                    name="get_repository",
                    description="Get detailed information about a repository",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "project": {
                                "type": "string",
                                "description": "The Azure DevOps project name"
                            },
                            "repository": {
                                "type": "string",
                                "description": "The repository name or ID"
                            }
                        },
                        "required": ["project", "repository"]
                    }
                ),
                Tool(
                    name="list_builds",
                    description="List builds in an Azure DevOps project",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "project": {
                                "type": "string",
                                "description": "The Azure DevOps project name"
                            },
                            "definition_id": {
                                "type": "integer",
                                "description": "Optional build definition ID to filter builds"
                            },
                            "top": {
                                "type": "integer",
                                "description": "Maximum number of builds to return (default: 50)",
                                "minimum": 1,
                                "maximum": 200,
                                "default": 50
                            }
                        },
                        "required": ["project"]
                    }
                ),
                Tool(
                    name="get_build",
                    description="Get detailed information about a build",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "project": {
                                "type": "string",
                                "description": "The Azure DevOps project name"
                            },
                            "build_id": {
                                "type": "integer",
                                "description": "The build ID"
                            }
                        },
                        "required": ["project", "build_id"]
                    }
                ),
                Tool(
                    name="list_teams",
                    description="List teams in an Azure DevOps project",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "project": {
                                "type": "string",
                                "description": "The Azure DevOps project name"
                            }
                        },
                        "required": ["project"]
                    }
                ),
                Tool(
                    name="get_team",
                    description="Get detailed information about a team",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "project": {
                                "type": "string",
                                "description": "The Azure DevOps project name"
                            },
                            "team": {
                                "type": "string",
                                "description": "The team name or ID"
                            }
                        },
                        "required": ["project", "team"]
                    }
                ),
                Tool(
                    name="list_projects",
                    description="List all projects in the Azure DevOps organization",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    }
                ),
                Tool(
                    name="get_project",
                    description="Get detailed information about a project",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "project": {
                                "type": "string",
                                "description": "The Azure DevOps project name"
                            }
                        },
                        "required": ["project"]
                    }
                )
            ]
        
        @self.server.call_tool()
        async def call_tool(name: str, arguments: dict) -> List[TextContent | ImageContent | EmbeddedResource]:
            """Handle tool calls."""
            try:
                async with AzureDevOpsClient(self.organization) as client:
                    if name == "list_work_items":
                        project = arguments["project"]
                        wiql = arguments.get("wiql")
                        top = arguments.get("top", 50)
                        
                        result = await client.list_work_items(project, wiql, top)
                        work_items = result.get("workItems", [])
                        
                        if not work_items:
                            return [TextContent(type="text", text="No work items found.")]
                        
                        # Format work items for display
                        formatted_items = []
                        for item in work_items:
                            fields = item.get("fields", {})
                            formatted_items.append({
                                "id": item.get("id"),
                                "title": fields.get("System.Title", "No title"),
                                "type": fields.get("System.WorkItemType", "Unknown"),
                                "state": fields.get("System.State", "Unknown"),
                                "assignedTo": fields.get("System.AssignedTo", {}).get("displayName", "Unassigned"),
                                "createdDate": fields.get("System.CreatedDate"),
                                "changedDate": fields.get("System.ChangedDate")
                            })
                        
                        return [TextContent(
                            type="text",
                            text=f"Found {len(formatted_items)} work items:\n\n" + 
                                 json.dumps(formatted_items, indent=2, default=str)
                        )]
                    
                    elif name == "get_work_item":
                        work_item_id = arguments["work_item_id"]
                        expand = arguments.get("expand", "All")
                        
                        result = await client.get_work_item(work_item_id, expand)
                        
                        return [TextContent(
                            type="text",
                            text=f"Work Item Details:\n\n{json.dumps(result, indent=2, default=str)}"
                        )]
                    
                    elif name == "create_work_item":
                        project = arguments["project"]
                        work_item_type = arguments["work_item_type"]
                        
                        # Build fields dictionary
                        fields = {
                            "System.Title": arguments["title"]
                        }
                        
                        if "description" in arguments:
                            fields["System.Description"] = arguments["description"]
                        if "assigned_to" in arguments:
                            fields["System.AssignedTo"] = arguments["assigned_to"]
                        if "priority" in arguments:
                            fields["Microsoft.VSTS.Common.Priority"] = arguments["priority"]
                        if "tags" in arguments:
                            fields["System.Tags"] = arguments["tags"]
                        
                        result = await client.create_work_item(project, work_item_type, fields)
                        
                        return [TextContent(
                            type="text",
                            text=f"Work item created successfully:\n\n{json.dumps(result, indent=2, default=str)}"
                        )]
                    
                    elif name == "update_work_item":
                        work_item_id = arguments["work_item_id"]
                        
                        # Build fields dictionary for update
                        fields = {}
                        if "title" in arguments:
                            fields["System.Title"] = arguments["title"]
                        if "description" in arguments:
                            fields["System.Description"] = arguments["description"]
                        if "state" in arguments:
                            fields["System.State"] = arguments["state"]
                        if "assigned_to" in arguments:
                            fields["System.AssignedTo"] = arguments["assigned_to"]
                        if "priority" in arguments:
                            fields["Microsoft.VSTS.Common.Priority"] = arguments["priority"]
                        if "tags" in arguments:
                            fields["System.Tags"] = arguments["tags"]
                        
                        if not fields:
                            return [TextContent(type="text", text="No fields provided to update.")]
                        
                        result = await client.update_work_item(work_item_id, fields)
                        
                        return [TextContent(
                            type="text",
                            text=f"Work item updated successfully:\n\n{json.dumps(result, indent=2, default=str)}"
                        )]
                    
                    elif name == "list_repositories":
                        project = arguments["project"]
                        result = await client.list_repositories(project)
                        
                        return [TextContent(
                            type="text",
                            text=f"Repositories:\n\n{json.dumps(result, indent=2, default=str)}"
                        )]
                    
                    elif name == "get_repository":
                        project = arguments["project"]
                        repository = arguments["repository"]
                        result = await client.get_repository(project, repository)
                        
                        return [TextContent(
                            type="text",
                            text=f"Repository Details:\n\n{json.dumps(result, indent=2, default=str)}"
                        )]
                    
                    elif name == "list_builds":
                        project = arguments["project"]
                        definition_id = arguments.get("definition_id")
                        top = arguments.get("top", 50)
                        result = await client.list_builds(project, definition_id, top)
                        
                        return [TextContent(
                            type="text",
                            text=f"Builds:\n\n{json.dumps(result, indent=2, default=str)}"
                        )]
                    
                    elif name == "get_build":
                        project = arguments["project"]
                        build_id = arguments["build_id"]
                        result = await client.get_build(project, build_id)
                        
                        return [TextContent(
                            type="text",
                            text=f"Build Details:\n\n{json.dumps(result, indent=2, default=str)}"
                        )]
                    
                    elif name == "list_teams":
                        project = arguments["project"]
                        result = await client.list_teams(project)
                        
                        return [TextContent(
                            type="text",
                            text=f"Teams:\n\n{json.dumps(result, indent=2, default=str)}"
                        )]
                    
                    elif name == "get_team":
                        project = arguments["project"]
                        team = arguments["team"]
                        result = await client.get_team(project, team)
                        
                        return [TextContent(
                            type="text",
                            text=f"Team Details:\n\n{json.dumps(result, indent=2, default=str)}"
                        )]
                    
                    elif name == "list_projects":
                        result = await client.list_projects()
                        
                        return [TextContent(
                            type="text",
                            text=f"Projects:\n\n{json.dumps(result, indent=2, default=str)}"
                        )]
                    
                    elif name == "get_project":
                        project = arguments["project"]
                        result = await client.get_project(project)
                        
                        return [TextContent(
                            type="text",
                            text=f"Project Details:\n\n{json.dumps(result, indent=2, default=str)}"
                        )]
                    
                    else:
                        return [TextContent(type="text", text=f"Unknown tool: {name}")]
                        
            except Exception as e:
                logger.error(f"Error in tool call {name}: {str(e)}")
                return [TextContent(
                    type="text",
                    text=f"Error executing {name}: {str(e)}"
                )]
    
    def _register_resources(self):
        """Register available resources."""
        
        @self.server.list_resources()
        async def list_resources() -> List[Resource]:
            """List available Azure DevOps resources."""
            resources = []
            
            if self.default_project:
                resources.extend([
                    Resource(
                        uri=f"azure-devops://{self.organization}/{self.default_project}/work-items",
                        name=f"Work Items - {self.default_project}",
                        description=f"Work items from the {self.default_project} project",
                        mimeType="application/json"
                    ),
                    Resource(
                        uri=f"azure-devops://{self.organization}/{self.default_project}/repositories",
                        name=f"Repositories - {self.default_project}",
                        description=f"Repositories in the {self.default_project} project",
                        mimeType="application/json"
                    ),
                    Resource(
                        uri=f"azure-devops://{self.organization}/{self.default_project}/builds",
                        name=f"Builds - {self.default_project}",
                        description=f"Builds from the {self.default_project} project",
                        mimeType="application/json"
                    )
                ])
            
            resources.append(
                Resource(
                    uri=f"azure-devops://{self.organization}/projects",
                    name="Organization Projects",
                    description=f"All projects in the {self.organization} organization",
                    mimeType="application/json"
                )
            )
            
            return resources
        
        @self.server.read_resource()
        async def read_resource(uri: str) -> str:
            """Read content from an Azure DevOps resource."""
            try:
                parts = uri.replace("azure-devops://", "").split("/")
                
                if len(parts) < 2:
                    raise ValueError("Invalid resource URI")
                
                org = parts[0]
                if org != self.organization:
                    raise ValueError(f"Organization mismatch: expected {self.organization}, got {org}")
                
                async with AzureDevOpsClient(self.organization) as client:
                    if parts[-1] == "projects":
                        # List all projects
                        result = await client.list_projects()
                        return json.dumps(result, indent=2, default=str)
                    
                    elif len(parts) >= 3:
                        project = parts[1]
                        resource_type = parts[2]
                        
                        if resource_type == "work-items":
                            result = await client.list_work_items(project, top=100)
                            return json.dumps(result, indent=2, default=str)
                        
                        elif resource_type == "repositories":
                            result = await client.list_repositories(project)
                            return json.dumps(result, indent=2, default=str)
                        
                        elif resource_type == "builds":
                            result = await client.list_builds(project, top=50)
                            return json.dumps(result, indent=2, default=str)
                    
                    raise ValueError(f"Unknown resource type in URI: {uri}")
                    
            except Exception as e:
                logger.error(f"Error reading resource {uri}: {str(e)}")
                return json.dumps({"error": str(e)})
    
    async def run(self):
        """Run the MCP server."""
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                self.server.create_initialization_options()
            )


async def main():
    """Main entry point for the Azure DevOps MCP server."""
    try:
        server = AzureDevOpsMCPServer()
        await server.run()
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        raise


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
