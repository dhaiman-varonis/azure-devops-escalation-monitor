# VS Code Copilot Instructions for Azure DevOps MCP Agent

This project contains an MCP (Model Context Protocol) server that connects AI applications to Azure DevOps services.

## Project Structure

- `azure_devops_mcp_agent/` - Main package
  - `__init__.py` - Package initialization
  - `server.py` - MCP server implementation
  - `client.py` - Azure DevOps API client
  - `config.py` - Configuration management
- `tests/` - Test files
- `examples/` - Usage examples
- `.vscode/mcp.json` - VS Code MCP configuration
- `pyproject.toml` - Project configuration and dependencies
- `README.md` - Project documentation

## Key Components

### MCP Server (`server.py`)
- Implements the Model Context Protocol server
- Exposes Azure DevOps functionality as MCP tools
- Provides resources for browsing Azure DevOps data
- Tools include: work item management, repository access, build information, team details

### Azure DevOps Client (`client.py`)
- Handles authentication with Azure DevOps REST API
- Provides async methods for all Azure DevOps operations
- Supports Personal Access Token authentication
- Includes comprehensive error handling

### Available MCP Tools
1. `list_work_items` - Query work items with optional WIQL
2. `get_work_item` - Get detailed work item information
3. `create_work_item` - Create new work items
4. `update_work_item` - Update existing work items
5. `list_repositories` - List project repositories
6. `get_repository` - Get repository details
7. `list_builds` - Query build information
8. `get_build` - Get detailed build information
9. `list_teams` - List project teams
10. `get_team` - Get team details
11. `list_projects` - List organization projects
12. `get_project` - Get project details

## Configuration

Requires environment variables:
- `AZURE_DEVOPS_ORGANIZATION` - Your Azure DevOps organization name
- `AZURE_DEVOPS_PAT` - Personal Access Token for authentication
- `AZURE_DEVOPS_PROJECT` - (Optional) Default project name

## Development Notes

- Uses `httpx` for async HTTP requests
- Implements proper MCP protocol with JSON-RPC 2.0
- Supports both stdio and HTTP transports
- Includes comprehensive error handling and logging
- Follows Azure DevOps REST API v7.1 conventions

## Testing

Run tests with: `pytest tests/`

The test suite covers:
- Authentication mechanisms
- API client functionality
- Configuration validation
- Error handling scenarios

## MCP Integration

This server can be used with any MCP-compatible client:
- Claude Desktop
- VS Code with MCP extension
- Custom MCP clients
- Any application supporting the MCP protocol

The `.vscode/mcp.json` file configures this server for VS Code MCP integration.
