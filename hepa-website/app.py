<<<<<<< HEAD
import os
from flask import Flask, render_template, request, jsonify, abort
from flask_cors import CORS
from smtplib import SMTP_SSL
from email.message import EmailMessage
=======
from flask import Flask, render_template, abort
>>>>>>> 6fdd95a (Make homepage dynamic: loop services, industries, projects & tech)
from dotenv import load_dotenv
import os

<<<<<<< HEAD
# ─── Load environment ─────────────────────────────────────────────────────────
load_dotenv()  # expects a .env in your project root
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
EMAIL_TO   = os.getenv("EMAIL_TO")
if not EMAIL_USER or not EMAIL_PASS or not EMAIL_TO:
    raise RuntimeError("Missing EMAIL_USER, EMAIL_PASS, or EMAIL_TO in .env")

# ─── Email helper ─────────────────────────────────────────────────────────────
def _send_email(sender, password, recipient, subject, body):
    msg = EmailMessage()
    msg["From"] = sender
    msg["To"]   = recipient
    msg["Subject"] = subject
    msg.set_content(body)
    with SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender, password)
        smtp.send_message(msg)

# ─── Flask app setup ─────────────────────────────────────────────────────────
app = Flask(__name__)
CORS(app)

# ─── Your content definitions ─────────────────────────────────────────────────
SERVICES = [
    {"slug": "network-engineering",       "title": "Network Engineering", "description": "…your copy here…"},
    {"slug": "devops",                     "title": "DevOps & Platform Engineering", "description": "…"},
    {"slug": "cloud",                      "title": "Cloud Solutions (AWS, Azure)",    "description": "…"},
    {"slug": "cybersecurity",              "title": "Cyber Security & Compliance",      "description": "…"},
    {"slug": "it-support",                 "title": "IT Support & Managed Services",    "description": "…"},
    {"slug": "automation",                 "title": "Automation (CI/CD, Infra, Workflows)", "description": "…"},
    {"slug": "data-iot",                   "title": "Data Analytics & IoT",             "description": "…"},
    {"slug": "web-mobile",                 "title": "Web & Mobile Development",         "description": "…"},
    {"slug": "consulting",                 "title": "Digital Transformation Consulting", "description": "…"},
    {"slug": "training",                   "title": "Training & Workshops",             "description": "…"},
]

INDUSTRIES = [
    {"slug": "finance",       "title": "Finance",       "description": "…"},
    {"slug": "healthcare",    "title": "Healthcare",    "description": "…"},
    {"slug": "retail",        "title": "Retail & E-commerce", "description": "…"},
    {"slug": "manufacturing", "title": "Manufacturing", "description": "…"},
    {"slug": "startups",      "title": "Startups",      "description": "…"},
    {"slug": "government",    "title": "Government",    "description": "…"},
    {"slug": "telecom",       "title": "Telecom",       "description": "…"},
    {"slug": "smart-buildings","title": "Smart Buildings","description": "…"},
    {"slug": "education",     "title": "Education",     "description": "…"},
]

PROJECTS = [
    {"slug": "dc-automation-platform","title": "DC Automation Platform","description": "…"},
    {"slug": "hybrid-cloud-migration","title": "Hybrid Cloud Migration","description": "…"},
    {"slug": "network-overhaul-smb",  "title": "Network Overhaul for SMB","description": "…"},
    {"slug": "secure-iot-rollout",    "title": "Secure IoT Rollout",    "description": "…"},
    {"slug": "custom-web-dashboard",  "title": "Custom Web Dashboard",  "description": "…"},
]

TECHS = [
    {"slug": "cisco",       "title": "Cisco",       "description": "…"},
    {"slug": "aws",         "title": "AWS",         "description": "…"},
    {"slug": "azure",       "title": "Azure",       "description": "…"},
    {"slug": "kubernetes",  "title": "Kubernetes",  "description": "…"},
    {"slug": "linux",       "title": "Linux",       "description": "…"},
    {"slug": "python",      "title": "Python",      "description": "…"},
    {"slug": "ansible",     "title": "Ansible",     "description": "…"},
]

# ─── Routes ───────────────────────────────────────────────────────────────────
@app.route("/")
def home():
    return render_template(
        "index.html",
        services=SERVICES,
        industries=INDUSTRIES,
        projects=PROJECTS,
        techs=TECHS
    )

@app.route("/services/<slug>")
def service_detail(slug):
    svc = next((x for x in SERVICES if x["slug"] == slug), None)
    if not svc:
        abort(404)
    return render_template("service_detail.html", service=svc)

@app.route("/industries/<slug>")
def industry_detail(slug):
    ind = next((x for x in INDUSTRIES if x["slug"] == slug), None)
    if not ind:
        abort(404)
    return render_template("industry_detail.html", industry=ind)

@app.route("/projects/<slug>")
def project_detail(slug):
    pj = next((x for x in PROJECTS if x["slug"] == slug), None)
    if not pj:
        abort(404)
    return render_template("project_detail.html", project=pj)

@app.route("/tech/<slug>")
def tech_detail(slug):
    tech = next((x for x in TECHS if x["slug"] == slug), None)
    if not tech:
        abort(404)
    return render_template("tech_detail.html", tech=tech)

@app.route("/submit_contact", methods=["POST"])
def submit_contact():
    data = request.json or {}
    name    = data.get("name")
    email   = data.get("email")
    message = data.get("message")
    if not (name and email and message):
        return jsonify(success=False, message="Missing fields"), 400

    # send email
    try:
        _send_email(
            sender    = EMAIL_USER,
            password  = EMAIL_PASS,
            recipient = EMAIL_TO,
            subject   = f"New message from {name}",
            body      = f"Name: {name}\nEmail: {email}\n\n{message}"
        )
    except Exception as e:
        app.logger.error("Email error: %s", e)
        return jsonify(success=False, message="Failed to send email."), 500

    return jsonify(success=True, message="Thank you! Your message has been received.")

# ─── Boot ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
=======
load_dotenv()  # … your email config, etc …

app = Flask(__name__)

# ─── DATA ─────────────────────────────────────────────────────────────────────

SERVICES = [
    {"slug":"network-engineering", "title":"Network Engineering", 
     "description":"Design, deploy & manage scalable enterprise networks.",
     "features":["BGP routing","VLAN segmentation","SD-WAN"]},
    {"slug":"devops", "title":"DevOps & Platform Engineering", 
     "description":"Accelerate delivery with CI/CD, IaC, and GitOps workflows.",
     "features":["GitLab CI/CD","Terraform","Ansible"]},
    # … 8 more …
]

INDUSTRIES = [
    {"slug":"finance","title":"Finance",
     "description":"Secure, compliant infrastructure for banking.",
     "features":["PCI-DSS","HA clustering"]},
    {"slug":"healthcare","title":"Healthcare",
     "description":"HIPAA-compliant security for hospitals.",
     "features":["Encrypted data","RBAC"]},
    # … 8 more …
]

CASE_STUDIES = [
    {"title":"Data Center & Network Automation",
     "challenge":"Automate provisioning across multi-VLAN/subnets.",
     "solution":"Used Tinkerbell + GitLab CI/CD + Arista EOS templates.",
     "result":"70% faster deployments, full documentation."},
    # you can add more case studies here …
]

TECH_STACK = [
    {"name":"Cisco","logo":"cisco.png"},
    {"name":"AWS","logo":"aws.svg"},
    {"name":"Azure","logo":"azure-original.svg"},
    {"name":"Kubernetes","logo":"kubernetes-plain.svg"},
    {"name":"Linux","logo":"linux-original.svg"},
    {"name":"Python","logo":"python-original.svg"},
    {"name":"Ansible","logo":"ansible-original.svg"},
    {"name":"AWS (again)","logo":"aws_logo_smile_1200x630.png"},
]

PROJECTS = [
    {"slug":"dc-automation-platform","title":"DC Automation Platform"},
    {"slug":"hybrid-cloud-migration","title":"Hybrid Cloud Migration"},
    {"slug":"network-overhaul-smb","title":"Network Overhaul for SMB"},
    {"slug":"secure-iot-rollout","title":"Secure IoT Rollout"},
    {"slug":"custom-web-dashboard","title":"Custom Web Dashboard"},
]

CERTIFICATIONS = [
    "Cisco CCNA","Cisco CCNP","CKAD","CKA",
    "Fortinet NSE","AWS","Azure","Python","Linux","Ansible","Java"
]

TESTIMONIALS = [
    {"quote":"Hepa delivered a seamless network migration. Always ahead!","author":"CEO, FinTech"},
    {"quote":"Their automation saved us hundreds of hours.","author":"IT Manager, Manufacturing"},
]

BLOG_POSTS = [
    {"slug":"security-mistakes-smbs","title":"5 Security Mistakes SMBs Make (And How to Fix Them)"},
    {"slug":"ci-cd-automation-guide","title":"Beginner's Guide to CI/CD Automation"},
    {"slug":"optimizing-hybrid-cloud","title":"Optimizing Hybrid Cloud with Kubernetes"},
    {"slug":"network-segmentation-2025","title":"Why Network Segmentation Matters in 2025"},
]

RESOURCES = [
    {"filename":"network-checklist.pdf","title":"Network Security Checklist (PDF)"},
    {"filename":"cloud-migration-guide.pdf","title":"Cloud Migration Planning Guide"},
    {"filename":"k8s-day0-1-template.pdf","title":"Kubernetes Day 0/1 Template Sample"},
]

LANGUAGES = ["English","Albanian","German","Italian","Spanish","Polish","Croatian"]

TEAM = [
    {"name":"Ardian Krasniqi","role":"Lead Network Engineer",
     "photo":"45.jpg","linkedin":"https://linkedin.com/in/ardian-krasniqi",
     "bio":"Expert in BGP, VRF & enterprise networks."},
    {"name":"Blerim Dervishi","role":"DevOps Engineer",
     "photo":"78.jpg","linkedin":"https://linkedin.com/in/blerim-dervishi",
     "bio":"CI/CD & cloud-native workflow automation."},
    {"name":"Elira Gashi","role":"Business Manager",
     "photo":"63.jpg","linkedin":"https://linkedin.com/in/elira-gashi",
     "bio":"Client relations & strategic growth leadership."},
]

# ─── VIEWS ────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html",
        services=SERVICES,
        industries=INDUSTRIES,
        case_studies=CASE_STUDIES,
        tech_stack=TECH_STACK,
        projects=PROJECTS,
        certifications=CERTIFICATIONS,
        testimonials=TESTIMONIALS,
        blog_posts=BLOG_POSTS,
        resources=RESOURCES,
        languages=LANGUAGES,
        team=TEAM
    )

@app.route("/services/<slug>")
def service_detail(slug):
    svc = next((s for s in SERVICES if s["slug"]==slug), None)
    if not svc: abort(404)
    return render_template("service_detail.html", service=svc)

@app.route("/industries/<slug>")
def industry_detail(slug):
    ind = next((i for i in INDUSTRIES if i["slug"]==slug), None)
    if not ind: abort(404)
    return render_template("industry_detail.html", industry=ind)

# if you want detail pages for projects, blog, etc, repeat same pattern…

if __name__=="__main__":
>>>>>>> 6fdd95a (Make homepage dynamic: loop services, industries, projects & tech)
    app.run(debug=True)
