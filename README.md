# 🛡️ Argus: ABAC Security & Automated Audit System

**Argus** is a high-security Django API designed to protect sensitive documents using **Attribute-Based Access Control (ABAC)**. It features real-time security logging via **Celery/Redis** and automated PDF audit reports sent via email using **Celery Beat**.

---

## 🚀 Key Features

* **ABAC Permission Engine**: Access is granted based on User Department, Clearance Level, and Time-Lock policies.
* **Time-Fence Security**: Automated denial of access outside of department-specific operating hours.
* **Asynchronous Logging**: Security violations (403 Forbidden) are logged in the background using **Celery** to ensure zero latency for the user.
* **Automated Audits**: **Celery Beat** triggers a scheduled task to compile security violations into a **PDF Report** and emails it to administrators.



---

## 🛠️ Technology Stack

* **Framework**: Django & Django Rest Framework (DRF)
* **Database**: PostgreSQL
* **Task Queue**: Celery
* **Message Broker**: Redis
* **Scheduler**: Celery Beat
* **PDF Generation**: ReportLab
* **Authentication**: SimpleJWT

---

## 🛡️ Security Logic (The "Sentinel" Layer)

The system evaluates three layers of protection before allowing access to a resource:

1. **Time Lock**: Checks the `AccessPolicy` for the user's department. Access is denied if the current local time is outside the allowed window.
2. **Department Matching**: Users can only access documents belonging to their own department.
3. **Clearance Level**: Each document has a `sensitivity_level`. Users with a lower `clearance_level` are blocked and logged.



---

## 📋 Security Event Logs

Every failed attempt creates a log entry with the following classifications:

| Action | Reason |
| :--- | :--- |
| **TIME_LOCK_DENIAL** | User attempted access outside of policy hours. |
| **DEPARTMENT_MISMATCH** | User attempted to access/delete a resource in another department. |
| **INSUFFICIENT_CLEARANCE** | User's clearance level is lower than the document's sensitivity. |

---

## ⚙️ Setup & Installation

### 1. Clone the repo and install dependencies
```bash
pipenv install
pipenv shell

2. Environment Variables
Create a .env file in the root directory with your specific configuration:
Plaintext
DEBUG=True
SECRET_KEY=django-insecure-argus-key-123
DATABASE_URL=postgres://postgres:password@localhost:5432/argus_db
CELERY_BROKER_URL=redis://127.0.0.1:6379/0
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
ADMIN_EMAIL=admin@yourorg.com

3. Start the Services
Open separate terminals for each of the following:
Django Server: python manage.py runserver
Redis: redis-server
Celery Worker: celery -A argus_config worker --loglevel=info
Celery Beat: celery -A argus_config beat --loglevel=info
