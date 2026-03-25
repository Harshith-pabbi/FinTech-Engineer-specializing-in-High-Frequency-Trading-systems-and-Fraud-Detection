
# SentinelStream

SentinelStream is a high-throughput, horizontally scalable transaction guard for a Neo-bank. It sits between a payment gateway and a core ledger, designed to process 10,000+ Transactions Per Second (TPS) with sub-200ms latency.

## Architecture & Technology Stack

- **Framework**: FastAPI (Async)
- **Database**: PostgreSQL (Star Schema: `FactTransaction`, `DimUser`, `DimMerchant`) with SQLAlchemy AsyncIO
- **Cache/Speed**: Redis (handling Idempotency Middleware)
- **Task Queue**: Celery with RabbitMQ (handling non-blocking async webhooks)
- **ML Layer**: Scikit-Learn Isolation Forest Pipeline (real-time risk scoring)
- **Validation**: Pydantic for strict payload enforcement

## Getting Started

### Prerequisites
- Docker and Docker Compose installed on your host machine.

### Installation & Execution

1. **Clone/Navigate** to the project directory:
   ```bash
   cd SentinelStream
   ```

2. **Run the Docker Stack**:
   Start the entire orchestrated environment in detached mode:
   ```bash
   docker-compose up -d --build
   ```
   This will bring up PostgreSQL, Redis, RabbitMQ, the FastAPI web server on port `8000`, and the background Celery worker.

### Usage

**1. Send a Transaction (POST `/api/v1/transaction`)**

The API requires an `idempotency-key` header to prevent duplicate charges.
```bash
curl -X POST http://localhost:8000/api/v1/transaction \
  -H "Content-Type: application/json" \
  -H "idempotency-key: req-555" \
  -d '{
      "user_id": "usr_999",
      "merchant_id": "mer_777",
      "amount": 250.00,
      "currency": "USD",
      "category": "groceries",
      "location": "Home",
      "user_status": "active"
  }'
```

**2. Watch the background worker:**
```bash
docker-compose logs -f worker
```
You will see Celery processing the async webhook triggered by the transaction.

## Testing

A basic `pytest` suite is included to verify the Fraud Engine (Rule Engine + ML Score).

To run the tests locally (if you have the Python environment set up):
```bash
python -m pytest tests/
```

Or run them inside the Docker container:
```bash
docker-compose exec web pytest tests/
```

## Modular File Structure
```
SentinelStream/
├── app/
│   ├── api/          # FastAPI Routes
│   ├── core/         # Settings & Config
│   ├── db/           # SQLAlchemy Async Models & Sessions
│   ├── schemas/      # Pydantic Schemas
│   ├── services/     # Idempotency, ML Pipeline, Rule Engine
│   └── worker/       # Celery Tasks & App Initialization
├── tests/            # PyTest Suite
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```
