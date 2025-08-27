# migration_manager.py
import os
import subprocess
import sys

# Fix import path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import inspect, text
from database import engine
from src.models import Base


def run_command(cmd):
    """Esegue comando shell"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr


def auto_migrate():
    """Auto-migrazione solo se necessario"""
    print("🔍 Controllo se servono migrazioni...")

    # Prima controlla se ci sono differenze senza creare file
    success, output = run_command("alembic check")
    if success:
        print("✅ Database già aggiornato")
        return True

    # Se alembic check fallisce, significa che ci sono differenze
    print("📝 Rilevate modifiche, creo migrazione...")
    success, output = run_command("alembic revision --autogenerate -m 'Auto update'")

    if "No changes in schema detected" in output:
        print("✅ Nessuna migrazione necessaria")
        return True

    if success:
        print("✅ Migrazione creata")
        # Applica migrazione
        success, output = run_command("alembic upgrade head")
        if success:
            print("✅ Migrazione applicata")
            return True
        else:
            print(f"❌ Errore applicazione: {output}")
    else:
        print(f"❌ Errore creazione migrazione: {output}")

    return False


def setup_database():
    """Setup database completo"""
    print("🗄️ Setup database...")

    # Test connessione
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("✅ Connessione database OK")
    except Exception as e:
        print(f"❌ Errore connessione: {e}")
        return False

    # Controlla tabelle
    inspector = inspect(engine)
    tables = inspector.get_table_names()

    if len(tables) == 0:
        print("📋 Database vuoto, creo tabelle...")
        Base.metadata.create_all(bind=engine)
        run_command("alembic stamp head")
        print("✅ Database inizializzato")
    else:
        print("🔄 Database esistente, controllo migrazioni...")
        auto_migrate()

    print("🎉 Database pronto!")
    return True