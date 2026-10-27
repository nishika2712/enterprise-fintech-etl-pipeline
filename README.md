# Fintech Transaction ETL & Data Quality Pipeline

[![CI](https://github.com/nishika2712/enterprise-fintech-etl-pipeline/actions/workflows/ci.yml/badge.svg)](https://github.com/nishika2712/enterprise-fintech-etl-pipeline/actions)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Apache Spark](https://img.shields.io/badge/Apache%20Spark-3.5-orange.svg)](https://spark.apache.org/)

A batch ETL and data quality pipeline for financial transaction records. It reads raw JSON transactions, removes invalid records with PySpark, aggregates spending per customer, and writes the result as Parquet. Transformation logic is covered by Pytest and run automatically through GitHub Actions.

> This is a portfolio project built on small, mock datasets. It demonstrates pipeline structure, testing and CI. It is not a production-scale system.

---

## Business Use Case

Raw transaction logs often contain failed transactions and invalid amounts. Running risk or spending analytics directly on operational databases adds load to production systems. This project shows a simple, testable way to prepare that data separately:

1. **Ingest** raw JSON transaction records.
2. **Clean and transform** with PySpark: drop invalid and failed transactions, then aggregate spend per customer.
3. **Persist** the output as Parquet (columnar format) in a data-lake-style folder layout.
4. **Validate** the transformation logic with Pytest.
5. **Automate** test runs with GitHub Actions.

---

## Sample Data

**Input** (`data/raw_transactions.json`)

| transaction_id | customer_id | amount | status    |
|----------------|-------------|--------|-----------|
| T1             | C1          | 100.0  | COMPLETED |
| T2             | C1          | -10.0  | FAILED    |

**Output** (`data/output_parquet/`)

| customer_id | total_spent |
|-------------|-------------|
| C1          | 100.0       |

T2 is dropped because it is a failed transaction with a negative amount.

## Data Quality Rules

- Failed transactions are excluded.
- Negative-amount records are excluded.
- Remaining transactions are aggregated into `total_spent` per `customer_id`.
- These rules are asserted in `tests/test_transform.py`.

## Mock Data Generator

`etl/generate_mock_events.py` creates random mock transactions for local testing. It deliberately includes negative amounts and `FAILED` / `PENDING` statuses so the cleaning logic has something to remove. Output goes to `data/generated_transactions.json`, separate from the committed sample input.

```bash
python etl/generate_mock_events.py
```

---

## Project Structure

```text
enterprise-fintech-etl-pipeline/
├── .github/
│   └── workflows/ci.yml           # GitHub Actions: install, test, run pipeline on push
├── data/
│   ├── raw_transactions.json      # Sample input transactions
│   └── output_parquet/            # Parquet output
├── dags/
│   └── fintech_etl_dag.py         # Airflow DAG definition (authored, not deployed)
├── dbt/                           # dbt project scaffold (exploratory)
│   ├── dbt_project.yml
│   └── models/
│       ├── staging/
│       └── marts/
├── etl/
│   ├── transform_spark.py         # PySpark cleaning and aggregation
│   └── generate_mock_events.py    # Mock transaction generator for local testing
├── tests/
│   └── test_transform.py          # Pytest transformation tests
├── docker-compose.yml             # Airflow setup draft (exploratory, unverified)
├── pytest.ini                     # Adds project root to the import path
├── requirements.txt               # Python dependencies
└── README.md
```

## Technology Stack

| Area            | Tools                   |
|-----------------|-------------------------|
| Language        | Python                  |
| Processing      | Apache Spark (PySpark)  |
| Storage format  | Apache Parquet          |
| Testing         | Pytest                  |
| CI/CD           | GitHub Actions          |
| Version control | Git, GitHub             |

Airflow and dbt files are included as exploratory work (see Limitations).

---

## Getting Started

### Prerequisites

- Python 3.10 or higher (3.12 tested)
- Java 17 (required by Spark). On macOS: `brew install openjdk@17`, then:

```bash
echo 'export JAVA_HOME=$(/usr/libexec/java_home -v 17)' >> ~/.zshrc
source ~/.zshrc
java -version
```

### 1. Clone the repository

```bash
git clone https://github.com/nishika2712/enterprise-fintech-etl-pipeline.git
cd enterprise-fintech-etl-pipeline
```

### 2. Create a virtual environment and install dependencies

```bash
python3 -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate

pip install -r requirements.txt
```

### 3. Run the PySpark pipeline

```bash
python etl/transform_spark.py
```

The output is written to `data/output_parquet/`.

### 4. Run the tests

```bash
pytest tests/ -v
```

The first run takes 10 to 20 seconds while Spark starts.

---

## CI/CD

`.github/workflows/ci.yml` runs on every push to `main`. It:

1. Starts a clean Ubuntu runner.
2. Sets up Python and Java 17.
3. Installs dependencies from `requirements.txt`.
4. Runs the Pytest suite.
5. Runs the PySpark pipeline end to end.

---

## Limitations and Next Steps

- **Scale:** inputs are small mock files. The logic is written in PySpark, but it has not been tested on large volumes.
- **Storage:** output is local Parquet files, not a cloud data lake or warehouse.
- **Airflow:** the DAG in `dags/` is authored but has not been run in a live Airflow environment. `docker-compose.yml` is an unverified draft: it does not yet initialize the metadata database or start a scheduler. Airflow is not in `requirements.txt`.
- **dbt:** `dbt/` is a project scaffold with `staging` and `marts` folders. The models have not been validated with `dbt run` / `dbt test`, and no dbt adapter is installed.
- **Streaming:** there is no streaming or CDC component. A Kafka-based ingestion flow is a possible future extension.
- **Other extensions:** schema validation on ingest, incremental loads, loading the output into a warehouse such as BigQuery, and data quality reporting.