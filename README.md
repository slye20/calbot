# ✅ Project Spec: AI Calendar Assistant using Google Calendar API

## 🔥 Project Name
**CalBot** — Your AI-powered personal calendar assistant

---

## 🧠 What It Does

A chatbot (via API or UI) that understands natural language and performs scheduling tasks using Google Calendar:

### 🗣️ Sample Prompts:
- "Schedule a meeting with Sarah at 2pm tomorrow"
- "What’s on my calendar for Friday?"
- "Cancel my 3pm meeting today"
- "Reschedule my meeting with Alex to next Tuesday at 10am"

---

## 🔧 Core Features

### 1. **Natural Language Scheduling**
- Parse date, time, title, and participants from user input
- Create calendar events using Google Calendar API

### 2. **List Upcoming Events**
- Show next `n` events or events on a specific day
- Filter by calendar, keyword, or time

### 3. **Cancel Events**
- Find event by title/time
- Cancel or delete from Google Calendar

### 4. **Reschedule Events**
- Find a specific event and update its time or date

---

## ✨ Bonus Features (Optional)
- Use OpenAI to suggest meeting titles or agendas
- Integrate with Gmail to detect recent contacts
- Summarize daily schedule at start of day

---

## 🧱 Tech Stack

| Layer | Stack |
|-------|-------|
| AI | OpenAI GPT-4 + Function Calling |
| Backend | Python (FastAPI or Flask) |
| API | Google Calendar API (via `google-api-python-client`) |
| Auth | Google OAuth 2.0 (user consent screen) |
| Optional Frontend | Streamlit / Next.js / React chatbot UI |

---

## ✅ User Flow

1. **User authenticates with Google** (OAuth)
2. **User sends a natural prompt** → GPT interprets
3. **GPT uses function calling** to invoke backend function
4. **Backend talks to Google Calendar API**
5. **Bot replies with confirmation / list / action result**

---

## 🔐 Auth Notes
- You'll need to set up a Google Cloud Project
- Enable Google Calendar API
- Implement OAuth 2.0 for user access
  - `https://www.googleapis.com/auth/calendar`

---

## 🧪 Testing Ideas
- “Book a call with John next Friday at 11am”
- “Move my 1pm meeting to 4pm today”
- “What do I have on Wednesday?”
- “Cancel my Zoom call tomorrow”

---