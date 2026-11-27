import os
import sys
import time
import subprocess
import requests

def wait_for_server(url="http://localhost:3000/api/health", timeout=15):
    start = time.time()
    while time.time() - start < timeout:
        try:
            res = requests.get(url, timeout=2)
            if res.status_code == 200:
                print(f"[OK] Servidor detectado y respondiendo en {url}")
                return True
        except Exception:
            time.sleep(1)
    return False

def main():
    print("=" * 60)
    print(" EJECUTANDO SUITE DE PRUEBAS PLAYWRIGHT (FRONTEND Y BACKEND)")
    print(" Generando reporte HTML oficial estilo Rahul Shetty...")
    print("=" * 60)

    # Verificar si el servidor local está activo
    server_running = wait_for_server(timeout=3)
    server_process = None

    if not server_running:
        print("[INFO] Levantando servidor local en segundo plano para las pruebas...")
        server_process = subprocess.Popen(["node", "src/server.js"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if not wait_for_server(timeout=10):
            print("[ERROR] No se pudo iniciar el servidor local en http://localhost:3000")
            if server_process:
                server_process.kill()
            sys.exit(1)

    try:
        # Ejecutar pytest con pytest-html
        report_file = "reporte_playwright_usuarios.html"
        cmd = [
            sys.executable,
            "-m",
            "pytest",
            "tests_e2e",
            f"--html={report_file}",
            "--self-contained-html",
            "-v"
        ]
        print(f"[EJECUTANDO] {' '.join(cmd)}")
        result = subprocess.run(cmd)
        
        print("\n" + "=" * 60)
        if result.returncode == 0:
            print(f"[ÉXITO] Todas las pruebas pasaron correctamente.")
            print(f"[REPORTE GENERADO] Archivo listo: {os.path.abspath(report_file)}")
        else:
            print(f"[AVISO] Algunas pruebas finalizaron con código: {result.returncode}")
        print("=" * 60)
    finally:
        if server_process:
            print("[INFO] Deteniendo servidor local de pruebas...")
            server_process.terminate()
            try:
                server_process.wait(timeout=3)
            except Exception:
                server_process.kill()

if __name__ == "__main__":
    main()
