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
POSTGRES_DB=warehouse_inventory
POSTGRES_USER=admin
POSTGRES_PASSWORD=admin
POSTGRES_PORT=5432
POSTGRES_HOST=localhost

PGADMIN_DEFAULT_EMAIL=admin@admin.com
PGADMIN_DEFAULT_PASSWORD=admin
```

2. Rename `.env.example` in `warehouse` dir into `.env`

Make sure it includes:
```env
# Django
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

POSTGRES_DB=warehouse_inventory
POSTGRES_USER=admin
POSTGRES_PASSWORD=admin
POSTGRES_PORT=5432
POSTGRES_HOST=localhost
```

---

### 5️⃣ Start the Database

```bash
make db-up
```

Wait a few seconds for the DB to fully initialize.

---

### 6️⃣ Run Migrations

```bash
make migrate
```

---

### 7️⃣ Seed the Database with Sample Data (Optional for sample data)

```bash
make seed
```

This seeds:
- Products
- Warehouses
- Inventory

---

### 8️⃣ Run the Django Development Server

```bash
make run
```

- Visit: [http://localhost:8000/api/product/products/](http://localhost:8000/api/product/products/)
- Visit: [http://localhost:8000/api/warehouse/warehouses/](http://localhost:8000/api/warehouse/warehouses/)
- Visit: [http://localhost:8000/api/warehouse/inventory/](http://localhost:8000/api/warehouse/inventory/)

---

## 🐘 Accessing PostgreSQL via pgAdmin

1. Open your browser to: [http://localhost:15433](http://localhost:15433)
2. Login with:
   - **Email:** `admin@admin.com`
   - **Password:** `admin`
3. Register new server:
   - Right click on `Servers` , then `Register` > `Server...`
   - **Name:** `warehouse`
   - **Host Name/ address** - `database`
   - **Port:** `5432`
   - **Username:** `admin`
   - **Password:** `admin`
   - **Database:** `warehouse_inventory`

---

## 🧰 Useful Makefile Commands

```bash
make db-up         # Start PostgreSQL (via Docker)
make db-down       # Stop database container
make migrate       # Run Django migrations
make seed          # Seed database with sample data
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
make db-clean```