import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from email_agent import send_alert_email, send_daily_report
from vehicle_data import vehicle_info

with open("theme.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Place ARISE logo at the absolute top left of the page
# st.markdown(
#     """
#     <style>
#     .arise-logo-top-left {
#         position: absolute;
#         top: 1.5rem;
#         left: 1.5rem;
#         z-index: 1000;
#     }
#     </style>
#     <img src="arise_logo.png" class="arise-logo-top-left" width="120">
#     """,
#     unsafe_allow_html=True
# )

# --- ARISE Logo (update path as needed) ---
st.image("/Users/polar/Desktop/maintenance app/arise_logo.png", width=180)
# Helper function to convert column number (1-indexed) to Excel column letter
# e.g., 1 -> 'A', 27 -> 'AA'
def colnum_to_letter(n):
    string = ""
    while n > 0:
        n, remainder = divmod(n - 1, 26)
        string = chr(65 + remainder) + string
    return string

# ----------------- Google Sheets Setup -----------------
try:
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open("Maintenance Logs").sheet1
    SHEETS_AVAILABLE = True
except FileNotFoundError:
    print("⚠️ Warning: creds.json not found. Google Sheets integration disabled.")
    SHEETS_AVAILABLE = False
    sheet = None
except Exception as e:
    print(f"⚠️ Warning: Google Sheets setup failed: {e}")
    SHEETS_AVAILABLE = False
    sheet = None

# ----------------- Language Dictionary -----------------
lang = {
    "en": {
        "title": "Maintenance Check",
        "driving_now": "Are you driving now?",
        "vehicle": "Select Vehicle / Equipment",
        "not_selected": "Please select a vehicle.",
        "checklist_title": "Pre-Drive Checklist",
        "submit_btn": "Submit Checklist",
        "status_driving": "🚘 You're in driving mode. Emergency + End buttons will appear in next step.",
        "options": ["✅", "❌", "⚠️"],
        "checklist_items": [
            "Meter Reading", "Fuel", "Aggregation Functions", "Engine Oil",
            "Coolant", "Leakages", "Noise", "Dashboard Indications",
            "Battery Condition", "Oil (Trans/Diff)"
        ],
        "checklist_help": {
            "Meter Reading": "Note the odometer/hour meter reading.",
            "Fuel": "Is there enough fuel for operation?",
            "Aggregation Functions": "Do all equipment functions respond properly?",
            "Engine Oil": "Is the oil level sufficient?",
            "Coolant": "Is coolant level okay and no leaks?",
            "Leakages": "Any visible leaks under the vehicle?",
            "Noise": "Any strange sounds when starting or moving?",
            "Dashboard Indications": "Any warning lights on the dashboard?",
            "Battery Condition": "Battery well connected and operational?",
            "Oil (Trans/Diff)": "Transmission/differential oil okay (for heavy equipment)?"
        },
        "select_unit": "Select specific unit",
        "vehicle_details": "### 🔍 Vehicle Details",
        "labels": {
            "Make": "Make", "Application": "Application", "Depart": "Department", "Entity": "Entity", "Location": "Location"
        }
    },
    "fr": {
        "title": "Contrôle de maintenance",
        "driving_now": "Conduisez-vous actuellement ?",
        "vehicle": "Sélectionnez un véhicule / équipement",
        "not_selected": "Veuillez sélectionner un véhicule.",
        "checklist_title": "Liste de contrôle avant conduite",
        "submit_btn": "Soumettre",
        "status_driving": "🚘 Vous êtes en mode conduite. Les boutons d'urgence + fin apparaîtront à l'étape suivante.",
        "options": ["✅", "❌", "⚠️"],
        "checklist_items": [
            "Compteur", "Carburant", "Fonctions d'agrégation", "Huile moteur",
            "Liquide de refroidissement", "Fuites", "Bruit", "Indicateurs de tableau de bord",
            "État de la batterie", "Huile (Transmission / Différentiel)"
        ],
        "checklist_help": {
            "Compteur": "Relevez le compteur kilométrique ou horaire.",
            "Carburant": "Y a-t-il assez de carburant pour la tâche ?",
            "Fonctions d'agrégation": "Toutes les fonctions de l’équipement répondent-elles correctement ?",
            "Huile moteur": "Le niveau d’huile est-il suffisant ?",
            "Liquide de refroidissement": "Le niveau de liquide est-il bon ? Fuites ?",
            "Fuites": "Fuites visibles sous le véhicule ?",
            "Bruit": "Bruit étrange lors du démarrage ou du déplacement ?",
            "Indicateurs de tableau de bord": "Des voyants d’alerte sont-ils allumés ?",
            "État de la batterie": "Batterie bien connectée et fonctionnelle ?",
            "Huile (Transmission / Différentiel)": "Huile de transmission / différentiel correcte (engins lourds) ?"
        },
        "select_unit": "Sélectionnez l'unité spécifique",
        "vehicle_details": "### 🔍 Détails du véhicule",
        "labels": {
            "Make": "Marque", "Application": "Application", "Depart": "Département", "Entity": "Entité", "Location": "Emplacement"
        }
    }
}

if "is_driving" not in st.session_state:
    st.session_state.is_driving = False

if "start_time" not in st.session_state:
    st.session_state.start_time = None

st.set_page_config(page_title="Maintenance App", layout="centered")

# Inject ARISE custom theme styles
with open("theme.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Display ARISE logo (centered)
# st.markdown(
#     """
#     <div style='text-align: center; margin-bottom: 20px;'>
#         <img src='arise_logo.png' width='220'/>
#     </div>
#     """,
#     unsafe_allow_html=True
# )

language = st.selectbox("🌍 Langue / Language", ["en", "fr"])
text = lang[language]
st.title(text["title"])

# Driving status section with enhanced styling
with st.container():
    st.markdown('<div class="main">', unsafe_allow_html=True)
    driving_status = st.radio(
        text["driving_now"],
        ["No", "Yes"] if language == "en" else ["Non", "Oui"]
    )
    st.markdown('</div>', unsafe_allow_html=True)

if driving_status in ["No", "Non"]:
    # Vehicle type translations
    vehicle_type_translations = {
        "en": {
            "Log Truck": "Log Truck",
            "Log Charger": "Log Charger", 
            "Light Vehicle": "Light Vehicle",
            "Utility": "Utility",
            "Bull Dozzer": "Bull Dozer"
        },
        "fr": {
            "Log Truck": "Camion de grumes",
            "Log Charger": "Chargeur de grumes",
            "Light Vehicle": "Véhicule léger", 
            "Utility": "Utilitaires",
            "Bull Dozzer": "Bouteur"
        }
    }
    
    # Application translations
    application_translations = {
        "en": {
            "Log Truck": "Log Truck",
            "Log Charger": "Log Charger",
            "Pick Up": "Pick Up",
            "Light vehicle": "Light Vehicle",
            "Land Cruiser-Pickup": "Land Cruiser-Pickup",
            "Canter": "Canter",
            "Low bed": "Low Bed",
            "Dumper": "Dumper",
            "Emp.Bus": "Employee Bus",
            "Mini Bus": "Mini Bus",
            "Generator": "Generator",
            "School Bus": "School Bus",
            "Dump Truck": "Dump Truck",
            "Motor Grader": "Motor Grader",
            "Wheel Laoder": "Wheel Loader",
            "Excavator": "Excavator",
            "Bull Dozzer": "Bull Dozer"
        },
        "fr": {
            "Log Truck": "Camion de grumes",
            "Log Charger": "Chargeur de grumes", 
            "Pick Up": "Pick-up",
            "Light vehicle": "Véhicule léger",
            "Land Cruiser-Pickup": "Land Cruiser-Pickup",
            "Canter": "Canter",
            "Low bed": "Plateau bas",
            "Dumper": "Dumper",
            "Emp.Bus": "Bus employés",
            "Mini Bus": "Mini bus",
            "Generator": "Générateur",
            "School Bus": "Bus scolaire",
            "Dump Truck": "Camion benne",
            "Motor Grader": "Niveleuse",
            "Wheel Laoder": "Chargeur sur roues",
            "Excavator": "Excavatrice",
            "Bull Dozzer": "Bouteur"
        }
    }
    
    # Get vehicle types and translate them
    vehicle_types_en = sorted(set(v["Asset"] for v in vehicle_info.values()))
    vehicle_types = [vehicle_type_translations[language].get(vt, vt) for vt in vehicle_types_en]
    
    # Create reverse mapping for selection
    fr_to_en_vehicle = {}
    for en_key, fr_value in vehicle_type_translations["fr"].items():
        fr_to_en_vehicle[fr_value] = en_key
    
    selected_type_display = st.selectbox(text["vehicle"], [""] + vehicle_types)
    
    # Convert back to English for internal use
    if selected_type_display:
        if language == "fr":
            selected_type = fr_to_en_vehicle.get(selected_type_display, selected_type_display)
        else:
            selected_type = selected_type_display
    else:
        selected_type = ""

    selected_vehicle = ""
    if selected_type == "Utility":
        # Get all unique applications for Utility and translate them
        utility_apps_en = sorted(set(
            v["Application"] for v in vehicle_info.values() if v["Asset"] == "Utility"
        ))
        utility_apps = [application_translations[language].get(app, app) for app in utility_apps_en]
        
        selected_app_display = st.selectbox("Sélectionnez l'application" if language == "fr" else "Select Application", [""] + utility_apps)
        
        # Convert back to English for filtering
        if selected_app_display:
            if language == "fr":
                # Create reverse mapping for applications
                fr_to_en_app = {}
                for en_app, fr_app in application_translations["fr"].items():
                    fr_to_en_app[fr_app] = en_app
                selected_app = fr_to_en_app.get(selected_app_display, selected_app_display)
            else:
                selected_app = selected_app_display
        else:
            selected_app = ""
            
        if selected_app:
            filtered_vehicles = sorted([
                k for k, v in vehicle_info.items()
                if v["Asset"] == "Utility" and v["Application"] == selected_app
            ])
            selected_vehicle = st.selectbox(text["select_unit"], [""] + filtered_vehicles)
    else:
        filtered_vehicles = sorted([
            k for k, v in vehicle_info.items() if v["Asset"] == selected_type
        ])
        selected_vehicle = st.selectbox(text["select_unit"], [""] + filtered_vehicles)

    if selected_vehicle:
        details = vehicle_info[selected_vehicle]
        
        # Vehicle details with enhanced styling
        with st.container():
            st.markdown('<div class="main">', unsafe_allow_html=True)
            st.markdown(text["vehicle_details"])
            for key in ["Make", "Application", "Depart", "Entity", "Location"]:
                label = text["labels"][key]
                st.markdown(f"**{label}**: {details.get(key, '-')}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.subheader(text["checklist_title"])
        # Show icon legend once at the top
        if language == "en":
            st.markdown(
                "**Legend:**  \
                ✅ = Good/Normal  \
                ❌ = Critical/Bad  \
                ⚠️ = Warning/Needs Attention"
            )
        else:
            st.markdown(
                "**Légende :**  \
                ✅ = Bon/Normal  \
                ❌ = Critique/Mauvais  \
                ⚠️ = Avertissement/Besoin d'attention"
            )
        checklist_items = lang[language]["checklist_items"]
        # Only show last item for heavy equipment
        if selected_type not in ["Excavator", "Log Charger", "Excavatrice", "Chargeur de grumes"]:
            checklist_items = checklist_items[:-1]
        responses = {}
        extra_text = {}
        for item in checklist_items:
            # Meter Reading: number input
            if item in ["Meter Reading", "Compteur"]:
                st.markdown(f"**{item}**")
                st.caption("Please type in meter reading number from dashboard" if language == "en" else "Veuillez saisir le numéro du compteur depuis le tableau de bord")
                responses[item] = st.number_input("", min_value=0, step=1, key=f"meter_{item}")
                st.markdown("\n")
            # Fuel, Engine Oil, Coolant, Battery Condition: icon-specific help
            elif item in ["Fuel", "Carburant"]:
                st.markdown(f"**{item}**")
                st.caption(text["checklist_help"].get(item, ""))
                responses[item] = st.radio("", text["options"], key=f"fuel_{item}")
                st.markdown("\n")
            elif item in ["Engine Oil", "Huile moteur", "Coolant", "Liquide de refroidissement", "Battery Condition", "État de la batterie"]:
                st.markdown(f"**{item}**")
                st.caption(text["checklist_help"].get(item, ""))
                responses[item] = st.radio("", text["options"], key=f"oil_{item}")
                st.markdown("\n")
            # Leakages and Noise: icon + optional text
            elif item in ["Leakages", "Fuites", "Noise", "Bruit"]:
                st.markdown(f"**{item}**")
                st.caption(text["checklist_help"].get(item, ""))
                if item in ["Leakages", "Fuites"]:
                    responses[item] = st.radio("", text["options"], key=f"leak_{item}")
                    extra_text[item] = st.text_input("Describe what's going on (optional)" if language == "en" else "Décrivez ce qui se passe (optionnel)", key=f"leak_text_{item}")
                else:
                    responses[item] = st.radio("", text["options"], key=f"noise_{item}")
                    extra_text[item] = st.text_input("Describe what's going on (optional)" if language == "en" else "Décrivez ce qui se passe (optionnel)", key=f"noise_text_{item}")
                st.markdown("\n")
            else:
                st.markdown(f"**{item}**")
                st.caption(text["checklist_help"].get(item, ""))
                responses[item] = st.radio("", text["options"], key=f"other_{item}")
                st.markdown("\n")
        # Submit button with enhanced styling
        with st.container():
            st.markdown('<div class="main">', unsafe_allow_html=True)
            if st.button(text["submit_btn"]):
                st.markdown('</div>', unsafe_allow_html=True)
            now = datetime.now()
            st.session_state.start_time = now
            st.session_state.is_driving = True
            english_keys = lang["en"]["checklist_items"]
            # Mapping from French to English checklist items
            fr_to_en = dict(zip(lang["fr"]["checklist_items"], lang["en"]["checklist_items"]))
            checklist_values = []
            for item in english_keys:
                # If in French, get the French key for this English item
                if language == "fr":
                    fr_key = [k for k, v in fr_to_en.items() if v == item]
                    if fr_key:
                        key = fr_key[0]
                    else:
                        key = item  # fallback
                else:
                    key = item
                val = responses.get(key, "")
                # For Leakages/Noise, append text if present
                if item in ["Leakages", "Noise"] and extra_text.get(key):
                    val = f"{val} - {extra_text[key]}"
                checklist_values.append(val)
            if not SHEETS_AVAILABLE:
                st.warning("⚠️ Google Sheets not available. Checklist data saved locally only.")
                st.success("✅ Checklist submitted successfully! (Local mode)")
                
                # Still check for critical issues and send email alerts
                critical_fields_en = ["Coolant", "Battery Condition", "Engine Oil"]
                critical_fields_fr = ["Liquide de refroidissement", "État de la batterie", "Huile moteur"]

                issues = []
                if language == "en":
                    for field in critical_fields_en:
                        if responses.get(field) == "❌":
                            issues.append(field)
                else:
                    fr_to_en_critical = {
                        "Liquide de refroidissement": "Coolant",
                        "État de la batterie": "Battery Condition",
                        "Huile moteur": "Engine Oil"
                    }
                    for field in critical_fields_fr:
                        if responses.get(field) == "❌":
                            issues.append(fr_to_en_critical[field])

                if issues:
                    send_alert_email(selected_vehicle, issues, now.strftime("%Y-%m-%d %H:%M:%S"))
            else:
                try:
                    # Find row index by vehicle ID (assumes Vehicle/equipment_NO is unique and in column A)
                    cell = sheet.find(selected_vehicle)
                    row_index = cell.row
                    
                    # Get the headers to find the correct column positions
                    headers = sheet.row_values(1)
                    
                    # Debug: Print headers to see what we're working with
                    print(f"Headers found: {headers}")
                    
                    # Find the "Last Updated" column - try multiple variations
                    last_updated_col_index = None
                    for i, header in enumerate(headers):
                        header_lower = header.lower().strip()
                        if any(phrase in header_lower for phrase in ["last updated", "last update", "lastupdated", "lastupdate"]):
                            last_updated_col_index = i + 1  # Convert to 1-indexed
                            print(f"Found 'Last Updated' column at index {i+1} (column {colnum_to_letter(i+1)})")
                            break
                    
                    # If "Last Updated" column not found, try to find it by position
                    if last_updated_col_index is None:
                        # Assume it's the second-to-last column (common position)
                        last_updated_col_index = len(headers) - 1
                        print(f"Using fallback: column {colnum_to_letter(last_updated_col_index)}")
                    
                    # Calculate checklist columns (assuming they start after the static columns)
                    static_cols = 7  # A-G
                    checklist_start_col = static_cols + 1  # H is column 8
                    checklist_end_col = checklist_start_col + len(english_keys) - 1
                    start_letter = colnum_to_letter(checklist_start_col)
                    end_letter = colnum_to_letter(checklist_end_col)
                    update_range = f"{start_letter}{row_index}:{end_letter}{row_index}"
                    sheet.update(update_range, [checklist_values])
                    
                    # Update last updated timestamp in the correct column
                    last_update_letter = colnum_to_letter(last_updated_col_index)
                    print(f"Updating timestamp in column {last_update_letter} at row {row_index}")
                    
                    # Try to update the timestamp - if it fails, try the next column
                    try:
                        sheet.update_acell(f"{last_update_letter}{row_index}", now.strftime("%Y-%m-%d %H:%M:%S"))
                        print(f"✅ Successfully updated timestamp in {last_update_letter}{row_index}")
                    except Exception as timestamp_error:
                        print(f"❌ Failed to update in {last_update_letter}, trying next column...")
                        # Try the next column as fallback
                        fallback_col = colnum_to_letter(last_updated_col_index + 1)
                        sheet.update_acell(f"{fallback_col}{row_index}", now.strftime("%Y-%m-%d %H:%M:%S"))
                        print(f"✅ Updated timestamp in fallback column {fallback_col}{row_index}")
                    
                    st.success("✅ Checklist submitted successfully!")
                    
                    # After updating the sheet, check for critical issues and send alert email if needed
                    critical_fields_en = ["Coolant", "Battery Condition", "Engine Oil"]
                    critical_fields_fr = ["Liquide de refroidissement", "État de la batterie", "Huile moteur"]

                    issues = []
                    if language == "en":
                        for field in critical_fields_en:
                            if responses.get(field) == "❌":
                                issues.append(field)
                    else:
                        fr_to_en_critical = {
                            "Liquide de refroidissement": "Coolant",
                            "État de la batterie": "Battery Condition",
                            "Huile moteur": "Engine Oil"
                        }
                        for field in critical_fields_fr:
                            if responses.get(field) == "❌":
                                issues.append(fr_to_en_critical[field])

                    if issues:
                        send_alert_email(selected_vehicle, issues, now.strftime("%Y-%m-%d %H:%M:%S"))
                        
                except Exception as e:
                    st.error(f"❌ Failed to update sheet: {e}")

    else:
        st.warning(text["not_selected"])
else:
    st.info(text["status_driving"])
    if st.button("🚨 Emergency Stop"):
        reason = st.text_area("Describe what happened:")
        if reason:
            end_time = datetime.now()
            duration = "-"
            if st.session_state.start_time:
                duration = (end_time - st.session_state.start_time).total_seconds() / 60
                duration = f"{duration:.1f} mins"
            
            if SHEETS_AVAILABLE:
                row = [
                    end_time.strftime("%Y-%m-%d %H:%M:%S"), "EMERGENCY",
                    "-", "-", "-", "-", "-", "-", "-", "-", "-", "-",
                    "🚨", duration, reason
                ]
                sheet.append_row(row)
                st.success("🚨 Emergency logged and driving stopped.")
            else:
                st.warning("⚠️ Google Sheets not available. Emergency logged locally only.")
                st.success("🚨 Emergency logged and driving stopped. (Local mode)")
            
            st.session_state.is_driving = False
        else:
            st.warning("Please describe the emergency.")
    
    if st.button("🛑 End Trip"):
        end_time = datetime.now()
        duration = "-"
        if st.session_state.start_time:
            duration = (end_time - st.session_state.start_time).total_seconds() / 60
            duration = f"{duration:.1f} mins"
        
        if SHEETS_AVAILABLE:
            row = [
                end_time.strftime("%Y-%m-%d %H:%M:%S"), "END",
                "-", "-", "-", "-", "-", "-", "-", "-", "-", "-",
                "🛑", duration, "Normal end"
            ]
            sheet.append_row(row)
            st.success("✅ Trip ended and logged.")
        else:
            st.warning("⚠️ Google Sheets not available. Trip ended logged locally only.")
            st.success("✅ Trip ended and logged. (Local mode)")
        
        st.session_state.is_driving = False

# Add manual daily report trigger for testing
st.markdown("---")

# Admin tools with enhanced styling
with st.container():
    st.markdown('<div class="main">', unsafe_allow_html=True)
    st.subheader("🔧 Admin Tools")
    if st.button("📊 Send Daily Report (Test)"):
        try:
            if send_daily_report():
                st.success("✅ Daily report sent successfully!")
            else:
                st.error("❌ Failed to send daily report")
        except Exception as e:
            st.error(f"❌ Error sending daily report: {e}")
    st.markdown('</div>', unsafe_allow_html=True)
