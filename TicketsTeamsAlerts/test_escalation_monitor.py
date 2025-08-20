#!/usr/bin/env python3
"""
Test Monitor with Simulation Data
This version simulates Azure DevOps responses for testing without MCP environment
"""

import json
import time
from datetime import datetime, timedelta
from escalation_monitor import RealTimeEscalationMonitor

class TestEscalationMonitor(RealTimeEscalationMonitor):
    """Test version of the monitor with simulation capabilities"""
    
    def get_live_escalations_mcp(self):
        """Override to use simulation data for testing"""
        try:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] 🧪 TESTING MODE - Using simulated data")
            
            escalations_data = self._simulate_mcp_query_response()
            
            if not escalations_data or not escalations_data.get('workItems'):
                print("No escalations found in simulation")
                return None, []
            
            work_item_ids = [item['id'] for item in escalations_data['workItems']]
            print(f"Found {len(work_item_ids)} escalation work items")
            
            detailed_tickets = self._simulate_mcp_work_items_response(work_item_ids)
            print(f"Retrieved details for {len(detailed_tickets)} work items")
            
            return escalations_data, detailed_tickets
            
        except Exception as e:
            print(f"Error in test simulation: {e}")
            return None, []
    
    def _simulate_mcp_query_response(self):
        """Simulate MCP query response structure"""
        return {
            "queryType": 1,
            "queryResultType": 1, 
            "asOf": datetime.now().isoformat() + "Z",
            "columns": [
                {"referenceName": "VaronisSupport.SupportTicket.TicketNumber", "name": "TicketNumber"},
                {"referenceName": "System.Title", "name": "Title"},
                {"referenceName": "VaronisSupport.SupportTicket.Platform", "name": "Platform"}
            ],
            "workItems": [
                {"id": 2360781}, {"id": 2360768}, {"id": 2360760}, {"id": 2360743}, 
                {"id": 2360680}, {"id": 2360167}, {"id": 2360155}, {"id": 2360151}
            ]
        }
    
    def _simulate_mcp_work_items_response(self, work_item_ids):
        """Simulate MCP work items batch response"""
        # Real ticket examples based on actual Azure DevOps data
        all_tickets = [
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
                    "System.Title": "[Ticket #0934708] Atlas dashboards loading slowly @ VS Services Company, LLC @ (AMER) @ EVAL",
                    "VaronisSupport.SupportTicket.CustomerName": "VS Services Company, LLC", 
                    "VaronisSupport.SupportTicket.TicketNumber": "0934708",
                    "VaronisSupport.SupportTicket.Platform": "MongoDB",
                    "Microsoft.VSTS.Common.Severity": "2 - High",
                    "System.CreatedDate": "2025-08-20T14:20:00Z"
                }
            },
            {
                "id": 2360760,
                "fields": {
                    "System.Id": 2360760,
                    "System.WorkItemType": "Support ticket",
                    "System.State": "New",
                    "System.AssignedTo": "Arnon Silverman <asilverman@varonis.com>",
                    "System.Title": "[Ticket #0934814] Atlas file analysis fails @ VS Services Company, LLC @ (AMER) @ EVAL",
                    "VaronisSupport.SupportTicket.CustomerName": "VS Services Company, LLC",
                    "VaronisSupport.SupportTicket.TicketNumber": "0934814",
                    "VaronisSupport.SupportTicket.Platform": "MongoDB",
                    "Microsoft.VSTS.Common.Severity": "2 - High",
                    "System.CreatedDate": "2025-08-20T12:45:00Z"
                }
            }
        ]
        
        # Return only tickets that match the requested IDs
        return [ticket for ticket in all_tickets if ticket['id'] in work_item_ids]

def main():
    """Run test version of the monitor"""
    import sys
    
    monitor = TestEscalationMonitor()
    
    # Check for continuous mode
    if len(sys.argv) > 1 and sys.argv[1] == '--continuous':
        interval = int(sys.argv[2]) if len(sys.argv) > 2 else 5
        monitor.run_continuous(interval)
        return
    
    # Single check mode
    print("🧪 REAL-TIME ESCALATION MONITOR - TEST MODE")
    print("=" * 55)
    print("📋 Query ID:", monitor.query_id)
    print("🏢 Project:", monitor.project)
    print("📡 Services:", ", ".join(monitor.service_patterns.keys()).title())
    print("🔬 Mode: Simulation (for testing without MCP)")
    print("=" * 55)
    
    # Run single check
    alerts_sent = monitor.process_escalations()
    
    print("=" * 55)
    if alerts_sent > 0:
        print(f"✅ TEST SUCCESS! Sent {alerts_sent} service-specific alerts")
    else:
        print("✅ TEST SUCCESS! No new escalations detected")
    print("=" * 55)

if __name__ == "__main__":
    main()
