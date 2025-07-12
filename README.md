# ARISE Maintenance App

A comprehensive maintenance management system for ARISE Integrated Industrial Platforms, built with Streamlit and Google Sheets integration.

## 🚀 Features

### Core Functionality

- **Bilingual Support**: English and French interface
- **Vehicle/Equipment Registry**: Complete database integration
- **Pre-Drive Checklists**: Comprehensive maintenance checks
- **Real-time Updates**: Google Sheets integration
- **Critical Issue Alerts**: Email notifications for urgent problems
- **Daily Reports**: Automated daily summaries

### Vehicle Management

- **Multi-level Selection**: Vehicle type → Application → Specific unit
- **Utility Vehicles**: Special handling for Canter, Low bed, etc.
- **Equipment Tracking**: Log trucks, chargers, light vehicles, utilities

### Maintenance Checks

- **Meter Readings**: Odometer/hour meter tracking
- **Critical Systems**: Coolant, Battery, Engine Oil monitoring
- **Visual Indicators**: ✅ Good, ❌ Critical, ⚠️ Warning
- **Optional Notes**: Additional details for leaks and noise issues

### Automated Features

- **Email Alerts**: Instant notifications for critical issues
- **Daily Reports**: 9 PM automated summaries
- **Status Tracking**: Last updated timestamps
- **Data Persistence**: Google Sheets integration

## 🛠️ Installation

### Prerequisites

- Python 3.8+
- Google Cloud Platform account
- Gmail account for notifications

### Setup Instructions

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/arise-maintenance-app.git
   cd arise-maintenance-app
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Google Sheets**

   - Create a Google Cloud Project
   - Enable Google Sheets API
   - Create service account credentials
   - Download `creds.json` to project root

4. **Set up Gmail for notifications**

   - Enable 2-factor authentication
   - Generate app password
   - Update email settings in `email_agent.py`

5. **Configure Google Sheets**
   - Create "Maintenance Logs" spreadsheet
   - Share with service account email
   - Set up proper column headers

## 📁 Project Structure

```
arise-maintenance-app/
├── app.py                 # Main Streamlit application
├── email_agent.py         # Email notification system
├── daily_scheduler.py     # Automated daily reports
├── vehicle_data.py        # Vehicle registry data
├── theme.css             # Custom styling
├── requirements.txt      # Python dependencies
├── creds.json           # Google API credentials (not in repo)
├── arise_logo.png       # ARISE branding
└── README.md            # This file
```

## 🚗 Vehicle Categories

### Log Trucks

- **MAN Trucks**: AM series (AM500IT, AM418IT, etc.)
- **Shacman Trucks**: AP series (AP 083 IT, AP 086 IT, etc.)
- **Mercedes**: DB series (DB 225 AA, DB 228 AA)

### Log Chargers

- **Komatsu**: WA470 series, WA500
- **CAT**: 980H, 950H
- **Volvo**: L220H
- **LTMG**: LT15J, LT12JS
- **XCMG**: LW600KN series

### Light Vehicles

- **Toyota**: Pick-ups and Land Cruisers
- **Mitsubishi**: Various models
- **Suzuki**: Light vehicles
- **Hyundai**: Various models

### Utility Equipment

- **Canter**: ISUZU trucks
- **Low Bed**: Transport trailers
- **Dumpers**: Various models
- **Generators**: Power equipment
- **Buses**: Employee and school transport

## 📊 Daily Reports

### Automated Features

- **Schedule**: Daily at 9:00 PM
- **Content**: Critical issues summary
- **Format**: Vehicle details with specific problems
- **Delivery**: Email to maintenance team

### Critical Fields Monitored

- **Coolant**: Engine cooling system
- **Battery Condition**: Electrical system
- **Engine Oil**: Lubrication system

## 🔧 Configuration

### Email Settings (`email_agent.py`)

```python
sender = "your-email@gmail.com"
app_password = "your-app-password"
```

### Google Sheets Setup

1. Create "Maintenance Logs" spreadsheet
2. Set up columns: Timestamp, Vehicle/equipment_NO, Asset, Make, etc.
3. Add "Last Updated" column for timestamps

### Daily Scheduler

```bash
python daily_scheduler.py
```

## 🎨 Customization

### Theme Styling

- Edit `theme.css` for custom styling
- ARISE brand colors and fonts
- Responsive design for mobile devices

### Language Support

- English and French interfaces
- Vehicle type translations
- Application name translations

## 📧 Email Notifications

### Alert Triggers

- ❌ Critical issues in Coolant, Battery, or Engine Oil
- ⚠️ Warning conditions
- Daily summary reports

### Email Content

- Vehicle identification
- Specific issues found
- Timestamp of detection
- Link to maintenance spreadsheet

## 🚀 Deployment

### Local Development

```bash
streamlit run app.py
```

### Production Deployment

1. Set up server with Python 3.8+
2. Install dependencies
3. Configure environment variables
4. Set up systemd service for scheduler
5. Configure reverse proxy (nginx)

### Environment Variables

```bash
GOOGLE_CREDENTIALS_PATH=creds.json
GMAIL_USER=your-email@gmail.com
GMAIL_PASSWORD=your-app-password
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is proprietary to ARISE Integrated Industrial Platforms.

## 🆘 Support

For technical support or questions:

- Check the troubleshooting section
- Review the configuration guide
- Contact the development team

## 🔄 Updates

### Recent Changes

- Added bilingual support (English/French)
- Implemented daily automated reports
- Enhanced email notification system
- Improved UI/UX with ARISE branding
- Added comprehensive vehicle registry

### Planned Features

- Mobile app version
- Advanced analytics dashboard
- Integration with other ARISE systems
- Enhanced reporting capabilities

---

**Built for ARISE Integrated Industrial Platforms** 🏭
