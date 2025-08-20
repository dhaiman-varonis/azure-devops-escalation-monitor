#!/usr/bin/env python3
"""
Generate Teams messages for Atlas tickets using Azure DevOps MCP data
"""

import json
from teams_message_generator import TeamsMessageGenerator


def create_atlas_tickets_teams_message():
    """
    Create a Teams message using the Atlas ticket data we found.
    This uses the actual search results from Azure DevOps.
    """
    
    # Atlas tickets data from our search (top results)
    atlas_tickets = [
        {
            "fields": {
                "system.id": "2300240",
                "system.workitemtype": "Task",
                "system.title": "Add Atlas Filer to RTA",
                "system.assignedto": "Matti Ben-Avraham <mbenavraham@varonis.com>",
                "system.state": "Closed",
                "system.tags": "",
                "system.createddate": "2025-07-01T12:33:51.9130000Z",
                "system.changeddate": "2025-08-13T04:41:32.9330000Z"
            }
        },
        {
            "fields": {
                "system.id": "2249539",
                "system.workitemtype": "Business Value Request",
                "system.title": "[BVR2249539] Alarm.com - MongoDB Atlas",
                "system.assignedto": "Jeremy Matheny <jmatheny@varonis.com>",
                "system.state": "Execution",
                "system.tags": "Shlomit_FollowUp",
                "system.createddate": "2025-05-02T14:13:16.0730000Z",
                "system.changeddate": "2025-08-05T12:08:34.3700000Z"
            }
        },
        {
            "fields": {
                "system.id": "2283775",
                "system.workitemtype": "Task",
                "system.title": "Add Atlas in DAC services",
                "system.assignedto": "Meital Zeltcer <mnivzeltcer@varonis.com>",
                "system.state": "Closed",
                "system.tags": "",
                "system.createddate": "2025-06-26T11:07:33.5030000Z",
                "system.changeddate": "2025-07-31T15:51:35.7130000Z"
            }
        },
        {
            "fields": {
                "system.id": "2286894",
                "system.workitemtype": "Feature",
                "system.title": "[Varonis\\Saas Integration] Support \"atlas\" Filer in SaaS",
                "system.assignedto": "Daniel Tshuva <dtshuva@varonis.com>",
                "system.state": "In Progress",
                "system.tags": "",
                "system.createddate": "2025-06-30T14:48:54.1830000Z",
                "system.changeddate": "2025-08-20T18:15:31.4930000Z"
            }
        },
        {
            "fields": {
                "system.id": "2353332",
                "system.workitemtype": "Bug",
                "system.title": "[v19][SaaS-DAC Integration][MongoDB Atlas] Some Atlas identities are not supported by SaaS, presented as \"No Value\"",
                "system.assignedto": "Daniel Tshuva <dtshuva@varonis.com>",
                "system.state": "On Hold",
                "system.tags": "Varonis/DAC Integration",
                "system.createddate": "2025-08-07T11:27:23.6500000Z",
                "system.changeddate": "2025-08-11T14:26:28.4900000Z"
            }
        }
    ]
    
    generator = TeamsMessageGenerator()
    
    # Generate Teams message
    teams_message = generator.format_multiple_tickets_for_teams(
        atlas_tickets,
        "🔍 Atlas Integration Status Update"
    )
    
    return teams_message


def create_simple_atlas_summary_message():
    """
    Create a simple text-based Teams message for Atlas tickets.
    """
    message = {
        "text": """📋 **Atlas Integration Status Update**
        
Found 5 key Atlas-related tickets:

🎫 **Task #2300240** - Add Atlas Filer to RTA
   📌 Status: Closed | 👤 Assigned: Matti Ben-Avraham
   🔗 [View Ticket](https://dev.azure.com/VaronisIO/Idu%20Client-Server/_workitems/edit/2300240)

🎫 **BVR #2249539** - Alarm.com - MongoDB Atlas  
   📌 Status: Execution | 👤 Assigned: Jeremy Matheny
   🔗 [View Ticket](https://dev.azure.com/VaronisIO/Idu%20Client-Server/_workitems/edit/2249539)

🎫 **Feature #2286894** - Support "atlas" Filer in SaaS
   📌 Status: In Progress | 👤 Assigned: Daniel Tshuva
   🔗 [View Ticket](https://dev.azure.com/VaronisIO/Idu%20Client-Server/_workitems/edit/2286894)

🎫 **Bug #2353332** - Atlas identities not supported in SaaS
   📌 Status: On Hold | 👤 Assigned: Daniel Tshuva
   🔗 [View Ticket](https://dev.azure.com/VaronisIO/Idu%20Client-Server/_workitems/edit/2353332)

📊 **Summary**: 2 Closed, 1 In Progress, 1 Execution, 1 On Hold
💡 **Total Atlas tickets found**: 285 across the project"""
    }
    
    return message


if __name__ == "__main__":
    print("=== Atlas Tickets Teams Message ===")
    
    # Generate adaptive card message
    adaptive_message = create_atlas_tickets_teams_message()
    print("Adaptive Card Message:")
    print(json.dumps(adaptive_message, indent=2))
    
    print("\n" + "="*50 + "\n")
    
    # Generate simple text message
    simple_message = create_simple_atlas_summary_message()
    print("Simple Text Message:")
    print(json.dumps(simple_message, indent=2))
    
    print("\n=== How to Use ===")
    print("1. Copy the JSON output above")
    print("2. Use Teams webhook or Graph API to send the message")
    print("3. Or copy the simple text version for manual posting")
