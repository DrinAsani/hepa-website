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

projects = [
    {
        "title": "Network Operation Center",
        "slug": "network-operation-center",
        "summary": "Development and operation of a 24/7 enterprise-grade NOC for real-time monitoring, troubleshooting, and uptime optimization.",
        "content": """Led the development and operation of a state-of-the-art Network Operation Center (NOC) to monitor, troubleshoot, and optimize enterprise networks in real-time. The NOC project focused on providing 24/7 visibility into network health, rapid incident response, and efficient management of large-scale infrastructure for clients in various industries. Leveraged modern automation tools, proactive alerting, and detailed reporting to ensure uptime, security, and continuous improvement."""
    },
    {
        "title": "Network Provisioning",
        "slug": "network-provisioning",
        "summary": "Automated provisioning of network devices and services across multi-vendor environments.",
        "content": "Designed and implemented automated workflows for rapid, reliable provisioning of switches, routers, and firewalls, reducing manual errors and deployment times."
    },
    {
        "title": "Network Migration",
        "slug": "network-migration",
        "summary": "Seamless migration of legacy networks to modern platforms with zero downtime.",
        "content": "Managed end-to-end migration of network infrastructure, including planning, risk assessment, execution, and validation, ensuring business continuity."
    },
    {
        "title": "High & Low Level Design",
        "slug": "high-low-level-design",
        "summary": "Produced detailed network architectures and implementation blueprints.",
        "content": "Developed high-level and low-level design documentation for critical infrastructure projects, aligning business goals with technical solutions."
    },
    {
        "title": "Networking & Infrastructure Projects",
        "slug": "networking-infrastructure-projects",
        "summary": "Delivered large-scale infrastructure solutions for enterprise clients.",
        "content": "Led and executed projects involving campus LAN/WAN, data center, and cloud networking, focusing on performance, security, and scalability."
    },
    {
        "title": "Tinkerbell Kubernetes Provisioning with DHCP Relay",
        "slug": "tinkerbell-k8s-dhcp-relay",
        "summary": "Automated bare-metal Kubernetes provisioning using Tinkerbell and DHCP relay.",
        "content": "Implemented Tinkerbell to orchestrate Kubernetes node deployments with DHCP relay support, enabling scalable on-premise cloud platforms."
    },
    {
        "title": "Server-to-Network Attachment Validation with BGP",
        "slug": "server-network-bgp-validation",
        "summary": "Validated BGP-based connectivity for server-to-network attachment models.",
        "content": "Designed and tested BGP peering scenarios for servers and network fabrics, ensuring robust and redundant connectivity models."
    },
    {
        "title": "Arista Device Migration",
        "slug": "arista-device-migration",
        "summary": "Migrated critical infrastructure to Arista EOS with zero disruption.",
        "content": "Planned and executed migration to Arista switching, including config translation, device cutover, and operational validation."
    },
    {
        "title": "EKS Anywhere (EKSa) + Tinkerbell Across Subnets",
        "slug": "eksa-tinkerbell-across-subnets",
        "summary": "Deployed EKS Anywhere with Tinkerbell over multiple network subnets.",
        "content": "Integrated AWS EKS Anywhere with Tinkerbell to provision and manage clusters across segmented subnets, improving isolation and scalability."
    },
    {
        "title": "AWS EC2 Python Automation",
        "slug": "aws-ec2-python-automation",
        "summary": "Automated AWS EC2 lifecycle management using Python.",
        "content": "Developed Python scripts to launch, configure, and monitor EC2 instances, enabling DevOps workflows and infrastructure-as-code practices."
    },
    {
        "title": "CI/CD Integration",
        "slug": "cicd-integration",
        "summary": "Integrated continuous integration and delivery for networking projects.",
        "content": "Built CI/CD pipelines for network automation and validation, leveraging GitLab CI and Ansible for rapid, repeatable deployments."
    },
    {
        "title": "Business & Web Projects",
        "slug": "business-web-projects",
        "summary": "Delivered tailored business applications and web solutions.",
        "content": "Collaborated with clients to design and deploy web and business process automation platforms, improving efficiency and digital presence."
    }
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

@app.route('/projects')
def projects_view():
    return render_template('projects.html', projects=projects)

@app.route('/projects/<slug>')
def project_detail(slug):
    project = next((p for p in projects if p['slug'] == slug), None)
    if not project:
        return "Project not found", 404
    return render_template('project_detail.html', project=project)
