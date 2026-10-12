# Next Genn Edu - Tuition Classroom WhatsApp Assistant

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Privacy: Guaranteed](https://img.shields.io/badge/Student%20Privacy-Strictly%20Enforced-green.svg)](#privacy--data-protection-guarantees)

An intelligent, privacy-first educational relay assistant built for tuition centers and private educators (**Next Genn Edu**). It connects teachers and students over WhatsApp to streamline question-answering, homework review, and lesson timetable rescheduling while strictly isolating student identities and schedule commitments.

---

## 🌟 Key Features

1. **Verified Classroom Enrollment Routing**:
   - Matches incoming WhatsApp phone numbers and LIDs strictly against authorized classroom pairs.
   - Prevents unauthorized third parties or unrelated students from accessing teacher channels or invoking actions.

2. **Multilingual Interaction Engine**:
   - Automatically identifies and honors language preferences across **Chinese (zh)**, **English (en)**, and **Malay (ms)**.
   - Preserves natural conversation tone without forcing unnatural translations.

3. **Intelligent Rescheduling Negotiation**:
   - Enables students or teachers to propose replacement slots for missed/rescheduled lessons.
   - Checks mutual calendar availability and detects slot collisions **without ever disclosing third-party course schedules or student names**.
   - Supports carry-forward policy into subsequent months.

4. **Educational Message & Media Relay**:
   - Students submit questions (with photo worksheets) directly to their assigned teacher.
   - Teachers deliver feedback, answers, and homework directly to the enrolled student.

5. **Hardened Security & Privacy Guard**:
   - Automatically redacts API keys, credentials, and internal system paths from outgoing text.
   - Ingress boundary blocks gateway/system command injection (`/help`, `/status`) from classroom chats.

---

## 🏗️ Project Architecture

```text
nextgenn-tuition-assistant/
├── config/
│   ├── roster.example.json      # Mock enrollment roster (anonymized phones/LIDs)
│   └── settings.example.yaml    # Timezone, policies & duration settings
├── src/
│   ├── __init__.py
│   ├── config.py                # Environment and configuration loader
│   ├── core/
│   │   ├── __init__.py
│   │   ├── models.py            # Participant, Classroom, LessonSlot, Proposal models
│   │   ├── language.py          # Multilingual engine (zh / en / ms)
│   │   └── security.py          # Token redaction & injection prevention
│   ├── services/
│   │   ├── __init__.py
│   │   ├── roster_service.py    # Participant identity verification
│   │   ├── timetable_service.py # Recurrence, slot math & collision detector
│   │   ├── reschedule_service.py# Rescheduling proposals & accept/reject status
│   │   └── relay_service.py     # Educational question/answer relay
│   └── adapter/
│       ├── __init__.py
│       └── whatsapp_adapter.py  # Ingress boundary & control barrier
├── tests/
│   ├── __init__.py
│   └── test_tuition.py          # Unit tests (security, language, timetable, relay)
├── .env.example
├── .gitignore                   # Excludes real roster, media, and state files
├── requirements.txt
└── README.md
```

---

## 🚀 Quick Start

### 1. Installation
```bash
git clone https://github.com/kelvinyi2004/nextgenn-tuition-assistant.git
cd nextgenn-tuition-assistant

# Optional: Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Roster & Settings
```bash
cp .env.example .env
cp config/roster.example.json config/roster.json
```
Edit `config/roster.json` to register your authorized teachers and students.

### 3. Run Verification Tests
```bash
python3 -m unittest discover tests
```

---

## 🔒 Privacy & Data Protection Guarantees

- **No Student Data Committed**: Real rosters (`config/roster.json`), class states (`data/`), photos (`photos/`), and session tokens are strictly excluded via `.gitignore`.
- **Zero Information Leakage during Scheduling**: Availability checks report only free/busy status to counterparts; other classes or student names are never revealed.
- **Zero Ingress Command Escalation**: Classroom participants are restricted exclusively to educational relaying and cannot trigger system commands.

---

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.
