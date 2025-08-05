# IM-Space-News-System

This project is a web application and data pipeline for collecting, storing, and visualizing space-related news articles. It leverages Django, Airflow, MongoDB, and Docker for a robust, scalable, and interactive experience.

## Project Structure

```
IM-Space-News-System/
│
├── app/                        # Django project and Streamlit app
│   ├── catalog/                # Django app for catalog views and templates
│   ├── space_catalog/          # Django project settings and URLs
│   ├── db.sqlite3              # SQLite DB for Django (dev only)
│   ├── manage.py               # Django management script
│   ├── requirements.txt        # Python dependencies for Django/Streamlit
│   └── Dockerfile              # Dockerfile for Django/Streamlit
│
├── dags/                       # Airflow DAGs and utilities
│   ├── spaceflight_dag.py      # Airflow DAG for Spaceflight API pipeline
│   ├── spaceflight_functions.py# ETL functions for DAG
│   └── utils/                  # Utility scripts for other APIs
│
├── logs/                       # Airflow logs (gitignored)
│
├── requirements.txt            # Python dependencies for Airflow
├── Dockerfile                  # Dockerfile for Airflow
├── docker-compose.yml          # Multi-service orchestration
├── .gitignore                  # Files and folders to ignore in git
└── README.md                   # Project documentation
```

## Features

- **Data Pipeline**: Uses Apache Airflow to extract articles from the Spaceflight News API and other sources, transform them, and load them into MongoDB.
- **Web Dashboard**: Django app displays articles, search, publisher grouping, and interactive dashboard with charts and word clouds.
- **Dockerized**: All components run in containers for easy setup and deployment.

## Technologies

- **Backend**: Django, Python
- **Data Pipeline**: Apache Airflow, Python
- **Database**: MongoDB (for articles), SQLite (for Django dev)
- **Visualization**: Plotly, WordCloud, Matplotlib
- **Containerization**: Docker, docker-compose

## Getting Started

### Prerequisites

- Docker & Docker Compose

### Quick Start

1. **Clone the repository**
   ```sh
   git clone <repo-url>
   cd IM-Space-News-System
   ```

2. **Start all services**
   ```sh
   docker-compose up --build
   ```

   This will start:
   - Airflow webserver (localhost:8080)
   - Airflow scheduler
   - PostgreSQL (for Airflow metadata)
   - MongoDB (localhost:27018)
   - Django app (localhost:8000)

3. **Access the apps**
   - Django: [http://localhost:8000](http://localhost:8000)
   - Airflow: [http://localhost:8080](http://localhost:8080)

4. **Run Airflow DAGs**
   - Open Airflow UI and trigger the `spaceflight_data_pipeline` DAG to fetch and load articles.

## Customization

- **MongoDB Connection**: The Django app connects to MongoDB at `host.docker.internal:27018` (for local dev). Adjust in [`catalog/views.py`](app/catalog/views.py) if needed.
- **Airflow DAGs**: Add or modify DAGs in [`dags/`](dags/).

## Folder Details

- [`app/catalog/views.py`](app/catalog/views.py): Django views for index, search, publishers, dashboard.
- [`dags/spaceflight_functions.py`](dags/spaceflight_functions.py): ETL logic for fetching and loading articles.
- [`dags/spaceflight_dag.py`](dags/spaceflight_dag.py): Airflow DAG definition.

## Page in use:
<img width="1920" height="1140" alt="image" src="https://github.com/user-attachments/assets/52939c33-22e7-4241-ac92-366a6273d003" />
<img width="1920" height="1140" alt="image" src="https://github.com/user-attachments/assets/46ff5d20-dbf1-4ad6-a256-7e59378a0055" />
<img width="1920" height="1140" alt="image" src="https://github.com/user-attachments/assets/5795bbd0-c15e-459a-81ca-4259605fb747" />
<img width="1920" height="1140" alt="image" src="https://github.com/user-attachments/assets/e247dd03-653b-4d93-86d8-ab456122edce" />
<img width="1920" height="1140" alt="image" src="https://github.com/user-attachments/assets/5d725451-9f88-4e9c-be50-9dc9f4136dbd" />
<img width="1920" height="1140" alt="image" src="https://github.com/user-attachments/assets/b80c5b25-06ef-4629-90b0-5963376be29c" />

*For more details, see the code and comments in each folder.*
