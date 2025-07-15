#!/usr/bin/env python3
"""
Test script for the daily scheduler
Run this to test if the daily report function works
"""

from email_agent import send_daily_report
from datetime import datetime

def test_daily_report():
    """Test the daily report function"""
    print(f"🧪 Testing daily report at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        success = send_daily_report()
        if success:
            print("✅ Daily report test completed successfully!")
        else:
            print("❌ Daily report test failed!")
        return success
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False

if __name__ == "__main__":
    test_daily_report() 