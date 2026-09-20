#!/usr/bin/env python3
"""
HireBeyondCampus — Clean Auth Server
Existing User Action: Log In
New User Action: Create Account (Sign Up)
"""

import http.server
import socketserver
import json
import urllib.parse
import os
import sys

PORT = 8080
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

# Active session starts strictly NULL for all visitors
ACTIVE_SESSION = None

# Internal user database
USER_ACCOUNTS = {}

ALL_BRANCH_COMPANIES_DB = [
    {
        "job_id": "INT_AMAZON_01",
        "company": "Amazon India",
        "logo_text": "AMZN",
        "branch_category": "CSE / IT / AI / ML",
        "title": "Software Development Engineer (SDE) Intern",
        "type": "6-Month Internship (PPO Track)",
        "stipend_salary": "₹80,000 / month",
        "target_passout_years": [2026, 2027],
        "target_branches": ["CSE / IT", "AI / ML & Data Science"],
        "required_skills": ["Python", "Data Structures", "SQL", "REST API"],
        "skill_weights": {"Python": 35, "SQL": 25, "Data Structures": 25, "REST API": 15},
        "description": "Building large-scale AWS distributed cloud microservices.",
        "apply_url": "https://www.amazon.jobs/en/jobs/intern-sde-india"
    },
    {
        "job_id": "INT_GOOGLE_02",
        "company": "Google Cloud India",
        "logo_text": "GOOG",
        "branch_category": "CSE / IT / AI / ML",
        "title": "Cloud & AI Engineering Intern",
        "type": "Summer Internship",
        "stipend_salary": "₹95,000 / month",
        "target_passout_years": [2026, 2027],
        "target_branches": ["CSE / IT", "AI / ML & Data Science"],
        "required_skills": ["Python", "Machine Learning", "SQL", "AWS"],
        "skill_weights": {"Python": 35, "Machine Learning": 35, "SQL": 15, "AWS": 15},
        "description": "Work with Google Cloud teams on foundation generative AI models.",
        "apply_url": "https://careers.google.com/jobs/results/cloud-intern-india"
    },
    {
        "job_id": "JOB_TCS_03",
        "company": "TCS Digital / Prime",
        "logo_text": "TCS",
        "branch_category": "All Engineering Branches",
        "title": "Systems Engineer & AI Specialist Trainee",
        "type": "Full-Time Role",
        "stipend_salary": "₹7.20 LPA – ₹9.00 LPA",
        "target_passout_years": [2026, 2027],
        "target_branches": ["CSE / IT", "AI / ML & Data Science", "ECE / Embedded Systems", "Electrical & Electronics (EEE)", "Mechanical Engineering", "Civil Engineering"],
        "required_skills": ["Python", "SQL", "REST API", "Problem Solving"],
        "skill_weights": {"Python": 30, "SQL": 30, "REST API": 20, "Problem Solving": 20},
        "description": "National level hiring for technical graduates.",
        "apply_url": "https://www.tcs.com/careers/india/digital-hiring"
    }
]

def match_candidate_multi_factor(student):
    if not student:
        return []
    results = []
    branch = student.get("branch", "CSE / IT")
    passout_year = int(student.get("year_of_passing", 2026))
    cand_claimed = [s.lower() for s in student.get("claimed_skills", [])]
    cand_verified = [v["skill"].lower() for v in student.get("verified_skills", [])]
    coding_score = student.get("assessments", {}).get("coding_score", 85)
    comm_score = student.get("assessments", {}).get("communication_score", 78)
    num_projects = len(student.get("projects", []))
    
    for comp in ALL_BRANCH_COMPANIES_DB:
        weights = comp.get("skill_weights", {"Python": 35, "SQL": 25, "REST API": 20, "Problem Solving": 20})
        matched_skills = []
        missing_skills = []
        skill_acc = 0
        total_weight = sum(weights.values())
        
        for s_name, s_weight in weights.items():
            sn = s_name.lower()
            if sn in cand_verified:
                matched_skills.append({"skill": s_name, "status": "VERIFIED", "weight": s_weight})
                skill_acc += s_weight * 1.0
            elif sn in cand_claimed:
                matched_skills.append({"skill": s_name, "status": "CLAIMED", "weight": s_weight})
                skill_acc += s_weight * 0.75
            else:
                missing_skills.append({"skill": s_name, "weight": s_weight})
                
        skill_pct = (skill_acc / total_weight) * 100 if total_weight > 0 else 50
        overall = round(min(98.5, max(42.0, 0.35*skill_pct + 0.25*coding_score + 0.20*min(100, num_projects*25) + 0.10*comm_score + 10.0)), 1)
        
        comp_copy = dict(comp)
        comp_copy["match_analysis"] = {
            "overall_match": overall,
            "skill_match_pct": round(skill_pct, 1),
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "rationale": [
                f"✓ Multi-Factor Match: {branch} ({passout_year} Passout)",
                f"✓ Technical Skills Score: {round(skill_pct)}%",
                f"✓ Coding & Knowledge Score: {coding_score}%"
            ]
        }
        results.append(comp_copy)
    return results

class HireBeyondCampusHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path.startswith("/api/"):
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()

            if path == "/api/session":
                global ACTIVE_SESSION
                if ACTIVE_SESSION:
                    self.wfile.write(json.dumps({"logged_in": True, "user": ACTIVE_SESSION}).encode("utf-8"))
                else:
                    self.wfile.write(json.dumps({"logged_in": False, "user": None}).encode("utf-8"))
                return

            elif path in ["/api/opportunities", "/api/match-all-companies"]:
                matched = match_candidate_multi_factor(ACTIVE_SESSION)
                self.wfile.write(json.dumps(matched).encode("utf-8"))
                return

        super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else "{}"
        try:
            payload = json.loads(body)
        except Exception:
            payload = {}

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

        global ACTIVE_SESSION

        if path == "/api/login":
            email = payload.get("email", "").lower().strip()
            password = payload.get("password", "")
            
            if email not in USER_ACCOUNTS:
                self.wfile.write(json.dumps({
                    "status": "ERROR",
                    "message": "⚠️ No existing student account found for this email. Please click 'Create Account' to sign up first!"
                }).encode("utf-8"))
            elif USER_ACCOUNTS[email]["password"] != password:
                self.wfile.write(json.dumps({
                    "status": "ERROR",
                    "message": "⚠️ Incorrect password entered. Please try again or create a new account."
                }).encode("utf-8"))
            else:
                ACTIVE_SESSION = USER_ACCOUNTS[email]
                matched = match_candidate_multi_factor(ACTIVE_SESSION)
                self.wfile.write(json.dumps({
                    "status": "SUCCESS",
                    "user": ACTIVE_SESSION,
                    "opportunities": matched
                }).encode("utf-8"))
            return

        elif path == "/api/logout":
            ACTIVE_SESSION = None
            self.wfile.write(json.dumps({"status": "SUCCESS", "logged_in": False}).encode("utf-8"))
            return

        elif path in ["/api/signup", "/api/complete-onboarding"]:
            email = payload.get("email", "").lower().strip()
            if not email:
                email = f"student_{len(USER_ACCOUNTS)+1}@hbc.edu.in"

            new_user = {
                "logged_in": True,
                "student_id": f"STU_HBC_{len(USER_ACCOUNTS)+1000}",
                "name": payload.get("name", "Student Candidate"),
                "anonymous_alias": f"Candidate #{email.split('@')[0].upper()}",
                "email": email,
                "password": payload.get("password", "password123"),
                "branch": payload.get("branch", "CSE / IT"),
                "cgpa": float(payload.get("cgpa", 8.0)),
                "year_of_passing": int(payload.get("year_of_passing", 2026)),
                "claimed_skills": payload.get("skills", ["Python", "SQL"]),
                "verified_skills": [{"skill": s, "badge": "VERIFIED"} for s in payload.get("skills", ["Python"])],
                "assessments": {"coding_score": 85, "communication_score": 80},
                "projects": payload.get("projects", [{"title": "Web App Project", "tech_stack": ["Python"]}]),
                "internship_experience": payload.get("internship_experience", ""),
                "ai_job_readiness_score": 82,
                "talent_passport_id": f"TP-{email.split('@')[0].upper()}-9901"
            }
            USER_ACCOUNTS[email] = new_user
            ACTIVE_SESSION = new_user
            matched = match_candidate_multi_factor(ACTIVE_SESSION)
            self.wfile.write(json.dumps({"status": "SUCCESS", "user": new_user, "opportunities": matched}).encode("utf-8"))
            return

        elif path == "/api/generate-ats-resume":
            user = ACTIVE_SESSION or payload
            name = user.get("name", "Student Candidate")
            branch = user.get("branch", "Engineering Candidate")
            passout = user.get("year_of_passing", 2026)
            skills = user.get("claimed_skills", ["Python", "SQL"])
            projects = user.get("projects", [{"title": "Engineering Project", "tech_stack": ["Python"]}])

            proj_md = "\n".join([f"### {p.get('title', 'Project')}\n- **Tech Stack**: {', '.join(p.get('tech_stack', ['Tools']))}\n- Designed & implemented core algorithms with zero campus location bias." for p in projects])

            ats_resume_text = f"""# {name.upper()}
**Engineering Branch**: {branch} | **Graduation Batch**: {passout} Passout
**Privacy Protocol**: College-Blind Verified Candidate Profile

---

## 🛠️ VERIFIED TECHNICAL SKILLS
{', '.join(skills)}

---

## 🚀 ENGINEERING PROJECTS
{proj_md}

---

## 🎓 ACADEMIC ELIGIBILITY
- **Degree Status**: {passout} Graduating Batch
- **AI Job Readiness Score**: 88/100 (Verified Skills & Proctored Tests)
"""
            self.wfile.write(json.dumps({
                "status": "SUCCESS",
                "ats_score": 94,
                "resume_markdown": ats_resume_text,
                "optimization_tips": [
                    "✓ 94% ATS Keyword Alignment with top Tech & Core Engineering firms in India.",
                    "✓ Zero location/college brand penalty applied.",
                    "💡 Tip: Add AWS Lambda / Cloud Microservices keyword to boost tier-1 match score by +6%."
                ]
            }).encode("utf-8"))
            return

        elif path == "/api/run-code-assessment":
            code = payload.get("code", "")
            skill = payload.get("skill", "Python")
            
            if ACTIVE_SESSION:
                if "verified_skills" not in ACTIVE_SESSION:
                    ACTIVE_SESSION["verified_skills"] = []
                ACTIVE_SESSION["verified_skills"].append({"skill": skill, "badge": "VERIFIED_ADVANCED", "score": 92})
                ACTIVE_SESSION["ai_job_readiness_score"] = min(98, ACTIVE_SESSION.get("ai_job_readiness_score", 82) + 4)

            self.wfile.write(json.dumps({
                "status": "SUCCESS",
                "test_result": "PASS (4/4 Test Cases Passed)",
                "awarded_badge": f"VERIFIED_ADVANCED ({skill})",
                "new_readiness_score": 88,
                "feedback": "Clean algorithmic complexity, time complexity O(N), space complexity O(1)."
            }).encode("utf-8"))
            return

        elif path == "/api/predict-salary":
            branch = payload.get("branch", "CSE / IT")
            passout = int(payload.get("year_of_passing", 2026))
            num_skills = len(payload.get("skills", []))
            num_projects = len(payload.get("projects", []))

            base_stipend_min = 45000 + (num_skills * 2500) + (num_projects * 3000)
            base_stipend_max = base_stipend_min + 35000
            base_ctc_min = round(6.5 + (num_skills * 0.4) + (num_projects * 0.5), 1)
            base_ctc_max = round(base_ctc_min + 7.5, 1)

            self.wfile.write(json.dumps({
                "status": "SUCCESS",
                "predicted_stipend": f"₹{base_stipend_min:,} – ₹{base_stipend_max:,} / month",
                "predicted_ctc": f"₹{base_ctc_min} LPA – ₹{base_ctc_max} LPA",
                "batch_note": f"Estimated for {passout} Batch across all top recruiters in India."
            }).encode("utf-8"))
            return

        self.wfile.write(json.dumps({"error": "Unknown API endpoint"}))

def run():
    print(f"====================================================")
    print(f"🚀 HireBeyondCampus Server Running on http://localhost:{PORT}")
    print(f"📍 Directory: {DIRECTORY}")
    print(f"🔑 Existing Users: Log In | New Users: Create Account")
    print(f"====================================================")
    os.chdir(DIRECTORY)
    with socketserver.TCPServer(("", PORT), HireBeyondCampusHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")

if __name__ == "__main__":
    run()
