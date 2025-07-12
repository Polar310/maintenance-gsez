#import schedule
import time
from datetime import datetime
from email_agent import send_daily_report

def run_daily_report():
    """Function to run the daily report"""
    print(f"🕘 Running daily report at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    success = send_daily_report()
    if success:
        print("✅ Daily report completed successfully")
    else:
        print("❌ Daily report failed")

def main():
    """Main function to schedule and run the daily report"""
    print("🚀 Starting daily report scheduler...")
    print("📅 Daily reports will be sent at 9:00 PM every day")
    
    # Schedule the daily report at 9 PM
    schedule.every().day.at("21:00").do(run_daily_report)
    
    # Also run once immediately for testing (comment out in production)
    # run_daily_report()
    
    print("⏰ Scheduler is running. Press Ctrl+C to stop.")
    
    # Keep the script running
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Scheduler stopped by user")
    except Exception as e:
        print(f"❌ Scheduler error: {e}") 