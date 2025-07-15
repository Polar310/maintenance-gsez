#!/usr/bin/env python3
"""
Simple script to run the daily scheduler
This will start the scheduler and keep it running
"""

import schedule
import time
from datetime import datetime
from email_agent import send_daily_report
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scheduler.log'),
        logging.StreamHandler()
    ]
)

def run_daily_report():
    """Function to run the daily report"""
    logging.info(f"🕘 Running daily report at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    success = send_daily_report()
    if success:
        logging.info("✅ Daily report completed successfully")
    else:
        logging.error("❌ Daily report failed")
    return success

def main():
    """Main function to schedule and run the daily report"""
    logging.info("🚀 Starting daily report scheduler...")
    logging.info("📅 Daily reports will be sent at 9:00 PM every day")
    
    # Schedule the daily report at 9 PM
    schedule.every().day.at("21:00").do(run_daily_report)
    
    # For testing: also run every 5 minutes (comment out in production)
    # schedule.every(5).minutes.do(run_daily_report)
    
    logging.info("⏰ Scheduler is running. Press Ctrl+C to stop.")
    
    # Keep the script running
    while True:
        try:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            logging.info("\n🛑 Scheduler stopped by user")
            break
        except Exception as e:
            logging.error(f"❌ Scheduler error: {e}")
            time.sleep(60)  # Wait before retrying

if __name__ == "__main__":
    main() 