import gradio as gr
import requests
import json
import os
from pathlib import Path
import html
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import io
import base64

gr.set_static_paths(paths=[Path.cwd().absolute()/"assets"])
ORCHESTRATOR_HOST = os.getenv("ORCHESTRATOR_HOST", "orchestrator")
ORCHESTRATOR_BASE_URL = f"http://{ORCHESTRATOR_HOST}:8080"

AUTH_ENDPOINT = f"{ORCHESTRATOR_BASE_URL}/login"
REGISTER_ENDPOINT = f"{ORCHESTRATOR_BASE_URL}/register"
GET_NOTES_ENDPOINT = f"{ORCHESTRATOR_BASE_URL}/notes"

kure_theme = gr.themes.Base(
    primary_hue=gr.themes.Color(
        c50="#F0FFF0", c100="#E0FFE0", c200="#C1FFC1", c300="#A2FFA2", c400="#83FF83",
        c500="#64FF64", c600="#57E657", c700="#49CC49", c800="#3BB33B", c900="#2E992E",
        c950="#218021",
    ),
    secondary_hue=gr.themes.Color(
        c50="#E0F7FA", c100="#B2EBF2", c200="#80DEEA", c300="#4DD0E1", c400="#26C6DA",
        c500="#00BCD4", c600="#00ACC1", c700="#0097A7", c800="#00838F", c900="#006064",
        c950="#004D40",
    ),
    neutral_hue=gr.themes.Color(
        name="neutral grey", c50="#F5F7FA", c100="#E8F0F2", c200="#D3D9DE", c300="#BCC4CC",
        c400="#A5B0B9", c500="#8E9BA7", c600="#6C757D", c700="#555D65", c800="#3E454D",
        c900="#2F3E46", c950="#1A2024"
    ),
    spacing_size="sm", radius_size="none",
    font=[gr.themes.GoogleFont("Poppins"), "ui-sans-serif", "system-ui", "sans-serif"],
    font_mono=[gr.themes.GoogleFont("IBM Plex Mono"), "ui-monospace", "monospace"],
).set(
    body_background_fill="#F5F7FA", body_text_color="#2F3E46",
    body_text_color_subdued="#6C757D", button_primary_background_fill="#2E992E",
    button_primary_background_fill_hover="#218021", button_primary_text_color="#FFFFFF",
    button_primary_border_color="#64FF64", button_primary_border_color_hover="#49CC49",
    button_secondary_background_fill="#80DEEA",
    button_secondary_background_fill_hover="#4DD0E1",
    button_secondary_text_color="#006064",
    block_border_width="1px", block_border_color="#E8F0F2", input_border_color="#BCC4CC",
    input_background_fill="#FFFFFF",
    block_background_fill="#FFFFFF",
    block_label_text_color="#2F3E46", block_title_text_color="#2F3E46",
    input_radius="sm",
    block_radius="md",
)
""" NOTES, DONT CHANGE  
background:
  radial-gradient(circle at center,
    rgba(255, 255, 255, 1) 0%,
    rgba(245, 255, 245, 1) 80%,
    rgba(245, 255, 245, 0) 100%
  ),
    url('/gradio_api/file=assets/border4.png') center center no-repeat;
    .gradio-container {
  background: url('/gradio_api/file=assets/image3.jpg') no-repeat center center;
  background-size: cover;}"""


custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@500;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500&display=swap');

body {
    font-family: 'Poppins', sans-serif;
    background: none;
}

.kure-header {
    background-color: #218021;
    width: 100%;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    margin-bottom: 0;
    position: fixed;
    top: 0;
    left: 0;
    z-index: 100;
}

.kure-header h1 {
    font-family: 'Quicksand', sans-serif;
    color: #F0FFF0;
    text-align: center;
    font-size: 2.8em;
    font-weight: 700;
    margin: 0;
    padding: 10px 0;
}

#login-box, #signup-box {
    max-width: 450px !important;
    min-width: 320px;
    margin: 100px auto 40px auto !important;
    padding: 35px !important;
    border: 1px solid #D3D9DE !important;
    background-color: #FFFFFF !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    border-radius: 8px !important;
}

#login-box h2, #signup-box h2 {
    text-align: center;
    color: #2F3E46;
    font-family: 'Quicksand', sans-serif;
    font-weight: 700;
    margin-top: 0;
    margin-bottom: 25px;
}

#login-box .gr-button, #signup-box .gr-button {
    width: 100%;
    margin-top: 15px;
    border-radius: 4px !important;
}

.switch-auth-button {
    background: none !important;
    border: none !important;
    color: #00838F !important;
    text-decoration: underline;
    font-weight: 500;
    margin-top: 20px !important;
    padding: 5px !important;
    box-shadow: none !important;
    width: auto !important;
    display: block;
    margin-left: auto;
    margin-right: auto;
    cursor: pointer;
}
.switch-auth-button:hover {
    color: #006064 !important;
}

#login-error-output, #signup-error-output {
    background-color: #FFFFFF !important;
    border-radius: 4px !important;
    min-height: 40px !important;
}
#login-error-output textarea, #signup-error-output textarea {
    color: #D8000C !important;
    font-weight: 500 !important;
    background-color: transparent !important;
    padding: 8px 10px !important;
    text-align: center !important;
}
#login-error-output .label-wrap, #signup-error-output .label-wrap {
    display: none !important;
}

#journal-page {
    max-width: 800px;
    margin: 80px auto 20px auto;
    padding: 20px;
    background-color: rgba(255, 255, 255, 0.05);
    max-height: calc(100vh - 200px); /* Set a maximum height */
    overflow-y: hidden;
}
#journal-page h2 {
  background: #ffffff;
  background: radial-gradient(circle, rgba(255, 255, 255, 1) 0%, rgba(245, 255, 245, 1) 100%);
  color: #218021;
  text-align: center;
  margin-bottom: 35px;
  padding: 10px;
  font-family: 'Quicksand', sans-serif;
  font-size: 1.8em;
  font-weight: 700;
  overflow-y: visible;
  scrollbar-width: none; /* Hide scrollbar for Firefox */
  -ms-overflow-style: none; /* Hide scrollbar for IE and Edge */
}

#notes-display {
    padding: 0 10px;
   overflow-y: scroll; /* Enable scrolling for the notes */
   flex-grow: 1;
   scrollbar-width: none; /* Hide scrollbar for Firefox */
   -ms-overflow-style: none; /* Hide scrollbar for IE and Edge */
}

#notes-display::-webkit-scrollbar {
  display: none; /* Hide scrollbar for Chrome, Safari, and Opera */
}

#notes-display .note-entry {
    background: #ffffff;
    background: radial-gradient(circle,rgba(255, 255, 255, 1) 0%, rgba(245, 255, 245, 1) 100%);
    margin-bottom: 25px;
    padding: 25px;
    border: 3px solid #E8F0F2;
    border-radius: 6px;
    box-shadow: 0 3px 8px rgba(0, 10, 0, 0.06);
    display: flex;
    flex-direction: column;
}
#notes-display .note-entry:last-child {
    margin-bottom: 0;
}
#notes-display .note-meta {
    font-size: 0.9em;
    color: #555D65;
    margin-bottom: 10px;
}
#notes-display .note-meta strong {
    color: #3E454D;
}
#notes-display .note-content {
    line-height: 1.6;
    color: #2F3E46;
    margin-bottom: 12px;
    white-space: pre-wrap;
    word-wrap: break-word;
    flex-grow: 1;
}

#notes-display .mood-help-line {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

#notes-display .note-moods {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    font-size: 0.9em;
    margin-top: 1em;
}
#notes-display .note-moods strong {
    margin-right: 5px;
    color: #3E454D;
}
#notes-display .note-moods span {
}

#notes-display .mood-tag {
    display: inline-block;
    padding: 3px 8px;
    border-radius: 10px;
    font-weight: 500;
    line-height: 1.4;
    font-size: 0.9em;
    margin-right: 5px;
}

#notes-display .help-link {
  background-color: transparent;
  color: green;
  padding: 6px 12px;
  border-radius: 0;
  text-decoration: none;
  font-weight: 500;
  font-size: 0.9em;
} 


#journal-page .logout-button-container {
    display: flex;
    justify-content: center;
    margin-top: 30px;
}

#journal-page .logout-button-container .gr-button {
    max-width: 200px;
    width: auto;
    padding-left: 30px;
    padding-right: 30px;
}

#notes-display .mood-joy { background-color: #FFFFFF; border: 1px solid #0C7D03; color: #0C7D03; }
#notes-display .mood-anticipation { background-color: #FFFFFF; border: 1px solid #0C7D03; color: #0C7D03; }
#notes-display .mood-suprise { background-color: #FFFFFF; border: 1px solid #01579B; color: #01579B; }
#notes-display .mood-trust { background-color: #FFFFFF; border: 1px solid #01579B; color: #01579B; }
#notes-display .mood-disgust { background-color: #FFFFFF; border: 1px solid #B71C1C; color: #B71C1C; }
#notes-display .mood-sadness { background-color: #FFFFFF; border: 1px solid #FF8C00; color: #FF8C00;  }
#notes-display .mood-fear { background-color: #FFFFFF; border: 1px solid #FF8C00; color: #FF8C00; }
#notes-display .mood-anger { background-color: #FFFFFF; border: 1px solid #B71C1C; color: #B71C1C; }

"""


def make_api_request(endpoint, data=None, method="POST", headers=None):
    try:
        if method.upper() == "POST":
            response = requests.post(endpoint, json=data, headers=headers, timeout=15)
        elif method.upper() == "GET":
            response = requests.get(endpoint, headers=headers, timeout=15)
        else:
             return None, f"Unsupported HTTP method: {method}"

        response.raise_for_status()
        return response, None

    except requests.exceptions.HTTPError as http_err:
        status_code = http_err.response.status_code
        print(f"HTTP error occurred: {http_err} - {status_code}")
        try:
            error_details = http_err.response.json()
            msg = error_details.get("error", error_details.get("detail", error_details.get("status", f"Server error ({status_code})")))
            if isinstance(msg, dict):
                msg = msg.get("message", f"Server error ({status_code})")

        except (json.JSONDecodeError, AttributeError, ValueError):
             msg = f"Server error ({status_code}). Check server logs."

        if status_code == 401:
             if "/login" in endpoint:
                 msg = "Invalid phone number or password."
             elif "/notes" in endpoint:
                 msg = "Authentication failed or token expired. Please log in again."
             else:
                 msg = "Authentication failed."
        elif status_code == 400 and "/register" in endpoint:
             if "Registration failed" in msg:
                 pass
             elif "Missing" in msg:
                 pass
             else:
                 msg = "Registration failed. The phone number might already be registered or input is invalid."
        elif status_code == 400 and "/login" in endpoint:
             msg = "Missing phone number or password."
        elif status_code == 422:
             msg = "Invalid data provided. Please check your input."
        elif status_code == 500 and "/notes" in endpoint:
            msg = "Could not retrieve notes due to a server issue."

        return None, msg
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
        return None, f"Cannot connect to the orchestrator at {ORCHESTRATOR_BASE_URL}. Please ensure it's running and accessible."
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
        return None, "The request timed out. Please try again later."
    except requests.exceptions.RequestException as req_err:
        print(f"An unexpected request error occurred: {req_err}")
        return None, f"An unexpected network error occurred."
    except Exception as e:
         print(f"An unexpected error occurred during API request: {e}")
         return None, f"An unexpected error occurred: {type(e).__name__}"


def fetch_notes(token):
    if not token:
        return [], "No authentication token found. Cannot fetch notes."

    print("Attempting to fetch notes...")
    headers = {"Authorization": f"Bearer {token}"}
    response, error_msg = make_api_request(GET_NOTES_ENDPOINT, method="GET", headers=headers)

    if error_msg:
        print(f"Failed to fetch notes: {error_msg}")
        return [], error_msg

    try:
        fetched_data = response.json()
        fetched_notes = fetched_data.get("notes")

        if not isinstance(fetched_notes, list):
             print(f"Error: Notes data received is not a list or missing 'notes' key: {type(fetched_notes)}")
             return [], "Received invalid notes data format from server."

        print(f"Successfully fetched {len(fetched_notes)} notes.")
        return fetched_notes, None
    except json.JSONDecodeError:
        print("Error: Could not parse notes JSON data from response.")
        return [], "Failed to understand notes data from server."
    except Exception as e:
        print(f"An unexpected error occurred parsing notes: {e}")
        return [], f"An unexpected error occurred while processing notes: {type(e).__name__}"


def login(phone, password):
    print(f"Step 1: Attempting login for phone: {phone}")
    login_error = ""
    notes_error = ""
    token = None
    notes = []

    if not phone or not password:
        login_error = "Phone number and password cannot be empty."
        return None, [], login_error, gr.update(visible=True), gr.update(visible=False)

    response, login_error_msg = make_api_request(AUTH_ENDPOINT, data={"phone_number": phone, "password": password})

    if login_error_msg:
        login_error = login_error_msg
        return None, [], login_error, gr.update(visible=True), gr.update(visible=False)

    try:
        login_data = response.json()
        token = login_data.get("access_token")
        if not token:
            print("Error: Login successful but no access token found in response body.")
            login_error = "Login failed: Missing token in server response."
            return None, [], login_error, gr.update(visible=True), gr.update(visible=False)

        print(f"Step 1 Success: Received token: {token[:10]}...")

        print("Step 2: Attempting to fetch notes with the new token...")
        notes, notes_error_msg = fetch_notes(token)

        if notes_error_msg:
            notes_error = notes_error_msg
            print(f"Step 2 Failed: {notes_error}")
            return token, [], notes_error, gr.update(visible=True), gr.update(visible=False)

        print("Step 2 Success: Notes fetched.")
        return token, notes, "", gr.update(visible=False), gr.update(visible=True)

    except json.JSONDecodeError:
        print("Error: Could not parse login JSON data from response.")
        login_error = "Login failed: Invalid response format from server."
        return None, [], login_error, gr.update(visible=True), gr.update(visible=False)
    except Exception as e:
        print(f"An unexpected error occurred after login: {e}")
        login_error = f"An unexpected error occurred: {type(e).__name__}"
        return None, [], login_error, gr.update(visible=True), gr.update(visible=False)


def signup(email, phone, password, confirm_password):
    print(f"Attempting signup for email: {email}, phone: {phone}")
    signup_error = ""

    if "@" not in email or "." not in email:
        signup_error = "Please enter a valid email address."
        return None, [], signup_error, gr.update(visible=True), gr.update(visible=False)
    if not all([email, phone, password, confirm_password]):
        signup_error = "All fields are required for sign-up."
        return None, [], signup_error, gr.update(visible=True), gr.update(visible=False)
    if password != confirm_password:
        signup_error = "Passwords do not match."
        return None, [], signup_error, gr.update(visible=True), gr.update(visible=False)

    response, signup_error_msg = make_api_request(
        REGISTER_ENDPOINT,
        data={"email": email, "phone_number": phone, "password": password}
    )

    if signup_error_msg:
        return None, [], signup_error_msg, gr.update(visible=True), gr.update(visible=False)

    print("Signup successful via orchestrator. Now attempting automatic login...")
    try:
        signup_response_data = response.json()
        print(f"Signup response message: {signup_response_data.get('status')}")
    except json.JSONDecodeError:
        print("Warning: Could not parse signup success response body.")
    except Exception as e:
        print(f"Warning: Error reading signup success response body: {e}")

    login_result_token, login_result_notes, login_error_msg, signup_page_update, journal_page_update = login(phone, password)

    if login_error_msg:
        print(f"Auto-login after signup failed: {login_error_msg}")
        return login_result_token, login_result_notes, login_error_msg, gr.update(visible=True), gr.update(visible=False)
    else:
        print("Auto-login after signup successful.")
        return login_result_token, login_result_notes, "", gr.update(visible=False), journal_page_update


def logout():
    print("Logging out.")
    return None, [], "", "", gr.update(visible=True), gr.update(visible=False), gr.update(visible=False)


def show_signup_page():
    print("Switching to Sign Up page")
    return gr.update(visible=False), gr.update(visible=True), "", ""


def show_login_page():
    print("Switching to Login page")
    return gr.update(visible=True), gr.update(visible=False), "", ""


def calculate_mood_stats(notes_list):
    """Calculate mood statistics from notes less than a month old"""
    if not notes_list or not isinstance(notes_list, list):
        return None, "No notes available for analysis"
    
    # Get current date for comparison
    current_date = datetime.now()
    one_month_ago = current_date - timedelta(days=30)
    
    # Count mood occurrences
    mood_counts = {}
    total_moods = 0
    
    for entry in notes_list:
        if not isinstance(entry, dict):
            continue
            
        # Check if the note is less than a month old
        raw_timestamp = entry.get('created_at', 'N/A')
        note_date = None
        
        if isinstance(raw_timestamp, str) and raw_timestamp != 'N/A':
            try:
                ts = raw_timestamp.replace('Z', '+00:00')
                if '.' in ts:
                    ts_parts = ts.split('.')
                    ts = ts_parts[0] + '.' + ts_parts[1][:6]
                    note_date = datetime.fromisoformat(ts)
                else:
                    note_date = datetime.fromisoformat(ts)
            except (ValueError, TypeError):
                note_date = None
                
        # Skip if note is older than a month or date parsing failed
        if not note_date or note_date < one_month_ago:
            continue
            
        # Count moods
        moods_data = entry.get('moods', [])
        if moods_data and isinstance(moods_data, list):
            for mood_item in moods_data:
                if isinstance(mood_item, dict) and 'mood' in mood_item:
                    mood_name = mood_item.get('mood')
                    mood_counts[mood_name] = mood_counts.get(mood_name, 0) + 1
                    total_moods += 1
    
    # If no moods found in the last month
    if total_moods == 0:
        return None, "No mood data found in the last 30 days"
    
    # Calculate percentages
    mood_percentages = {mood: (count / total_moods) * 100 for mood, count in mood_counts.items()}
    
    return mood_percentages, None

def generate_mood_chart(mood_percentages):
    """Generate a pie chart of mood percentages"""
    if not mood_percentages:
        return "<p style='text-align: center; color: #6C757D;'>No mood data available for the last 30 days.</p>"
    
    # Create the pie chart
    plt.figure(figsize=(10, 8))
    
    # Define colors for different moods
    mood_colors = {
        'Joy': '#0C7D03',
        'Anticipation': '#0C7D03',
        'Surprise': '#01579B',
        'Trust': '#01579B',
        'Disgust': '#B71C1C',
        'Sadness': '#800080',
        'Fear': '#800080',
        'Anger': '#B71C1C'
    }
    
    # Extract colors for each mood
    colors = [mood_colors.get(mood, '#6C757D') for mood in mood_percentages.keys()]
    
    # Create the pie chart
    plt.pie(
        mood_percentages.values(), 
        labels=[f"{mood}\n{percentage:.1f}%" for mood, percentage in mood_percentages.items()],
        colors=colors,
        autopct='',
        startangle=90,
        shadow=False,
        wedgeprops={'edgecolor': 'white', 'linewidth': 1}
    )
    
    plt.axis('equal')  # Equal aspect ratio ensures the pie chart is circular
    plt.title('Your Mood Distribution (Last 30 Days)', fontsize=16, pad=20, color='#006400')    

    # Save the chart to a bytes buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight', dpi=100)
    buffer.seek(0)
    
    # Convert the image to base64 for embedding in HTML
    image_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close()
    
    # Create HTML for the chart with centering
    chart_html = f"""
    <div style="text-align: center; margin: 20px auto;">
        <img src="data:image/png;base64,{image_data}" alt="Mood Distribution Chart" style="max-width: 70%; height: auto; display: inline-block;">
    </div>
    """
    
    return chart_html

def display_mood_analysis(notes_list):
    """Display mood analysis as a pie chart"""
    if not notes_list or not isinstance(notes_list, list):
        return "<p style='text-align: center; color: #6C757D;'>No notes available for mood analysis.</p>"
    
    mood_percentages, error_msg = calculate_mood_stats(notes_list)
    
    if error_msg:
        return f"<p style='text-align: center; color: #6C757D;'>{error_msg}</p>"
    
    return generate_mood_chart(mood_percentages)
def display_notes(notes_list):
    if not notes_list or not isinstance(notes_list, list):
        if isinstance(notes_list, str) and notes_list:
            return f"<p style='color: red; text-align: center;'>Error loading notes: {html.escape(notes_list)}</p>"
        return "<p style='text-align: center; color: #6C757D;'>No notes found or unable to load notes.</p>"

    output = ""
    try:
        notes_list.sort(key=lambda x: x.get('created_at', ''), reverse=True)
    except Exception as e:
        print(f"Warning: Could not sort notes by date - {e}")
    whatsapp_number = "+96181721205"
    help_text = "Reach out for help"
    whatsapp_url = f"https://wa.me/{whatsapp_number}?text={help_text.replace(' ', '%20')}"
    for i, entry in enumerate(notes_list):
        if not isinstance(entry, dict):
            print(f"Warning: note entry at index {i} is not a dictionary: {entry}")
            continue

        content = html.escape(entry.get('text', 'N/A')).replace('\n', '<br />')
        raw_timestamp = entry.get('created_at', 'N/A')
        is_suicidal = entry.get('is_suicidal', False)
        moods_data = entry.get('moods', [])

        formatted_time = html.escape(str(raw_timestamp))
        if isinstance(raw_timestamp, str) and raw_timestamp != 'N/A':
            try:
                ts = raw_timestamp.replace('Z', '+00:00')
                if '.' in ts:
                    ts_parts = ts.split('.')
                    ts = ts_parts[0] + '.' + ts_parts[1][:6]
                    dt_object = datetime.fromisoformat(ts)
                else:
                    dt_object = datetime.fromisoformat(ts)
                formatted_time = dt_object.strftime("%b %d, %Y, %I:%M %p %Z")
            except (ValueError, TypeError) as dt_error:
                print(f"Warning: Could not parse timestamp '{raw_timestamp}': {dt_error}")
                formatted_time = html.escape(str(raw_timestamp))

        output += f"<div class='note-entry'>\n\n"
        output += f"<div class='note-first-line' style='display: flex; align-items: center; gap: 10px; margin-bottom: 5px;'>\n" # Container for the first line

        # Date and time
        output += f"<div class='note-meta' style='display: flex; align-items: center; gap: 6px; margin: 0;'><img src='/gradio_api/file=assets/calendar.png' alt='Calendar' style='height: 35px;margin-right: 10px;'><span><strong style='color: orange;'>{formatted_time}</strong></span></div>"

        # Help link
        help_link_html = ""
        if is_suicidal:
            help_link_html = f"<div class='help-container' style='display: flex; align-items: center; gap: 10px; margin-left: auto;'><a href='{whatsapp_url}' target='_blank' class='help-link'>{help_text}</a><img src='/gradio_api/file=assets/help.png' alt='Help' style='height: 35px;'></div>\n"
        output += help_link_html

        output += f"</div>\n" # Closing the note-first-line div

        # Mood tags on the second line
        mood_tags_html = ""
        if moods_data and isinstance(moods_data, list):
            mood_names = [mood_item.get('mood') for mood_item in moods_data if isinstance(mood_item, dict) and 'mood' in mood_item]
            if mood_names:
                mood_tags_html = f"<div class='note-moods' style='display: flex; align-items: center; gap: 10px; margin-bottom: 5px;'><img src='/gradio_api/file=assets/mood.png' alt='Moods' class='icon-mood' style='height: 27px; margin-left: 7px;margin-right: 10px;'><span>{''.join(f'<span class=\"mood-tag mood-{html.escape(mood_name.lower())}\">{html.escape(mood_name)}</span> ' for mood_name in mood_names)}</span></div>"
        output += mood_tags_html

        # Line separator
        output += f"<hr style='border: 1px solid var(--mood-separator-color, rgba(235, 245, 235, 1)); margin: 5px 0;'>\n"

        output += f"<p class='note-content' style='display: flex; align-items: flex-start;'><img src='/gradio_api/file=assets/pen.png' alt='Note:' class='icon-writing' style='height: 27px; margin-left: 7px; margin-right: 10px; vertical-align: top;'>{content}</p>\n\n"
        output += f"</div>\n\n"

    return output

def show_notes_view():
        return gr.update(visible=True), gr.update(visible=False), False
    
def show_chart_view(notes_list):
        chart_html = display_mood_analysis(notes_list)
        return gr.update(visible=False), gr.update(visible=True, value=chart_html), True
def update_display(notes_list, is_chart_view):
        if is_chart_view:
            chart_html = display_mood_analysis(notes_list)
            return gr.update(value=display_notes(notes_list)), gr.update(value=chart_html)
        else:
            return gr.update(value=display_notes(notes_list)), gr.update()

with gr.Blocks(theme=kure_theme, css=custom_css) as demo:
    access_token = gr.State(None)
    notes_data = gr.State([])
    is_showing_chart = gr.State(False)

    with gr.Row():
        gr.HTML('<div class="kure-header"><h1>Kure</h1></div>')

    with gr.Column(visible=True, elem_id="login-box") as login_page:
        gr.Markdown("## Login")
        login_phone_input = gr.Textbox(label="Phone Number", placeholder="Enter your phone number", elem_id="login_phone")
        login_password_input = gr.Textbox(label="Password", type="password", placeholder="Enter your password", elem_id="login_password")
        login_error_output = gr.Textbox(value="", interactive=False, show_label=False, elem_id="login-error-output", visible=False)
        login_button = gr.Button("Login", variant="primary")
        switch_to_signup_button = gr.Button("Don't have an account? Sign Up", elem_classes=["switch-auth-button"])

    with gr.Column(visible=False, elem_id="signup-box") as signup_page:
        gr.Markdown("## Sign up to Kure")
        signup_email_input = gr.Textbox(label="Email", placeholder="Enter your email", elem_id="signup_email")
        signup_phone_input = gr.Textbox(label="Phone Number", placeholder="Enter your phone number", elem_id="signup_phone")
        signup_password_input = gr.Textbox(label="Password", type="password", placeholder="Create a password", elem_id="signup_password")
        signup_confirm_password_input = gr.Textbox(label="Confirm Password", type="password", placeholder="Enter your password again", elem_id="signup_confirm_password")
        signup_error_output = gr.Textbox(value="", interactive=False, show_label=False, elem_id="signup-error-output", visible=False)
        create_account_button = gr.Button("Create Account", variant="primary")
        switch_to_login_button = gr.Button("Already have an account? Login", elem_classes=["switch-auth-button"])

    with gr.Column(visible=False, elem_id="journal-page") as journal_page_ui:
        
        # Container for the view toggle buttons
        with gr.Row(elem_classes=["view-toggle-container"]):
            view_notes_button = gr.Button("View Notes", variant="primary")
            view_mood_chart_button = gr.Button("View Mood Analysis", variant="primary")
        
        # Notes display output
        notes_display_output = gr.Markdown(
            value="Notes will appear here...",
            elem_id="notes-display"
        )
        
        # Mood chart display output (initially hidden)
        mood_chart_output = gr.Markdown(
            value="Mood analysis will appear here...",
            elem_id="mood-chart-display",
            visible=False
        )
        
        with gr.Row(elem_classes=["logout-button-container"]):
             logout_button = gr.Button("Logout", variant="primary")

    
    # Connect the view toggle buttons
    view_notes_button.click(
        fn=show_notes_view,
        inputs=[],
        outputs=[notes_display_output, mood_chart_output, is_showing_chart]
    )
    
    view_mood_chart_button.click(
        fn=show_chart_view,
        inputs=[notes_data],
        outputs=[notes_display_output, mood_chart_output, is_showing_chart]
    )

    login_button.click(
        fn=login,
        inputs=[login_phone_input, login_password_input],
        outputs=[access_token, notes_data, login_error_output, login_page, journal_page_ui]
    )

    create_account_button.click(
        fn=signup,
        inputs=[
            signup_email_input,
            signup_phone_input,
            signup_password_input,
            signup_confirm_password_input
        ],
        outputs=[access_token, notes_data, signup_error_output, signup_page, journal_page_ui]
    )

    logout_button.click(
        fn=logout,
        inputs=[],
        outputs=[access_token, notes_data, login_error_output, signup_error_output, login_page, signup_page, journal_page_ui]
    )

    switch_to_signup_button.click(
        fn=show_signup_page,
        inputs=[],
        outputs=[login_page, signup_page, login_error_output, signup_error_output]
    )
    switch_to_login_button.click(
        fn=show_login_page,
        inputs=[],
        outputs=[login_page, signup_page, login_error_output, signup_error_output]
    )

    notes_data.change(
        fn=update_display,
        inputs=[notes_data, is_showing_chart],
        outputs=[notes_display_output, mood_chart_output]
    )
    login_error_output.change(
         fn=lambda err: gr.update(visible=bool(err)),
         inputs=[login_error_output],
         outputs=[login_error_output]
    )
    signup_error_output.change(
         fn=lambda err: gr.update(visible=bool(err)),
         inputs=[signup_error_output],
         outputs=[signup_error_output]
    )
    view_notes_button.click(
        fn=show_notes_view,
        inputs=[],
        outputs=[notes_display_output, mood_chart_output, is_showing_chart]
    )
    
    view_mood_chart_button.click(
        fn=show_chart_view,
        inputs=[notes_data],
        outputs=[notes_display_output, mood_chart_output, is_showing_chart]
    )


if __name__ == "__main__":
    print(f"Connecting to Orchestrator at: {ORCHESTRATOR_BASE_URL}")
    print(f"Login Endpoint (Auth): {AUTH_ENDPOINT}")
    print(f"Register Endpoint: {REGISTER_ENDPOINT}")
    print(f"Get Notes Endpoint: {GET_NOTES_ENDPOINT}")
    assets_path = Path.cwd().absolute() / "assets"
    if not assets_path.exists():
        print(f"Warning: Assets directory not found at {assets_path}. Background image may not load.")
    elif not (assets_path / "image4.jpg").exists():
         print(f"Warning: Background image 'image4.jpg' not found in {assets_path}.")

    demo.launch(server_name="0.0.0.0", server_port=7860, debug=True)