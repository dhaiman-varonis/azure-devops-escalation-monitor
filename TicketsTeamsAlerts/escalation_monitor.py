#!/usr/bin/env python3
"""
Real-time Escalation Monitor with Azure DevOps MCP Integration
This version uses actual Azure DevOps MCP calls to fetch live data
"""

import json
import requests
import urllib3
from datetime import datetime
import time
import sys

# Disable SSL warnings for corporate networks
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class RealTimeEscalationMonitor:
    def __init__(self):
        self.query_id = "522dd435-3a2f-42af-aeaa-f98cb5a3bedb"
        self.project = "Idu Client-Server"
        
        # Teams webhook URLs for different services - Updated with new working URLs
        self.webhooks = {
            'atlas': "https://varonis.webhook.office.com/webhookb2/3f90a29c-ae99-4f7d-ba1c-4f352d7da6be@080f3eaf-1e2e-4baf-8c3b-e36006ff4ee8/IncomingWebhook/ffd2fa48eb78405b8f41d1650d9c9b45/d6ec199a-488e-4b2c-95fa-86a18f61454a/V2V-fEl6OriwSiSXr6fx--Vcl1wg0hfIYKbJg7COp82HI1",
            'snowflake': "https://varonis.webhook.office.com/webhookb2/3f90a29c-ae99-4f7d-ba1c-4f352d7da6be@080f3eaf-1e2e-4baf-8c3b-e36006ff4ee8/IncomingWebhook/785cf0f989ed4701aa1fb9237ee0b38b/d6ec199a-488e-4b2c-95fa-86a18f61454a/V28e8EsdJsyeD_bvOW-RSngNGFSAiZ3B38Rfa2ivEY71k1",
            'salesforce': "https://varonis.webhook.office.com/webhookb2/3f90a29c-ae99-4f7d-ba1c-4f352d7da6be@080f3eaf-1e2e-4baf-8c3b-e36006ff4ee8/IncomingWebhook/c2addaaa96db40eeb4a616c6da4469db/d6ec199a-488e-4b2c-95fa-86a18f61454a/V2aTvdhQ0taYlGNcUz9XoFNo5QCEotax16HSaCJU8KxJw1"
        }
        
        # Service detection patterns - Platform-based only
        self.service_patterns = {
            'atlas': {
                'platform_matches': ['mongodb', 'mongo']
            },
            'snowflake': {
                'platform_matches': ['snowflake']
            },
            'salesforce': {
                'platform_matches': ['salesforce']
            }
        }
        
        # Track processed tickets to avoid duplicates
        self.processed_tickets = set()
        self.last_check_time = None
    
    def get_live_escalations_mcp(self):
        """
        Get live escalation data from Azure DevOps using MCP tools
        """
        try:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Fetching live escalations from Azure DevOps...")
            
            # Import MCP tools - these should be available in MCP environment
            try:
                from mcp_ado_wit_get_query_results_by_id import mcp_ado_wit_get_query_results_by_id
                from mcp_ado_wit_get_work_items_batch_by_ids import mcp_ado_wit_get_work_items_batch_by_ids
            except ImportError:
                if not self.mcp_available:
                    print("❌ MCP tools not available - this script requires MCP environment")
                    print("💡 For testing without MCP, use: python test_escalation_monitor.py")
                    return []
            
            # Get query results
            query_response = mcp_ado_wit_get_query_results_by_id(
                id=self.query_id,
                project=self.project
            )
            
            if not query_response or not query_response.get('workItems'):
                print("No escalations found or query failed")
                return None, []
            
            work_item_ids = [item['id'] for item in query_response['workItems']]
            print(f"Found {len(work_item_ids)} escalation work items")
            
            # Get detailed work item information
            detailed_response = mcp_ado_wit_get_work_items_batch_by_ids(
                project=self.project,
                ids=work_item_ids
            )
            
            detailed_tickets = detailed_response.get('value', []) if detailed_response else []
            print(f"Retrieved details for {len(detailed_tickets)} work items")
            
            return query_response, detailed_tickets
            
        except Exception as e:
            print(f"Error fetching escalations: {e}")
            return None, []
    
    def detect_service_type(self, ticket):
        """Platform-based service detection only"""
        fields = ticket.get('fields', {})
        
        platform = fields.get('VaronisSupport.SupportTicket.Platform', '').lower()
        
        # Check each service pattern - platform field only
        for service, patterns in self.service_patterns.items():
            if any(platform_match in platform for platform_match in patterns['platform_matches']):
                return service
        
        return None
    
    def is_new_ticket(self, ticket):
        """Check if this is a new ticket we haven't processed"""
        ticket_id = ticket.get('id')
        fields = ticket.get('fields', {})
        
        # Skip if already processed
        if ticket_id in self.processed_tickets:
            return False
        
        # Only process tickets in "New" state
        if fields.get('System.State', '') != 'New':
            return False
        
        # If we have a last check time, only process tickets created after that
        if self.last_check_time:
            created_date_str = fields.get('System.CreatedDate', '')
            if created_date_str:
                try:
                    created_date = datetime.fromisoformat(created_date_str.replace('Z', '+00:00'))
                    if created_date <= self.last_check_time:
                        return False
                except:
                    pass  # If date parsing fails, process the ticket anyway
        
        return True
    
    def create_service_alert(self, service, tickets):
        """Create clean Teams alert for specific service"""
        if not tickets:
            return None
        
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        service_name = service.title()
        
        message_text = f"New {service_name} ticket detected\n\n"
        message_text += f"**New {service_name} Tickets**: {len(tickets)} tickets\n"
        message_text += f"**Report Time**: {current_time}\n\n"
        
        # List each ticket
        for ticket in tickets:
            fields = ticket.get('fields', {})
            ticket_id = fields.get('System.Id')
            ticket_num = fields.get('VaronisSupport.SupportTicket.TicketNumber', 'Unknown')
            customer = fields.get('VaronisSupport.SupportTicket.CustomerName', 'Unknown')
            severity = fields.get('Microsoft.VSTS.Common.Severity', '')
            
            severity_text = ""
            if '1 -' in severity or 'critical' in severity.lower():
                severity_text = " (CRITICAL)"
            elif '2 -' in severity or 'high' in severity.lower():
                severity_text = " (HIGH)"
            
            message_text += f"• **[Ticket #{ticket_num}](https://dev.azure.com/VaronisIO/Idu%20Client-Server/_workitems/edit/{ticket_id})** - {customer}{severity_text}\n"
        
        return {"text": message_text}
    
    def send_service_alert(self, service, message):
        """Send alert to appropriate Teams channel"""
        if service not in self.webhooks:
            print(f"⚠️  No webhook configured for service: {service}")
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
                print(f"✅ Alert sent to {service.title()} Teams channel")
                return True
            else:
                print(f"❌ Failed to send {service} alert. Status: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Error sending {service} alert: {e}")
            return False
    
    def process_escalations(self):
        """Main processing logic"""
        escalations_data, detailed_tickets = self.get_live_escalations_mcp()
        
        if not detailed_tickets:
            print("No tickets to process")
            return 0
        
        # Process each ticket
        new_tickets_by_service = {}
        unmatched_new_tickets = []
        processed_count = 0
        
        for ticket in detailed_tickets:
            if not self.is_new_ticket(ticket):
                continue
            
            processed_count += 1
            service = self.detect_service_type(ticket)
            
            if service:
                if service not in new_tickets_by_service:
                    new_tickets_by_service[service] = []
                new_tickets_by_service[service].append(ticket)
                
                # Log detection
                fields = ticket.get('fields', {})
                ticket_num = fields.get('VaronisSupport.SupportTicket.TicketNumber', 'Unknown')
                title = fields.get('System.Title', '')[:50]
                print(f"🎯 Detected {service.title()} ticket #{ticket_num}: {title}...")
            else:
                unmatched_new_tickets.append(ticket)
        
        # Send alerts for each service
        alerts_sent = 0
        for service, tickets in new_tickets_by_service.items():
            message = self.create_service_alert(service, tickets)
            if message and self.send_service_alert(service, message):
                alerts_sent += 1
                # Mark tickets as processed
                for ticket in tickets:
                    self.processed_tickets.add(ticket.get('id'))
        
        # Log unmatched tickets
        if unmatched_new_tickets:
            print(f"⚠️  {len(unmatched_new_tickets)} new tickets didn't match any service pattern:")
            for ticket in unmatched_new_tickets:
                fields = ticket.get('fields', {})
                ticket_num = fields.get('VaronisSupport.SupportTicket.TicketNumber', 'Unknown')
                title = fields.get('System.Title', '')[:50]
                print(f"   - #{ticket_num}: {title}...")
        
        # Update last check time
        self.last_check_time = datetime.now()
        
        print(f"📊 Processed {processed_count} new tickets, sent {alerts_sent} service alerts")
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
    """Main execution function"""
    monitor = RealTimeEscalationMonitor()
    
    # Check for continuous mode
    if len(sys.argv) > 1 and sys.argv[1] == '--continuous':
        interval = int(sys.argv[2]) if len(sys.argv) > 2 else 5
        monitor.run_continuous(interval)
        return
    
    # Single check mode
    print("🚀 REAL-TIME ESCALATION MONITOR")
    print("=" * 50)
    print("📋 Query ID:", monitor.query_id)
    print("🏢 Project:", monitor.project)
    print("📡 Services:", ", ".join(monitor.service_patterns.keys()).title())
    print("=" * 50)
    
    # Run single check
    alerts_sent = monitor.process_escalations()
    
    print("=" * 50)
    if alerts_sent > 0:
        print(f"✅ SUCCESS! Sent {alerts_sent} service-specific alerts")
    else:
        print("✅ SUCCESS! No new escalations detected")
    print("=" * 50)

if __name__ == "__main__":
    main()
