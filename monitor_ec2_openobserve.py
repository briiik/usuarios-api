import os
import sys
import time
import json
import psutil
import requests

OPENOBSERVE_ENDPOINT = os.environ.get("OPENOBSERVE_ENDPOINT", "https://api.openobserve.ai")
OPENOBSERVE_ORG = os.environ.get("OPENOBSERVE_ORG", "default")
OPENOBSERVE_STREAM = os.environ.get("OPENOBSERVE_STREAM", "infrastructure_metrics")
OPENOBSERVE_AUTH = os.environ.get("OPENOBSERVE_AUTH", "")

def obtener_metricas():
    # CPU y RAM
    cpu_percent = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory()
    
    # Red (ancho de banda I/O)
    net_io = psutil.net_io_counters()
    
    # Disco
    disk = psutil.disk_usage('/') if os.name != 'nt' else psutil.disk_usage('C:\\')

    # Temperatura (en EC2 o máquinas virtuales se estima en base al cómputo si no hay sensor de silicio)
    temperatura = 42.0
    try:
        temps = psutil.sensors_temperatures()
        if temps:
            for name, entries in temps.items():
                if entries:
                    temperatura = entries[0].current
                    break
        else:
            temperatura = round(40.0 + (cpu_percent * 0.28), 1)
    except Exception:
        temperatura = round(40.0 + (cpu_percent * 0.28), 1)

    metrica = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "servidor": "AWS-EC2-usuarios-api",
        "ip_publica": "3.135.214.137",
        "cpu_percent": cpu_percent,
        "memoria_ram_mb": round(ram.used / (1024 * 1024), 2),
        "memoria_total_mb": round(ram.total / (1024 * 1024), 2),
        "memoria_porcentaje": ram.percent,
        "ancho_banda_enviado_kb": round(net_io.bytes_sent / 1024, 2),
        "ancho_banda_recibido_kb": round(net_io.bytes_recv / 1024, 2),
        "disco_porcentaje": disk.percent,
        "temperatura_celsius": temperatura
    }
    return metrica

def enviar_metrica(metrica):
    if not OPENOBSERVE_AUTH:
        print("[MOCK OBSERVE - Sin credenciales configuradas, imprimiendo métrica local]:")
        print(json.dumps(metrica, indent=2))
        return True

    url = f"{OPENOBSERVE_ENDPOINT}/api/{OPENOBSERVE_ORG}/{OPENOBSERVE_STREAM}/_json"
    headers = {
        "Content-Type": "application/json",
        "Authorization": OPENOBSERVE_AUTH if OPENOBSERVE_AUTH.startswith("Basic ") else f"Basic {OPENOBSERVE_AUTH}"
    }

    try:
        res = requests.post(url, headers=headers, json=[metrica], timeout=5)
        if res.status_code in (200, 201):
            print(f"[OK] Métrica enviada a OpenObserve ({res.status_code}) | CPU: {metrica['cpu_percent']}% | RAM: {metrica['memoria_porcentaje']}% | Temp: {metrica['temperatura_celsius']}°C")
            return True
        else:
            print(f"[ERROR] OpenObserve respondió con estado {res.status_code}: {res.text}")
            return False
    except Exception as e:
        print(f"[ERROR] Excepción al enviar métricas: {e}")
        return False

def main():
    print("=" * 65)
    print(" AGENTE DE MONITOREO DE INFRAESTRUCTURA PARA OPENOBSERVE")
    print(" Supervisando: CPU, RAM, Ancho de Banda y Temperatura")
    print("=" * 65)

    if "--once" in sys.argv:
        m = obtener_metricas()
        enviar_metrica(m)
        return

    intervalo = 15
    print(f"[INFO] Recolectando y transmitiendo cada {intervalo} segundos (Ctrl + C para salir)...")
    try:
        while True:
            m = obtener_metricas()
            enviar_metrica(m)
            time.sleep(intervalo)
    except KeyboardInterrupt:
        print("\n[INFO] Monitor detenido por el usuario.")

if __name__ == "__main__":
    main()
