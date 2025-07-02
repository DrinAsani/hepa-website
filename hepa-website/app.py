from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    message = data.get('message')

    print(f"Message from {name} ({email}): {message}")
    return jsonify({'success': True, 'message': 'Thank you! Your message has been received.'})

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/services/<service_slug>')
def service_detail(service_slug):
    services = {
        "network-engineering": {
            "title": "Network Engineering",
            "description": "Scalable, secure LAN/WAN design, BGP/OSPF routing, SD-WAN, wireless, and data center fabric implementation."
        },
        "devops": {
            "title": "DevOps & Platform Engineering",
            "description": "Infrastructure-as-Code, GitOps pipelines, Kubernetes operations, observability, and CI/CD automation."
        },
        "cloud": {
            "title": "Cloud Solutions (AWS, Azure)",
            "description": "Cloud architecture, migration, hybrid-cloud deployment, security, and cost optimization."
        },
        "cybersecurity": {
            "title": "Cyber Security & Compliance",
            "description": "Pen testing, firewalls, SIEM, ISO 27001 & NIST compliance, and vulnerability management."
        },
        "it-support": {
            "title": "IT Support & Managed Services",
            "description": "24/7 monitoring, helpdesk, incident response, backup, and maintenance."
        },
        "automation": {
            "title": "Automation (CI/CD, Infra, Workflows)",
            "description": "End-to-end automation pipelines using Ansible, GitLab CI/CD, Terraform, and Python."
        },
        "data-iot": {
            "title": "Data Analytics & IoT",
            "description": "Smart buildings, sensor integration, and custom dashboards with energy and usage analytics."
        },
        "web-mobile": {
            "title": "Web & Mobile Development",
            "description": "Custom web apps, responsive mobile apps, and dashboards tailored to user needs."
        },
        "consulting": {
            "title": "Digital Transformation Consulting",
            "description": "IT strategy, modernization, infrastructure assessments, and future-proof planning."
        },
        "training": {
            "title": "Training & Workshops",
            "description": "Customized team training sessions in DevOps, cloud, security, and automation."
        }
    }

    service = services.get(service_slug)
    if not service:
        return "Service not found", 404

    return render_template("service_detail.html", service=service)
