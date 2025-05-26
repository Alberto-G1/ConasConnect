Here’s a **cleanly organized, code-formatted rewrite** of your `README.md` content for **Conas Connect**, without altering the original information but improving structure, formatting, and clarity using Markdown best practices:

````markdown
# 📘 Conas Connect - Educational Platform

A comprehensive Django-based educational platform designed for students, lecturers, and administrators with role-based access control and premium content management.

---

## 🌟 Features

### 🔐 User Management
- **Multi-role System:** Students, Lecturers, and Presidents  
- **Student Types:** MUBIS (free premium access) and Non-MUBIS (paid access)  
- **MUBIS Number:** Automatic unique 7-digit ID generation  
- **User Profiles:** Extended info and profile pictures  
- **Authentication:** Secure login/logout with role-based redirects  

### 📚 Content Management
- **Content Types:** Free and Premium  
- **Supported Files:** Documents, images, video URLs  
- **Categories:** Structured classification  
- **Comments System:** Engage users on content  
- **View Tracking:** Analytics and stats  
- **Search Functionality:** Advanced discovery tools  

### 💳 Payment System
- **Plans:** Monthly, Quarterly, Annual  
- **Payment Tracking:** History and status  
- **Subscription Management:** Auto-renewal, cancel options  
- **Access Control:** Restrict premium content  
- **Revenue Analytics:** Admin-level statistics  

### 🛠️ Administrative Features
- **Dashboard Analytics:** Users, content, payments  
- **User Management:** Admin account controls  
- **Content Moderation:** Approve/reject submissions  
- **Payment Oversight:** View all transactions/subscriptions  

---

## 🏗️ Project Structure

```text
conas_connect/
├── conas_connect/          # Project settings
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── accounts/               # User system
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   ├── admin.py
│   ├── signals.py
│   ├── utils.py
│   ├── decorators.py
│   └── management/
├── content/                # Content app
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   ├── admin.py
│   └── utils.py
├── payments/               # Payment app
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   ├── admin.py
│   └── utils.py
├── static/
├── media/
├── templates/
├── requirements.txt
├── manage.py
├── start_server.sh
├── start_server.bat
└── test_setup.py
````

---

## 🚀 Quick Start

### ✅ Prerequisites

* Python 3.8+
* pip
* Virtual Environment (recommended)

### 🧰 Installation

```bash
# Clone repo
git clone <repository-url>
cd conas_connect

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py makemigrations
python manage.py migrate

# Setup initial data
python manage.py setup_initial_data

# (Optional) Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

### ⚡ Quick Setup (Automated)

```bash
# Linux/Mac
chmod +x start_server.sh
./start_server.sh

# Windows
start_server.bat
```

---

## 🔐 Default Credentials

After running `setup_initial_data`:

* **Username:** `admin`
* **Password:** `admin123`
* **Role:** `President` (full access)

---

## 👤 User Roles & Permissions

| Role                | Access                                                                                                 |
| ------------------- | ------------------------------------------------------------------------------------------------------ |
| Student (MUBIS)     | ✅ All content incl. premium <br> ✅ Comments <br> ✅ Analytics <br> ❌ Upload <br> ❌ Admin functions      |
| Student (Non-MUBIS) | ✅ Free content only <br> ✅ Comments <br> ✅ Subscription purchases <br> ❌ Upload <br> ❌ Admin functions |
| Lecturer            | ✅ All student rights <br> ✅ Upload/manage own content <br> ✅ Create categories <br> ❌ Manage users     |
| President           | ✅ Full system access <br> ✅ User/content/payment management <br> ✅ All admin features                  |

---

## 💳 Payment Plans

| Plan              | Duration | Price   | Features              |
| ----------------- | -------- | ------- | --------------------- |
| Monthly Premium   | 30 days  | \$10.00 | Full premium access   |
| Quarterly Premium | 90 days  | \$25.00 | Premium + savings     |
| Annual Premium    | 365 days | \$80.00 | Premium + max savings |

---

## 🛠️ API Endpoints

### 🔑 Authentication

* `POST /register/` – Register user
* `POST /login/` – Login
* `POST /logout/` – Logout

### 📦 Content

* `GET /content/` – List content
* `GET /content/<id>/` – Content details
* `POST /content/create/` – Create content *(Lecturer+)*
* `PUT /content/<id>/edit/` – Edit content *(Author/President)*
* `DELETE /content/<id>/delete/` – Delete content *(Author/President)*

### 💰 Payments

* `GET /payments/plans/` – List plans
* `POST /payments/initiate/<plan_id>/` – Start payment
* `POST /payments/complete/<transaction_id>/` – Complete payment
* `GET /payments/history/` – View history

### 🧑‍💼 Admin (President only)

* `GET /admin-panel/dashboard/` – Admin dashboard
* `GET /admin-panel/users/` – User management
* `GET /api/accounts/user-stats/` – User stats
* `GET /api/content/content-stats/` – Content stats

---

## 🗄️ Database Models

### 👥 User Models

* `CustomUser`: Django user with roles
* `UserProfile`: Extra user info

### 📦 Content Models

* `Category`: Content categories
* `Content`: Content with metadata
* `Comment`: Comments on content
* `ContentView`: Track views

### 💳 Payment Models

* `PaymentPlan`: Subscription options
* `Payment`: Transaction details
* `Subscription`: Access tracking

---

## 🔧 Configuration

### 📄 Environment Variables

Create a `.env` file:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# (Optional) Database
DATABASE_URL=sqlite:///db.sqlite3

# (Optional) Email settings
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
EMAIL_USE_TLS=True
```

### 📁 Media Files

* Upload Path: `media/`
* Profile Pictures: `media/profile_pics/`
* Content Files: `media/content_files/`
* Content Images: `media/content_images/`

---

## 🧪 Testing

```bash
# Verify setup
python test_setup.py

# Run tests
python manage.py test
```

---

## 📊 Management Commands

```bash
# Initialize system with default data
python manage.py setup_initial_data
```

Creates:

* Default admin user
* Sample categories
* Payment plans

---

## 🚀 Deployment

* Set `DEBUG=False`

* Use PostgreSQL or other production DB

* Collect static files:

  ```bash
  python manage.py collectstatic
  ```

* Configure email backend, secret key, and `ALLOWED_HOSTS`

---

## 🤝 Contributing

1. Fork the repo
2. Create a feature branch
3. Make changes
4. Add tests
5. Submit a PR

---

## 📝 License

Licensed under the **MIT License** – see `LICENSE` file.

---

## 🆘 Support

* Open an issue in the repo
* Contact the dev team
* Read the documentation

---

## 🔄 Version History

**v1.0.0**

* Core user management
* Content system
* Payment integration
* Admin features
