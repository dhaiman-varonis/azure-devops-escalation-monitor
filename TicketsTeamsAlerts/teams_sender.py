#!/usr/bin/env python3
"""
Teams Message Sender - Multiple integration options for sending Azure DevOps ticket updates to Teams
"""

import json
import requests
import os
from typing import Dict, Any, Optional
from teams_message_generator import TeamsMessageGenerator

class TeamsSender:
    def __init__(self):
        self.generator = TeamsMessageGenerator()
        
    def send_via_webhook(self, webhook_url: str, message_data: Dict[str, Any]) -> bool:
        """
        Send message via Teams Incoming Webhook
        
        Args:
            webhook_url: Teams webhook URL
            message_data: Message payload from TeamsMessageGenerator
            
        Returns:
            bool: Success status
        """
        try:
            headers = {
                'Content-Type': 'application/json'
            }
            
            response = requests.post(webhook_url, json=message_data, headers=headers)
            
            if response.status_code == 200:
                print("✅ Message sent successfully via webhook!")
                return True
            else:
                print(f"❌ Failed to send message. Status: {response.status_code}")
                print(f"Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Error sending message: {str(e)}")
            return False
    
    def send_via_graph_api(self, access_token: str, chat_id: str, message_data: Dict[str, Any]) -> bool:
        """
        Send message via Microsoft Graph API
        
        Args:
            access_token: Microsoft Graph access token
            chat_id: Teams chat/channel ID
            message_data: Message payload
            
        Returns:
            bool: Success status
        """
        try:
            url = f"https://graph.microsoft.com/v1.0/chats/{chat_id}/messages"
            
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
            
            response = requests.post(url, json=message_data, headers=headers)
            
            if response.status_code == 201:
                print("✅ Message sent successfully via Graph API!")
                return True
            else:
                print(f"❌ Failed to send message. Status: {response.status_code}")
                print(f"Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Error sending message: {str(e)}")
            return False

    def get_webhook_instructions(self) -> str:
        """Get instructions for setting up Teams webhook"""
        return """
🔧 Teams Webhook Setup Instructions:

1. Go to your Teams channel
2. Click the three dots (...) next to the channel name
3. Select "Connectors"
4. Find "Incoming Webhook" and click "Configure"
5. Give it a name like "Azure DevOps Tickets"
6. Optionally upload an icon
7. Click "Create"
8. Copy the webhook URL that's generated
9. Use it with this script

Example webhook URL format:
https://varonis.webhook.office.com/webhookb2/xxx-xxx-xxx/IncomingWebhook/xxx/xxx
        """

    def get_graph_api_instructions(self) -> str:
        """Get instructions for Graph API setup"""
        return """
🔧 Microsoft Graph API Setup Instructions:

1. Register an app in Azure AD:
   - Go to portal.azure.com > Azure Active Directory > App registrations
   - Click "New registration"
   - Name: "Teams Message Sender"
   - Select appropriate account types
   - Register the app

2. Configure API permissions:
   - Go to "API permissions"
   - Add permission > Microsoft Graph > Application permissions
   - Add: Chat.ReadWrite, TeamsAppInstallation.ReadWrite
   - Grant admin consent

3. Create client secret:
   - Go to "Certificates & secrets"
   - Click "New client secret"
   - Copy the secret value

4. Get access token using client credentials flow

5. Find your chat/channel ID:
   - Use Graph Explorer or Teams admin tools
        """

def demo_atlas_teams_integration():
    """Demo function showing all integration options"""
    
    # Sample Atlas tickets (you can replace with real data from your Azure DevOps query)
    sample_tickets = [
        {
            "id": 2300240,
            "title": "Add Atlas Filer to RTA",
            "workItemType": "Task",
            "state": "Closed",
            "assignedTo": {"displayName": "Matti Ben-Avraham", "uniqueName": "mbenavraham@varonis.com"},
            "url": "https://dev.azure.com/VaronisIO/Idu%20Client-Server/_workitems/edit/2300240"
        },
        {
            "id": 2249539,
            "title": "[BVR2249539] Alarm.com - MongoDB Atlas",
            "workItemType": "Business Value Request",
            "state": "Execution",
            "assignedTo": {"displayName": "Jeremy Matheny", "uniqueName": "jmatheny@varonis.com"},
            "url": "https://dev.azure.com/VaronisIO/Idu%20Client-Server/_workitems/edit/2249539"
        }
    ]
    
    sender = TeamsSender()
    
    print("=== Teams Integration Options ===\n")
    
    # Option 1: Webhook (Easiest)
    print("🎯 Option 1: Teams Incoming Webhook (Recommended)")
    print(sender.get_webhook_instructions())
    print()
    
    # Generate message
    adaptive_card = sender.generator.format_multiple_tickets_for_teams(sample_tickets, "Atlas Integration Status Update")
    
    # For simple text, let's create a basic message
    simple_message = {
        "text": f"🔔 **Atlas Integration Status Update**\n\nFound {len(sample_tickets)} ticket(s):\n\n" + 
                "\n".join([f"• **{ticket['workItemType']} #{ticket['id']}**: {ticket['title']}\n  Status: {ticket['state']} | Assigned: {ticket['assignedTo']['displayName']}" 
                          for ticket in sample_tickets])
    }
    
    print("📋 Generated Messages:")
    print("\n--- Adaptive Card Format ---")
    print(json.dumps(adaptive_card, indent=2)[:500] + "...")
    
    print("\n--- Simple Text Format ---")
    print(json.dumps(simple_message, indent=2))
    
    print("\n🚀 To send via webhook:")
    print("webhook_url = 'YOUR_WEBHOOK_URL_HERE'")
    print("sender.send_via_webhook(webhook_url, adaptive_card)")
    
    print("\n" + "="*60)
    
    # Option 2: Graph API (Advanced)
    print("\n🎯 Option 2: Microsoft Graph API (Advanced)")
    print(sender.get_graph_api_instructions())
    
    print("\n🚀 To send via Graph API:")
    print("access_token = 'YOUR_ACCESS_TOKEN'")
    print("chat_id = 'YOUR_CHAT_ID'")
    print("sender.send_via_graph_api(access_token, chat_id, adaptive_card)")
    
    print("\n" + "="*60)
    
    # Option 3: MCP Integration
    print("\n🎯 Option 3: Teams MCP Server (AI Assistant)")
    print("""
The Teams MCP server we added to your VS Code configuration provides:
- Direct Teams integration via AI assistant
- OAuth2 authentication with Microsoft
- Team and channel management
- Message sending capabilities

After restarting VS Code, you can use natural language like:
"Send this Atlas ticket update to our dev team channel"
    """)

if __name__ == "__main__":
    demo_atlas_teams_integration()
