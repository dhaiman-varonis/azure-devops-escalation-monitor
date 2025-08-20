#!/usr/bin/env python3
"""
Teams Message Generator for Azure DevOps Tickets
Generates formatted Teams messages with ticket details from Azure DevOps
"""

import json
from typing import Dict, List, Any
from datetime import datetime


class TeamsMessageGenerator:
    """Generate Teams messages for Azure DevOps tickets."""
    
    def __init__(self):
        self.base_url = "https://dev.azure.com/VaronisIO"
    
    def format_ticket_for_teams(self, ticket: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format a single ticket for Teams message.
        
        Args:
            ticket: Ticket data from Azure DevOps search results
            
        Returns:
            Formatted Teams message payload
        """
        fields = ticket.get("fields", {})
        
        # Extract key information
        ticket_id = fields.get("system.id", "Unknown")
        title = fields.get("system.title", "No title")
        work_item_type = fields.get("system.workitemtype", "Unknown")
        state = fields.get("system.state", "Unknown")
        assigned_to = fields.get("system.assignedto", "Unassigned")
        created_date = fields.get("system.createddate", "")
        changed_date = fields.get("system.changeddate", "")
        
        # Format dates
        created_str = self._format_date(created_date) if created_date else "Unknown"
        changed_str = self._format_date(changed_date) if changed_date else "Unknown"
        
        # Get ticket URL
        ticket_url = f"{self.base_url}/Idu%20Client-Server/_workitems/edit/{ticket_id}"
        
        # Create Teams adaptive card
        teams_message = {
            "type": "message",
            "attachments": [
                {
                    "contentType": "application/vnd.microsoft.card.adaptive",
                    "content": {
                        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                        "type": "AdaptiveCard",
                        "version": "1.4",
                        "body": [
                            {
                                "type": "TextBlock",
                                "text": f"🎫 {work_item_type} #{ticket_id}",
                                "weight": "Bolder",
                                "size": "Medium",
                                "color": self._get_type_color(work_item_type)
                            },
                            {
                                "type": "TextBlock",
                                "text": title,
                                "weight": "Bolder",
                                "wrap": True
                            },
                            {
                                "type": "FactSet",
                                "facts": [
                                    {
                                        "title": "Status:",
                                        "value": state
                                    },
                                    {
                                        "title": "Assigned To:",
                                        "value": assigned_to
                                    },
                                    {
                                        "title": "Created:",
                                        "value": created_str
                                    },
                                    {
                                        "title": "Last Updated:",
                                        "value": changed_str
                                    }
                                ]
                            }
                        ],
                        "actions": [
                            {
                                "type": "Action.OpenUrl",
                                "title": "View in Azure DevOps",
                                "url": ticket_url
                            }
                        ]
                    }
                }
            ]
        }
        
        return teams_message
    
    def format_multiple_tickets_for_teams(self, tickets: List[Dict[str, Any]], 
                                         title: str = "Azure DevOps Tickets") -> Dict[str, Any]:
        """
        Format multiple tickets for Teams message.
        
        Args:
            tickets: List of ticket data from Azure DevOps
            title: Title for the message
            
        Returns:
            Formatted Teams message payload
        """
        if not tickets:
            return {
                "type": "message",
                "attachments": [
                    {
                        "contentType": "application/vnd.microsoft.card.adaptive",
                        "content": {
                            "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                            "type": "AdaptiveCard",
                            "version": "1.4",
                            "body": [
                                {
                                    "type": "TextBlock",
                                    "text": "No tickets found",
                                    "weight": "Bolder",
                                    "size": "Medium"
                                }
                            ]
                        }
                    }
                ]
            }
        
        # Create summary
        body_elements = [
            {
                "type": "TextBlock",
                "text": f"📋 {title}",
                "weight": "Bolder",
                "size": "Large"
            },
            {
                "type": "TextBlock",
                "text": f"Found {len(tickets)} ticket(s)",
                "isSubtle": True
            }
        ]
        
        # Add each ticket as a container
        for ticket in tickets[:10]:  # Limit to 10 tickets to avoid message size limits
            fields = ticket.get("fields", {})
            ticket_id = fields.get("system.id", "Unknown")
            title_text = fields.get("system.title", "No title")
            work_item_type = fields.get("system.workitemtype", "Unknown")
            state = fields.get("system.state", "Unknown")
            assigned_to = fields.get("system.assignedto", "Unassigned")
            
            ticket_url = f"{self.base_url}/Idu%20Client-Server/_workitems/edit/{ticket_id}"
            
            body_elements.append({
                "type": "Container",
                "style": "emphasis",
                "items": [
                    {
                        "type": "ColumnSet",
                        "columns": [
                            {
                                "type": "Column",
                                "width": "stretch",
                                "items": [
                                    {
                                        "type": "TextBlock",
                                        "text": f"**{work_item_type} #{ticket_id}**",
                                        "weight": "Bolder"
                                    },
                                    {
                                        "type": "TextBlock",
                                        "text": title_text,
                                        "wrap": True
                                    },
                                    {
                                        "type": "TextBlock",
                                        "text": f"Status: {state} | Assigned: {assigned_to}",
                                        "isSubtle": True,
                                        "size": "Small"
                                    }
                                ]
                            },
                            {
                                "type": "Column",
                                "width": "auto",
                                "items": [
                                    {
                                        "type": "ActionSet",
                                        "actions": [
                                            {
                                                "type": "Action.OpenUrl",
                                                "title": "View",
                                                "url": ticket_url
                                            }
                                        ]
                                    }
                                ]
                            }
                        ]
                    }
                ]
            })
        
        if len(tickets) > 10:
            body_elements.append({
                "type": "TextBlock",
                "text": f"... and {len(tickets) - 10} more tickets",
                "isSubtle": True
            })
        
        return {
            "type": "message",
            "attachments": [
                {
                    "contentType": "application/vnd.microsoft.card.adaptive",
                    "content": {
                        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                        "type": "AdaptiveCard",
                        "version": "1.4",
                        "body": body_elements
                    }
                }
            ]
        }
    
    def _format_date(self, date_str: str) -> str:
        """Format ISO date string to readable format."""
        try:
            dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            return dt.strftime("%Y-%m-%d %H:%M")
        except:
            return date_str
    
    def _get_type_color(self, work_item_type: str) -> str:
        """Get color based on work item type."""
        colors = {
            "Bug": "Attention",
            "Task": "Good",
            "Feature": "Accent",
            "User Story": "Good",
            "Epic": "Warning",
            "Product Backlog Item": "Good"
        }
        return colors.get(work_item_type, "Default")


def format_atlas_tickets_for_teams(atlas_search_results: Dict[str, Any]) -> str:
    """
    Format Atlas search results for Teams message.
    
    Args:
        atlas_search_results: Results from Azure DevOps search
        
    Returns:
        JSON string of formatted Teams message
    """
    generator = TeamsMessageGenerator()
    tickets = atlas_search_results.get("results", [])
    
    message = generator.format_multiple_tickets_for_teams(
        tickets, 
        "🔍 Atlas-Related Tickets"
    )
    
    return json.dumps(message, indent=2)


# Example usage
if __name__ == "__main__":
    # Example Atlas ticket data (this would come from your Azure DevOps search)
    example_ticket = {
        "fields": {
            "system.id": "2300240",
            "system.workitemtype": "Task",
            "system.title": "Add Atlas Filer to RTA",
            "system.assignedto": "Matti Ben-Avraham <mbenavraham@varonis.com>",
            "system.state": "Closed",
            "system.createddate": "2025-07-01T12:33:51.9130000Z",
            "system.changeddate": "2025-08-13T04:41:32.9330000Z"
        }
    }
    
    generator = TeamsMessageGenerator()
    
    # Generate single ticket message
    single_message = generator.format_ticket_for_teams(example_ticket)
    print("Single Ticket Message:")
    print(json.dumps(single_message, indent=2))
    
    # Generate multiple tickets message
    multiple_message = generator.format_multiple_tickets_for_teams(
        [example_ticket], 
        "Atlas Tickets Update"
    )
    print("\nMultiple Tickets Message:")
    print(json.dumps(multiple_message, indent=2))
