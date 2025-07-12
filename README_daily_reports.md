# Daily Maintenance Reports

## Overview

The daily report system automatically sends an email at 9:00 PM every day with a summary of all vehicles that have critical issues (❌) in the following fields:

- Coolant
- Battery Condition
- Engine Oil

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Scheduler

To start the daily report scheduler:

```bash
python daily_scheduler.py
```

The scheduler will:

- Run continuously in the background
- Send daily reports at 9:00 PM every day
- Log all activities to the console

### 3. Test the Daily Report

You can test the daily report manually by:

1. Running the Streamlit app: `streamlit run app.py`
2. Going to the "Admin Tools" section at the bottom
3. Clicking "📊 Send Daily Report (Test)"

## Email Content

The daily report email includes:

- Summary of total entries for the day
- List of vehicles with critical issues
- Specific issues for each vehicle
- Timestamp of when issues were reported
- Link to the full maintenance spreadsheet

## Production Deployment

For production deployment, consider:

1. Using a service like `systemd` (Linux) or `launchd` (macOS) to keep the scheduler running
2. Setting up proper logging
3. Adding error notifications
4. Using environment variables for sensitive data

## Example Email

```
📊 Daily Maintenance Report - 2024-01-15

📈 Summary:
- Total entries today: 25
- Vehicles with critical issues: 3

🚨 Vehicles with Critical Issues:

🛻 Vehicle: AM500IT
❗ Issues: Coolant, Engine Oil
🕒 Time: 2024-01-15 14:30:22

🛻 Vehicle: WA470-3
❗ Issues: Battery Condition
🕒 Time: 2024-01-15 16:45:10

📋 Full maintenance log:
https://docs.google.com/spreadsheets/d/17pmwdqIlq1ws_M2paN81TlIbPn-3TKpp5M3mBi9NIXY/edit?usp=sharing

---
This is an automated daily report from the ARISE Maintenance System.
```
