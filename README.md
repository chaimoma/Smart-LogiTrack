# Smart LogiTrack – Predictive Urban Transport System (ETA)

**Smart LogiTrack** is a comprehensive logistics "Control Tower" designed to predict the Estimated Time of Arrival (ETA) for urban taxi trips. It features a distributed ETL pipeline, a machine learning regression model, and a secure FastAPI service.

## 🚀 Project Overview

The system automates the journey of data from raw Parquet files to live API predictions:

* **Data Ingestion**: Downloads and stores raw "Bronze" taxi data.
* **Processing**: Uses **PySpark** for cleaning (Silver zone) and feature engineering (detecting outliers in distance/duration).
* **Orchestration**: Managed by **Apache Airflow** to ensure a reliable workflow from ingestion to model training.
* **Machine Learning**: A regression model trained to predict `duration_minutes` based on pickup hours, location IDs, and trip distance.
* **Delivery**: A **FastAPI** backend secured with **JWT** providing ETA predictions and advanced SQL-based analytics.

---

## 🛠 Tech Stack

* **Languages**: Python 3.11
* **Data Processing**: PySpark
* **Database**: PostgreSQL
* **Orchestration**: Apache Airflow
* **API Framework**: FastAPI, SQLAlchemy (Raw SQL/CTEs)
* **ML Libraries**: Scikit-learn / Keras
* **DevOps**: Docker & Docker Compose

---

## ⚙️ How to Run

### 1. Prerequisites

* Ubuntu 24.04 LTS (Recommended)
* Docker & Docker Compose installed

### 2. Setup Environment

Clone the repository and create your `.env` file:

```bash
git clone https://github.com/chaimoma/Smart-LogiTrack.git
cd Smart-LogiTrack
# Ensure your .env contains POSTGRES_USER, PASSWORD, and JWT_SECRET

```

### 3. Launch Services

Start the infrastructure (Postgres and Airflow):

```bash
docker compose up --build -d

```

*Note: If port 5432 is already in use on your host, stop your local postgres service first.*

### 4. Run the Pipeline

1. Access Airflow at `http://localhost:8080` (login: `admin` / `admin`).
2. Unpause and trigger the `smart_logitrack_dag`.
3. Wait for the **Silver data** to be loaded into Postgres and the **model.pkl** to be generated.

### 5. Run the Backend (Local Mode)

Since the backend is run outside Docker for development flexibility:

```bash
source venv/bin/activate
pip install -r requirements.txt
cd backend
uvicorn main:app --host 0.0.0.0 --port 8001 --reload

```

### 6. Testing the API

Go to `http://localhost:8001/docs` to:

* **Register/Login** to get your JWT token.
* **POST /predict** to get your ETA.
* **GET /analytics** to view performance metrics via SQL CTEs.

---

## 🧪 Testing

Run unit tests for the API and preprocessing:

```bash
pytest tests/

```
