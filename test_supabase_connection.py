import os
import requests
import json
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo local .env
load_dotenv()

SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://ospintibmmfqwrpmkphv.supabase.co")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "")
SUPABASE_SECRET = os.environ.get("SUPABASE_SECRET", "")

def probar_conexion_supabase():
    print("=" * 65)
    print(" COMPROBACIÓN DE CONECTIVIDAD A SUPABASE CLOUD")
    print(f" URL Base: {SUPABASE_URL}")
    print("=" * 65)

    if not SUPABASE_KEY:
        print("[ERROR] No se encontró la variable SUPABASE_KEY en el archivo .env.")
        print("Asegúrate de tener un archivo .env en la raíz con SUPABASE_KEY configurada.")
        return

    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}"
    }

    try:
        # Intentar consultar la tabla 'roles' a través de la Data API (PostgREST)
        endpoint = f"{SUPABASE_URL}/rest/v1/roles?select=*"
        print(f"[INTENTO] Consultando PostgREST endpoint: {endpoint}")
        res = requests.get(endpoint, headers=headers, timeout=6)
        print(f"[HTTP STATUS]: {res.status_code}")
        
        if res.status_code == 200:
            print("[CONEXIÓN EXITOSA] Datos recibidos desde Supabase:")
            print(json.dumps(res.json(), indent=2))
        elif res.status_code == 404 or "does not exist" in res.text:
            print("[AVISO] La base de datos responde pero aún no se han ejecutado las tablas.")
            print("👉 Pega el archivo 'supabase_schema.sql' en el SQL Editor de Supabase y vuelve a probar.")
        else:
            print(f"[RESPUESTA SUPABASE]: {res.text}")
    except Exception as e:
        print(f"[ERROR DE CONEXIÓN]: {e}")

if __name__ == "__main__":
    probar_conexion_supabase()
