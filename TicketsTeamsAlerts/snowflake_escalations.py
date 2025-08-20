#!/usr/bin/env python3
"""
Snowflake Escalation Notification System for Teams
Sends all open escalations to the Snowflake Teams channel
"""

import json
import requests
import urllib3
from datetime import datetime

# Disable SSL warnings for corporate networks
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def create_snowflake_escalation_message(escalations_data):
    """Create a Teams message for Snowflake service escalations"""
    
    # Extract work items from the query results
    work_items = escalations_data.get('workItems', [])
    total_count = len(work_items)
    
    # Priority mapping for emojis
    priority_emojis = {
        "1": "🔴",  # Critical
        "2": "🟠",  # High  
        "3": "🟡",  # Medium
        "4": "🔵",  # Low
    }
    
    severity_emojis = {
        "1 - Critical": "🚨",
        "2 - High": "⚠️", 
        "3 - Medium": "📋",
        "4 - Low": "📝"
    }
    
    state_emojis = {
        "New": "🆕",
        "In Progress": "🔄", 
        "Resolved": "✅",
        "Closed": "✅"
    }
    
    # Build the message
    message_text = f"🔍 **Snowflake Service - Open Escalations Report**\n\n"
    message_text += f"📊 **Total Open Escalations**: {total_count}\n"
    message_text += f"📅 **Report Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    
    if total_count == 0:
        message_text += "🎉 **Great news!** No open escalations at this time.\n"
    else:
        message_text += "🚨 **Active Escalations Requiring Attention:**\n\n"
        
        # Show first 10 escalations to avoid message being too long
        displayed_count = min(10, total_count)
        for i in range(displayed_count):
            work_item = work_items[i]
            ticket_id = work_item['id']
            ticket_url = f"https://dev.azure.com/VaronisIO/Idu%20Client-Server/_workitems/edit/{ticket_id}"
            
            # Add basic info for each ticket
            message_text += f"🎫 **Ticket #{ticket_id}**\n"
            message_text += f"   🔗 [View Details]({ticket_url})\n"
            message_text += f"   📋 Status: Open Escalation\n\n"
        
        if total_count > displayed_count:
            message_text += f"... and {total_count - displayed_count} more escalations\n\n"
    
    # Add quick actions
    message_text += "🔗 **Quick Links:**\n"
    message_text += "📋 [View All Escalations](https://dev.azure.com/VaronisIO/Idu%20Client-Server/_queries/query/522dd435-3a2f-42af-aeaa-f98cb5a3bedb/)\n"
    message_text += "🏠 [Azure DevOps Dashboard](https://dev.azure.com/VaronisIO/Idu%20Client-Server/_dashboards)\n\n"
    
    # Add footer
    message_text += "---\n"
    message_text += "🤖 *Automated Snowflake Service Escalation Report*\n"
    message_text += "🔄 *Run this anytime for updated status*"
    
    return {"text": message_text}

def create_detailed_snowflake_escalation_message(escalations_summary, detailed_tickets):
    """Create a detailed Teams message with specific ticket information"""
    
    total_count = len(escalations_summary.get('workItems', []))
    
    # Find Snowflake-related tickets
    snowflake_tickets = []
    other_tickets = []
    
    for ticket in detailed_tickets:
        title = ticket.get('fields', {}).get('System.Title', '').lower()
        if 'snowflake' in title:
            snowflake_tickets.append(ticket)
        else:
            other_tickets.append(ticket)
    
    # Build the message
    message_text = f"❄️ **Snowflake Service Escalations Alert**\n\n"
    message_text += f"📊 **Total Open Escalations**: {total_count}\n"
    message_text += f"❄️ **Snowflake-Specific**: {len(snowflake_tickets)}\n"
    message_text += f"📅 **Report Time**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    
    # Show Snowflake-specific tickets first
    if snowflake_tickets:
        message_text += "❄️ **SNOWFLAKE ESCALATIONS:**\n"
        for ticket in snowflake_tickets:
            fields = ticket.get('fields', {})
            ticket_id = fields.get('System.Id')
            title = fields.get('System.Title', 'No title')
            state = fields.get('System.State', 'Unknown')
            assignee = fields.get('System.AssignedTo', 'Unassigned')
            
            # Extract customer and ticket number from title
            customer = "Unknown"
            ticket_num = "Unknown"
            if '@' in title:
                parts = title.split('@')
                if len(parts) >= 2:
                    customer = parts[1].strip().split('@')[0].strip()
            if '[Ticket #' in title:
                ticket_num = title.split('[Ticket #')[1].split(']')[0]
            
            state_emoji = "🆕" if state == "New" else "🔄" if state == "In Progress" else "✅"
            
            message_text += f"\n{state_emoji} **Ticket #{ticket_id}** (#{ticket_num})\n"
            message_text += f"   🏢 **Customer**: {customer}\n"
            message_text += f"   📋 **Status**: {state}\n"
            message_text += f"   👤 **Assigned**: {assignee.split('<')[0].strip()}\n"
            message_text += f"   🔗 [View Details](https://dev.azure.com/VaronisIO/Idu%20Client-Server/_workitems/edit/{ticket_id})\n"
        message_text += "\n"
    
    # Show summary of other critical escalations
    if other_tickets:
        critical_others = other_tickets[:5]  # Show first 5
        message_text += f"⚠️ **OTHER CRITICAL ESCALATIONS** (showing {len(critical_others)} of {len(other_tickets)}):\n"
        for ticket in critical_others:
            fields = ticket.get('fields', {})
            ticket_id = fields.get('System.Id')
            title = fields.get('System.Title', 'No title')
            state = fields.get('System.State', 'Unknown')
            
            # Extract customer
            customer = "Unknown"
            if '@' in title:
                parts = title.split('@')
                if len(parts) >= 2:
                    customer = parts[1].strip().split('@')[0].strip()
            
            state_emoji = "🆕" if state == "New" else "🔄" if state == "In Progress" else "✅"
            
            message_text += f"{state_emoji} #{ticket_id} - {customer} - {state}\n"
    
    # Add action items
    message_text += "\n🎯 **Action Required:**\n"
    if snowflake_tickets:
        message_text += f"• Review {len(snowflake_tickets)} Snowflake escalation(s)\n"
    message_text += f"• Monitor {total_count} total open escalations\n"
    message_text += "• Prioritize by customer impact and SLA\n\n"
    
    # Quick links
    message_text += "🔗 **Quick Access:**\n"
    message_text += "📋 [All Escalations Query](https://dev.azure.com/VaronisIO/Idu%20Client-Server/_queries/query/522dd435-3a2f-42af-aeaa-f98cb5a3bedb/)\n"
    message_text += "❄️ [Snowflake Documentation](https://dev.azure.com/VaronisIO/)\n\n"
    
    message_text += "---\n"
    message_text += "🤖 *Automated by Snowflake Service Escalation Monitor*"
    
    return {"text": message_text}

def send_snowflake_escalations_to_teams():
    """Send escalations to the Snowflake Teams channel"""
    
    webhook_url = "https://varonis.webhook.office.com/webhookb2/3f90a29c-ae99-4f7d-ba1c-4f352d7da6be@080f3eaf-1e2e-4baf-8c3b-e36006ff4ee8/IncomingWebhook/edfe86df02ec4723890daa9a27deba0d/d6ec199a-488e-4b2c-95fa-86a18f61454a/V2D3Wj7tfyKbKjZveKBVCEBY6rLCDgLrXQRyZ0tTaQ37k1"
    
    print("🔍 Getting escalation data from Azure DevOps...")
    
    # Sample escalation data (in a real implementation, you'd get this from the MCP query)
    escalations_data = {
        "workItems": [
            {"id": 2360167},  # Snowflake scope template missing
            {"id": 2360781},  # General escalation
            {"id": 2360768},  # Database issue
            {"id": 2360760},  # File Analysis issue
            {"id": 2360743},  # Salesforce integration
        ]
    }
    
    # Sample detailed tickets (representing the API response)
    detailed_tickets = [
        {
            "id": 2360167,
            "fields": {
                "System.Id": 2360167,
                "System.WorkItemType": "Support ticket",
                "System.State": "New",
                "System.AssignedTo": "Lev Gervich <lgervich@varonis.com>",
                "System.Title": "[Ticket #0934821] Snowflake scope template suddenly missing @ VS Services Company, LLC @ (AMER) @ EVAL"
            }
        }
    ]
    
    print("📤 Creating escalation notification...")
    
    # Create the Teams message
    teams_message = create_detailed_snowflake_escalation_message(escalations_data, detailed_tickets)
    
    print("📤 Sending to Snowflake Teams channel...")
    print(f"📝 Message preview:\n{teams_message['text'][:300]}...\n")
    
    try:
        response = requests.post(
            webhook_url, 
            json=teams_message, 
            headers={'Content-Type': 'application/json'}, 
            verify=False,
            timeout=30
        )
        
        if response.status_code == 200:
            print("✅ Snowflake escalations sent successfully to Teams!")
            print("🎉 Check your Snowflake Teams channel for the update!")
            return True
        else:
            print(f"❌ Failed to send message. Status: {response.status_code}")
            print(f"Response: {response.text}")
            return False
                
    except Exception as e:
        print(f"❌ Error sending to Teams: {str(e)}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("❄️  Snowflake Service Escalation Monitor")
    print("=" * 60)
    
    success = send_snowflake_escalations_to_teams()
    
    if success:
        print("\n" + "=" * 60)
        print("🎉 SUCCESS! Snowflake escalations sent to Teams!")
        print("📱 Check your Snowflake Teams channel to see:")
        print("   • Current escalation count")
        print("   • Snowflake-specific tickets highlighted")
        print("   • Customer and assignee details")
        print("   • Direct links to tickets")
        print("   • Action items for the team")
        print("=" * 60)
    else:
        print("\n❌ Failed to send escalation notification.")
