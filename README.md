# 🛡️ FraudLens

**AI-Powered Mule Account & Suspicious Transaction Detection System**

> CyberShield PSBs Hackathon Series 2026  
> Bank of India + IIT Hyderabad | Prize Pool: Rs. 20 Lakhs  
> An Initiative of Govt. of India, Ministry of Finance

---

## 👥 Team

| Role | Name |
|---|---|
| **Team Lead + ML Engineer** | Ashutosh |
| **Dashboard Developer** | Diksha |
| **Graph Analytics Engineer** | Divyansh Pratap Singh |
| **Data + Integration Engineer** | Garvit Agrawal |

**Institution:** GL Bajaj Group of Institutions, Mathura (CSE, AI/ML Specialization)

**GitHub:** https://github.com/dikshaashadeep-ship-it/fraudlens-hackathon

---

## 🎯 Problem Statement

Every day, criminals move stolen money through innocent people's bank accounts — these are called **mule accounts**. Detecting them manually from millions of daily transactions is impossible for investigators. Traditional rule-based systems produce excessive false alerts and miss hidden fraud networks spanning multiple accounts.

**Our solution:** An AI-powered system that automatically detects suspicious transactions, discovers mule account networks, assigns risk scores, and explains each fraud case in plain English — all from a simple CSV file upload on a clean web dashboard.

---

## 💡 Our Unique Idea — FraudLens

*"An AI-powered fraud intelligence platform that detects suspicious transactions, uncovers mule-account networks, and generates explainable risk insights in real time."*

### 1. 🕸️ Visual Mule Network Graph
Every bank account is drawn as a **node** and every money transfer as an **edge**. Mule accounts appear as heavily connected hub-nodes — investigators can see the fraud network at a glance instead of reading thousands of rows.

### 2. 🤖 Gemini AI "Why is this fraud?" Explainer
For every flagged account, the system calls **Gemini API** and auto-generates a **3-line plain-English explanation**. No other beginner team will have AI-generated explanations — this is our **key differentiator**.

*Example:* "Account A1234 received Rs. 80,000 from 6 unrelated sources in 2 hours and transferred everything out within 15 minutes — mule account behavior. Risk Score: 91/100."

### 3. 📰 Fraud Alert Timeline
Flagged events appear in a **live timeline** sorted by time and risk score — like a news feed of fraud alerts. Intuitive and actionable for investigators.

---

## 🎲 Risk Scoring Model

Every transaction receives a score out of **100** based on weighted fraud indicators:

| Fraud Indicator | Points | Risk Band | Action |
|---|---|---|---|
| Large Transaction Amount | +30 | Unusual spending pattern |
| Rapid Multiple Transfers | +20 | Quick fund movement |
| Mule Account Pattern | +40 | Relay behavior detected |
| Blacklisted Receiver | +50 | Known fraud account |

**Risk Bands:**
- **0–30 (LOW):** Normal — monitor only
- **31–70 (MEDIUM):** Flag for review
- **71–100 (HIGH):** Immediate action needed

---

## ⚙️ System Workflow

```
1. CSV Upload  →  2. Data Cleaning  →  3. Risk Scoring  →  4. ML Model  →  5. Graph Analysis  →  6. Gemini AI  →  7. Dashboard
```

CSV upload → data validation & cleaning → rule-based risk scoring → ML anomaly detection → graph-based mule discovery → Gemini AI explanation → investigator dashboard with alerts & downloadable report.

---

## 🛠️ Tech Stack

| Component | Tool | Why Chosen |
|---|---|---|
| Data Processing | Python + Pandas | Easy to learn, most used in data science |
| ML Anomaly Detection | Scikit-Learn (Isolation Forest) | Free, beginner-friendly, powerful |
| Graph Visualization | NetworkX + Plotly | Industry standard for fraud graph analytics |
| Web Dashboard | Streamlit | Build web app in pure Python — no HTML needed |
| AI Explanations | Google Gemini API (Free tier) | Best-in-class GenAI, free for students |

---

## 🚀 Installation & Setup

### Prerequisites
- **Python 3.8+** (check: `python --version`)
- **Gemini API Key** (free tier: https://ai.google.dev)

### Step-by-Step Setup

**Step 1: Clone Repository**
```bash
git clone https://github.com/dikshaashadeep-ship-it/fraudlens-hackathon.git
cd fraudlens-hackathon
```

**Step 2: Create Virtual Environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python -m venv venv
source venv/bin/activate
```

**Step 3: Install Dependencies**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Step 4: Set Gemini API Key**
```bash
# Windows (Command Prompt)
set GEMINI_API_KEY=your_api_key_here

# Mac/Linux
export GEMINI_API_KEY="your_api_key_here"
```

**Step 5: Run Dashboard**
```bash
streamlit run app.py
```

**Opens at:** `http://localhost:8501` ✅

### Test with Sample Data
1. Upload CSV from `datasets/` folder
2. Dashboard auto-generates:
   - Risk scores (0–100) per transaction
   - Mule account network graph
   - Gemini AI explanations
   - Fraud alert timeline
   - Downloadable investigation report

---

## 👥 Team

| Name | Role |
|---|---|
| **Ashutosh** | Team Lead + ML Engineer |
| **Diksha** | Dashboard Developer |
| **Divyansh Pratap Singh** | Graph Analytics Engineer |
| **Garvit Agrawal** | Data + Integration Engineer |

**Institution:** GL Bajaj Group of Institutions, Mathura (CSE, AI/ML Specialization)

---

## 📝 Detailed Solution Approach

### Step 1 — Data Ingestion & Cleaning
User uploads transaction CSV via Streamlit. Python/Pandas handles missing values, data type validation, timestamp parsing, and feature engineering (e.g., transaction frequency per account per hour).

### Step 2 — Rule-Based Risk Scoring
Each transaction is scored 0–100 using weighted indicators: large amount (+30), rapid transfers (+20), mule relay pattern (+40), blacklisted receiver (+50). Scores above 70 are flagged **High Risk**.

### Step 3 — ML Anomaly Detection (Isolation Forest)
Scikit-Learn **Isolation Forest** detects statistical anomalies that rule-based scoring may miss. Anomaly prediction is combined with the risk score for final classification.

### Step 4 — Graph-Based Mule Detection (NetworkX)
Accounts modelled as graph nodes; transactions as directed edges. High in-degree (many senders) + high out-degree (many receivers) = probable mule node. Community detection reveals hidden fraud clusters.

### Step 5 — Gemini AI Explanation Engine
For each High Risk account, a structured prompt is sent to **Gemini API**. Response is a 3-line plain-English investigation summary — immediately actionable for non-technical investigators.

### Step 6 — Interactive Streamlit Dashboard
All outputs on one web app: color-coded risk table, Plotly charts, NetworkX network graph, fraud alert timeline, Gemini explanation panel, downloadable report.

---

## 📊 Dataset Description

**Since real bank transaction data is confidential, we use a synthetic (AI-generated) dataset that accurately mimics real-world fraud patterns.**

### Dataset 1 — Synthetic Transaction Data
500–1000 realistic transactions generated using Python (Pandas + NumPy).

| Column | Type | Description | Example |
|---|---|---|---|
| `transaction_id` | String | Unique transaction ID | TXN00123 |
| `sender_account` | String | Account sending money | ACC0045 |
| `receiver_account` | String | Account receiving money | MULE002 |
| `amount` | Float | Transaction amount (Rs.) | 82500.00 |
| `timestamp` | DateTime | Date and time | 2024-01-15 14:32 |
| `location` | String | City of transaction | Mumbai |
| `is_blacklisted` | Integer | 1 if blacklisted, else 0 | 1 |
| `risk_score` | Integer | Calculated risk score (0–100) | 91 |

### Dataset 2 — Fraud Alerts (Secondary)
Simulates government cyber-fraud tickets and bank fraud monitoring alerts.

| Column | Type | Description | Example |
|---|---|---|---|
| `alert_id` | String | Unique alert ID | ALT00056 |
| `account_id` | String | Flagged account | MULE002 |
| `alert_type` | String | Type of fraud alert | Rapid Transfer |
| `severity` | String | Low / Medium / High | High |
| `reported_by` | String | Bank System or Govt | Govt Cyber Cell |
| `alert_date` | Date | When alert generated | 2024-01-15 |

### Data Composition
- **75% Normal transactions:** Rs. 500–25,000, varied accounts, normal timing
- **25% Mule transactions:** Rs. 40,000–1,50,000, rapid transfers within 30 min
- **5 Mule accounts** (MULE001–MULE005) acting as fund relay hubs
- **3 Blacklisted accounts** pre-flagged in dataset
- **Reproducibility:** Python random seed=42

---

## 📂 Project Structure

```
fraudlens-hackathon/
├── app.py                    # Main Streamlit dashboard
├── requirements.txt
├── src/
│   ├── data_loader.py       # CSV ingestion & cleaning
│   ├── risk_scorer.py       # Rule-based scoring (0–100)
│   ├── ml_detector.py       # Isolation Forest anomaly detection
│   ├── graph_analyzer.py    # NetworkX mule account detection
│   ├── gemini_explainer.py  # Gemini API explanations
│   └── report_generator.py  # Investigation report export
├── datasets/
│   ├── synthetic_transactions.csv
│   └── fraud_alerts.csv
└── docs/
    └── README.md
```

---

## 📈 Expected Impact

| Metric | Without FraudLens | With FraudLens |
|---|---|---|
| **Manual Review** | Investigators manually review thousands of rows | AI auto-flags top accounts — ~80% time reduction |
| **Mule Detection** | Days to detect fraud network | Detected in under 5 seconds from CSV upload |
| **Fraud Explanation** | No explanation provided | Gemini AI writes plain-English reason per account |
| **Visual Overview** | No network visualization | Interactive graph shows full fraud picture |

---

## 📅 Project Timeline

| Phase | Duration | Deliverable |
|---|---|---|
| **Week 1** | Now – 10 June | Register, form team, GitHub repo, sample CSV dataset |
| **Week 2** | 10–17 June | Pandas cleaning, risk scoring logic, basic Streamlit dashboard |
| **Week 3** | 17–24 June | ML model (Isolation Forest), NetworkX graph, module integration |
| **Week 4** | 24 June–1 July | Gemini API explanations, fraud timeline, UI polish |
| **Week 5–7** | July–15 Aug | Testing, bug fixes, PPT + architecture diagram, demo video |
| **Final Week** | Before 27 Aug | Full rehearsal, final testing, IIT Hyderabad Grand Finale |

---

## 🏆 Hackathon Details

| Detail | Info |
|---|---|
| **Event** | PSB's Cybersecurity, Fraud & AI Hackathon 2026 |
| **Organizers** | Bank of India + IIT Hyderabad |
| **Initiative** | Govt. of India, Ministry of Finance, Dept. of Financial Services |
| **Problem Statement** | PS-2: Mule Account & Suspicious Transaction Detection |
| **Registration Deadline** | 15 June 2026 |
| **Grand Finale** | 27–28 August 2026 |
| **Prize Pool** | Rs. 20 Lakhs |
| **Eligibility** | Open to all students; teams of 3–4 members preferred |
| **Official Portal** | [boihackathon.cse.iith.ac.in](https://boihackathon.cse.iith.ac.in) |

---

## 📄 License

MIT License — see [LICENSE](./LICENSE) file.

---

**GL Bajaj Group of Institutions, Mathura | CyberShield PSBs Hackathon 2026**

*Built with ❤️ for real-world fraud detection impact* 🛡️