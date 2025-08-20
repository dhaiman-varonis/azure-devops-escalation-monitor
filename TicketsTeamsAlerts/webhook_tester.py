#!/usr/bin/env python3
"""
Teams Webhook Tester
Test individual webhook URLs to diagnose issues
"""

import requests
import urllib3
from datetime import datetime

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def test_webhook(service_name, webhook_url):
    """Test a single webhook URL"""
    test_message = {
        "text": f"🧪 **Test Alert for {service_name.title()}**\n\n"
                f"This is a test message sent at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"If you receive this, the webhook is working correctly!"
    }
    
    print(f"Testing {service_name} webhook...")
    
    try:
        response = requests.post(
            webhook_url,
            json=test_message,
            verify=False,
            timeout=30
        )
        
        if response.status_code == 200:
            print(f"✅ {service_name.title()} webhook is working!")
            return True
        else:
            print(f"❌ {service_name.title()} webhook failed with status: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing {service_name} webhook: {e}")
        return False

def main():
    # Updated webhook URLs from user
    webhooks = {
        'atlas': "https://varonis.webhook.office.com/webhookb2/3f90a29c-ae99-4f7d-ba1c-4f352d7da6be@080f3eaf-1e2e-4baf-8c3b-e36006ff4ee8/IncomingWebhook/ffd2fa48eb78405b8f41d1650d9c9b45/d6ec199a-488e-4b2c-95fa-86a18f61454a/V2V-fEl6OriwSiSXr6fx--Vcl1wg0hfIYKbJg7COp82HI1",
        'snowflake': "https://varonis.webhook.office.com/webhookb2/3f90a29c-ae99-4f7d-ba1c-4f352d7da6be@080f3eaf-1e2e-4baf-8c3b-e36006ff4ee8/IncomingWebhook/785cf0f989ed4701aa1fb9237ee0b38b/d6ec199a-488e-4b2c-95fa-86a18f61454a/V28e8EsdJsyeD_bvOW-RSngNGFSAiZ3B38Rfa2ivEY71k1",
        'salesforce': "https://varonis.webhook.office.com/webhookb2/3f90a29c-ae99-4f7d-ba1c-4f352d7da6be@080f3eaf-1e2e-4baf-8c3b-e36006ff4ee8/IncomingWebhook/c2addaaa96db40eeb4a616c6da4469db/d6ec199a-488e-4b2c-95fa-86a18f61454a/V2aTvdhQ0taYlGNcUz9XoFNo5QCEotax16HSaCJU8KxJw1"
    }
    
    print("🧪 TEAMS WEBHOOK TESTER")
    print("=" * 40)
    
    working_webhooks = {}
    failed_webhooks = {}
    
    for service, url in webhooks.items():
        if test_webhook(service, url):
            working_webhooks[service] = url
        else:
            failed_webhooks[service] = url
        print()
    
    print("=" * 40)
    print("📊 TEST RESULTS:")
    print(f"✅ Working: {list(working_webhooks.keys())}")
    print(f"❌ Failed: {list(failed_webhooks.keys())}")
    
    if failed_webhooks:
        print("\n🔧 NEXT STEPS:")
        print("1. Check if the Teams channels still exist")
        print("2. Regenerate webhook URLs in Teams channel settings")
        print("3. Update the URLs in your monitor script")
        print("\n📋 Failed webhook URLs to replace:")
        for service, url in failed_webhooks.items():
            print(f"   {service}: {url}")

if __name__ == "__main__":
    main()
