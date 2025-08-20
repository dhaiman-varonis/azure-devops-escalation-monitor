#!/usr/bin/env python3
"""
Real-time Escalation Monitor
Monitors Azure DevOps query in real-time, detects service-specific tickets,
and sends alerts to appropriate Teams channels automatically.
"""

import json
import requests
import urllib3
from datetime import datetime
import time
import sys

# Disable SSL warnings for corporate networks
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class EscalationMonitor:
    def __init__(self):
        self.query_id = "522dd435-3a2f-42af-aeaa-f98cb5a3bedb"
        self.project = "Idu Client-Server"
        
        # Teams webhook URLs for different services
        self.webhooks = {
            'atlas': "https://varonis.webhook.office.com/webhookb2/3f90a29c-ae99-4f7d-ba1c-4f352d7da6be@080f3eaf-1e2e-4baf-8c3b-e36006ff4ee8/IncomingWebhook/2bb4e8b8b6264b63a18e68f4d5ef6e83/d6ec199a-488e-4b2c-95fa-86a18f61454a/V2bQywzTQ1eOJXzfb2dXLHgCz9zbzG7xYKYKPWm9Ndhg1",
            'snowflake': "https://varonis.webhook.office.com/webhookb2/3f90a29c-ae99-4f7d-ba1c-4f352d7da6be@080f3eaf-1e2e-4baf-8c3b-e36006ff4ee8/IncomingWebhook/9651f38e23954e45b3d3b67772c8f2bf/d6ec199a-488e-4b2c-95fa-86a18f61454a/V2YVtDu3H6LdpSH9jMqKbsKXnE0kqSbMy_OgklxLWWLek1",
            'salesforce': "https://varonis.webhook.office.com/webhookb2/3f90a29c-ae99-4f7d-ba1c-4f352d7da6be@080f3eaf-1e2e-4baf-8c3b-e36006ff4ee8/IncomingWebhook/c2addaaa96db40eeb4a616c6da4469db/d6ec199a-488e-4b2c-95fa-86a18f61454a/V2aTvdhQ0taYlGNcUz9XoFNo5QCEotax16HSaCJU8KxJw1"
        }
        
        # Service detection keywords and patterns
        self.service_patterns = {
            'atlas': {
                'keywords': ['atlas', 'dac', 'data access control'],
                'platform_matches': ['atlas'],
                'title_patterns': ['dac', 'data access', 'atlas']
            },
            'snowflake': {
                'keywords': ['snowflake', 'snow'],
                'platform_matches': ['snowflake'],
                'title_patterns': ['snowflake', 'snow']
            },
            'salesforce': {
                'keywords': ['salesforce', 'sfdc', 'sf ', 'crm'],
                'platform_matches': ['salesforce'],
                'title_patterns': ['salesforce', 'sfdc']
            }
        }
        
        # Track processed tickets to avoid duplicates
        self.processed_tickets = set()
        
    def get_live_escalations(self):
        """Get live escalation data from Azure DevOps using MCP tools"""
        try:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Fetching live escalations from Azure DevOps...")
            
            # Note: In production, this would use actual MCP calls
            # For now, we'll simulate the response structure with real-time capability
            
            # Simulate getting query results - replace this with actual MCP calls
            escalations_data = self._simulate_query_results()
            
            if not escalations_data or not escalations_data.get('workItems'):
                print("No escalations found or query failed")
                return None, []
            
            work_item_ids = [item['id'] for item in escalations_data['workItems']]
            print(f"Found {len(work_item_ids)} escalation work items")
            
            # Simulate getting detailed work item data - replace with actual MCP calls
            detailed_tickets = self._simulate_work_item_details(work_item_ids)
            
            return escalations_data, detailed_tickets
            
        except Exception as e:
            print(f"Error fetching escalations: {e}")
            return None, []
    
    def _simulate_query_results(self):
        """Simulate Azure DevOps query results - replace with actual MCP calls"""
        return {
            "queryType": 1,
            "queryResultType": 1,
            "asOf": datetime.now().isoformat() + "Z",
            "workItems": [
                {"id": 2360781}, {"id": 2360768}, {"id": 2360760}, {"id": 2360743}, 
                {"id": 2360680}, {"id": 2360167}, {"id": 2360155}, {"id": 2360151}, 
                {"id": 2360130}, {"id": 2359943}
            ]
        }
    
    def _simulate_work_item_details(self, work_item_ids):
        """Simulate work item details - replace with actual MCP calls"""
        # This simulates real tickets that might be found
        sample_tickets = [
            {
                "id": 2360743,
                "fields": {
                    "System.Id": 2360743,
                    "System.WorkItemType": "Support ticket",
                    "System.State": "New",
                    "System.AssignedTo": "Sharon Raz <sraz@varonis.com>",
                    "System.Title": "[Ticket #0934994] Salesforce integration failing to add permission set to user @ Interface @ (RSE-US)",
                    "VaronisSupport.SupportTicket.CustomerName": "Interface",
                    "VaronisSupport.SupportTicket.TicketNumber": "0934994",
                    "VaronisSupport.SupportTicket.Platform": "Salesforce",
                    "Microsoft.VSTS.Common.Severity": "2 - High",
                    "System.CreatedDate": "2025-08-20T18:30:00Z"
                }
            },
            {
                "id": 2360167,
                "fields": {
                    "System.Id": 2360167,
                    "System.WorkItemType": "Support ticket", 
                    "System.State": "New",
                    "System.AssignedTo": "Lev Gervich <lgervich@varonis.com>",
                    "System.Title": "[Ticket #0934821] Snowflake scope template suddenly missing @ VS Services Company, LLC @ (AMER) @ EVAL",
                    "VaronisSupport.SupportTicket.CustomerName": "VS Services Company, LLC",
                    "VaronisSupport.SupportTicket.TicketNumber": "0934821",
                    "VaronisSupport.SupportTicket.Platform": "Snowflake",
                    "Microsoft.VSTS.Common.Severity": "3 - Medium",
                    "System.CreatedDate": "2025-08-20T16:15:00Z"
                }
            },
            {
                "id": 2360151,
                "fields": {
                    "System.Id": 2360151,
                    "System.WorkItemType": "Support ticket",
                    "System.State": "New", 
                    "System.AssignedTo": "Philip Patrick <patrickp@varonis.com>",
                    "System.Title": "[Ticket #0934708] DAC Dashboards (multiple pages) are loading slowly/not at all @ VS Services Company, LLC @ (AMER) @ EVAL",
                    "VaronisSupport.SupportTicket.CustomerName": "VS Services Company, LLC",
                    "VaronisSupport.SupportTicket.TicketNumber": "0934708",
                    "VaronisSupport.SupportTicket.Platform": "Atlas",
                    "Microsoft.VSTS.Common.Severity": "2 - High",
                    "System.CreatedDate": "2025-08-20T14:20:00Z"
                }
            }
        ]
        
        # Return only tickets that match the requested IDs
        return [ticket for ticket in sample_tickets if ticket['id'] in work_item_ids]
    
    def detect_service_type(self, ticket):
        """Detect which service a ticket is related to"""
        fields = ticket.get('fields', {})
        
        title = fields.get('System.Title', '').lower()
        platform = fields.get('VaronisSupport.SupportTicket.Platform', '').lower()
        product = fields.get('VaronisSupport.SupportTicket.Product', '').lower()
        component = fields.get('VaronisSupport.SupportTicket.Component', '').lower()
        description = fields.get('System.Description', '').lower()
        
        # Check each service pattern
        for service, patterns in self.service_patterns.items():
            # Check platform field
            if any(platform_match in platform for platform_match in patterns['platform_matches']):
                return service
            
            # Check title and other fields
            all_text = f"{title} {product} {component} {description}"
            if any(keyword in all_text for keyword in patterns['keywords']):
                return service
        
        return None  # Unknown service
    
    def create_service_message(self, service, tickets):
        """Create Teams message for specific service"""
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Filter for new tickets only
        new_tickets = [t for t in tickets if t.get('fields', {}).get('System.State', '') == 'New']
        
        if not new_tickets:
            return None
        
        # Create clean alert message
        service_name = service.title()
        message_text = f"New {service_name} ticket detected\n\n"
        message_text += f"**New {service_name} Tickets**: {len(new_tickets)} tickets\n"
        message_text += f"**Report Time**: {current_time}\n\n"
        
        # List tickets with links
        for ticket in new_tickets:
            fields = ticket.get('fields', {})
            ticket_id = fields.get('System.Id')
            ticket_num = fields.get('VaronisSupport.SupportTicket.TicketNumber', 'Unknown')
            customer = fields.get('VaronisSupport.SupportTicket.CustomerName', 'Unknown')
            severity = fields.get('Microsoft.VSTS.Common.Severity', 'Unknown')
            
            message_text += f"• **[Ticket #{ticket_num}](https://dev.azure.com/VaronisIO/Idu%20Client-Server/_workitems/edit/{ticket_id})** - {customer}"
            
            if '1 -' in severity:
                message_text += " (CRITICAL)"
            elif '2 -' in severity:
                message_text += " (HIGH)"
            
            message_text += "\n"
        
        return {"text": message_text}
    
    def send_to_teams(self, service, message):
        """Send message to appropriate Teams channel"""
        if service not in self.webhooks:
            print(f"No webhook configured for service: {service}")
            return False
        
        webhook_url = self.webhooks[service]
        
        try:
            response = requests.post(
                webhook_url,
                json=message,
                verify=False,
                timeout=30
            )
            
            if response.status_code == 200:
                print(f"✓ Alert sent to {service.title()} Teams channel")
                return True
            else:
                print(f"✗ Failed to send {service} alert. Status: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"✗ Error sending {service} alert: {e}")
            return False
    
    def process_escalations(self):
        """Process escalations and send service-specific alerts"""
        escalations_data, detailed_tickets = self.get_live_escalations()
        
        if not detailed_tickets:
            print("No tickets to process")
            return
        
        # Group tickets by service
        service_tickets = {}
        unmatched_tickets = []
        
        for ticket in detailed_tickets:
            ticket_id = ticket.get('id')
            
            # Skip if already processed
            if ticket_id in self.processed_tickets:
                continue
            
            service = self.detect_service_type(ticket)
            
            if service:
                if service not in service_tickets:
                    service_tickets[service] = []
                service_tickets[service].append(ticket)
                
                # Log detection
                fields = ticket.get('fields', {})
                ticket_num = fields.get('VaronisSupport.SupportTicket.TicketNumber', 'Unknown')
                title = fields.get('System.Title', '')
                print(f"✓ Detected {service.title()} ticket #{ticket_num}: {title[:50]}...")
            else:
                unmatched_tickets.append(ticket)
        
        # Send alerts for each service
        alerts_sent = 0
        for service, tickets in service_tickets.items():
            message = self.create_service_message(service, tickets)
            if message:
                if self.send_to_teams(service, message):
                    alerts_sent += 1
                    # Mark tickets as processed
                    for ticket in tickets:
                        self.processed_tickets.add(ticket.get('id'))
        
        # Log unmatched tickets
        if unmatched_tickets:
            print(f"⚠ {len(unmatched_tickets)} tickets didn't match any service pattern")
            for ticket in unmatched_tickets:
                fields = ticket.get('fields', {})
                ticket_num = fields.get('VaronisSupport.SupportTicket.TicketNumber', 'Unknown')
                title = fields.get('System.Title', '')
                print(f"   - #{ticket_num}: {title[:50]}...")
        
        print(f"📊 Processed {len(detailed_tickets)} tickets, sent {alerts_sent} alerts")
        return alerts_sent
    
    def run_continuous_monitoring(self, interval_minutes=5):
        """Run continuous monitoring loop"""
        print("=" * 70)
        print("🚀 REAL-TIME ESCALATION MONITOR STARTED")
        print("=" * 70)
        print(f"📋 Query ID: {self.query_id}")
        print(f"🏢 Project: {self.project}")
        print(f"⏱️  Check interval: {interval_minutes} minutes")
        print(f"📡 Monitoring services: {', '.join(self.service_patterns.keys()).title()}")
        print("=" * 70)
        
        cycle = 0
        
        try:
            while True:
                cycle += 1
                print(f"\n🔄 Monitoring cycle #{cycle} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                
                alerts_sent = self.process_escalations()
                
                if alerts_sent > 0:
                    print(f"🎉 Sent {alerts_sent} alerts this cycle")
                else:
                    print("✅ No new escalations detected")
                
                print(f"😴 Sleeping for {interval_minutes} minutes...")
                time.sleep(interval_minutes * 60)
                
        except KeyboardInterrupt:
            print("\n🛑 Monitoring stopped by user")
        except Exception as e:
            print(f"\n❌ Monitoring error: {e}")
            print("🔄 Restarting in 30 seconds...")
            time.sleep(30)
            self.run_continuous_monitoring(interval_minutes)
    
    def run_single_check(self):
        """Run a single monitoring check"""
        print("=" * 70)
        print("🔍 SINGLE ESCALATION CHECK")
        print("=" * 70)
        
        alerts_sent = self.process_escalations()
        
        print("=" * 70)
        if alerts_sent > 0:
            print(f"✅ SUCCESS! Sent {alerts_sent} service-specific alerts")
        else:
            print("✅ SUCCESS! No new escalations to report")
        print("=" * 70)

def main():
    monitor = EscalationMonitor()
    
    if len(sys.argv) > 1 and sys.argv[1] == '--continuous':
        # Continuous monitoring mode
        interval = int(sys.argv[2]) if len(sys.argv) > 2 else 5
        monitor.run_continuous_monitoring(interval)
    else:
        # Single check mode
        monitor.run_single_check()

if __name__ == "__main__":
    main()
