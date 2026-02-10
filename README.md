# 💰 Personal Finance API – FastAPI Backend

## US

### Overview
Personal Finance API is a cloud-ready backend REST service built with FastAPI following a modular clean architecture.  
The system allows users to manage financial transactions, budgets, and analytics in a secure environment.

This project focuses on real-world backend engineering practices such as authentication, financial domain modeling, and layered architecture.

---

### Features
- JWT Authentication
- Income & Expense Tracking
- Category Management
- Budget Control
- Monthly Financial Reports
- Clean Architecture

---

### Tech Stack
- FastAPI
- Python
- SQLModel / SQLAlchemy
- PostgreSQL (planned)
- Docker (planned)

---

### Architecture Diagram

```
Client
   │
   ▼
Routes (API Layer)
   │
   ▼
Services (Business Logic)
   │
   ▼
Repositories (Data Access)
   │
   ▼
Database (PostgreSQL)
```

---

### Project Structure

```
app/
 ├── api/
 ├── core/
 ├── db/
 ├── models/
 ├── schemas/
 ├── repositories/
 ├── services/
 └── utils/
```

---

### Status
 Initial architecture setup in progress.

---

## 🇪🇸 

### Descripción
Personal Finance API es un backend REST preparado para la nube desarrollado con FastAPI siguiendo una arquitectura modular limpia.

El sistema permite gestionar transacciones financieras, presupuestos y reportes dentro de un entorno seguro.

---

### Funcionalidades
- Autenticación JWT
- Registro de ingresos y gastos
- Gestión de categorías
- Control de presupuestos
- Reportes financieros
- Arquitectura limpia

---

### Estado
Arquitectura inicial en desarrollo.
