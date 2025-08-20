# Azure DevOps Real-time Escalation Monitor - MCP Integration Guide

## Overview
This system monitors Azure DevOps escalation queries in real-time and automatically routes alerts to the appropriate Teams channels based on service detection.

## Files
- `production_monitor.py` - Production-ready monitor with MCP integration
- `mcp_realtime_monitor.py` - Testing version with simulation
- Individual service monitors: `atlas_escalations.py`, `snowflake_escalations.py`, `salesforce_escalations.py`

## MCP Integration Requirements

### Required MCP Tools
The production monitor requires these Azure DevOps MCP tools:
```python
from mcp_tools import (
    mcp_ado_wit_get_query_results_by_id,
    mcp_ado_wit_get_work_items_batch_by_ids
)
```

### Configuration
Update these settings in `production_monitor.py`:

1. **Teams Webhook URLs** - Replace expired URLs:
```python
self.webhooks = {
    'atlas': "YOUR_ATLAS_WEBHOOK_URL",
    'snowflake': "YOUR_SNOWFLAKE_WEBHOOK_URL", 
    'salesforce': "YOUR_SALESFORCE_WEBHOOK_URL"
}
```

2. **Azure DevOps Configuration**:
```python
self.query_id = "522dd435-3a2f-42af-aeaa-f98cb5a3bedb"
self.project = "Idu Client-Server"
```

## Usage

### Single Check Mode
```bash
python production_monitor.py
```

### Continuous Monitoring Mode
```bash
# Check every 5 minutes (default)
python production_monitor.py --continuous

# Check every 2 minutes
python production_monitor.py --continuous 2
```

## Service Detection Logic
The system automatically detects service types using:

1. **Platform Field** (highest priority)
   - Direct match against `VaronisSupport.SupportTicket.Platform`

2. **Title Keywords**
   - Atlas: 'dac', 'data access', 'atlas', 'dashboard', 'file analysis'
   - Snowflake: 'snowflake', 'snow', 'scope template'
   - Salesforce: 'salesforce', 'sfdc', 'permission set'

3. **Description Keywords**
   - Fallback pattern matching in ticket descriptions

## Message Format
Clean, simple Teams alerts:
```
New Salesforce ticket detected

**New Salesforce Tickets**: 1 tickets
**Report Time**: 2024-12-19 14:23:45

• [Ticket #0934994](link) - Interface (HIGH)
```

## State Management
- Tracks processed tickets to avoid duplicates
- Only processes tickets in "New" state
- Maintains session memory until restart

## Error Handling
- Graceful fallback to simulation mode if MCP tools unavailable
- SSL warning suppression for corporate networks
- Comprehensive error logging

## Deployment Steps

1. **Update webhook URLs** in production_monitor.py
2. **Deploy to MCP environment** where Azure DevOps tools are available
3. **Test single run** first: `python production_monitor.py`
4. **Enable continuous monitoring** for production: `python production_monitor.py --continuous 5`

## GitHub Repository
All code is available at: https://github.com/dhaiman-varonis/azure-devops-escalation-monitor

## Monitoring Output
The system provides detailed logging:
```
🚀 REAL-TIME ESCALATION MONITOR
============================================================
📋 Query: 522dd435-3a2f-42af-aeaa-f98cb5a3bedb
🏢 Project: Idu Client-Server
📡 Services: Atlas, Snowflake, Salesforce
🔧 MCP Mode: Enabled
============================================================
[14:23:45] 🔄 Fetching escalations from Azure DevOps...
📊 Found 4 escalation work items
📋 Retrieved details for 4 work items
🎯 Salesforce ticket #0934994 detected
✅ Salesforce alert sent successfully
📊 Processed 1 new tickets → 1 alerts sent
============================================================
✅ SUCCESS! 1 alerts sent to Teams
============================================================
```

## Testing
Use `mcp_realtime_monitor.py` for testing without MCP tools. It includes simulation data and validates the complete workflow.
