# 🚀 Enterprise Fintech ETL & Data Pipeline

[![Data Engineering CI Pipeline](https://github.com/nishika2712/enterprise-fintech-etl-pipeline/actions/workflows/ci.yml/badge.svg)](https://github.com/nishika2712/enterprise-fintech-etl-pipeline/actions)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Apache Spark](https://img.shields.io/badge/Apache%20Spark-3.5-orange.svg)](https://spark.apache.org/)
[![Apache Airflow](https://img.shields.io/badge/Apache%20Airflow-Orchestration-red.svg)](https://airflow.apache.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An end-to-end batch ETL and data quality pipeline designed for fintech platforms. This project automates the ingestion, cleaning, transformation, and validation of high-volume financial transaction records into optimized columnar data lake storage.

---

## 💡 Business Use Case & Core Idea
In modern fintech and lending ecosystems (such as enterprise financial platforms), raw operational transaction logs arrive with structural anomalies, failed transaction statuses, and zero-value errors. Querying operational databases directly for risk analytics degrades production performance. 

This project solves that challenge by:
1. **Ingesting** raw JSON transaction feeds.
2. **Transforming** datasets using distributed PySpark processing to filter out invalid/failed transactions and aggregate customer spending behaviors.
3. **Persisting** data into compressed, high-performance **Parquet** columnar files (Data Lake format).
4. **Orchestrating** workflows sequentially using **Apache Airflow DAGs**.
5. **Enforcing Quality** via automated **Pytest** unit tests and **GitHub Actions CI/CD** automation.

---

## 🏗️ Architecture & Project Structure

```text
enterprise-fintech-etl-pipeline/
├── .github/
│   └── workflows/ci.yml                # Automated CI/CD pipeline (Pytest & Python execution on push)
├── data/
│   ├── raw_transactions.json           # Raw mock input financial transactions
│   └── output_parquet/                 # Processed Data Lake storage (Parquet format)
├── dags/
│   └── fintech_etl_dag.py              # Apache Airflow DAG orchestration script
├── etl/
│   └── transform_spark.py              # PySpark batch extraction, data cleaning & aggregation script
├── tests/
│   └── test_transform.py               # Pytest automated data quality & transformation unit tests
├── requirements.txt                    # Project python dependencies
└── README.md                           # Project documentation

## 🛠️ Technology Stack
1. Programming Language: Python
2. Data Processing & ETL: Apache Spark (PySpark)
3. Orchestration: Apache Airflow (DAGs & BashOperators)
4. Storage Format: Apache Parquet (Columnar Data Lake storage)
5. Data Quality & Testing: Pytest
6. DevOps & CI/CD: GitHub Actions
7. Version Control: Git & GitHub

## ⚙️ Getting Started & Local Setup
1. Clone the Repository
git clone [https://github.com/nishika2712/enterprise-fintech-etl-pipeline.git](https://github.com/nishika2712/enterprise-fintech-etl-pipeline.git)
cd enterprise-fintech-etl-pipeline

2. Set Up a Virtual Environment & Install Dependencies
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
pip install -r requirements.txt

3. Run the PySpark ETL Pipeline
Execute the transformation script to process raw transactions and generate Parquet outputs:
python etl/transform_spark.py

4. Run Automated Data Quality Tests
Execute the unit test suite to verify transformation logic and data integrity:
pytest tests/

## 🔄 CI/CD Pipeline Automation
This repository utilizes GitHub Actions (.github/workflows/ci.yml). Every time code is pushed to the main branch, the CI server automatically:
1. Provisions a clean Ubuntu virtual machine.
2. Installs all project dependencies.
3. Executes the full Pytest data validation suite.
4. Runs the end-to-end PySpark batch ingestion pipeline.