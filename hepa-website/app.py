import os
from flask import Flask, render_template, abort
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Demo data
SERVICES = [
    {"slug": "network-engineering", "title": "Network Engineering", "content": "We design and optimize enterprise networks for speed, security, and reliability.", "features": ["LAN/WAN Design", "BGP, OSPF, EVPN", "Wireless Solutions"]},
    {"slug": "devops", "title": "DevOps & Platform Engineering", "content": "Automate and accelerate software delivery with CI/CD and infrastructure as code.", "features": ["CI/CD Pipelines", "Terraform & Ansible", "Monitoring & Observability"]},
    {"slug": "cloud", "title": "Cloud Solutions", "content": "AWS, Azure, and hybrid-cloud architecture, migrations, and ops.", "features": ["Cloud Migration", "Serverless", "Security & Compliance"]},
    {"slug": "cybersecurity", "title": "Cyber Security & Compliance", "content": "Protect your business with audits, vulnerability scans, and policy design.", "features": ["Vulnerability Scanning", "Policy & Audit", "Incident Response"]},
    {"slug": "it-support", "title": "IT Support & Managed Services", "content": "24/7 helpdesk, remote monitoring, and managed IT for your business.", "features": ["Remote Helpdesk", "SLAs", "Patch Management"]},
]

PROJECTS = [
    {"slug": "dc-automation-platform", "title": "DC Automation Platform", "summary": "Automated provisioning across VLANs & data centers.", "content": "End-to-end bare-metal and cloud automation for modern data centers.", "results": "70% reduction in manual deployment time."},
    {"slug": "secure-iot-rollout", "title": "Secure IoT Rollout", "summary": "Securing smart device deployments.", "content": "IoT devices securely onboarded and managed at scale.", "results": "Zero security incidents, rapid rollout."}
]

TEAM = [
    {"name": "Ardian Krasniqi", "role": "Lead Network Engineer", "photo": "team1.jpg"},
    {"name": "Blerim Dervishi", "role": "DevOps & Automation Engineer", "photo": "team2.jpg"},
    {"name": "Elira Gashi", "role": "Business Manager", "photo": "team3.jpg"},
]

@app.route("/")
def index():
    return render_template("index.html", services=SERVICES, projects=PROJECTS, team=TEAM)

@app.route("/services")
def services():
    return render_template("services.html", services=SERVICES)

@app.route("/services/<slug>")
def service_detail(slug):
    svc = next((s for s in SERVICES if s["slug"] == slug), None)
    if not svc:
        abort(404)
    return render_template("service_detail.html", service=svc)

@app.route("/projects")
def projects():
    return render_template("projects.html", projects=PROJECTS)

@app.route("/projects/<slug>")
def project_detail(slug):
    proj = next((p for p in PROJECTS if p["slug"] == slug), None)
    if not proj:
        abort(404)
    return render_template("project_detail.html", project=proj)

@app.route("/team")
def team():
    return render_template("team.html", team=TEAM)

@app.route("/contact")
def contact():
    return render_template("contact.html")

if __name__ == "__main__":
    app.run(debug=True)
