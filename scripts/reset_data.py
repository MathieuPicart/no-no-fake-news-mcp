import sys
import os

# Add project root to path to allow imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy import text
from app.db.database import engine
from app.services.cache import CacheManager
from app.config import settings

def reset_db():
    print("🧹 Vuidage de la table 'analyses'...")
    try:
        with engine.connect() as connection:
            transaction = connection.begin()
            try:
                # Truncate table and reset serial ID
                connection.execute(text("TRUNCATE TABLE analyses RESTART IDENTITY;"))
                transaction.commit()
                print("✅ Base de données réinitialisée avec succès.")
            except Exception as e:
                transaction.rollback()
                print(f"❌ Erreur lors du vuidage de la table : {e}")
    except Exception as e:
        print(f"❌ Impossible de se connecter à la base de données : {e}")

def reset_cache():
    print("⚡ Vuidage du cache Redis...")
    cache = CacheManager()
    if cache.enabled and cache.client:
        try:
            cache.client.flushall()
            print("✅ Cache Redis vidé avec succès.")
        except Exception as e:
            print(f"❌ Erreur lors du vuidage du cache : {e}")
    else:
        print("⚠️ Redis n'est pas activé ou n'est pas joignable.")

if __name__ == "__main__":
    print("--- No No Fake News - Data Reset Tool ---")
    reset_db()
    reset_cache()
    print("-----------------------------------------")
