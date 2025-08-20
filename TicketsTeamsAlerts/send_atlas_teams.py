#!/usr/bin/env python3
"""
Send Atlas tickets to Teams with Teams-compatible webhook format
"""

import json
import requests
import urllib3

# Disable SSL warnings for corporate networks
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def create_teams_webhook_message():
    """Create a Teams webhook compatible message"""
    
    # Sample Atlas tickets data (using the same data from our previous examples)
    atlas_tickets = [
        {
            "id": "2300240",
            "title": "Add Atlas Filer to RTA",
            "type": "Task",
            "state": "Closed",
            "assignee": "Matti Ben-Avraham <mbenavraham@varonis.com>",
            "url": "https://dev.azure.com/VaronisIO/Idu%20Client-Server/_workitems/edit/2300240"
        },
        {
            "id": "2249539", 
            "title": "[BVR2249539] Alarm.com - MongoDB Atlas",
            "type": "Business Value Request",
            "state": "Execution",
            "assignee": "Jeremy Matheny <jmatheny@varonis.com>",
            "url": "https://dev.azure.com/VaronisIO/Idu%20Client-Server/_workitems/edit/2249539"
        },
        {
            "id": "2283775",
            "title": "Add Atlas in DAC services", 
            "type": "Task",
            "state": "Closed",
            "assignee": "Meital Zeltcer <mnivzeltcer@varonis.com>",
            "url": "https://dev.azure.com/VaronisIO/Idu%20Client-Server/_workitems/edit/2283775"
        },
        {
            "id": "2286894",
            "title": "[Varonis\\Saas Integration] Support \"atlas\" Filer in SaaS",
            "type": "Feature", 
            "state": "In Progress",
            "assignee": "Daniel Tshuva <dtshuva@varonis.com>",
            "url": "https://dev.azure.com/VaronisIO/Idu%20Client-Server/_workitems/edit/2286894"
        },
        {
            "id": "2353332",
            "title": "[v19][SaaS-DAC Integration][MongoDB Atlas] Some Atlas identities are not supported by SaaS, presented as \"No Value\"",
            "type": "Bug",
            "state": "On Hold", 
            "assignee": "Daniel Tshuva <dtshuva@varonis.com>",
            "url": "https://dev.azure.com/VaronisIO/Idu%20Client-Server/_workitems/edit/2353332"
        }
    ]
    
    # Create simple Teams webhook message
    message_text = "📋 **Atlas Integration Status Update**\n\n"
    message_text += f"Found **{len(atlas_tickets)}** Atlas-related tickets:\n\n"
    
    for ticket in atlas_tickets:
        status_emoji = "✅" if ticket["state"] == "Closed" else "🔄" if ticket["state"] == "In Progress" else "⚡" if ticket["state"] == "Execution" else "⏸️"
        message_text += f"{status_emoji} **{ticket['type']} #{ticket['id']}** - {ticket['title']}\n"
        message_text += f"   📍 Status: {ticket['state']} | 👤 Assigned: {ticket['assignee'].split('<')[0].strip()}\n"
        message_text += f"   🔗 [View Ticket]({ticket['url']})\n\n"
    
    message_text += "📊 **Summary**: 2 Closed, 1 In Progress, 1 Execution, 1 On Hold\n"
    message_text += "💡 **Total Atlas tickets found**: 285 across the project"
    
    # Teams webhook format
    teams_message = {
        "text": message_text
    }
    
    return teams_message

def send_atlas_to_teams():
    webhook_url = "https://varonis.webhook.office.com/webhookb2/3f90a29c-ae99-4f7d-ba1c-4f352d7da6be@080f3eaf-1e2e-4baf-8c3b-e36006ff4ee8/IncomingWebhook/975c8d8421e44cb2b4fe3acd64adfe44/d6ec199a-488e-4b2c-95fa-86a18f61454a/V2i15L0FZHs7R2jXdX800JlgbEZXtZaUiaCToBnQ7vvIc1"
    
    print("🔍 Generating Atlas tickets message...")
    
    # Create Teams-compatible message
    teams_message = create_teams_webhook_message()
    
    print("📤 Sending Atlas tickets to Teams...")
    print(f"📝 Message preview:\n{teams_message['text'][:200]}...\n")
    
    try:
        response = requests.post(
            webhook_url, 
            json=teams_message, 
            headers={'Content-Type': 'application/json'}, 
            verify=False,
            timeout=30
        )
        
        if response.status_code == 200:
            print("✅ Atlas tickets sent successfully to Teams!")
            print("🎉 Check your Teams channel for the Atlas update!")
            print(f"📊 Sent details for 5 Atlas tickets")
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
    print("🚀 Sending Atlas Tickets to Teams (Webhook Format)")
    print("=" * 60)
    
    success = send_atlas_to_teams()
    
    if success:
        print("\n" + "=" * 60)
        print("🎉 SUCCESS! Your Atlas tickets are now in Teams!")
        print("📱 Go check your Teams channel to see:")
        print("   • 5 Atlas tickets with full details")
        print("   • Clickable links to each ticket")
        print("   • Status and assignee information")
        print("   • Clear status summary")
        print("=" * 60)
    else:
        print("\n❌ Failed to send message.")
