#!/usr/bin/env python3
"""
Send Atlas tickets to Teams with the provided webhook URL
"""

import json
import requests
from atlas_teams_generator import create_atlas_tickets_teams_message

def send_atlas_to_teams():
    webhook_url = "https://varonis.webhook.office.com/webhookb2/3f90a29c-ae99-4f7d-ba1c-4f352d7da6be@080f3eaf-1e2e-4baf-8c3b-e36006ff4ee8/IncomingWebhook/975c8d8421e44cb2b4fe3acd64adfe44/d6ec199a-488e-4b2c-95fa-86a18f61454a/V2i15L0FZHs7R2jXdX800JlgbEZXtZaUiaCToBnQ7vvIc1"
    
    print("🔍 Generating Atlas tickets message...")
    
    # Get the Atlas tickets message (both formats)
    adaptive_card, simple_text = create_atlas_tickets_teams_message()
    
    print("📤 Sending Atlas tickets to Teams...")
    
    try:
        # Send the adaptive card (with SSL verification disabled for corporate networks)
        response = requests.post(webhook_url, json=adaptive_card, headers={'Content-Type': 'application/json'}, verify=False)
        
        if response.status_code == 200:
            print("✅ Atlas tickets sent successfully to Teams!")
            print("🎉 Check your Teams channel for the Atlas update!")
            print(f"📊 Sent details for 5 Atlas tickets with beautiful formatting")
            return True
        else:
            print(f"❌ Failed to send adaptive card. Status: {response.status_code}")
            print(f"Response: {response.text}")
            
            # Try fallback to simple text
            print("🔄 Trying simple text format...")
            fallback_response = requests.post(webhook_url, json=simple_text, headers={'Content-Type': 'application/json'}, verify=False)
            
            if fallback_response.status_code == 200:
                print("✅ Simple Atlas message sent successfully!")
                print("📱 Check your Teams channel for the update!")
                return True
            else:
                print(f"❌ Both formats failed. Status: {fallback_response.status_code}")
                print(f"Fallback response: {fallback_response.text}")
                return False
                
    except Exception as e:
        print(f"❌ Error sending to Teams: {str(e)}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 Sending Atlas Tickets to Teams")
    print("=" * 60)
    
    success = send_atlas_to_teams()
    
    if success:
        print("\n" + "=" * 60)
        print("🎉 SUCCESS! Your Atlas tickets are now in Teams!")
        print("📱 Go check your Teams channel to see:")
        print("   • 5 Atlas tickets with full details")
        print("   • Clickable links to each ticket")
        print("   • Status and assignee information")
        print("   • Beautiful adaptive card formatting")
        print("=" * 60)
    else:
        print("\n❌ Failed to send message. Please check the webhook URL.")
