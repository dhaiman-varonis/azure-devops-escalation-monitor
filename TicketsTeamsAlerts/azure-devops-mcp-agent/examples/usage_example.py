#!/usr/bin/env python3
"""
Example script demonstrating how to use the Azure DevOps MCP Agent.
This script shows how to interact with Azure DevOps through the MCP protocol.
"""

import asyncio
import json
import os
from typing import Dict, Any

# This would normally be imported from the MCP client SDK
# For demonstration purposes, we'll show what the interaction would look like

async def example_mcp_client_interaction():
    """
    Example of how an MCP client would interact with the Azure DevOps MCP Agent.
    This demonstrates the types of requests that would be sent to the server.
    """
    
    print("=== Azure DevOps MCP Agent Example ===\n")
    
    # Example 1: List projects
    print("1. Listing all projects in the organization:")
    list_projects_request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": "list_projects",
            "arguments": {}
        }
    }
    print(f"Request: {json.dumps(list_projects_request, indent=2)}")
    print("Expected response: List of all projects in the organization\n")
    
    # Example 2: List work items
    print("2. Listing work items from a project:")
    list_work_items_request = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/call",
        "params": {
            "name": "list_work_items",
            "arguments": {
                "project": "MyProject",
                "top": 10
            }
        }
    }
    print(f"Request: {json.dumps(list_work_items_request, indent=2)}")
    print("Expected response: List of recent work items\n")
    
    # Example 3: Create a work item
    print("3. Creating a new work item:")
    create_work_item_request = {
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {
            "name": "create_work_item",
            "arguments": {
                "project": "MyProject",
                "work_item_type": "Bug",
                "title": "Fix login issue",
                "description": "Users are unable to log in with their credentials",
                "assigned_to": "developer@company.com",
                "priority": 2,
                "tags": "login;authentication;bug"
            }
        }
    }
    print(f"Request: {json.dumps(create_work_item_request, indent=2)}")
    print("Expected response: Details of the created work item\n")
    
    # Example 4: Custom WIQL query
    print("4. Using custom WIQL query to find specific work items:")
    custom_query_request = {
        "jsonrpc": "2.0",
        "id": 4,
        "method": "tools/call",
        "params": {
            "name": "list_work_items",
            "arguments": {
                "project": "MyProject",
                "wiql": """
                    SELECT [System.Id], [System.Title], [System.State] 
                    FROM WorkItems 
                    WHERE [System.TeamProject] = 'MyProject' 
                    AND [System.WorkItemType] = 'Bug' 
                    AND [System.State] = 'Active'
                    ORDER BY [System.CreatedDate] DESC
                """,
                "top": 20
            }
        }
    }
    print(f"Request: {json.dumps(custom_query_request, indent=2)}")
    print("Expected response: Active bugs in the project\n")
    
    # Example 5: Get build information
    print("5. Getting recent builds:")
    list_builds_request = {
        "jsonrpc": "2.0",
        "id": 5,
        "method": "tools/call",
        "params": {
            "name": "list_builds",
            "arguments": {
                "project": "MyProject",
                "top": 5
            }
        }
    }
    print(f"Request: {json.dumps(list_builds_request, indent=2)}")
    print("Expected response: Recent build information\n")


def create_claude_desktop_config():
    """
    Create an example Claude Desktop configuration for the Azure DevOps MCP Agent.
    """
    config = {
        "mcpServers": {
            "azure-devops": {
                "command": "python",
                "args": ["-m", "azure_devops_mcp_agent.server"],
                "env": {
                    "AZURE_DEVOPS_ORGANIZATION": "your-organization",
                    "AZURE_DEVOPS_PAT": "your-personal-access-token",
                    "AZURE_DEVOPS_PROJECT": "your-default-project"
                }
            }
        }
    }
    
    print("=== Claude Desktop Configuration ===\n")
    print("Add this to your Claude Desktop configuration file:")
    print("(Usually located at ~/Library/Application Support/Claude/claude_desktop_config.json)\n")
    print(json.dumps(config, indent=2))
    print("\n" + "="*50 + "\n")


def show_environment_setup():
    """Show how to set up environment variables."""
    print("=== Environment Setup ===\n")
    print("Option 1: Create a .env file in your project directory:")
    print("""
AZURE_DEVOPS_ORGANIZATION=your-organization-name
AZURE_DEVOPS_PAT=your-personal-access-token
AZURE_DEVOPS_PROJECT=your-default-project-name
""")
    
    print("Option 2: Set environment variables in your shell:")
    print("""
export AZURE_DEVOPS_ORGANIZATION=your-organization-name
export AZURE_DEVOPS_PAT=your-personal-access-token
export AZURE_DEVOPS_PROJECT=your-default-project-name
""")
    
    print("Option 3: Pass them when running the server:")
    print("""
AZURE_DEVOPS_ORGANIZATION=your-org AZURE_DEVOPS_PAT=your-pat python -m azure_devops_mcp_agent.server
""")
    print("\n" + "="*50 + "\n")


def show_installation_instructions():
    """Show installation instructions."""
    print("=== Installation Instructions ===\n")
    print("1. Install the package:")
    print("   pip install -e .")
    print("\n2. Or install dependencies manually:")
    print("   pip install mcp httpx python-dotenv")
    print("\n3. Set up environment variables (see Environment Setup section)")
    print("\n4. Run the server:")
    print("   azure-devops-mcp-agent")
    print("   # or")
    print("   python -m azure_devops_mcp_agent.server")
    print("\n5. Connect from your MCP client (e.g., Claude Desktop)")
    print("\n" + "="*50 + "\n")


async def main():
    """Main function to run all examples."""
    show_installation_instructions()
    show_environment_setup()
    create_claude_desktop_config()
    await example_mcp_client_interaction()
    
    print("=== Getting Started ===\n")
    print("To get started with Azure DevOps:")
    print("1. Create a Personal Access Token:")
    print("   - Go to https://dev.azure.com/your-organization")
    print("   - Click on User Settings (top right) > Personal Access Tokens")
    print("   - Create a new token with Work Items (Read & Write) scope")
    print("2. Set up your environment variables")
    print("3. Install and run the MCP server")
    print("4. Connect from your MCP client")
    print("\nFor more information, see the README.md file.")


if __name__ == "__main__":
    asyncio.run(main())
