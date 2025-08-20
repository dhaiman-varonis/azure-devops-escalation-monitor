#!/usr/bin/env python3
"""
Simple Teams Webhook Sender - Easy way to send Atlas ticket updates to Teams
No authentication required, just a webhook URL
"""

import json
import requests
from atlas_teams_generator import create_atlas_tickets_teams_message

def send_to_teams_webhook(webhook_url: str):
    """
    Send Atlas tickets to Teams via webhook
    
    Args:
        webhook_url: Your Teams incoming webhook URL
    """
    
    print("🔍 Generating Atlas tickets message...")
    
    # Get the Atlas tickets message (both formats)
    adaptive_card, simple_text = create_atlas_tickets_teams_message()
    
    print("📤 Sending to Teams...")
    
    try:
        # Try sending the adaptive card first
        response = requests.post(webhook_url, json=adaptive_card, headers={'Content-Type': 'application/json'})
        
        if response.status_code == 200:
            print("✅ Atlas tickets sent successfully to Teams!")
            print("🎉 Check your Teams channel for the update!")
            return True
        else:
            print(f"❌ Failed to send. Status: {response.status_code}")
            print(f"Response: {response.text}")
            
            # Try fallback to simple text
            print("🔄 Trying simple text format...")
            fallback_response = requests.post(webhook_url, json=simple_text, headers={'Content-Type': 'application/json'})
            
            if fallback_response.status_code == 200:
                print("✅ Simple message sent successfully!")
                return True
            else:
                print(f"❌ Fallback also failed: {fallback_response.status_code}")
                return False
                
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def setup_webhook_instructions():
    """Show how to set up Teams webhook"""
    print("""
🔧 Teams Webhook Setup (Easy 2-minute setup):

1. Go to your Teams channel
2. Click the 3 dots (...) next to channel name  
3. Select "Connectors" or "Manage channel"
4. Find "Incoming Webhook" and click "Configure"
5. Name: "Azure DevOps Atlas Updates"
6. Upload icon (optional)
7. Click "Create"
8. COPY THE WEBHOOK URL - it looks like:
   https://varonis.webhook.office.com/webhookb2/xxx.../IncomingWebhook/xxx.../xxx...

9. Paste the URL below and run this script!
    """)

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 Teams Atlas Ticket Sender")
    print("=" * 60)
    
    # Show setup instructions
    setup_webhook_instructions()
    
    # Get webhook URL from user
    webhook_url = input("\n📋 Paste your Teams webhook URL here: ").strip()
    
    if not webhook_url:
        print("❌ No webhook URL provided!")
        print("\n💡 Get your webhook URL from Teams and run this script again.")
        exit(1)
    
    if not webhook_url.startswith("https://"):
        print("❌ Invalid webhook URL! Should start with https://")
        exit(1)
    
    print(f"\n🎯 Using webhook: {webhook_url[:50]}...")
    
    # Send the message
    success = send_to_teams_webhook(webhook_url)
    
    if success:
        print("\n🎉 Done! Your Atlas tickets are now posted in Teams!")
        print("📱 Check your Teams channel to see the update.")
    else:
        print("\n❌ Failed to send message. Check your webhook URL and try again.")
        print("💡 Make sure you copied the complete webhook URL from Teams.")
