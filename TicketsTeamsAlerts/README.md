# Azure DevOps Real-time Escalation Monitor

A comprehensive real-time monitoring system that automatically detects Azure DevOps escalation tickets and routes alerts to appropriate Microsoft Teams channels based on service type.

## 🚀 Features

- **Real-time Monitoring** - Continuous monitoring of Azure DevOps escalation queries
- **Automatic Service Detection** - Platform-based detection for Atlas (MongoDB), Snowflake, and Salesforce
- **Teams Integration** - Sends clean, actionable alerts to service-specific Teams channels
- **Duplicate Prevention** - Tracks processed tickets to avoid duplicate alerts
- **MCP Integration** - Ready for Azure DevOps MCP tool integration

## 📁 Files

### Core Files
## Files Overview

- **`escalation_monitor.py`** - Production-ready monitor (requires MCP environment)
- **`test_escalation_monitor.py`** - Testing version with simulation data  
- **`webhook_tester.py`** - Utility to test Teams webhook connectivity
- **`MCP_INTEGRATION_GUIDE.md`** - Complete deployment and configuration guide

## 🎯 Service Detection

The system uses **platform-based detection only** for maximum accuracy:

- **Atlas**: `mongodb`, `mongo` platform values → Routes to Atlas Teams channel
- **Snowflake**: `snowflake` platform values → Routes to Snowflake Teams channel  
- **Salesforce**: `salesforce` platform values → Routes to Salesforce Teams channel

## 🔧 Quick Start

### Prerequisites
- Python 3.8+
- Azure DevOps MCP tools (for production)
- Valid Teams webhook URLs

### Installation
```bash
git clone https://github.com/dhaiman-varonis/azure-devops-escalation-monitor.git
cd azure-devops-escalation-monitor
pip install requests urllib3
```

### Configuration
Update webhook URLs in the monitor files:
```python
self.webhooks = {
    'atlas': "YOUR_ATLAS_WEBHOOK_URL",
    'snowflake': "YOUR_SNOWFLAKE_WEBHOOK_URL", 
    'salesforce': "YOUR_SALESFORCE_WEBHOOK_URL"
}
```

### Usage

#### Test Webhooks
```bash
python webhook_tester.py
```

### Testing/Development (No MCP Required)
```bash
python test_escalation_monitor.py

# For continuous testing (checks every 5 minutes)
python test_escalation_monitor.py --continuous 5

#### Production (with MCP)
```bash
### Production Use (Requires MCP Environment)
```bash
python escalation_monitor.py

# For continuous monitoring (checks every 5 minutes)
python escalation_monitor.py --continuous 5
```

## 📊 Sample Output

```
🚀 REAL-TIME ESCALATION MONITOR
==================================================
📋 Query ID: 522dd435-3a2f-42af-aeaa-f98cb5a3bedb
🏢 Project: Idu Client-Server
📡 Services: Atlas, Snowflake, Salesforce
==================================================
[00:44:18] Fetching live escalations from Azure DevOps...
🎯 Detected Salesforce ticket #0934994
🎯 Detected Snowflake ticket #0934821
🎯 Detected Atlas ticket #0934708
✅ Alert sent to Salesforce Teams channel
✅ Alert sent to Snowflake Teams channel
✅ Alert sent to Atlas Teams channel
📊 Processed 4 new tickets, sent 3 service alerts
==================================================
✅ SUCCESS! Sent 3 service-specific alerts
==================================================
```

## 🔄 Teams Alert Format

Clean, actionable alerts sent to Teams:

```
New Salesforce ticket detected

**New Salesforce Tickets**: 1 tickets
**Report Time**: 2024-12-19 14:23:45

• [Ticket #0934994](link) - Interface (HIGH)
```

## 🏗️ Architecture

- **Platform Detection**: Uses `VaronisSupport.SupportTicket.Platform` field exclusively
- **State Management**: Tracks processed tickets to prevent duplicates
- **Error Handling**: Graceful fallback and comprehensive logging
- **MCP Ready**: Structured for Azure DevOps MCP tool integration

## 📚 Documentation

See `MCP_INTEGRATION_GUIDE.md` for detailed deployment instructions and MCP integration steps.

## 🛠️ Development

The system includes simulation mode for testing without MCP tools:
- Realistic ticket data
- All detection logic validation  
- Webhook testing capabilities

## 📈 Monitoring

- Only processes tickets in "New" state
- Configurable check intervals
- Detailed logging and error reporting
- Session-based duplicate prevention

---

**Repository**: https://github.com/dhaiman-varonis/azure-devops-escalation-monitor  
**Author**: Varonis Development Team  
**License**: Internal Use
