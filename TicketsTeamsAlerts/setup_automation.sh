#!/bin/bash

# Salesforce Escalation Monitor - Automation Setup
# This script helps set up automated monitoring for Salesforce escalations

echo "☁️ SALESFORCE ESCALATION MONITOR - AUTOMATION SETUP"
echo "=================================================="
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/salesforce_escalations.py"
VENV_PYTHON="$SCRIPT_DIR/.venv/bin/python"

echo "📁 Script Directory: $SCRIPT_DIR"
echo "🐍 Python Script: $PYTHON_SCRIPT"
echo "🔧 Virtual Environment: $VENV_PYTHON"
echo ""

# Check if the Python script exists
if [ ! -f "$PYTHON_SCRIPT" ]; then
    echo "❌ Error: salesforce_escalations.py not found!"
    exit 1
fi

# Check if virtual environment exists
if [ ! -f "$VENV_PYTHON" ]; then
    echo "❌ Error: Virtual environment not found!"
    echo "💡 Run: python -m venv .venv && source .venv/bin/activate && pip install requests"
    exit 1
fi

echo "✅ All files found. Setting up automation options..."
echo ""

echo "🤖 AUTOMATION OPTIONS:"
echo ""
echo "1️⃣  CRON JOB (Every 15 minutes)"
echo "   Add this line to your crontab (run: crontab -e):"
echo "   */15 * * * * $VENV_PYTHON $PYTHON_SCRIPT >> $SCRIPT_DIR/monitor.log 2>&1"
echo ""

echo "2️⃣  CRON JOB (Every hour)"
echo "   Add this line to your crontab (run: crontab -e):"
echo "   0 * * * * $VENV_PYTHON $PYTHON_SCRIPT >> $SCRIPT_DIR/monitor.log 2>&1"
echo ""

echo "3️⃣  CRON JOB (Business hours only - 9 AM to 6 PM, weekdays)"
echo "   Add this line to your crontab (run: crontab -e):"
echo "   */15 9-18 * * 1-5 $VENV_PYTHON $PYTHON_SCRIPT >> $SCRIPT_DIR/monitor.log 2>&1"
echo ""

echo "4️⃣  MANUAL SETUP CRON"
read -p "Would you like to add a cron job now? (y/n): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "📝 Choose monitoring frequency:"
    echo "1) Every 15 minutes (recommended for active monitoring)"
    echo "2) Every hour (lighter monitoring)"  
    echo "3) Business hours only (9 AM - 6 PM, weekdays)"
    echo ""
    read -p "Enter choice (1-3): " freq_choice
    
    case $freq_choice in
        1)
            CRON_SCHEDULE="*/15 * * * *"
            DESCRIPTION="every 15 minutes"
            ;;
        2)
            CRON_SCHEDULE="0 * * * *"
            DESCRIPTION="every hour"
            ;;
        3)
            CRON_SCHEDULE="*/15 9-18 * * 1-5"
            DESCRIPTION="every 15 minutes during business hours (9 AM - 6 PM, weekdays)"
            ;;
        *)
            echo "❌ Invalid choice. Exiting."
            exit 1
            ;;
    esac
    
    CRON_LINE="$CRON_SCHEDULE $VENV_PYTHON $PYTHON_SCRIPT >> $SCRIPT_DIR/monitor.log 2>&1"
    
    echo ""
    echo "📋 Adding cron job: $DESCRIPTION"
    echo "🔧 Command: $CRON_LINE"
    echo ""
    
    # Add to crontab
    (crontab -l 2>/dev/null; echo "$CRON_LINE") | crontab -
    
    if [ $? -eq 0 ]; then
        echo "✅ Cron job added successfully!"
        echo "📊 Monitor will run $DESCRIPTION"
        echo "📝 Logs will be saved to: $SCRIPT_DIR/monitor.log"
        echo ""
        echo "🔍 To view current cron jobs: crontab -l"
        echo "📜 To view logs: tail -f $SCRIPT_DIR/monitor.log"
        echo "❌ To remove cron job: crontab -e (and delete the line)"
    else
        echo "❌ Failed to add cron job. You may need to add it manually."
    fi
fi

echo ""
echo "5️⃣  TEST RUN"
read -p "Would you like to test the monitor now? (y/n): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "🧪 Running test..."
    $VENV_PYTHON $PYTHON_SCRIPT
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "📚 USEFUL COMMANDS:"
echo "   View cron jobs:     crontab -l"
echo "   Edit cron jobs:     crontab -e"
echo "   View monitor logs:  tail -f $SCRIPT_DIR/monitor.log"
echo "   Test manually:      $VENV_PYTHON $PYTHON_SCRIPT"
echo ""
echo "🎉 Your Salesforce escalation monitor is ready!"
echo "💡 The monitor will now automatically check for new Salesforce escalations"
echo "   and send alerts to your Teams channel when new tickets are detected."
