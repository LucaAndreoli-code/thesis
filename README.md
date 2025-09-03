# Simple Pay

Repository contenente il progetto full-stack per la tesi di laurea - Sistema bancario online semplificato

## Tecnologie

**Frontend:**

- Vue.js 3 with Vite
- Tailwind CSS (@plugin DaisyUI)

**Backend:**

- Python FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic (migrations)

## Get started

### Requisiti:

- Python 3.11+
- Node.js 18+
- npm
- Docker & Docker Compose

### Dopo aver clonato la repo:

#### 1. Avvio del database:

```bash
cd simplePay-be
docker-compose up
```

#### 2. Avvio del backend:

**macOS/Linux:**

```bash
cd simplePay-be
python3 -m venv venv
source ./venv/bin/activate
pip3 install -r requirements.txt
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

**Windows:**

```bash
cd simplePay-be
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

#### 3. Avvio del frontend:

**macOS & Windows:**

```bash
cd simplePay-fe
npm install
npm run dev
```

### Accesso Applicazione:

1. **Frontend:** `http://localhost:5173/`
2. **Backend API:** `http://localhost:8000/`
3. **Documentazione API:** `http://localhost:8000/docs`

### Utenze di test:

- Email: `test@simplepay.com` - Password: `password123`
- Email: `admin@simplepay.com` - Password: `password123`

<!-- ## Testing

### Backend:
```bash
cd backend
pytest tests/
```

### Frontend:
```bash
cd frontend
npm test              # Test unitari
npm run test:e2e      # Test E2E
```

## Configurazione

Copia il file `.env.example` in `.env` e modifica le variabili secondo il tuo ambiente:

```bash
cp .env.example .env
``` -->

## Funzionalità

- 👤 Registrazione e autenticazione utenti
- 💳 Gestione conti correnti
- 💰 Visualizzazione saldo e movimenti
- 🏦 Bonifici verso banche esterne (mock)
- 🔒 Sistema sicurezza JWT
