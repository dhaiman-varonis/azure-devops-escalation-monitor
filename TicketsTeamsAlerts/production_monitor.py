#!/usr/bin/env python3
"""
Production Real-time Escalation Monitor
Integrates with actual Azure DevOps MCP tools for live monitoring
"""

import json
import requests
import urllib3
from datetime import datetime
import time
import sys

# Disable SSL warnings for corporate networks
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Import MCP tools (these should be available when running in MCP environment)
try:
    # These imports would work when running in the MCP environment
    # For now, we'll handle the import gracefully
    from mcp_tools import (
        mcp_ado_wit_get_query_results_by_id,
        mcp_ado_wit_get_work_items_batch_by_ids
    )
    MCP_AVAILABLE = True
except ImportError:
    print("⚠️  MCP tools not available - using simulation mode")
    MCP_AVAILABLE = False

class ProductionEscalationMonitor:
    def __init__(self):
        self.query_id = "522dd435-3a2f-42af-aeaa-f98cb5a3bedb"
        self.project = "Idu Client-Server"
        
        # Teams webhook URLs - update these with working URLs
        self.webhooks = {
            'atlas': "https://varonis.webhook.office.com/webhookb2/3f90a29c-ae99-4f7d-ba1c-4f352d7da6be@080f3eaf-1e2e-4baf-8c3b-e36006ff4ee8/IncomingWebhook/2bb4e8b8b6264b63a18e68f4d5ef6e83/d6ec199a-488e-4b2c-95fa-86a18f61454a/V2bQywzTQ1eOJXzfb2dXLHgCz9zbzG7xYKYKPWm9Ndhg1",
            'snowflake': "https://varonis.webhook.office.com/webhookb2/3f90a29c-ae99-4f7d-ba1c-4f352d7da6be@080f3eaf-1e2e-4baf-8c3b-e36006ff4ee8/IncomingWebhook/9651f38e23954e45b3d3b67772c8f2bf/d6ec199a-488e-4b2c-95fa-86a18f61454a/V2YVtDu3H6LdpSH9jMqKbsKXnE0kqSbMy_OgklxLWWLek1",
            'salesforce': "https://varonis.webhook.office.com/webhookb2/3f90a29c-ae99-4f7d-ba1c-4f352d7da6be@080f3eaf-1e2e-4baf-8c3b-e36006ff4ee8/IncomingWebhook/c2addaaa96db40eeb4a616c6da4469db/d6ec199a-488e-4b2c-95fa-86a18f61454a/V2aTvdhQ0taYlGNcUz9XoFNo5QCEotax16HSaCJU8KxJw1"
        }
        
        # Service detection patterns
        self.service_patterns = {
            'atlas': {
                'platform_keywords': ['atlas', 'dac'],
                'title_keywords': ['dac', 'data access', 'atlas', 'dashboard', 'file analysis'],
                'description_keywords': ['data access control', 'atlas', 'dac']
            },
            'snowflake': {
                'platform_keywords': ['snowflake'],
                'title_keywords': ['snowflake', 'snow', 'scope template'],
                'description_keywords': ['snowflake', 'snow']
            },
            'salesforce': {
                'platform_keywords': ['salesforce'],
                'title_keywords': ['salesforce', 'sfdc', 'permission set'],
                'description_keywords': ['salesforce', 'sfdc', 'crm']
            }
        }
        
        # State tracking
        self.processed_tickets = set()
        self.last_check_time = None
        self.mcp_available = MCP_AVAILABLE
    
    def get_live_escalations(self):
        """Get live escalation data using real MCP tools or simulation"""
        try:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] 🔄 Fetching escalations from Azure DevOps...")
            
            if self.mcp_available:
                # Use real MCP tools
                return self._get_escalations_via_mcp()
            else:
                # Use simulation for testing
                print("📝 Using simulation mode")
                return self._get_escalations_simulation()
                
        except Exception as e:
            print(f"❌ Error fetching escalations: {e}")
            return None, []
    
    def _get_escalations_via_mcp(self):
        """Get escalations using real MCP tools"""
        # Get query results
        query_response = mcp_ado_wit_get_query_results_by_id(
            id=self.query_id,
            project=self.project
        )
        
        if not query_response or not query_response.get('workItems'):
            return None, []
        
        # Extract work item IDs
        work_item_ids = [item['id'] for item in query_response['workItems']]
        print(f"📊 Found {len(work_item_ids)} escalation work items")
        
        # Get detailed work item information
        detailed_response = mcp_ado_wit_get_work_items_batch_by_ids(
            project=self.project,
            ids=work_item_ids
        )
        
        detailed_tickets = detailed_response.get('value', []) if detailed_response else []
        print(f"📋 Retrieved details for {len(detailed_tickets)} work items")
        
        return query_response, detailed_tickets
    
    def _get_escalations_simulation(self):
        """Simulation for testing without MCP"""
        escalations_data = {
            "queryType": 1,
            "queryResultType": 1,
            "asOf": datetime.now().isoformat() + "Z",
            "workItems": [
                {"id": 2360743}, {"id": 2360167}, {"id": 2360151}, {"id": 2360760}
            ]
        }
        
        detailed_tickets = [
            {
                "id": 2360743,
                "fields": {
                    "System.Id": 2360743,
                    "System.State": "New",
                    "System.Title": "[Ticket #0934994] Salesforce integration failing to add permission set to user @ Interface @ (RSE-US)",
                    "VaronisSupport.SupportTicket.CustomerName": "Interface",
                    "VaronisSupport.SupportTicket.TicketNumber": "0934994",
                    "VaronisSupport.SupportTicket.Platform": "Salesforce",
                    "Microsoft.VSTS.Common.Severity": "2 - High",
                    "System.CreatedDate": datetime.now().isoformat() + "Z"
                }
            },
            {
                "id": 2360167,
                "fields": {
                    "System.Id": 2360167,
                    "System.State": "New",
                    "System.Title": "[Ticket #0934821] Snowflake scope template suddenly missing @ VS Services Company, LLC @ (AMER) @ EVAL",
                    "VaronisSupport.SupportTicket.CustomerName": "VS Services Company, LLC",
                    "VaronisSupport.SupportTicket.TicketNumber": "0934821",
                    "VaronisSupport.SupportTicket.Platform": "Snowflake",
                    "Microsoft.VSTS.Common.Severity": "3 - Medium",
                    "System.CreatedDate": datetime.now().isoformat() + "Z"
                }
            }
        ]
        
        return escalations_data, detailed_tickets
    
    def detect_service(self, ticket):
        """Detect service type with improved accuracy"""
        fields = ticket.get('fields', {})
        
        # Get relevant fields
        title = fields.get('System.Title', '').lower()
        platform = fields.get('VaronisSupport.SupportTicket.Platform', '').lower()
        description = fields.get('System.Description', '').lower()
        
        # Check each service
        for service, patterns in self.service_patterns.items():
            # Priority 1: Platform field match
            if any(keyword in platform for keyword in patterns['platform_keywords']):
                return service
            
            # Priority 2: Title keywords
            if any(keyword in title for keyword in patterns['title_keywords']):
                return service
            
            # Priority 3: Description keywords
            if any(keyword in description for keyword in patterns['description_keywords']):
                return service
        
        return None
    
    def is_new_ticket(self, ticket):
        """Check if ticket should be processed"""
        ticket_id = ticket.get('id')
        
        # Skip if already processed
        if ticket_id in self.processed_tickets:
            return False
        
        fields = ticket.get('fields', {})
        
        # Only process "New" tickets
        if fields.get('System.State', '') != 'New':
            return False
        
        return True
    
    def create_alert_message(self, service, tickets):
        """Create clean Teams alert message"""
        if not tickets:
            return None
        
        service_name = service.title()
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        message = f"New {service_name} ticket detected\n\n"
        message += f"**New {service_name} Tickets**: {len(tickets)} tickets\n"
        message += f"**Report Time**: {current_time}\n\n"
        
        for ticket in tickets:
            fields = ticket.get('fields', {})
            ticket_id = fields.get('System.Id')
            ticket_num = fields.get('VaronisSupport.SupportTicket.TicketNumber', 'Unknown')
            customer = fields.get('VaronisSupport.SupportTicket.CustomerName', 'Unknown')
            severity = fields.get('Microsoft.VSTS.Common.Severity', '')
            
            # Add severity indicator
            severity_indicator = ""
            if '1 -' in severity or 'critical' in severity.lower():
                severity_indicator = " (CRITICAL)"
            elif '2 -' in severity or 'high' in severity.lower():
                severity_indicator = " (HIGH)"
            
            message += f"• **[Ticket #{ticket_num}](https://dev.azure.com/VaronisIO/Idu%20Client-Server/_workitems/edit/{ticket_id})** - {customer}{severity_indicator}\n"
        
        return {"text": message}
    
    def send_alert(self, service, message):
        """Send alert to Teams channel"""
        if service not in self.webhooks:
            print(f"⚠️  No webhook for {service}")
            return False
        
        try:
            response = requests.post(
                self.webhooks[service],
                json=message,
                verify=False,
                timeout=30
            )
            
            if response.status_code == 200:
                print(f"✅ {service.title()} alert sent successfully")
                return True
            else:
                print(f"❌ {service.title()} alert failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Error sending {service} alert: {e}")
            return False
    
    def process_escalations(self):
        """Main processing logic"""
        escalations_data, detailed_tickets = self.get_live_escalations()
        
        if not detailed_tickets:
            print("📭 No tickets to process")
            return 0
        
        # Group new tickets by service
        service_tickets = {}
        unmatched_tickets = []
        new_ticket_count = 0
        
        for ticket in detailed_tickets:
            if not self.is_new_ticket(ticket):
                continue
            
            new_ticket_count += 1
            service = self.detect_service(ticket)
            
            if service:
                if service not in service_tickets:
                    service_tickets[service] = []
                service_tickets[service].append(ticket)
                
                # Log detection
                fields = ticket.get('fields', {})
                ticket_num = fields.get('VaronisSupport.SupportTicket.TicketNumber', 'Unknown')
                print(f"🎯 {service.title()} ticket #{ticket_num} detected")
            else:
                unmatched_tickets.append(ticket)
        
        # Send alerts
        alerts_sent = 0
        for service, tickets in service_tickets.items():
            message = self.create_alert_message(service, tickets)
            if message and self.send_alert(service, message):
                alerts_sent += 1
                # Mark as processed
                for ticket in tickets:
                    self.processed_tickets.add(ticket.get('id'))
        
        # Report unmatched
        if unmatched_tickets:
            print(f"⚠️  {len(unmatched_tickets)} tickets didn't match any service")
        
        print(f"📊 Processed {new_ticket_count} new tickets → {alerts_sent} alerts sent")
        return alerts_sent
    
    def run_single_check(self):
        """Run one monitoring cycle"""
        print("🚀 REAL-TIME ESCALATION MONITOR")
        print("=" * 60)
        print(f"📋 Query: {self.query_id}")
        print(f"🏢 Project: {self.project}")
        print(f"📡 Services: {', '.join(self.service_patterns.keys()).title()}")
        print(f"🔧 MCP Mode: {'Enabled' if self.mcp_available else 'Simulation'}")
        print("=" * 60)
        
        alerts_sent = self.process_escalations()
        
        print("=" * 60)
        if alerts_sent > 0:
            print(f"✅ SUCCESS! {alerts_sent} alerts sent to Teams")
        else:
            print("✅ No new escalations detected")
        print("=" * 60)
        
        return alerts_sent
    
    def run_continuous(self, interval_minutes=5):
        """Run continuous monitoring"""
        print("🔄 Starting continuous monitoring...")
        print(f"⏰ Check interval: {interval_minutes} minutes")
        print("Press Ctrl+C to stop")
        print()
        
        cycle = 0
        try:
            while True:
                cycle += 1
                print(f"🔄 Cycle #{cycle} - {datetime.now().strftime('%H:%M:%S')}")
                
                alerts_sent = self.process_escalations()
                
                if alerts_sent > 0:
                    print(f"🎉 Cycle #{cycle} complete - {alerts_sent} alerts sent")
                else:
                    print(f"✅ Cycle #{cycle} complete - no new escalations")
                
                print(f"😴 Waiting {interval_minutes} minutes...\n")
                time.sleep(interval_minutes * 60)
                
        except KeyboardInterrupt:
            print("🛑 Monitoring stopped by user")

def main():
    monitor = ProductionEscalationMonitor()
    
    if len(sys.argv) > 1 and sys.argv[1] == '--continuous':
        interval = int(sys.argv[2]) if len(sys.argv) > 2 else 5
        monitor.run_continuous(interval)
    else:
        monitor.run_single_check()

if __name__ == "__main__":
    main()
