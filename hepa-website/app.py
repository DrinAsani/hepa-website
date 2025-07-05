import os
from flask import Flask, render_template, abort, request, flash, redirect, url_for
from dotenv import load_dotenv
from flask_mail import Mail, Message

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev')  # Needed for flash messages

# Flask-Mail configuration
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.example.com')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'true').lower() == 'true'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME', 'your@email.com')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD', 'yourpassword')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER', app.config['MAIL_USERNAME'])

mail = Mail(app)

# Demo data
SERVICES = [
    {"slug": "network-engineering", "title": "Network Engineering", "content": "We design and optimize enterprise networks for speed, security, and reliability.", "features": ["LAN/WAN Design", "BGP, OSPF, EVPN", "Wireless Solutions"]},
    {"slug": "devops", "title": "DevOps & Platform Engineering", "content": "Automate and accelerate software delivery with CI/CD and infrastructure as code.", "features": ["CI/CD Pipelines", "Terraform & Ansible", "Monitoring & Observability"]},
    {"slug": "noc", "title": "Network Operation Center", "content": "Designing and implementing a centralized platform to monitor, manage, and optimize enterprise-wide network operations.", "features": ["24/7 Proactive Monitoring & Incident Response", "Centralized Visibility & Reporting", "SLA Management & Operational Efficiency"]},
    {"slug": "cloud", "title": "Cloud Solutions", "content": "AWS, Azure, and hybrid-cloud architecture, migrations, and ops.", "features": ["Cloud Migration", "Serverless", "Security & Compliance"]},
    {"slug": "cybersecurity", "title": "Cyber Security & Compliance", "content": "Protect your business with audits, vulnerability scans, and policy design.", "features": ["Vulnerability Scanning", "Policy & Audit", "Incident Response"]},
    {"slug": "it-support", "title": "IT Support & Managed Services", "content": "24/7 helpdesk, remote monitoring, and managed IT for your business.", "features": ["Remote Helpdesk", "SLAs", "Patch Management"]},
    {"slug": "web-design", "title": "Website Design & Development", "content": "Create fast, modern, SEO-optimized websites with clean UX/UI—built with frameworks like React, Vue, or Django.", "features": ["SEO-optimized, fast-loading pages with clean UX", "Mobile-first design and cross-browser compatibility", "Integration with CMSs (e.g., WordPress, Strapi) or headless architecture"]},
    {"slug": "api", "title": "API Development & Integration", "content": "Develop secure RESTful and GraphQL APIs, and integrate third-party APIs (payment gateways, CRMs, cloud services, etc.) into client applications.", "features": ["Secure RESTful and GraphQL API design", "Integration with third-party services (payments, CRMs, cloud APIs)", "Versioning and documentation using tools like Swagger or Postman"]},
    {"slug": "e-commerce", "title": "E-commerce Platforms", "content": "Set up modern e-commerce systems with payment processing, inventory management, and customer portals using tools like Stripe, Shopify APIs, or custom builds.", "features": ["Product catalog, shopping cart, and checkout flows", "Integration with Stripe, PayPal, and crypto payments", "Admin panel for order, inventory, and user management"]},
]

PROJECTS = [
    {
        "title": "Network Operation Center",
        "slug": "network-operation-center",
        "summary": "Development and operation of a 24/7 enterprise-grade NOC for real-time monitoring, troubleshooting, and uptime optimization.",
        "content": (
            "Led the development and operation of a state-of-the-art Network Operation Center (NOC) to monitor, "
            "troubleshoot, and optimize enterprise networks in real-time. The NOC project focused on providing 24/7 "
            "visibility into network health, rapid incident response, and efficient management of large-scale infrastructure "
            "for clients in various industries. Leveraged modern automation tools, proactive alerting, and detailed reporting "
            "to ensure uptime, security, and continuous improvement."
        )
    },
    {
        "title": "Network Provisioning",
        "slug": "network-provisioning",
        "summary": "Automated provisioning of network devices and services across multi-vendor environments.",
        "content": (
            "Designed and implemented automated workflows for rapid, reliable provisioning of switches, routers, "
            "and firewalls, reducing manual errors and deployment times."
        )
    },
    {
        "title": "Network Migration",
        "slug": "network-migration",
        "summary": "Seamless migration of legacy networks to modern platforms with zero downtime.",
        "content": (
            "Managed end-to-end migration of network infrastructure, including planning, risk assessment, execution, "
            "and validation, ensuring business continuity."
        )
    },
    {
        "title": "High & Low Level Design",
        "slug": "high-low-level-design",
        "summary": "Produced detailed network architectures and implementation blueprints.",
        "content": (
            "Developed high-level and low-level design documentation for critical infrastructure projects, aligning "
            "business goals with technical solutions."
        )
    },
    {
        "title": "Networking & Infrastructure Projects",
        "slug": "networking-infrastructure-projects",
        "summary": "Delivered large-scale infrastructure solutions for enterprise clients.",
        "content": (
            "Led and executed projects involving campus LAN/WAN, data center, and cloud networking, focusing on "
            "performance, security, and scalability."
        )
    },
    {
        "title": "Tinkerbell Kubernetes Provisioning with DHCP Relay",
        "slug": "tinkerbell-k8s-dhcp-relay",
        "summary": "Automated bare-metal Kubernetes provisioning using Tinkerbell and DHCP relay.",
        "content": (
            "Implemented Tinkerbell to orchestrate Kubernetes node deployments with DHCP relay support, enabling "
            "scalable on-premise cloud platforms."
        )
    },
    {
        "title": "Server-to-Network Attachment Validation with BGP",
        "slug": "server-network-bgp-validation",
        "summary": "Validated BGP-based connectivity for server-to-network attachment models.",
        "content": (
            "Designed and tested BGP peering scenarios for servers and network fabrics, ensuring robust and "
            "redundant connectivity models."
        )
    },
    {
        "title": "Arista Device Migration",
        "slug": "arista-device-migration",
        "summary": "Migrated critical infrastructure to Arista EOS with zero disruption.",
        "content": (
            "Planned and executed migration to Arista switching, including config translation, device cutover, "
            "and operational validation."
        )
    },
    {
        "title": "EKS Anywhere (EKSa) + Tinkerbell Across Subnets",
        "slug": "eksa-tinkerbell-across-subnets",
        "summary": "Deployed EKS Anywhere with Tinkerbell over multiple network subnets.",
        "content": (
            "Integrated AWS EKS Anywhere with Tinkerbell to provision and manage clusters across segmented subnets, "
            "improving isolation and scalability."
        )
    },
    {
        "title": "AWS EC2 Python Automation",
        "slug": "aws-ec2-python-automation",
        "summary": "Automated AWS EC2 lifecycle management using Python.",
        "content": (
            "Developed Python scripts to launch, configure, and monitor EC2 instances, enabling DevOps workflows "
            "and infrastructure-as-code practices."
        )
    },
    {
        "title": "CI/CD Integration",
        "slug": "cicd-integration",
        "summary": "Integrated continuous integration and delivery for networking projects.",
        "content": (
            "Built CI/CD pipelines for network automation and validation, leveraging GitLab CI and Ansible for "
            "rapid, repeatable deployments."
        )
    },
    {
        "title": "Business & Web Projects",
        "slug": "business-web-projects",
        "summary": "Delivered tailored business applications and web solutions.",
        "content": (
            "Collaborated with clients to design and deploy web and business process automation platforms, improving "
            "efficiency and digital presence."
        )
    },
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

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name    = request.form.get('name')
        email   = request.form.get('email')
        message = request.form.get('message')

        subject   = "New Contact Form Submission"
        recipient = app.config['MAIL_USERNAME']  # you can also set a separate RECEIVER

        msg = Message(subject, sender=email, recipients=[recipient])
        msg.body = f"From: {name} <{email}>\n\n{message}"

        try:
            mail.send(msg)
            flash('Your message has been sent!', 'success')
        except Exception as e:
            # print the real error to console for debugging
            print("Mail send error:", e)
            flash('Something went wrong. Please try again later.', 'danger')

        return redirect(url_for('contact'))

    return render_template('contact.html')

@app.route('/tech-in-kosova')
def tech_kosova():
    return render_template('tech_kosova.html')

if __name__ == "__main__":
    app.run(debug=True)