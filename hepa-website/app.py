from flask import Flask, render_template, request, jsonify, abort
from flask_cors import CORS
from dotenv import load_dotenv
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)
CORS(app)

# ----------------------------------
# 1) Services catalog
# ----------------------------------
services = {
    "network-engineering": {
        "title": "Network Engineering",
        "description": (
            "Scalable, secure LAN/WAN design, BGP/OSPF routing, SD-WAN, "
            "wireless, and data center fabric implementation."
        ),
        "image": "network-diagram.png",
        "features": [
            "Custom topology design",
            "BGP & OSPF peering",
            "SD-WAN deployment",
            "Wireless site surveys"
        ],
        "case_studies": [
            { "name": "ACME Corp Data Center", "result": "70% faster provisioning time" },
            { "name": "Global Retail WAN",    "result": "99.99% uptime SLA" }
        ]
    },
    "devops": {
        "title": "DevOps & Platform Engineering",
        "description": (
            "Infrastructure-as-Code, GitOps pipelines, Kubernetes operations, "
            "observability, and CI/CD automation."
        ),
        "image": "devops-workflow.png",
        "features": [
            "Terraform & Ansible IaC",
            "GitLab/GitHub Actions pipelines",
            "Kubernetes cluster hardening",
            "Prometheus + Grafana monitoring"
        ]
    },
    "cloud": {
        "title": "Cloud Solutions (AWS, Azure)",
        "description": (
            "Cloud architecture, migration, hybrid-cloud deployment, security, "
            "and cost optimization."
        ),
        "image": "cloud-architecture.png",
        "features": [
            "AWS / Azure design & migration",
            "Hybrid-cloud connectivity",
            "Security & compliance",
            "Cost optimization"
        ]
    },
    "cybersecurity": {
        "title": "Cyber Security & Compliance",
        "description": (
            "Pen testing, firewalls, SIEM, ISO 27001 & NIST compliance, "
            "and vulnerability management."
        ),
        "features": [
            "Vulnerability assessments",
            "Penetration testing",
            "Security policy design",
            "Compliance audits"
        ]
    },
    "it-support": {
        "title": "IT Support & Managed Services",
        "description": (
            "24/7 monitoring, helpdesk, incident response, backup, "
            "and ongoing maintenance."
        ),
        "features": [
            "Round-the-clock monitoring",
            "Remote & on-site support",
            "Automated backups",
            "SLAs & reporting"
        ]
    },
    "automation": {
        "title": "Automation (CI/CD, Infra, Workflows)",
        "description": (
            "End-to-end automation pipelines using Ansible, GitLab CI/CD, "
            "Terraform, and Python."
        ),
        "features": [
            "CI/CD pipeline design",
            "Infrastructure provisioning",
            "Workflow orchestration",
            "Automated testing"
        ]
    },
    "data-iot": {
        "title": "Data Analytics & IoT",
        "description": (
            "Smart buildings, sensor integration, and custom dashboards with "
            "energy and usage analytics."
        ),
        "features": [
            "Sensor network design",
            "Data collection & storage",
            "Dashboards & reporting",
            "Predictive analytics"
        ]
    },
    "web-mobile": {
        "title": "Web & Mobile Development",
        "description": (
            "Custom web apps, responsive mobile apps, and dashboards tailored "
            "to your users’ needs."
        ),
        "features": [
            "Responsive UI/UX",
            "API development",
            "Cross-platform mobile apps",
            "Performance optimization"
        ]
    },
    "consulting": {
        "title": "Digital Transformation Consulting",
        "description": (
            "IT strategy, modernization, infrastructure assessments, "
            "and future-proof planning."
        ),
        "features": [
            "Technology roadmaps",
            "Risk assessments",
            "Cost/benefit analysis",
            "Change management"
        ]
    },
    "training": {
        "title": "Training & Workshops",
        "description": (
            "Customized team training sessions in DevOps, cloud, security, "
            "and automation."
        ),
        "features": [
            "Hands-on labs",
            "Custom curricula",
            "Certification prep",
            "Post-training support"
        ]
    }
}

# ----------------------------------
# 2) Industries catalog
# ----------------------------------
industries = {
    "finance": {
        "title": "Finance",
        "description": "We help banks and fintechs build rock-solid, compliant network and security solutions.",
        "features": [
            "PCI-DSS compliant architectures",
            "High-availability trading networks",
            "Encrypted data lakes"
        ]
    },
    "healthcare": {
        "title": "Healthcare",
        "description": "Secure patient data, telemedicine platforms, and HIPAA-compliant cloud deployments.",
        "features": [
            "EHR network integrations",
            "Secure VPN setups",
            "Data privacy audits"
        ]
    },
    "retail-ecommerce": {
        "title": "Retail & E-commerce",
        "description": "Scale your online storefront, optimize inventory data flows, and secure customer transactions.",
        "features": [
            "CDN & caching strategies",
            "Payment gateway security",
            "Real-time analytics dashboards"
        ]
    },
    "manufacturing": {
        "title": "Manufacturing",
        "description": "Connect IIoT sensors, automate workflows, and monitor plant-floor networks in real-time.",
        "features": [
            "SCADA network design",
            "Sensor data pipelines",
            "Predictive maintenance alerts"
        ]
    },
    "startups": {
        "title": "Startups",
        "description": "Rapid MVP deployments, cloud cost optimization, and rock-solid DevOps pipelines.",
        "features": [
            "Lean IaC blueprints",
            "Automated CI/CD",
            "Scalable Kubernetes clusters"
        ]
    },
    "government": {
        "title": "Government",
        "description": "Secure, compliant public-sector IT with strong auth, logging, and disaster-recovery.",
        "features": [
            "Gov-cloud architectures",
            "Audit & compliance tooling",
            "Geo-redundant failover"
        ]
    },
    "telecom": {
        "title": "Telecom",
        "description": "Carrier-grade networks, SD-WAN, and 5G edge integrations for next-gen services.",
        "features": [
            "BGP/MPLS backbones",
            "5G core slicing",
            "Low-latency peering"
        ]
    },
    "smart-buildings": {
        "title": "Smart Buildings",
        "description": "Automate lighting, HVAC, and security systems with robust IoT networks.",
        "features": [
            "Mesh Wi-Fi deployments",
            "Sensor orchestration",
            "Building-wide analytics"
        ]
    },
    "education": {
        "title": "Education",
        "description": "Campus networks, e-learning platforms, and secure remote-access for students and staff.",
        "features": [
            "Classroom AV networking",
            "VPN for remote learners",
            "Identity-aware proxies"
        ]
    },
    "other": {
        "title": "Any Business",
        "description": "Tailor-made IT, network, and automation solutions for every sector.",
        "features": [
            "Custom consulting",
            "Scalable deployments",
            "Ongoing support"
        ]
    }
}

# ----------------------------------
# 3) Projects catalog
# ----------------------------------
projects = {
    "dc-automation-platform": {
        "title": "DC Automation Platform",
        "description": "Automated provisioning for rack servers and switches via PXE, Terraform & Python.",
        "features": [
            "Day-0/1 config templating",
            "Zero-touch workflows",
            "GitOps-driven documentation"
        ]
    },
    "hybrid-cloud-migration": {
        "title": "Hybrid Cloud Migration",
        "description": "Lift-and-shift critical workloads from on-prem to AWS & Azure with minimal downtime.",
        "features": [
            "Data replication pipelines",
            "Secure VPN tunnels",
            "Cost-optimization analysis"
        ]
    },
    "network-overhaul-smb": {
        "title": "Network Overhaul for SMB",
        "description": "Redesign of SMB network with SD-WAN, VoIP QoS, and managed firewall.",
        "features": [
            "SD-WAN rollout",
            "QoS for voice/video",
            "Centralized logging"
        ]
    },
    "secure-iot-rollout": {
        "title": "Secure IoT Rollout",
        "description": "End-to-end security for hundreds of IoT devices in manufacturing.",
        "features": [
            "Certificate-based auth",
            "Edge firewalls",
            "Encrypted telemetry"
        ]
    },
    "custom-web-dashboard": {
        "title": "Custom Web Dashboard",
        "description": "Real-time portal built with React, Flask, and Prometheus back-end.",
        "features": [
            "Websocket data streams",
            "Role-based access control",
            "Alerting & notifications"
        ]
    }
}

# ----------------------------------
# 4) Tech catalog
# ----------------------------------
technologies = {
    "cisco": {
        "title": "Cisco",
        "description": "Enterprise routing, switching, and wireless at massive scale."
    },
    "aws": {
        "title": "AWS",
        "description": "Full-stack cloud services: compute, storage, networking, serverless, and more."
    },
    "azure": {
        "title": "Azure",
        "description": "Microsoft’s global cloud with deep enterprise integration."
    },
    "kubernetes": {
        "title": "Kubernetes",
        "description": "Container orchestration for automated deployment, scaling, and management."
    },
    "linux": {
        "title": "Linux",
        "description": "Open-source OS powering servers, networking, and embedded devices."
    },
    "python": {
        "title": "Python",
        "description": "Scripting, automation, web services, and data analytics with a rich ecosystem."
    },
    "ansible": {
        "title": "Ansible",
        "description": "Agentless automation for configuration management and orchestration."
    }
}

# ----------------------------------
# 5) Routes
# ----------------------------------

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/services/<slug>')
def service_detail(slug):
    svc = services.get(slug)
    if not svc:
        abort(404)
    return render_template('service_detail.html', service=svc)

@app.route('/industries/<slug>')
def industry_detail(slug):
    item = industries.get(slug)
    if not item:
        abort(404)
    return render_template('industry_detail.html', item=item)

@app.route('/projects/<slug>')
def project_detail(slug):
    item = projects.get(slug)
    if not item:
        abort(404)
    return render_template('project_detail.html', item=item)

@app.route('/tech/<slug>')
def tech_detail(slug):
    item = technologies.get(slug)
    if not item:
        abort(404)
    return render_template('tech_detail.html', item=item)

@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    data = request.json or {}
    name    = data.get('name', '—')
    email   = data.get('email', '—')
    message = data.get('message', '')
    subject = f"New Contact: {name}"
    body    = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"

    try:
        _send_email(subject, body)
        return jsonify(success=True, message="Thank you! Your message has been sent.")
    except Exception as e:
        app.logger.error("Email error: %s", e)
        return jsonify(success=False, message="Failed to send email."), 500

def _send_email(subject, body):
    sender    = os.getenv('EMAIL_USER')
    recipient = os.getenv('EMAIL_TO')
    password  = os.getenv('EMAIL_PASS')

    msg = MIMEMultipart()
    msg['From']    = sender
    msg['To']      = recipient
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(sender, password)
        smtp.send_message(msg)

if __name__ == '__main__':
    app.run(debug=True)
