# Simple Pay

Repository contenente il progetto full-stack per la tesi di laurea - Sistema bancario online semplificato

## Demo Online

L'applicazione è disponibile online all'indirizzo:

**[SimplePay](https://thesis-app-myxvz.ondigitalocean.app/)**
**[Swagger/OpenAPI](https://thesis-app-myxvz.ondigitalocean.app/be/docs)**

### Utenze di test:

- Email: `test@example.com` - Password: `password123`
- Email: `user@example.com` - Password: `password123`

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
python -m uvicorn src.main:app --host 0.0.0.0 --port 8000
```

**Windows:**

```bash
cd simplePay-be
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn src.main:app --host 0.0.0.0 --port 8000
```

Swagger disponibile a questo indirizzo post avvio: **[Swagger/OpenAPI Locale](http://0.0.0.0:8000/docs)**

#### 3. Avvio del frontend:

**macOS & Windows:**

```bash
cd simplePay-fe
npm install
npm run dev
```

### Accesso Applicazione:

1. **Frontend:** `http://localhost:4173/`
2. **Backend API:** `http://localhost:8000/`
3. **Documentazione API:** `http://localhost:8000/docs`

### Configurazione delle ambiente di test:

**Test Backend:**

Con database avviato:

```bash
cd simplePay-be
pytest -v
```

**Test Fronted:**

Avviare il database di test del backend:

```bash
cd simplePay-be
python -m src.main --env test
```

Successivamente avviare i test cypress:

Esegue i test:

```bash
cd simplePay-fe
npm run cy:run
```

Apre cypress:

```bash
cd simplePay-fe
npm run cy:open
```

### Configurazione delle variabili d'ambiente:

Prima di avviare l'applicazione, se necessario modificare variabili d'ambiente su questi file:

**Backend:**

```bash
# Modificare le variabili nel file
simplePay-be/.env
```

**Frontend:**

```bash
# Modificare le variabili nel file
simplePay-fe/.env.development
```

## Funzionalità

- 👤 Registrazione e autenticazione utenti
- 💳 Gestione conti correnti
- 💰 Visualizzazione saldo e movimenti
- 🏦 Bonifici verso banche esterne (mock)
- 🔒 Sistema sicurezza JWT
