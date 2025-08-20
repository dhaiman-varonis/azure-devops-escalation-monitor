#!/usr/bin/env python3
"""
Test the Salesforce message format
"""

import json
from datetime import datetime

def create_salesforce_teams_message():
    """Create test Salesforce escalation message for Teams"""
    
    # Sample data
    escalations_summary = {"workItems": [{"id": i} for i in range(10)]}
    
    detailed_tickets = [
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
                "Microsoft.VSTS.Common.Severity": "2 - High",
                "Microsoft.VSTS.Common.Priority": "2",
                "VaronisSupport.SupportTicket.VaronisStatus": "New"
            }
        }
    ]
    
    total_escalations = len(escalations_summary.get('workItems', []))
    current_time = datetime.now()
    
    # Filter for Salesforce-related tickets
    salesforce_tickets = []
    
    for ticket in detailed_tickets:
        fields = ticket.get('fields', {})
        title = fields.get('System.Title', '').lower()
        
        # Check if it's Salesforce-related
        salesforce_keywords = ['salesforce', 'sfdc', 'sf ', 'crm']
        is_salesforce = any(keyword in title for keyword in salesforce_keywords)
        
        if is_salesforce:
            salesforce_tickets.append(ticket)
    
    # Build message focusing on Salesforce tickets
    current_time_str = current_time.strftime('%Y-%m-%d %H:%M:%S')
    
    # Filter new Salesforce tickets (those in "New" state)
    new_salesforce_tickets = [t for t in salesforce_tickets if t.get('fields', {}).get('System.State', '') == 'New']
    
    alert_level = "NEW SALESFORCE ESCALATIONS DETECTED!" if new_salesforce_tickets else "SALESFORCE MONITORING - ALL CLEAR"
    
    message_text = f"{alert_level}\n\n"
    
    # Quick summary
    message_text += f"**SALESFORCE MONITORING REPORT**\n"
    message_text += f"• **New Salesforce Tickets**: {len(new_salesforce_tickets)} tickets\n"
    message_text += f"• **Active Salesforce**: {len(salesforce_tickets)} total\n"
    message_text += f"• **Total Escalations**: {total_escalations}\n"
    message_text += f"• **Report Time**: {current_time_str}\n\n"
    
    # Show new Salesforce tickets first
    if new_salesforce_tickets:
        message_text += f"**NEW SALESFORCE ESCALATIONS**\n\n"
        
        for ticket in new_salesforce_tickets:
            fields = ticket.get('fields', {})
            ticket_id = fields.get('System.Id')
            title = fields.get('System.Title', '')
            assignee = fields.get('System.AssignedTo', 'Unassigned').split('<')[0].strip()
            customer = fields.get('VaronisSupport.SupportTicket.CustomerName', 'Unknown')
            ticket_num = fields.get('VaronisSupport.SupportTicket.TicketNumber', 'Unknown')
            severity = fields.get('Microsoft.VSTS.Common.Severity', 'Unknown')
            priority = fields.get('Microsoft.VSTS.Common.Priority', '4')
            
            # Determine priority text based on severity and priority
            if '1 -' in severity or priority == '1':
                priority_text = "CRITICAL"
            elif '2 -' in severity or priority == '2':
                priority_text = "HIGH"
            else:
                priority_text = "NEW"
            
            # Extract issue type from title
            issue_type = "Integration Issue"
            if "permission" in title.lower():
                issue_type = "Permission Management"
            elif "authentication" in title.lower() or "timeout" in title.lower():
                issue_type = "Authentication/Connection"
            elif "data" in title.lower() or "sync" in title.lower():
                issue_type = "Data Processing"
            
            message_text += f"**#{ticket_num}** - {priority_text}\n"
            message_text += f"• **Customer**: {customer}\n"
            message_text += f"• **Issue**: {issue_type}\n"
            message_text += f"• **Assigned**: {assignee}\n"
            message_text += f"• [View Ticket](https://dev.azure.com/VaronisIO/Idu%20Client-Server/_workitems/edit/{ticket_id})\n\n"
    
    # Quick actions for new tickets
    if new_salesforce_tickets:
        message_text += f"**IMMEDIATE ACTIONS NEEDED**:\n"
        critical_new = [t for t in new_salesforce_tickets if '1 -' in t.get('fields', {}).get('Microsoft.VSTS.Common.Severity', '')]
        high_new = [t for t in new_salesforce_tickets if '2 -' in t.get('fields', {}).get('Microsoft.VSTS.Common.Severity', '')]
        
        if critical_new:
            message_text += f"• **URGENT**: {len(critical_new)} critical Salesforce ticket(s) need immediate attention\n"
        if high_new:
            message_text += f"• **HIGH**: {len(high_new)} high priority Salesforce ticket(s) require handling\n"
        
        message_text += f"• **CONTACT**: Reach out to affected customers\n"
        message_text += f"• **INVESTIGATE**: Check Salesforce connector status\n\n"
    
    # Footer for monitoring
    message_text += f"---\n"
    message_text += f"**Automated Salesforce Monitor** | **Real-time Azure DevOps data**\n"
    message_text += f"[Live Query](https://dev.azure.com/VaronisIO/Idu%20Client-Server/_queries/query/522dd435-3a2f-42af-aeaa-f98cb5a3bedb/)"
    
    return {"text": message_text}

if __name__ == "__main__":
    message = create_salesforce_teams_message()
    print("SALESFORCE TEAMS MESSAGE:")
    print("=" * 60)
    print(message['text'])
    print("=" * 60)
