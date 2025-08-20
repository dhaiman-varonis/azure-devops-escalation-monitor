# Azure DevOps MCP Agent

An MCP (Model Context Protocol) server that connects AI applications to Azure DevOps, enabling AI assistants to interact with work items, repositories, builds, and other Azure DevOps services.

## Features

- **Work Items Management**: Create, read, update work items (user stories, bugs, tasks, etc.)
- **Repository Operations**: Access repository information, branches, commits
- **Build Information**: Query build status, history, and results
- **Team Management**: Access team information and project details
- **Secure Authentication**: OAuth 2.0 and Personal Access Token support

## Installation

```bash
# Install with pip
pip install azure-devops-mcp-agent

# Or install from source
git clone <repository-url>
cd azure-devops-mcp-agent
pip install -e .
```

## Configuration

1. Set up your Azure DevOps credentials:

```bash
# Using Personal Access Token (recommended for development)
export AZURE_DEVOPS_PAT="your_personal_access_token"
export AZURE_DEVOPS_ORGANIZATION="your_organization"

# Or using OAuth (recommended for production)
export AZURE_DEVOPS_CLIENT_ID="your_client_id"
export AZURE_DEVOPS_CLIENT_SECRET="your_client_secret"
export AZURE_DEVOPS_TENANT_ID="your_tenant_id"
export AZURE_DEVOPS_ORGANIZATION="your_organization"
```

2. Create a `.env` file (optional):

```env
AZURE_DEVOPS_PAT=your_personal_access_token
AZURE_DEVOPS_ORGANIZATION=your_organization
AZURE_DEVOPS_PROJECT=your_default_project
```

## Usage

### Running the MCP Server

```bash
# Run the server
azure-devops-mcp-agent

# Or run with Python module
python -m azure_devops_mcp_agent.server
```

### Connecting with Claude Desktop

Add the following to your Claude Desktop configuration file:

```json
{
  "mcpServers": {
    "azure-devops": {
      "command": "azure-devops-mcp-agent",
      "env": {
        "AZURE_DEVOPS_PAT": "your_personal_access_token",
        "AZURE_DEVOPS_ORGANIZATION": "your_organization"
      }
    }
  }
}
```

### Available Tools

- `list_work_items`: Get work items from a project
- `get_work_item`: Get detailed information about a specific work item
- `create_work_item`: Create a new work item
- `update_work_item`: Update an existing work item
- `list_repositories`: Get repositories in a project
- `get_repository`: Get detailed repository information
- `list_builds`: Get build information
- `get_build`: Get detailed build information
- `list_teams`: Get teams in a project
- `get_team`: Get detailed team information

## Development

1. Clone the repository
2. Install development dependencies:

```bash
pip install -e ".[dev]"
```

3. Run tests:

```bash
pytest
```

4. Format code:

```bash
black .
ruff --fix .
```

## License

MIT License - see LICENSE file for details.
