import smtplib 
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import gspread 
from datetime import datetime, timedelta
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import io
import base64

#set google sheets 
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)
sheet = client.open("Maintenance Logs").sheet1

def send_alert_email(vehicle,issues,timestamp): 
    sender = "gsezmaintenance.alerts@gmail.com"
    receiver = "gsezmaintenance.alerts@gmail.com"
    app_password = "srtqffxswhbgautt"
    
    subject = f"Maintenance Alert - {vehicle}"
    body = f"""
    🔧 Critical issue has occured
     
    🛻 Vehicle: {vehicle}
    🕒 Time: {timestamp}
    ❗ Issues: {', '.join(issues)}
    
    here is the link to the maintenance log: 
    https://docs.google.com/spreadsheets/d/17pmwdqIlq1ws_M2paN81TlIbPn-3TKpp5M3mBi9NIXY/edit?usp=sharing
    """
    
    message = MIMEMultipart()
    message["From"] = sender
    message["To"] = receiver
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))
    
    try: 
        with smtplib.SMTP("smtp.gmail.com", 587) as server: 
            server.starttls()
            server.login(sender, app_password)
            server.send_message(message)
        print("✅ Alert email sent.")
    
    except Exception as e: 
        print("❌ Failed to send email:", e)

def send_daily_report():
    """
    Send daily report of all vehicles with critical issues (❌) and warnings (⚠️) in Coolant, Battery Condition, and Engine Oil
    """
    try:
        # Get all data from the sheet
        all_data = sheet.get_all_records()
        
        # Define critical fields to check
        critical_fields = ["Coolant", "Battery Condition", "Engine Oil"]
        
        # Find vehicles with critical issues (❌) from ALL data
        critical_vehicles = []
        warning_vehicles = []
        
        for row in all_data:
            vehicle = row.get('Vehicle/equipment_NO', 'Unknown')
            asset = row.get('Asset', 'Unknown')
            make = row.get('Make', 'Unknown')
            
            critical_issues = []
            warning_issues = []
            
            for field in critical_fields:
                if row.get(field) == "❌":
                    critical_issues.append(field)
                elif row.get(field) == "⚠️":
                    warning_issues.append(field)
            
            if critical_issues:
                critical_vehicles.append({
                    'vehicle': vehicle,
                    'asset': asset,
                    'make': make,
                    'issues': critical_issues
                })
            
            if warning_issues:
                warning_vehicles.append({
                    'vehicle': vehicle,
                    'asset': asset,
                    'make': make,
                    'issues': warning_issues
                })
        
        # Get today's date for the report
        today = datetime.now().date()
        
        # Prepare email content
        sender = "gsezmaintenance.alerts@gmail.com"
        receiver = "gsezmaintenance.alerts@gmail.com"
        app_password = "srtqffxswhbgautt"
        
        subject = f"📊 Daily Maintenance Report - {today.strftime('%Y-%m-%d')}"
        
        # Create detailed body
        body = f"""
        📊 Daily Maintenance Report - {today.strftime('%Y-%m-%d')}
        
        📈 Summary:
        - Vehicles with critical issues (❌): {len(critical_vehicles)}
        - Vehicles with warnings (⚠️): {len(warning_vehicles)}
        
        """
        
        if critical_vehicles:
            body += """
        🚨 Vehicles with Critical Issues (❌):
        """
            for vehicle_info in critical_vehicles:
                body += f"""
        🛻 Vehicle/Equipment: {vehicle_info['vehicle']}
        📋 Asset: {vehicle_info['asset']}
        🏭 Make: {vehicle_info['make']}
        ❗ Issues: {', '.join(vehicle_info['issues'])}
        """
        else:
            body += """
        ✅ No vehicles with critical issues found!
        """
        
        if warning_vehicles:
            body += """
        
        ⚠️ Vehicles with Warnings (⚠️):
        """
            for vehicle_info in warning_vehicles:
                body += f"""
        🛻 Vehicle/Equipment: {vehicle_info['vehicle']}
        📋 Asset: {vehicle_info['asset']}
        🏭 Make: {vehicle_info['make']}
        ⚠️ Issues: {', '.join(vehicle_info['issues'])}
        """
        else:
            body += """
        
        ✅ No vehicles with warnings found!
        """
        
        body += f"""
        
        📋 Full maintenance log: 
        https://docs.google.com/spreadsheets/d/17pmwdqIlq1ws_M2paN81TlIbPn-3TKpp5M3mBi9NIXY/edit?usp=sharing
        
        ---
        This is an automated daily report from the ARISE Maintenance System.
        """
        
        # Create and send email
        message = MIMEMultipart()
        message["From"] = sender
        message["To"] = receiver
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))
        
        with smtplib.SMTP("smtp.gmail.com", 587) as server: 
            server.starttls()
            server.login(sender, app_password)
            server.send_message(message)
        
        print(f"✅ Daily report sent for {today.strftime('%Y-%m-%d')}")
        print(f"📊 Found {len(critical_vehicles)} vehicles with critical issues")
        print(f"⚠️ Found {len(warning_vehicles)} vehicles with warnings")
        return True
        
    except Exception as e:
        print(f"❌ Failed to send daily report: {e}")
        return False

def send_daily_summary(): 
    #setup sheets 
    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", 
                                                             [
                                                                 "https://spreadsheets.google.com/feeds", 
                                                              "https://www.googleapis.com/auth/drive"
                                                              ])
    client = gspread.authorize(creds)
    sheet = client.open("Maintenance Logs").sheet1
    records = sheet.get_all_records()
    
    today = datetime.now().date()
    today_logs = [r for r in records if r["Timestamp"].startswith(str(today))]
    
    critical_today = [r for r in today_logs if "❌" in r.values()]
    body = f"""
    📊 Daily Maintenance Summary ({today})

    Total submissions: {len(today_logs)}
    Issues flagged: {len(critical_today)}

    Vehicles with issues:
    {', '.join(set(r['Vehicle'] for r in critical_today)) if critical_today else "None 🎉"}

    Check full log here: https://docs.google.com/spreadsheets/d/17pmwdqIlq1ws_M2paN81TlIbPn-3TKpp5M3mBi9NIXY/edit?usp=sharing
    
    """
    
    #send via gmail 
    msg = MIMEMultipart()
    msg["From"] = "gsezmaintenance.alerts@gmail.com"
    msg["To"] = "gsezmaintenance.alerts@gmail.com"
    msg["Subject"] = f"📊 Daily Maintenance Summary ({today})"
    msg.attach(MIMEText(body, "plain"))
    
    with smtplib.SMTP("smtp.gmail.com", 587) as server: 
        server.starttls()
        server.login("gsezmaintenance.alerts@gmail.com", "GSEZARISE_maintenance")
        server.send_message(msg)
