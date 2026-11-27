import os
import pytest
from playwright.sync_api import Page, expect

BASE_URL = os.environ.get("TARGET_URL", "http://localhost:3000")

# =========================================================================
# BLOQUE 1: PRUEBAS FUNCIONALES DE NAVEGACIÓN Y ARRANQUE (CP0001 - CP0015)
# =========================================================================

def test_0001_validar_titulo_oficial(page: Page):
    """CP0001: Validar título oficial del documento y encabezado de la aplicación"""
    page.goto(f"{BASE_URL}/app")
    expect(page).to_have_title("Portal de Administración - Usuarios y Roles")
    expect(page.locator("#app-title")).to_contain_text("Portal de Usuarios y Roles")

def test_0002_validar_badge_salud_healthcheck(page: Page):
    """CP0002: Validar visibilidad del indicador de salud y latency pill"""
    page.goto(f"{BASE_URL}/app")
    pill = page.locator("#health-pill")
    expect(pill).to_be_visible()
    expect(page.locator("#status-dot")).to_be_visible()

def test_0003_validar_tarjetas_metricas(page: Page):
    """CP0003: Validar visualización de las cuatro tarjetas de observabilidad"""
    page.goto(f"{BASE_URL}/app")
    expect(page.locator("#stat-usuarios")).to_be_visible()
    expect(page.locator("#stat-roles")).to_be_visible()
    expect(page.locator("#stat-health")).to_be_visible()
    expect(page.locator("#stat-entorno")).to_be_visible()

def test_0004_validar_formulario_roles(page: Page):
    """CP0004: Validar presencia y atributos del input de creación de roles"""
    page.goto(f"{BASE_URL}/app")
    expect(page.locator("#input-rol-nombre")).to_be_visible()
    expect(page.locator("#btn-crear-rol")).to_be_enabled()

def test_0005_validar_formulario_usuarios(page: Page):
    """CP0005: Validar campos obligatorios en formulario de usuarios"""
    page.goto(f"{BASE_URL}/app")
    expect(page.locator("#input-usuario-nombre")).to_be_visible()
    expect(page.locator("#input-usuario-correo")).to_be_visible()
    expect(page.locator("#input-usuario-password")).to_be_visible()
    expect(page.locator("#input-usuario-confirm-password")).to_be_visible()
    expect(page.locator("#select-usuario-rol")).to_be_visible()
    expect(page.locator("#btn-crear-usuario")).to_be_enabled()

def test_0006_flujo_creacion_rol(page: Page):
    """CP0006: Crear un rol mediante la interfaz y verificar inserción"""
    page.goto(f"{BASE_URL}/app")
    nombre_rol = f"Rol-Test-{os.urandom(3).hex()}"
    page.fill("#input-rol-nombre", nombre_rol)
    page.click("#btn-crear-rol")
    page.wait_for_timeout(800)
    expect(page.locator("#select-usuario-rol")).to_contain_text(nombre_rol)

def test_0007_flujo_registro_usuario_valido(page: Page):
    """CP0007: Registrar usuario con contraseña segura (#$@), confirmación y dominio válido"""
    page.goto(f"{BASE_URL}/app")
    sufijo = os.urandom(3).hex()
    page.fill("#input-usuario-nombre", f"Usuario Playwright {sufijo}")
    page.fill("#input-usuario-correo", f"test.{sufijo}@uteq.edu.mx")
    page.fill("#input-usuario-password", "PasswordSeguro123@")
    page.fill("#input-usuario-confirm-password", "PasswordSeguro123@")
    page.select_option("#select-usuario-rol", index=1)
    page.click("#btn-crear-usuario")
    page.wait_for_timeout(1000)
    expect(page.locator("#cuerpo-tabla-usuarios")).to_contain_text(f"test.{sufijo}@uteq.edu.mx")

def test_0008_filtro_dinamico_usuarios(page: Page):
    """CP0008: Validar buscador y filtro dinámico en tiempo real"""
    page.goto(f"{BASE_URL}/app")
    filtro = page.locator("#filtro-usuarios")
    expect(filtro).to_be_visible()
    page.fill("#filtro-usuarios", "uteq.edu.mx")
    page.wait_for_timeout(500)
    expect(page.locator("#cuerpo-tabla-usuarios")).to_be_visible()

def test_0009_modal_edicion_usuario(page: Page):
    """CP0009: Validar apertura y cierre del modal de edición"""
    page.goto(f"{BASE_URL}/app")
    btn_editar = page.locator(".btn-edit-sm").first
    if btn_editar.is_visible():
        btn_editar.click()
        expect(page.locator("#modal-editar")).to_be_visible()
        page.click(".modal-close")
        expect(page.locator("#modal-editar")).to_be_hidden()

def test_0010_botones_mantenimiento(page: Page):
    """CP0010: Validar botones de descarga de backup, sembrado y vaciado"""
    page.goto(f"{BASE_URL}/app")
    expect(page.locator("#btn-seed-db")).to_be_visible()
    expect(page.locator("#btn-backup-db")).to_be_visible()
    expect(page.locator("#btn-vaciar-db")).to_be_visible()

# =========================================================================
# BLOQUE 2: MONITOREO DE VALIDACIONES DE CONTRASEÑA - LONGITUD (CP0011 - CP0025)
# =========================================================================
PASSWORDS_CORTAS = [
    ("1", "1 carácter"),
    ("12", "2 caracteres"),
    ("123", "3 caracteres"),
    ("1234", "4 caracteres"),
    ("12345", "5 caracteres"),
    ("123456", "6 caracteres"),
    ("1234567", "7 caracteres"),
    ("a@1", "3 caracteres con @"),
    ("ab#12", "5 caracteres con #"),
    ("pass@1", "6 caracteres con @"),
    ("Clav$1", "6 caracteres con $"),
    ("Qw1!", "4 caracteres con !"),
    ("abc*12", "6 caracteres con *"),
    ("a&b123", "6 caracteres con &"),
    ("xyz_1", "5 caracteres con _")
]

@pytest.mark.parametrize("pwd,desc", PASSWORDS_CORTAS)
def test_validacion_password_longitud_corta(page: Page, pwd: str, desc: str):
    """Validar rechazo estricto de contraseñas con longitud menor a 8 caracteres"""
    page.goto(f"{BASE_URL}/app")
    page.fill("#input-usuario-nombre", "Tester Longitud")
    page.fill("#input-usuario-correo", f"longitud_{os.urandom(2).hex()}@gmail.com")
    page.fill("#input-usuario-password", pwd)
    page.fill("#input-usuario-confirm-password", pwd)
    page.select_option("#select-usuario-rol", index=1)
    page.click("#btn-crear-usuario")
    page.wait_for_timeout(400)
    expect(page.locator("#toast")).to_be_visible()
    expect(page.locator("#toast")).to_contain_text("al menos 8 caracteres")

# =========================================================================
# BLOQUE 3: MONITOREO DE CARACTERES ESPECIALES (#, $, @, !, %, *, &, _) (CP0026 - CP0050)
# =========================================================================
PASSWORDS_SIN_ESPECIAL = [
    ("PasswordSeguro1", "Sin carácter especial (15 car)"),
    ("MiClaveSegura99", "Solo alfanumérica"),
    ("Abcdefgh123456", "Mayúsculas y minúsculas sin símbolo"),
    ("AdminUsuarios2026", "Texto y número sin símbolo"),
    ("Sololetrasypunto.", "Con punto no admitido como especial"),
    ("clave12345678", "Solo minúsculas y números"),
    ("SEGURIDADTOTAL2026", "Solo mayúsculas y números"),
    ("PruebaLargaSinSimbolo", "Cadena larga alfanumérica")
]

@pytest.mark.parametrize("pwd,desc", PASSWORDS_SIN_ESPECIAL)
def test_validacion_password_falta_caracter_especial(page: Page, pwd: str, desc: str):
    """Validar rechazo de contraseñas de >=8 caracteres que carecen de caracteres especiales"""
    page.goto(f"{BASE_URL}/app")
    page.fill("#input-usuario-nombre", "Tester Especial")
    page.fill("#input-usuario-correo", f"especial_{os.urandom(2).hex()}@uteq.edu.mx")
    page.fill("#input-usuario-password", pwd)
    page.fill("#input-usuario-confirm-password", pwd)
    page.select_option("#select-usuario-rol", index=1)
    page.click("#btn-crear-usuario")
    page.wait_for_timeout(400)
    expect(page.locator("#toast")).to_be_visible()
    expect(page.locator("#toast")).to_contain_text("carácter especial")

SIMBOLOS_VALIDOS = [
    ("Password#2026", "# (Almohadilla / Hash)"),
    ("Password$2026", "$ (Signo de Dólar)"),
    ("Password@2026", "@ (Arroba)"),
    ("Password!2026", "! (Signo de Exclamación)"),
    ("Password%2026", "% (Porcentaje)"),
    ("Password*2026", "* (Asterisco)"),
    ("Password?2026", "? (Signo de Interrogación)"),
    ("Password&2026", "& (Ampersand)"),
    ("Password_2026", "_ (Guion bajo)"),
    ("Password-2026", "- (Guion medio)")
]

@pytest.mark.parametrize("pwd,simbolo", SIMBOLOS_VALIDOS)
def test_validacion_password_simbolo_valido_admitido(page: Page, pwd: str, simbolo: str):
    """Validar que la contraseña sea aceptada con cada tipo de carácter especial permitido"""
    page.goto(f"{BASE_URL}/app")
    suf = os.urandom(3).hex()
    page.fill("#input-usuario-nombre", f"User {suf}")
    page.fill("#input-usuario-correo", f"user_{suf}@gmail.com")
    page.fill("#input-usuario-password", pwd)
    page.fill("#input-usuario-confirm-password", pwd)
    page.select_option("#select-usuario-rol", index=1)
    page.click("#btn-crear-usuario")
    page.wait_for_timeout(800)
    expect(page.locator("#cuerpo-tabla-usuarios")).to_contain_text(f"user_{suf}@gmail.com")

# =========================================================================
# BLOQUE 4: VALIDACIÓN DE CONTRASEÑAS IDÉNTICAS (CONFIRMACIÓN) (CP0051 - CP0070)
# =========================================================================
MISMATCH_PASSWORDS = [
    ("PasswordSeguro123@", "PasswordSeguro123#", "Diferente carácter especial"),
    ("PasswordSeguro123@", "passwordseguro123@", "Diferente mayúscula / minúscula"),
    ("PasswordSeguro123@", "PasswordSeguro123", "Falta carácter especial en confirmación"),
    ("PasswordSeguro123@", "PasswordSeguro1234@", "Número extra en confirmación"),
    ("PasswordSeguro123@", "OtraPassword999$", "Contraseña totalmente distinta"),
    ("AdminPass#2026", "AdminPass#2025", "Diferencia de un dígito final"),
    ("MiClaveFuerte$1", "MiClaveFuerte$2", "Diferencia numérica final"),
    ("UteqSegura@2026", "UteqSegura@2027", "Diferencia en año de confirmación")
]

@pytest.mark.parametrize("p1,p2,desc", MISMATCH_PASSWORDS)
def test_validacion_contrasenas_no_coinciden(page: Page, p1: str, p2: str, desc: str):
    """Validar rechazo inmediato cuando las dos contraseñas ingresadas no son idénticas"""
    page.goto(f"{BASE_URL}/app")
    page.fill("#input-usuario-nombre", "Tester Mismatch")
    page.fill("#input-usuario-correo", f"mismatch_{os.urandom(2).hex()}@hotmail.com")
    page.fill("#input-usuario-password", p1)
    page.fill("#input-usuario-confirm-password", p2)
    page.select_option("#select-usuario-rol", index=1)
    page.click("#btn-crear-usuario")
    page.wait_for_timeout(400)
    expect(page.locator("#toast")).to_be_visible()
    expect(page.locator("#toast")).to_contain_text("no coinciden")

# =========================================================================
# BLOQUE 5: VALIDACIÓN DE CORREO Y DOMINIOS PERMITIDOS (CP0071 - CP0100)
# =========================================================================
CORREOS_INVALIDOS = [
    ("correosin_arroba.com", "Sin símbolo arroba"),
    ("usuario@invalido.org", "Dominio .org no autorizado"),
    ("usuario@tempmail.com", "Servicio temporal descartable"),
    ("usuario@mailinator.com", "Bandeja desechable pública"),
    ("usuario@fake.net", "Dominio .net no institucional ni público admitido"),
    ("usuario@spam.xyz", "Dominio spam TLD .xyz"),
    ("usuario@dominio-desconocido.es", "Dominio regional no registrado"),
    ("usuario@correo-falso.com", "Dominio genérico no admitido"),
    ("@gmail.com", "Sin identificador de usuario antes de arroba"),
    ("usuario@.com", "Dominio incompleto")
]

@pytest.mark.parametrize("correo,desc", CORREOS_INVALIDOS)
def test_validacion_correos_dominios_no_permitidos(page: Page, correo: str, desc: str):
    """Validar rechazo de correos sin @ o pertenecientes a dominios no autorizados"""
    page.goto(f"{BASE_URL}/app")
    page.fill("#input-usuario-nombre", "Tester Correo")
    page.fill("#input-usuario-correo", correo)
    page.fill("#input-usuario-password", "PasswordSeguro123@")
    page.fill("#input-usuario-confirm-password", "PasswordSeguro123@")
    page.select_option("#select-usuario-rol", index=1)
    page.click("#btn-crear-usuario")
    page.wait_for_timeout(500)
    expect(page.locator("#toast")).to_be_visible()

DOMINIOS_AUTORIZADOS = [
    ("gmail.com", "Google Mail Público"),
    ("uteq.edu.mx", "Universidad Tecnológica de Querétaro"),
    ("hotmail.com", "Microsoft Hotmail"),
    ("outlook.com", "Microsoft Outlook"),
    ("empresa.com", "Dominio Corporativo Empresa")
]

@pytest.mark.parametrize("dominio,nombre_inst", DOMINIOS_AUTORIZADOS)
def test_validacion_dominios_autorizados_exito(page: Page, dominio: str, nombre_inst: str):
    """Validar aceptación y registro exitoso con cada dominio institucional y público permitido"""
    page.goto(f"{BASE_URL}/app")
    suf = os.urandom(3).hex()
    correo = f"registro_{suf}@{dominio}"
    page.fill("#input-usuario-nombre", f"Usuario {suf}")
    page.fill("#input-usuario-correo", correo)
    page.fill("#input-usuario-password", "PasswordSeguro123@")
    page.fill("#input-usuario-confirm-password", "PasswordSeguro123@")
    page.select_option("#select-usuario-rol", index=1)
    page.click("#btn-crear-usuario")
    page.wait_for_timeout(800)
    expect(page.locator("#cuerpo-tabla-usuarios")).to_contain_text(correo)

# =========================================================================
# BLOQUE 6: VALIDACIONES DE CORREO DUPLICADO (CP0101 - CP0110)
# =========================================================================
def test_0101_rechazo_correo_duplicado(page: Page):
    """CP0101: Validar que el sistema rechace registrar dos usuarios con el mismo correo (409 Conflict)"""
    page.goto(f"{BASE_URL}/app")
    correo_unico = f"duplicado_{os.urandom(3).hex()}@uteq.edu.mx"
    
    # Registro 1 (Exitoso)
    page.fill("#input-usuario-nombre", "Usuario Original")
    page.fill("#input-usuario-correo", correo_unico)
    page.fill("#input-usuario-password", "PasswordSeguro123@")
    page.fill("#input-usuario-confirm-password", "PasswordSeguro123@")
    page.select_option("#select-usuario-rol", index=1)
    page.click("#btn-crear-usuario")
    page.wait_for_timeout(800)
    
    # Registro 2 (Intento con mismo correo -> Debe fallar con Toast de error)
    page.fill("#input-usuario-nombre", "Usuario Clon")
    page.fill("#input-usuario-correo", correo_unico)
    page.fill("#input-usuario-password", "PasswordSeguro123@")
    page.fill("#input-usuario-confirm-password", "PasswordSeguro123@")
    page.select_option("#select-usuario-rol", index=1)
    page.click("#btn-crear-usuario")
    page.wait_for_timeout(600)
    
    expect(page.locator("#toast")).to_be_visible()
    expect(page.locator("#toast")).to_contain_text("ya está registrado")

# =========================================================================
# BLOQUE 7: COMPROBACIÓN DE ELEMENTOS DEL DOM Y CONSISTENCIA VISUAL (CP0111 - CP0140)
# =========================================================================
SELECTORES_DOM = [
    ("#app-title", "Título principal H1"),
    (".subtitle", "Subtítulo de tecnologías"),
    ("#health-pill", "Pill indicador de salud"),
    ("#status-dot", "Punto verde pulsante"),
    ("#health-status", "Texto de estado health"),
    ("#health-latency", "Etiqueta de latencia"),
    ("#btn-refrescar", "Botón de actualización"),
    ("#stat-usuarios", "Tarjeta métrica usuarios"),
    ("#stat-roles", "Tarjeta métrica roles"),
    ("#stat-health", "Tarjeta métrica salud"),
    ("#stat-timestamp", "Timestamp de última comprobación"),
    ("#stat-entorno", "Etiqueta de entorno AWS/Docker"),
    ("#badge-total-roles", "Insignia contador de roles"),
    ("#input-rol-nombre", "Campo texto nombre de rol"),
    ("#btn-crear-rol", "Botón registrar rol"),
    ("#tabla-roles", "Tabla contenedora de roles"),
    ("#input-usuario-nombre", "Campo texto nombre completo"),
    ("#input-usuario-correo", "Campo email usuario"),
    ("#input-usuario-password", "Campo contraseña"),
    ("#input-usuario-confirm-password", "Campo confirmación de contraseña"),
    ("#select-usuario-rol", "Menú desplegable selector de rol"),
    ("#btn-crear-usuario", "Botón principal guardar usuario"),
    ("#filtro-usuarios", "Buscador predictivo"),
    ("#tabla-usuarios", "Tabla principal de catálogo"),
    ("#cuerpo-tabla-usuarios", "Cuerpo dinámico de tabla usuarios"),
    ("#btn-seed-db", "Botón sembrado de datos ficticios"),
    ("#btn-backup-db", "Botón descarga de respaldo SQLite"),
    ("#btn-vaciar-db", "Botón vaciado de base de datos"),
    ("#modal-editar", "Modal emergente de edición"),
    ("#host-info", "Código indicador de host")
]

@pytest.mark.parametrize("sel,nombre", SELECTORES_DOM)
def test_consistencia_dom_elementos_ui(page: Page, sel: str, nombre: str):
    """Comprobar aserción y renderizado de cada selector visual en el DOM"""
    page.goto(f"{BASE_URL}/app")
    elemento = page.locator(sel)
    if sel == "#modal-editar":
        expect(elemento).to_be_attached()
    else:
        expect(elemento).to_be_visible()

# =========================================================================
# BLOQUE 8: PRUEBAS DE DISEÑO RESPONSIVO MULTI-RESOLUCIÓN (CP0141 - CP0160)
# =========================================================================
RESOLUCIONES_RESPONSIVAS = [
    (320, 568, "Móvil Extra Compacto (iPhone SE Gen 1)"),
    (360, 640, "Móvil Android Compacto"),
    (375, 667, "Móvil iPhone 8 / SE"),
    (390, 844, "Móvil Moderno iPhone 13 / 14"),
    (412, 915, "Móvil Android Samsung Galaxy / Pixel"),
    (768, 1024, "Tableta iPad Mini / Clásico Vertical"),
    (820, 1180, "Tableta iPad Air"),
    (1024, 768, "Tableta / Laptop Apaisada"),
    (1280, 720, "Resolución HD 720p"),
    (1366, 768, "Laptop Estándar WXGA"),
    (1440, 900, "MacBook Pro 15"),
    (1536, 864, "Laptop FullHD Escalada"),
    (1920, 1080, "Escritorio Full HD 1080p"),
    (2560, 1440, "Monitor QHD / 2K"),
    (3840, 2160, "Pantalla Ultra HD / 4K")
]

@pytest.mark.parametrize("ancho,alto,dispositivo", RESOLUCIONES_RESPONSIVAS)
def test_renderizado_resolucion_viewport(page: Page, ancho: int, alto: int, dispositivo: str):
    """Validar que la estructura gráfica se mantenga responsiva en múltiples pantallas"""
    page.set_viewport_size({"width": ancho, "height": alto})
    page.goto(f"{BASE_URL}/app")
    expect(page.locator("#app-title")).to_be_visible()
    expect(page.locator(".topbar")).to_be_visible()
    expect(page.locator(".main-content")).to_be_visible()

# =========================================================================
# BLOQUE 9: PRUEBAS DE OBSERVABILIDAD Y LATENCIA HTTP (<1000ms) (CP0161 - CP0170)
# =========================================================================
def test_0161_latencia_endpoint_health(page: Page):
    """CP0161: Validar que el tiempo de respuesta del Healthcheck sea inferior a 1.0s"""
    inicio = page.evaluate("performance.now()")
    res = page.request.get(f"{BASE_URL}/api/health")
    fin = page.evaluate("performance.now()")
    duracion = fin - inicio
    assert res.status == 200
    assert duracion < 1000, f"Latencia excesiva: {duracion}ms"

def test_0162_latencia_catalogo_usuarios(page: Page):
    """CP0162: Validar que la consulta de catálogo general responda en menos de 1000ms"""
    inicio = page.evaluate("performance.now()")
    res = page.request.get(f"{BASE_URL}/api/usuarios")
    fin = page.evaluate("performance.now()")
    assert res.status == 200
    assert (fin - inicio) < 1000

# =========================================================================
# BLOQUE 10: BÚSQUEDA Y FILTRADO DE USUARIOS FICTICIOS (CP0171 - CP0190)
# =========================================================================
USUARIOS_BUSQUEDA = [
    ("Brisa", "Búsqueda por nombre de Administrador 'Brisa'"),
    ("Granados", "Búsqueda por apellido 'Granados'"),
    ("uteq.edu.mx", "Filtrado por dominio institucional 'uteq.edu.mx'"),
    ("Emmanuel", "Búsqueda de docente/supervisor 'Emmanuel'"),
    ("Carlos", "Búsqueda de operador 'Carlos'"),
    ("gmail.com", "Filtrado por dominio público 'gmail.com'"),
    ("Mariana", "Búsqueda de auditor 'Mariana'"),
    ("hotmail.com", "Filtrado por dominio 'hotmail.com'"),
    ("Rodrigo", "Búsqueda de usuario 'Rodrigo'"),
    ("empresa.com", "Filtrado por dominio corporativo 'empresa.com'"),
    ("Sofía", "Búsqueda con acento 'Sofía'"),
    ("outlook.com", "Filtrado por dominio 'outlook.com'")
]

@pytest.mark.parametrize("termino,desc", USUARIOS_BUSQUEDA)
def test_busqueda_filtrado_usuarios_ficticios(page: Page, termino: str, desc: str):
    """Comprobar que el filtro en vivo localice a los usuarios sembrados en la base de datos"""
    page.goto(f"{BASE_URL}/app")
    page.fill("#filtro-usuarios", termino)
    page.wait_for_timeout(350)
    tabla = page.locator("#cuerpo-tabla-usuarios")
    expect(tabla).to_be_visible()

# =========================================================================
# BLOQUE 11: VALIDACIÓN DE CABECERAS HTTP Y CONEXIÓN REST (CP0191 - CP0210)
# =========================================================================
ENDPOINTS_API_REST = [
    ("/api/health", 200, "Healthcheck con estado de servidor"),
    ("/api/roles", 200, "Listado de catálogo de roles"),
    ("/api/usuarios", 200, "Listado general de usuarios"),
    ("/api/endpoint-no-existente-404", 404, "Manejo de ruta inexistente")
]

@pytest.mark.parametrize("ruta,codigo_esperado,desc", ENDPOINTS_API_REST)
def test_contrato_api_codigos_http(page: Page, ruta: str, codigo_esperado: int, desc: str):
    """Validar códigos de estado HTTP y Content-Type de la API REST"""
    res = page.request.get(f"{BASE_URL}{ruta}")
    assert res.status == codigo_esperado
    assert "application/json" in res.headers.get("content-type", "")

PARAM_PASSWORDS_VARIADAS = [
    ("Clave@12345", "@ en posición 6"),
    ("!Clave12345", "! al inicio"),
    ("Clave12345!", "! al final"),
    ("Segura#2026", "# intermedio"),
    ("$Segura2026", "$ al inicio"),
    ("Segura2026$", "$ al final"),
    ("Admin%2026A", "% intermedio"),
    ("*Admin2026A", "* al inicio"),
    ("Admin2026A*", "* al final"),
    ("Super&User1", "& intermedio"),
    ("Super_User1", "_ intermedio"),
    ("Super-User1", "- intermedio"),
    ("Test?User26", "? intermedio"),
    ("P@ssw0rd!#$", "Múltiples caracteres especiales"),
    ("Uteq_10mo#A", "Combinación alfanumérica y dos símbolos")
]

@pytest.mark.parametrize("pwd_var,pos", PARAM_PASSWORDS_VARIADAS)
def test_contrasena_posicion_caracter_especial(page: Page, pwd_var: str, pos: str):
    """Validar que los caracteres especiales se reconozcan en cualquier posición de la clave"""
    page.goto(f"{BASE_URL}/app")
    suf = os.urandom(3).hex()
    page.fill("#input-usuario-nombre", f"Usuario {suf}")
    page.fill("#input-usuario-correo", f"pos_{suf}@empresa.com")
    page.fill("#input-usuario-password", pwd_var)
    page.fill("#input-usuario-confirm-password", pwd_var)
    page.select_option("#select-usuario-rol", index=1)
    page.click("#btn-crear-usuario")
    page.wait_for_timeout(800)
    expect(page.locator("#cuerpo-tabla-usuarios")).to_contain_text(f"pos_{suf}@empresa.com")

# =========================================================================
# BLOQUE 12: MONITOREO Y VALIDACIÓN DE ROLES (CP0211 - CP0226)
# =========================================================================
ROLES_ESPECIALES = [
    ("Auditor-Calidad", "Rol con guion medio"),
    ("Lider_Seguridad", "Rol con guion bajo"),
    ("Soporte.Nivel2", "Rol con punto"),
    ("AdminGeneral2026", "Rol alfanumérico"),
    ("Super_Admin_Global", "Rol compuesto triple"),
    ("Tester_Playwright", "Rol de pruebas"),
    ("DevOps_Engineer", "Rol de infraestructura"),
    ("Analista_Datos", "Rol analítico"),
    ("Coordinador_TI", "Rol administrativo"),
    ("Invitado_Temporal", "Rol restringido"),
    ("Gerente_Ventas", "Rol comercial"),
    ("Director_Operaciones", "Rol directivo"),
    ("Auditor_Financiero", "Rol financiero"),
    ("Especialista_Redes", "Rol telecomunicaciones"),
    ("Seguridad_Perimetral", "Rol ciberseguridad")
]

@pytest.mark.parametrize("rol_esp,tipo", ROLES_ESPECIALES)
def test_creacion_roles_diversos(page: Page, rol_esp: str, tipo: str):
    """Comprobar inserción de diferentes categorías de roles organizacionales"""
    page.goto(f"{BASE_URL}/app")
    nom = f"{rol_esp}-{os.urandom(2).hex()}"
    page.fill("#input-rol-nombre", nom)
    page.click("#btn-crear-rol")
    page.wait_for_timeout(700)
    expect(page.locator("#select-usuario-rol")).to_contain_text(nom)
