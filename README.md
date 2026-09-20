# HireBeyondCampus (HBC)

> **AI-Powered Placement & Opportunity Engine for Engineering Students Across India**  
> *"Talent should be discovered, not limited by campus location."*

---

## 🌟 Overview

**HireBeyondCampus** is an intelligent placement platform designed to connect engineering students across India directly with top tech and core engineering companies (Amazon, Google Cloud, TCS Digital, Swiggy, Microsoft) based on **Branch, Skills, Verified Knowledge, Projects, Passout Batch (2026/2027), and Resume** — without requesting college names or geographic location.

---

## 🚀 Key Features

* 🔒 **Zero College & Zero Location Privacy Policy**: Eliminates campus-brand and geographic discrimination. Candidate passports are anonymized (`Candidate #A1042`).
* 🎓 **Passout Batch Scope (2026 & 2027 Only)**: Tailored specifically for **2026 Passout (Final Year)** and **2027 Passout (Pre-Final Year)** graduating batches.
* 🔤 **Alphabetically Sorted Engineering Branches**: Dropdown placeholder `-- Select Engineering Branch --` leading to 30+ sorted branches (Aeronautical, AI & DS, AI & ML, Civil, CSE, ECE, EEE, Mechanical, Robotics, etc.).
* 🛠️ **50+ Technical Skills Grid**: Comprehensive skills categorized into CS/Software, AI/ML, ECE/EEE, Mechanical/Robotics, Civil, and Chemical streams. Enforces a strict **Max 10 Skill Limit**.
* 📁 **Dynamic Projects Manager**: Students can add **up to 10 projects** with tech stack details.
* 📄 **Final Step Resume Upload**: Resume upload is placed at **Step 5 (the final onboarding question)** alongside internship experience.
* 🔒 **Standard Password Format Rules**: Enforces 8+ characters, uppercase (A-Z), lowercase (a-z), number (0-9), and special character (`@$!%*...`).
* 🛡️ **New User Login Guard**: Unregistered logins are blocked and prompted with a direct CTA to create an account first.
* ✨ **Amazon Bedrock AI ATS Resume Builder**: Generates ATS-compliant Markdown resumes with a **94/100 ATS Match Score** and 1-click Markdown export.
* 💻 **Live Proctored Code Playground**: Embedded code editor that executes test cases, awards `VERIFIED_ADVANCED` badges, and updates candidate readiness scores to **88/100**.
* 💰 **AI Salary & Stipend Predictor**: Calculates real-time estimated internship stipends (`₹55,000 – ₹90,000 / month`) and full-time CTC trajectories (`₹8.5 LPA – ₹18.0 LPA`).
* 📊 **AI Skill Deficit Heatmap**: Compares candidate skills against 2026/2027 All-India hiring benchmarks and generates a 4-Week Training Roadmap.

---

## ☁️ AWS Cloud Architecture

```
                               ┌─────────────────────────────────────────┐
                               │            FRONTEND USERS               │
                               │  [Students]   [Recruiters]   [Colleges] │
                               └────────────────────┬────────────────────┘
                                                    │
                                                    ▼
                               ┌─────────────────────────────────────────┐
                               │          AWS AMPLIFY / S3 + CDN         │
                               │       HireBeyondCampus Web Application  │
                               └────────────────────┬────────────────────┘
                                                    │
                                                    ▼
                               ┌─────────────────────────────────────────┐
                               │            AMAZON COGNITO               │
                               │    JWT Auth & Role-Based Access Control │
                               └────────────────────┬────────────────────┘
                                                    │
                                                    ▼
                               ┌─────────────────────────────────────────┐
                               │           AMAZON API GATEWAY            │
                               │       REST API / WebSocket Routes       │
                               └────────────────────┬────────────────────┘
                                                    │
                                                    ▼
                               ┌─────────────────────────────────────────┐
                               │               AWS LAMBDA                │
                               │    Microservices & Serverless Logic     │
                               └───────┬────────────┬────────────┬───────┘
                                       │            │            │
           ┌───────────────────────────┘            │            └───────────────────────────┐
           ▼                                        ▼                                        ▼
 ┌──────────────────┐                    ┌──────────────────┐                    ┌──────────────────┐
 │  AMAZON BEDROCK  │                    │ AMAZON DYNAMODB  │                    │    AMAZON S3     │
 │ Claude 3 Sonnet  │                    │ Single-Table DB  │                    │ Resumes & Badges │
 ├──────────────────┤                    ├──────────────────┤                    ├──────────────────┤
 │ • Resume Parser  │                    │ • Students Table │                    │ • /resumes/*.pdf │
 │ • ATS Generator  │                    │ • Jobs Table     │                    │ • /badges/*.json │
 │ • AI Interview   │                    │ • Assessments    │                    │ • /passports/*   │
 │ • Skill-Gap Path │                    └──────────────────┘                    └──────────────────┘
 └──────────────────┘                               │
                                                    ▼
                                         ┌──────────────────┐
                                         │ SAGEMAKER INFER  │
                                         │  Matching Math   │
                                         └──────────────────┘
```

---

## 🛠️ Tech Stack

* **Frontend**: HTML5, Tailwind CSS, Lucide Icons, JavaScript (ES6+), Chart.js
* **Backend**: Python 3.13 (`http.server` native REST API engine)
* **Cloud & Serverless**: AWS Amplify, AWS Lambda, Amazon API Gateway, Amazon DynamoDB, Amazon Bedrock, Amazon Cognito, AWS SAM CLI

---

## 🚀 Quick Start (Run Locally)

### Option A: Direct Web Browser (Offline Mode)
Open `index.html` directly in any web browser (Chrome, Safari, Edge, Firefox).

### Option B: Local Python API Server
```bash
# Clone the repository
git clone https://github.com/SathvikaEswar/HireBeyondCampus.git
cd HireBeyondCampus

# Run Python 3.13 backend server
python3 server.py
```
Open **http://localhost:8080** in your browser.

---

## 🚢 AWS Builder Center Shipping Commands

```bash
# 1. Build Serverless Stack
sam build -t template.yaml

# 2. Deploy AWS Infrastructure Stack
sam deploy --stack-name HireBeyondCampusStack --capabilities CAPABILITY_IAM --region ap-south-1

# 3. Publish Web UI to AWS Amplify Edge
aws amplify create-app --name HireBeyondCampus --platform WEB
```

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.
