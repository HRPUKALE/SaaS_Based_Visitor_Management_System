from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from pydantic import BaseModel
from datetime import date
import pymysql
import os
from dotenv import load_dotenv
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from gemini_utils import send_to_gemini

# Load environment variables
load_dotenv()

# MySQL connection settings
MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', 'Hrpukale@131')
MYSQL_DB = os.environ.get('MYSQL_DB', 'voice_assistant_saas')

# FastAPI app with lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    # ✅ Startup logic: Create table if not exists
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(CREATE_TABLE_SQL)
        conn.commit()
    yield
    # 🔻 Add shutdown logic if needed

app = FastAPI(lifespan=lifespan)

# Enable CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Appointment model
class AppointmentBooking(BaseModel):
    employee_name: str
    department: str
    reason: str
    appointment_time: str
    visitor_name: str
    email: str
    phone: str
    appointment_date: str

# SQL to create bookings table
CREATE_TABLE_SQL = '''
CREATE TABLE IF NOT EXISTS bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(20),
    department VARCHAR(100),
    employee VARCHAR(100),
    date DATE,
    time TIME,
    reason TEXT
)
'''

def get_connection():
    return pymysql.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB,
        cursorclass=pymysql.cursors.DictCursor
    )

@app.post("/api/appointments")
def create_appointment(booking: AppointmentBooking):
    try:
        conn = get_connection()
        with conn:
            with conn.cursor() as cursor:
                sql = '''
                INSERT INTO bookings (name, email, phone, department, employee, date, time, reason)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                '''
                cursor.execute(sql, (
                    booking.visitor_name,
                    booking.email,
                    booking.phone,
                    booking.department,
                    booking.employee_name,
                    booking.appointment_date,
                    booking.appointment_time,
                    booking.reason
                ))
            conn.commit()
        return {"message": "Appointment saved successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/ping")
def ping():
    return {"message": "API is alive"}

# ---- Appointment Assistant Logic ----

def is_valid_value(val):
    return bool(val and str(val).strip().lower() not in ["none", "null"])

def all_fields_filled(state):
    return all(is_valid_value(state[k]) for k in [
        "employee_name", "department", "reason", "appointment_time",
        "visitor_name", "email", "phone"
    ])

def build_dynamic_prompt(state):
    missing = []
    if not is_valid_value(state["reason"]): missing.append("reason for appointment")
    if not is_valid_value(state["appointment_time"]): missing.append("appointment time")
    if not is_valid_value(state["visitor_name"]): missing.append("visitor's name")
    if not is_valid_value(state["email"]): missing.append("visitor's email")
    if not is_valid_value(state["phone"]): missing.append("visitor's phone number")

    if missing:
        return "Please provide: " + ", ".join(missing) + "."
    else:
        return (
            f"Here is a summary. Confirm if this is correct:\n"
            f"Employee: {state['employee_name']} ({state['department']})\n"
            f"Reason: {state['reason']}\n"
            f"Time: {state['appointment_time']}\n"
            f"Visitor: {state['visitor_name']}\n"
            f"Email: {state['email']}\n"
            f"Phone: {state['phone']}\n"
            f"Date: {state['appointment_date']} (today)"
        )

def run_assistant(messages, state=None, confirmed=False):
    if state is None:
        state = {
            "employee_name": None,
            "department": None,
            "reason": None,
            "appointment_time": None,
            "visitor_name": None,
            "email": None,
            "phone": None,
            "appointment_date": str(date.today())
        }

    client = chromadb.PersistentClient(path="./employee_db")
    collection = client.get_or_create_collection(
        name="employee_collection",
        embedding_function=SentenceTransformerEmbeddingFunction("all-MiniLM-L6-v2")
    )

    conversation = [{
        "role": "system",
        "content": (
            "You are an appointment booking assistant for Kanishka Software. "
            "You ONLY help visitors book appointments with employees. "
            "The employee name and department must be determined from the database. "
            "You only need to collect: reason for appointment, time (today only), visitor name, email, and phone. "
            "Do NOT ask for or mention the date; always use today's date internally. "
            "Only allow appointment times between 9:00 AM and 4:30 PM."
        )
    }] + messages

    def extract_possible_name(text):
        import re
        text = text.strip()
        if not text or "@" in text or any(char.isdigit() for char in text):
            return None
        confirm_words = {"yes", "haan", "ho", "done", "ok", "sure", "confirm"}
        if text.lower() in confirm_words:
            return None
        match = re.search(r"([A-Z][a-z]+( [A-Z][a-z]+)*)", text)
        if match:
            return match.group(0)
        if len(text.split()) <= 4:
            return text
        return None

    last_user_msg = next((msg["content"] for msg in reversed(messages) if msg["role"] == "user"), "")

    if not state["employee_name"] and last_user_msg:
        possible_name = extract_possible_name(last_user_msg)
        if possible_name:
            result = collection.query(query_texts=[possible_name], n_results=3)
            top_matches = result["metadatas"][0] if result["metadatas"][0] else []
            if top_matches:
                options = ", ".join(f"{e['employee_name']} ({e['department']})" for e in top_matches)
                ask = (
                    f"The user mentioned '{possible_name}'. Top matches are: {options}. "
                    "Which one is most correct? Reply only in format: Name | Department."
                )
                conversation.append({"role": "user", "content": ask})
                gemini_choice, _, _ = send_to_gemini(conversation)
                if '|' in gemini_choice:
                    emp, dept = map(str.strip, gemini_choice.split('|', 1))
                    state["employee_name"] = emp
                    state["department"] = dept
                else:
                    state["employee_name"] = top_matches[0]["employee_name"]
                    state["department"] = top_matches[0]["department"]
                return build_dynamic_prompt(state), state, None, False

    gemini_response, _, _ = send_to_gemini(conversation)

    lower_msg = last_user_msg.lower()
    if "interview" in lower_msg: state["reason"] = "Interview"
    if "pm" in lower_msg or "am" in lower_msg: state["appointment_time"] = last_user_msg
    if "@" in lower_msg:
        try:
            state["email"] = lower_msg.split()[-1].split("@")[0] + "@" + lower_msg.split("@")[1].split()[0]
        except: pass
    if "name is" in lower_msg:
        state["visitor_name"] = lower_msg.split("name is")[-1].split(",")[0].strip()
    if any(char.isdigit() for char in lower_msg):
        for word in lower_msg.split():
            if word.isdigit() and len(word) >= 8:
                state["phone"] = word

    if all_fields_filled(state) and not confirmed:
        return build_dynamic_prompt(state) + "\nAre all the details correct? (Type yes to confirm)", state, None, True

    if confirmed:
        booking_json = state.copy()
        state = {k: None for k in state}
        state["appointment_date"] = str(date.today())
        return "Appointment booked successfully!", state, booking_json, False

    return gemini_response, state, None, False
