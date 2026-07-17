# PersonaGraph

PersonaGraph is a powerful Human Digital Footprint Tracker designed to resolve and monitor open-source intelligence (OSINT) related to digital identities. It offers a modern dashboard to launch and manage identity investigations.

## Technologies Used

- **Frontend:** Next.js (App Router), Tailwind CSS v4, shadcn/ui, TanStack Query, Zustand.
- **Backend:** FastAPI, SQLAlchemy (Async), Alembic, Pydantic, Argon2 (Password Hashing).
- **Database:** PostgreSQL.

## Project Structure

- `/frontend` - The Next.js web application.
- `/backend` - The FastAPI Python server.
- `docker-compose.yml` - Infrastructure services (PostgreSQL database).

## Getting Started

### 1. Prerequisites
- Docker and Docker Compose
- Node.js (v18+)
- Python (3.10+)

### 2. Start the Database
The backend requires a PostgreSQL database to run. Use Docker Compose to spin it up:
```bash
docker-compose up -d
```

### 3. Setup the Backend
Navigate to the `backend` directory, set up your Python environment, and run the database migrations:
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
pip install -r requirements.txt

# Run migrations to set up your tables
alembic upgrade head

# Start the development server
uvicorn src.main:app --reload
```
The API will be available at `http://localhost:8000`. You can view the interactive documentation at `http://localhost:8000/docs`.

### 4. Setup the Frontend
Navigate to the `frontend` directory, install dependencies, and start the development server:
```bash
cd frontend
npm install
npm run dev
```
The web application will be available at `http://localhost:3000`.

## License
MIT
