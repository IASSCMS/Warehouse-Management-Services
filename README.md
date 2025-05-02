# 🏭 Warehouse Management Service

This project is part of the **Smart Supply Chain Management System**, focused on managing product inventory, warehouses, and stock levels.

---

## 📦 Tech Stack

- Python 3.12
- Django 5.2
- PostgreSQL (via Docker)
- pgAdmin (optional DB GUI)
- Makefile for simplified CLI commands

---

## 🚀 Getting Started

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/IASSCMS/Warehouse-Management-Services.git
cd Warehouse-Management-Services
```

---

### 2️⃣ Create and Activate Virtual Environment

```bash
python -m venv venv

. venv\Scripts\activate       # On Windows (Git Bash)
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Configure Environment

1. Rename `.env.example` in `database` dir into `.env`

Make sure it includes:
```env
PGADMIN_DEFAULT_EMAIL=admin@admin.com
PGADMIN_DEFAULT_PASSWORD=admin
```

2. Rename `.env.example` in `warehouse_managment` dir into `.env`

Make sure it includes:
```env
# Django
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# PostgreSQL
DATABASE_URL=
```

---

### 5️⃣ Start the Database

```bash
make db-up
```

---

### 6️⃣ Run the Django Development Server

```bash
make run
```

- Visit: [http://localhost:8000/api/product/](http://localhost:8000/api/products/)
- Visit: [http://localhost:8000/api/warehouse/](http://localhost:8000/api/warehouse/)

---

## 🐘 Accessing PostgreSQL via pgAdmin

1. Open your browser to: [http://localhost:15433](http://localhost:15433)
2. Login with:
   - **Email:** `admin@admin.com`
   - **Password:** `admin`
3. Register new server:
   - Right click on `Servers` , then `Register` > `Server...`
   - **Name:** `warehouse`
   - Get the below details from the DATABASE_URL
   - **Host Name/ address** - `_`
   - **Port:** `_`
   - **Username:** `_`
   - **Password:** `_`

---

## 🧰 Useful Makefile Commands

```bash
make db-up         # Start PostgreSQL (via Docker)
make db-down       # Stop database container
make migrate       # Run Django migrations
make db-psql       # Run psql shel
make run           # Start Django dev server
make db-clean      # Reset database (use with caution)
```

---

## 🧪 Optional: Create Superuser

```bash
make createsuperuser
```

Then access the Django admin: [http://localhost:8000/admin/](http://localhost:8000/admin/)

---

## 🧹 Clean Up

```bash
make db-clean
```
