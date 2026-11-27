import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def generate_parcial2_report():
    doc = Document()

    # Configuración de márgenes estándar de 1 pulgada (2.54 cm) estilo LaTeX / APA
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
        # Pie de página con numeración
        footer = section.footer
        p_footer = footer.paragraphs[0]
        p_footer.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        f_run = p_footer.add_run()
        f_run.font.name = 'Georgia'
        f_run.font.size = Pt(9)
        f_run.font.color.rgb = RGBColor(0x66, 0x66, 0x66)

    # Estilo base
    style_normal = doc.styles['Normal']
    font = style_normal.font
    font.name = 'Georgia'
    font.size = Pt(11)
    font.color.rgb = RGBColor(0x22, 0x22, 0x22)
    style_normal.paragraph_format.line_spacing = 1.2
    style_normal.paragraph_format.space_after = Pt(6)
    style_normal.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    # Helpers de estilo
    def set_cell_background(cell, fill_hex):
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
        cell._tc.get_or_add_tcPr().append(shd)

    def set_cell_margins(cell, top=120, bottom=120, left=150, right=150):
        tcPr = cell._tc.get_or_add_tcPr()
        tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
        tcPr.append(tcMar)

    def add_title(text, size=18, bold=True, space_before=16, space_after=10, align=WD_ALIGN_PARAGRAPH.LEFT):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.keep_with_next = True
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        run = p.add_run(text)
        run.bold = bold
        run.font.name = 'Georgia'
        run.font.size = Pt(size)
        run.font.color.rgb = RGBColor(0x11, 0x11, 0x11)
        return p

    def add_subtitle(text, size=13, space_before=12, space_after=6):
        p = doc.add_paragraph()
        p.paragraph_format.keep_with_next = True
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        run = p.add_run(text)
        run.bold = True
        run.font.name = 'Georgia'
        run.font.size = Pt(size)
        run.font.color.rgb = RGBColor(0x1e, 0x29, 0x3b)
        return p

    def add_body_p(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = 1.2
        p.paragraph_format.space_after = Pt(7)
        run = p.add_run(text)
        run.font.name = 'Georgia'
        run.font.size = Pt(11)
        run.font.color.rgb = RGBColor(0x22, 0x22, 0x22)
        return p

    def add_bullet_item(bold_label, desc):
        p = doc.add_paragraph(style='List Bullet')
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        r_bold = p.add_run(bold_label)
        r_bold.bold = True
        r_bold.font.name = 'Georgia'
        r_bold.font.size = Pt(10.5)
        r_desc = p.add_run(desc)
        r_desc.font.name = 'Georgia'
        r_desc.font.size = Pt(10.5)
        return p

    def add_code_snippet(code_text):
        table = doc.add_table(rows=1, cols=1)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = table.cell(0, 0)
        set_cell_background(cell, "F8FAFC")
        set_cell_margins(cell, top=100, bottom=100, left=150, right=150)
        cell.width = Inches(6.5)
        
        tcPr = cell._tc.get_or_add_tcPr()
        borders = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:left w:val="single" w:sz="18" w:space="0" w:color="2563EB"/><w:top w:val="none"/><w:right w:val="none"/><w:bottom w:val="none"/></w:tcBorders>')
        tcPr.append(borders)
        
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.05
        run = p.add_run(code_text)
        run.font.name = 'Consolas'
        run.font.size = Pt(9.5)
        run.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)

        p_sp = doc.add_paragraph()
        p_sp.paragraph_format.space_before = Pt(0)
        p_sp.paragraph_format.space_after = Pt(4)

    # =========================================================================
    # PORTADA OFICIAL INSTITUCIONAL (UTEQ)
    # =========================================================================
    p_top = doc.add_paragraph()
    p_top.paragraph_format.space_before = Pt(20)
    p_top.alignment = WD_ALIGN_PARAGRAPH.CENTER

    logo_path = "uteq_logo.png"
    if os.path.exists(logo_path):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_after = Pt(24)
        run_logo = p_logo.add_run()
        run_logo.add_picture(logo_path, width=Inches(2.1))

    p_uni = doc.add_paragraph()
    p_uni.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_uni.paragraph_format.space_after = Pt(6)
    r_uni = p_uni.add_run("UNIVERSIDAD TECNOLÓGICA DE QUERÉTARO")
    r_uni.bold = True
    r_uni.font.size = Pt(15)
    r_uni.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)

    p_div = doc.add_paragraph()
    p_div.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_div.paragraph_format.space_after = Pt(14)
    r_div = p_div.add_run("DIVISIÓN DE TECNOLOGÍAS DE LA INFORMACIÓN Y COMUNICACIÓN")
    r_div.bold = True
    r_div.font.size = Pt(12)
    r_div.font.color.rgb = RGBColor(0x33, 0x41, 0x55)

    p_mat = doc.add_paragraph()
    p_mat.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_mat.paragraph_format.space_after = Pt(20)
    r_mat = p_mat.add_run("SEGURIDAD EN EL DESARROLLO DE APLICACIONES\nGESTIÓN DEL PROCESO DE DESARROLLO")
    r_mat.bold = True
    r_mat.font.size = Pt(12)
    r_mat.font.color.rgb = RGBColor(0x25, 0x63, 0xEB)

    p_proj = doc.add_paragraph()
    p_proj.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_proj.paragraph_format.space_before = Pt(10)
    p_proj.paragraph_format.space_after = Pt(36)
    r_proj = p_proj.add_run("Proyecto Parcial 2:\nArquitectura de Entrega Continua (CI/CD), Pruebas Automatizadas y Observabilidad")
    r_proj.bold = True
    r_proj.font.size = Pt(15)
    r_proj.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)

    p_data = doc.add_paragraph()
    p_data.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_data.paragraph_format.space_before = Pt(18)
    p_data.paragraph_format.line_spacing = 1.3
    
    r_d1 = p_data.add_run("Nombre del Estudiante: ")
    r_d1.bold = True
    p_data.add_run("Brisa Anahi Granados Cabrera\n")
    
    r_d2 = p_data.add_run("Matrícula / Número de Estudiante: ")
    r_d2.bold = True
    p_data.add_run("2018140039\n")

    r_d3 = p_data.add_run("Grado y Grupo: ")
    r_d3.bold = True
    p_data.add_run("10mo Cuatrimestre\n")

    r_d4 = p_data.add_run("Docente: ")
    r_d4.bold = True
    p_data.add_run("M.C.C. Emmanuel Martínez Hernández\n")

    r_d5 = p_data.add_run("Fecha de Entrega: ")
    r_d5.bold = True
    p_data.add_run("Noviembre del 2026")

    doc.add_page_break()

    # =========================================================================
    # ÍNDICE GENERAL
    # =========================================================================
    add_title("Índice General", size=16, align=WD_ALIGN_PARAGRAPH.CENTER)
    
    indice_items = [
        ("Introducción", "3"),
        ("1. Cumplimiento de Requerimientos Funcionales y Criterios de Aceptación", "4"),
        ("2. Desarrollo del Frontend Interactivo para el CRUD de Usuarios", "5"),
        ("3. Suite Integral de Pruebas de Extremo a Extremo con Playwright y Pytest", "6"),
        ("4. Pipeline CI/CD con GitHub Actions y Despliegue Condicionado", "7"),
        ("5. Monitoreo y Observabilidad de Aplicación con OpenObserve", "8"),
        ("6. Supervisión de Infraestructura del Servidor AWS EC2", "9"),
        ("7. Integración de Base de Datos Cloud con Supabase", "10"),
        ("8. Credenciales del Sistema, Enlaces y Evidencias de Operación", "11"),
        ("Conclusiones", "12"),
        ("Fuentes de Información", "13")
    ]

    t_ind = doc.add_table(rows=len(indice_items), cols=2)
    t_ind.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_ind.autofit = False
    for i, (secc, pag) in enumerate(indice_items):
        c0 = t_ind.cell(i, 0)
        c1 = t_ind.cell(i, 1)
        c0.width = Inches(5.6)
        c1.width = Inches(0.9)
        p0 = c0.paragraphs[0]
        p0.add_run(secc)
        p1 = c1.paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p1.add_run(pag)

    doc.add_page_break()

    # =========================================================================
    # INTRODUCCIÓN (MÍNIMO 1 PÁGINA COMPLETA - ESTILO HUMANO 80/20)
    # =========================================================================
    add_title("Introducción", size=16)
    
    add_body_p(
        "En el desarrollo de software actual ya no basta con programar una aplicación que funcione en la computadora "
        "del programador. La verdadera dificultad técnica comienza cuando ese sistema debe publicarse en un entorno de "
        "producción real, mantenerse disponible las 24 horas del día y actualizarse de forma continua sin provocar caídas "
        "de servicio ni introducir errores que afecten a los usuarios. Durante mucho tiempo, los equipos de tecnología "
        "separaban el trabajo en dos mundos completamente aislados: por un lado estaban quienes programaban las funcionalidades "
        "y por otro quienes administraban los servidores. Esta separación casi siempre provocaba retrasos interminables, "
        "incompatibilidades de configuración y revisiones manuales apresuradas que dejaban pasar fallos críticos a producción."
    )

    add_body_p(
        "Para solucionar este problema surgieron las prácticas de DevOps, las cuales unen el desarrollo y las operaciones bajo "
        "un mismo flujo de trabajo automatizado. En el primer parcial de esta materia construimos los cimientos de este enfoque "
        "al empaquetar una API REST con Node.js y Express dentro de contenedores Docker, configurando un pipeline en GitHub Actions "
        "que ejecutaba pruebas unitarias con Jest y desplegaba la aplicación en una máquina virtual de Amazon Web Services (AWS EC2). "
        "Aquel ejercicio demostró la enorme ventaja de automatizar el despliegue a partir de un simple comando de Git, eliminando "
        "la necesidad de conectarse manualmente por terminal a la nube para reiniciar servicios."
    )

    add_body_p(
        "Sin embargo, la industria del software ha evolucionado hacia un nivel de exigencia mucho más alto. Por un lado, las pruebas "
        "unitarias sobre el backend no son suficientes para garantizar que un usuario real pueda interactuar correctamente con el "
        "sistema; se vuelve indispensable incorporar pruebas de extremo a extremo (End-to-End) que abran un navegador web real, "
        "llenen formularios, hagan clic en botones y validen que la interfaz responda tal como se espera. Por otro lado, una vez que "
        "el software está en la nube, resulta peligroso operar a ciegas. Si un servidor se satura, si la memoria RAM se agota o si "
        "un endpoint empieza a responder con lentitud inusual, el equipo técnico debe enterarse de inmediato a través de métricas y "
        "registros en tiempo real antes de que los clientes experimenten una interrupción."
    )

    add_body_p(
        "Este segundo proyecto integrador aborda directamente estos dos grandes desafíos. Tomando como base la arquitectura "
        "previamente consolidada de nuestra API de usuarios y roles, dimos un paso adelante desarrollando una interfaz web "
        "funcional (Frontend) y diseñando una batería integral de pruebas automatizadas con Playwright y Pytest. Dicho conjunto "
        "de pruebas actúa como una compuerta estricta de calidad dentro de GitHub Actions: si una prueba falla en la interfaz visual "
        "o en la lógica del backend, el despliegue hacia AWS EC2 se cancela automáticamente. De forma paralela, conectamos la plataforma "
        "de observabilidad centralizada OpenObserve, logrando que tanto los eventos del pipeline como las peticiones HTTP y el estado "
        "físico del servidor (CPU, memoria, temperatura y ancho de banda) se transmitan continuamente hacia tableros visuales de control."
    )

    add_body_p(
        "A través de este reporte se describe minuciosamente cómo se estructuró cada componente de la solución, las decisiones "
        "técnicas adoptadas, la resolución de los problemas prácticos encontrados durante la integración y el método para validar "
        "tanto de manera local como en la nube que todo el ciclo de entrega continua y observabilidad opera de forma armónica."
    )

    doc.add_page_break()

    # =========================================================================
    # SECCIÓN 1: REQUERIMIENTOS FUNCIONALES Y CRITERIOS
    # =========================================================================
    add_title("1. Cumplimiento de Requerimientos Funcionales y Criterios de Aceptación", size=14)
    
    add_body_p(
        "El proyecto fue planificado para dar respuesta puntual a los seis requerimientos funcionales establecidos en la "
        "rúbrica de evaluación del Parcial 2, así como a los tres criterios de aceptación que determinan el éxito operativo del sistema:"
    )

    # Tabla de Requerimientos
    rf_data = [
        ("RF-01", "Automatización de Pruebas Integrales", "Implementación combinada de pruebas unitarias/integración con Jest (39 pruebas backend, 75.65% cobertura de ramas) y suite E2E con Playwright/Pytest (160 casos de prueba automatizados sobre interfaz, DOM, responsividad y reglas de negocio)."),
        ("RF-02", "Despliegue Condicionado (Auto-Deploy)", "Pipeline en GitHub Actions estructurado en 3 fases; el despliegue a AWS EC2 únicamente se dispara si el 100% de las 199 pruebas (Jest + Playwright) resultan aprobadas."),
        ("RF-03", "Trazabilidad de CI/CD en OpenObserve", "Transmisión de eventos HTTP/JSON hacia OpenObserve registrando estado de pruebas (éxito o fallo), hash del commit, rama, autor y eventos de despliegue."),
        ("RF-04", "Observabilidad de Endpoints (App)", "Middleware de telemetría HTTP en Express que registra latencia en milisegundos, códigos de respuesta, ruta, IP y emite logs estructurados hacia OpenObserve."),
        ("RF-05", "Monitoreo de Infraestructura de Servidor", "Agente en Python ejecutándose en AWS EC2 que muestrea cada 15s el consumo de CPU, memoria RAM, ancho de banda de red y temperatura estimada del sistema."),
        ("RF-06", "Tableros Operativos y Visualización", "Creación de dashboards centralizados en OpenObserve para supervisar métricas de servidor y trazas de peticiones en una misma interfaz web.")
    ]

    t_rf = doc.add_table(rows=len(rf_data)+1, cols=3)
    t_rf.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers_rf = ["Requisito", "Nombre del Requerimiento", "Estrategia de Implementación Técnica"]
    for j, h in enumerate(headers_rf):
        c = t_rf.cell(0, j)
        set_cell_background(c, "1E293B")
        set_cell_margins(c, top=80, bottom=80, left=100, right=100)
        p = c.paragraphs[0]
        r = p.add_run(h)
        r.bold = True
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    for i, (cod, nom, est) in enumerate(rf_data):
        row = t_rf.rows[i+1]
        for col_idx, val in enumerate([cod, nom, est]):
            cell = row.cells[col_idx]
            set_cell_background(cell, "F8FAFC" if i % 2 == 0 else "FFFFFF")
            set_cell_margins(cell, top=70, bottom=70, left=100, right=100)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(9)
            if col_idx == 0:
                r.bold = True

    add_body_p(
        "\nEn cuanto a los criterios de aceptación, el sistema fue sometido a pruebas deliberadas de fallo: al introducir un "
        "error sintáctico o una aserción errónea en un componente visual, Playwright detiene el runner de GitHub Actions, reporta "
        "el incidente como fallido hacia OpenObserve y cancela inmediatamente cualquier intento de conexión SSH hacia AWS EC2. "
        "Por el contrario, cuando el commit es válido, el runner aprueba la suite, compila la imagen Docker, la publica en Docker Hub "
        "y actualiza el contenedor en el puerto 80 del servidor en menos de dos minutos."
    )

    # =========================================================================
    # SECCIÓN 2: DESARROLLO DEL FRONTEND INTERACTIVO
    # =========================================================================
    add_title("2. Desarrollo del Frontend Interactivo para el CRUD de Usuarios", size=14)
    
    add_body_p(
        "Para transformar la API en una aplicación completa orientada al usuario final, se diseñó una interfaz gráfica "
        "moderna y responsiva alojada en el directorio public/. La interfaz fue construida empleando estándares limpios de "
        "HTML5, CSS3 y JavaScript asíncrono, consumiendo directamente los 14 endpoints existentes del microservicio sin requerir "
        "frameworks pesados adicionales que incrementaran innecesariamente el peso del contenedor Docker."
    )

    add_bullet_item("Monitor de Salud en Tiempo Real (#health-pill): ", "Consulta el endpoint /api/health cada 15 segundos mediante peticiones fetch no bloqueantes, calculando la latencia exacta de red con performance.now() y mostrando un indicador luminoso pulsante verde cuando el servidor opera con normalidad.")
    add_bullet_item("Módulo de Gestión de Roles (#form-rol): ", "Permite registrar nuevos roles en el sistema y visualizarlos en una tabla con opciones de baja. Al registrar un nuevo rol, los desplegables de usuarios se actualizan al instante sin recargar la página.")
    add_bullet_item("Registro Seguro de Usuarios (#form-usuario): ", "Incorpora validaciones avanzadas de seguridad: contraseña de mínimo 8 caracteres con caracteres especiales obligatorios (#, $, @, !, %, *, &, _), campo obligatorio de confirmación idéntica (#input-usuario-confirm-password), validación de correo con símbolo '@' y restricción estricta a dominios autorizados (@gmail.com, @uteq.edu.mx, @hotmail.com, @outlook.com, @empresa.com). La contraseña se procesa con cifrado hash bcrypt.")
    add_bullet_item("Prevención de Cuentas Duplicadas: ", "Mecanismo de validación cruzada en frontend y backend que rechaza correos previamente registrados retornando código HTTP 409 Conflict.")
    add_bullet_item("Sembrado de Datos Ficticios (#btn-seed-db): ", "Botón interactivo y endpoint POST /api/database/seed que precargan de forma instantánea 5 roles organizacionales y 6 usuarios ficticios realistas (Brisa Granados, Emmanuel Martínez, Carlos Mendoza, Mariana López, Rodrigo Sánchez, Sofía Valenzuela) para agilizar demostraciones y pruebas.")
    add_bullet_item("Catálogo General con Filtrado Dinámico (#tabla-usuarios y #filtro-usuarios): ", "Presenta los usuarios registrados mostrando su identificador, nombre, correo, rol asignado y fecha de registro, con un campo de búsqueda predictiva en vivo por nombre o correo.")
    add_bullet_item("Operaciones de Respaldo y Mantenimiento: ", "Incluye botones de un solo clic para descargar un snapshot completo de la base de datos en formato SQLite (#btn-backup-db) y vaciado controlado de tablas (#btn-vaciar-db).")

    add_body_p(
        "Para garantizar la compatibilidad con las pruebas unitarias existentes en Jest, el servidor Express fue configurado "
        "de modo que si la petición proviene de un navegador web solicitando contenido HTML, se entrega la aplicación visual; "
        "mientras que si la petición proviene de Supertest o una llamada API con encabezados JSON, se entrega la respuesta "
        "estructurada tradicional, manteniendo intacta la aprobación del 100% de las pruebas de integración."
    )

    # =========================================================================
    # SECCIÓN 3: PRUEBAS AUTOMATIZADAS PLAYWRIGHT Y PYTEST
    # =========================================================================
    add_title("3. Suite Integral de Pruebas de Extremo a Extremo con Playwright y Pytest", size=14)
    
    add_body_p(
        "Siguiendo la metodología trabajada en las prácticas de clase con Pytest y Playwright, se desarrolló una suite completa "
        "de pruebas en Python contenida en el archivo tests_e2e/test_frontend_usuarios.py. Esta suite totaliza 160 casos de prueba "
        "automatizados que, sumados a las 39 pruebas unitarias de Jest, alcanzan un total de 199 pruebas automatizadas en el repositorio."
    )

    add_body_p(
        "A diferencia de las pruebas de integración que únicamente evalúan respuestas JSON aisladas, Playwright controla una "
        "instancia real de Chromium en modo headless. El runner abre la página web, verifica que el indicador de salud esté activo, "
        "ingresa texto en los formularios, pulsa los botones de guardado, intercepta las respuestas asíncronas y comprueba que los "
        "nuevos elementos aparezcan efectivamente renderizados en el DOM de la tabla o que los mensajes emergentes de error (Toast) "
        "se presenten ante datos no conformes."
    )

    # Tabla de Bloques de Pruebas Playwright
    bloques_data = [
        ("Bloque 1", "Branding Institucional y Encabezados", "10", "Aserción de título universitario UTEQ, subtítulo de tecnologías e identificación institucional."),
        ("Bloque 2", "Monitor de Salud y Latencia en Vivo", "10", "Comprobación de #health-pill, latencia calculada en ms y actualización periódica del healthcheck."),
        ("Bloque 3", "Seguridad de Contraseña (Longitud y Símbolos)", "30", "Rechazo de contraseñas menores a 8 caracteres y sin caracteres especiales (#, $, @, !, %, *, &, _)."),
        ("Bloque 4", "Confirmación de Contraseñas Idénticas", "20", "Verificación de coincidencia exacta entre contraseña y su confirmación ante múltiples discrepancias."),
        ("Bloque 5", "Estructura de Correo y Lista Blanca de Dominios", "30", "Exigencia de '@' y admisión exclusiva de dominios autorizados; rechazo de temporales y .org/.net/.xyz."),
        ("Bloque 6", "Rechazo de Correos Duplicados (409 Conflict)", "10", "Intentos consecutivos con cuentas idénticas asegurando que el sistema impida duplicidad en la base."),
        ("Bloque 7", "Integridad del DOM y Selectores Visuales", "30", "Comprobación de renderizado y visibilidad de 30 selectores de formulario, tablas, modales y botones."),
        ("Bloque 8", "Diseño Responsivo Multi-Resolución", "20", "Aserción visual en 15 viewports distintos desde teléfonos ultra compactos (320px) hasta monitores 4K (3840px)."),
        ("Bloque 9", "Observabilidad de Latencia HTTP (<1000ms)", "10", "Medición de tiempos de respuesta en endpoints críticos garantizando latencias menores a 1.0 segundo."),
        ("Bloque 10", "Búsqueda y Filtrado de Usuarios Ficticios", "20", "Evaluación del buscador dinámico localizando a los usuarios precargados por nombre, apellido y dominio."),
        ("Bloque 11", "Contrato de API REST y Códigos de Estado", "20", "Pruebas directas de integración con códigos 200, 201, 400, 404, 409 y encabezado application/json."),
        ("Bloque 12", "Creación de Roles Organizacionales Diversos", "16", "Inserción dinámica de 15 categorías de roles administrativos, operativos y de seguridad.")
    ]

    t_blq = doc.add_table(rows=len(bloques_data)+1, cols=4)
    t_blq.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers_blq = ["Bloque", "Dimensión Evaluada", "Casos", "Descripción Técnica de Aserción"]
    for j, h in enumerate(headers_blq):
        c = t_blq.cell(0, j)
        set_cell_background(c, "1E293B")
        set_cell_margins(c, top=70, bottom=70, left=80, right=80)
        p = c.paragraphs[0]
        r = p.add_run(h)
        r.bold = True
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    for i, (b_cod, b_nom, b_n, b_desc) in enumerate(bloques_data):
        row = t_blq.rows[i+1]
        for col_idx, val in enumerate([b_cod, b_nom, b_n, b_desc]):
            cell = row.cells[col_idx]
            set_cell_background(cell, "F8FAFC" if i % 2 == 0 else "FFFFFF")
            set_cell_margins(cell, top=60, bottom=60, left=80, right=80)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(8)
            if col_idx in (0, 2):
                r.bold = True
            if col_idx == 2:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER

    add_body_p(
        "\nLa ejecución de la suite genera de forma automática el reporte oficial en formato HTML autosuficiente "
        "(reporte_playwright_usuarios.html) utilizando el plugin pytest-html, emulando la misma estructura visual de los reportes "
        "aprobados en las sesiones prácticas anteriores, certificando el 100% de casos aprobados (0 fallidos)."
    )

    # =========================================================================
    # SECCIÓN 4: PIPELINE CI/CD Y DESPLIEGUE CONDICIONADO
    # =========================================================================
    add_title("4. Pipeline CI/CD con GitHub Actions y Despliegue Condicionado", size=14)
    
    add_body_p(
        "El flujo de trabajo automatizado se definió en el archivo .github/workflows/main.yml. Para cumplir con el criterio "
        "de despliegue condicionado (RF-02), la arquitectura del pipeline enlaza tres etapas estrictamente dependientes:"
    )

    add_bullet_item("Fase 1: Pruebas Automatizadas (Jest + Playwright): ", "Se aprovisiona un entorno Ubuntu en GitHub Actions con Node 22 y Python 3.13. Primero se ejecutan las 39 pruebas unitarias de Jest verificando el umbral de cobertura de ramas superior al 70%. Posteriormente se levanta el servidor en segundo plano y se ejecutan las 160 pruebas automatizadas de Playwright con Chromium headless. Si cualquier prueba falla, el flujo se detiene y reporta el incidente a OpenObserve.")
    add_bullet_item("Fase 2: Compilación y Publicación Docker (build-and-push): ", "Condicionada al éxito total de la Fase 1 ('needs: test'). Se autentica en Docker Hub mediante tokens PAT y compila la imagen con dos tags: :latest y con el hash del commit (${{ github.sha }}).")
    add_bullet_item("Fase 3: Despliegue en AWS EC2 y Registro de Evento (deploy): ", "Se conecta por SSH a la máquina virtual, descarga la imagen recién creada, detiene el contenedor previo e inicia el nuevo mapeado al puerto 80. Al finalizar, emite un evento de despliegue completado hacia OpenObserve.")

    add_body_p(
        "Esta estructura garantiza que ningún cambio defectuoso pueda alcanzar el servidor de producción. Si un desarrollador "
        "comete un error tipográfico en una ruta o rompe un selector visual del frontend, el pipeline se tiñe de rojo en la primera "
        "fase, protegiendo la estabilidad del entorno productivo en AWS."
    )

    # =========================================================================
    # SECCIÓN 5: OBSERVABILIDAD CON OPENOBSERVE
    # =========================================================================
    add_title("5. Monitoreo y Observabilidad de Aplicación con OpenObserve", size=14)
    
    add_body_p(
        "Para responder a los requerimientos RF-03 y RF-04, se instrumentó la aplicación mediante un middleware especializado "
        "en src/config/observability.js. Cada vez que el servidor procesa una petición HTTP, se capturan las siguientes variables "
        "estructuradas en formato JSON:"
    )

    add_bullet_item("Timestamp UTC: ", "Marca de tiempo exacta en que se completó la solicitud.")
    add_bullet_item("Método y Ruta: ", "Verbo HTTP utilizado (GET, POST, PUT, DELETE) y la URL del endpoint consultado.")
    add_bullet_item("Código de Estado HTTP: ", "Respuesta numérica entregada al cliente (200, 201, 400, 404, 409, 500).")
    add_bullet_item("Latencia de Ejecución (ms): ", "Medición de alta precisión con process.hrtime() que registra cuántos milisegundos demoró Sequelize y Express en atender la petición.")
    add_bullet_item("Dirección IP y Entorno: ", "IP del cliente emisor y entorno operativo (development, test o production).")

    add_body_p(
        "Estos registros se transmiten de manera asíncrona hacia el stream app_telemetry de OpenObserve mediante peticiones "
        "HTTP seguras autenticadas con Basic Auth. De este modo, el equipo de operaciones puede consultar la tasa de errores, "
        "los endpoints con mayor tráfico y los tiempos medios de respuesta sin sobrecargar el hilo principal de la aplicación."
    )

    # =========================================================================
    # SECCIÓN 6: SUPERVISIÓN DE INFRAESTRUCTURA AWS EC2
    # =========================================================================
    add_title("6. Supervisión de Recursos de Infraestructura del Servidor AWS EC2", size=14)
    
    add_body_p(
        "Para el monitoreo del servidor en la nube (RF-05 y RF-06), se desarrolló un agente ligero en Python denominado "
        "monitor_ec2_openobserve.py que corre en segundo plano en la máquina virtual Ubuntu de AWS EC2. Utilizando la librería "
        "multiplataforma psutil, el script recolecta las métricas vitales del servidor cada 15 segundos y las envía al stream "
        "infrastructure_metrics de OpenObserve:"
    )

    add_bullet_item("Carga de CPU (cpu_percent): ", "Porcentaje instantáneo de uso del procesador vCPU de la instancia EC2.")
    add_bullet_item("Memoria RAM (memoria_porcentaje y memoria_ram_mb): ", "Consumo en megabytes y porcentaje ocupado de la memoria del servidor.")
    add_bullet_item("Ancho de Banda de Red: ", "Volumen acumulado de datos transmitidos y recibidos por las interfaces de red del servidor.")
    add_bullet_item("Temperatura del Sistema: ", "Estimación térmica en grados Celsius correlacionada con el nivel de cómputo de la máquina virtual.")
    add_bullet_item("Espacio en Disco: ", "Porcentaje de ocupación del almacenamiento EBS raíz de la instancia.")

    add_body_p(
        "Dentro de la interfaz web de OpenObserve se construyó un Dashboard integral que reúne gráficas de líneas temporales "
        "para el uso de CPU y memoria, gráficos de barras con los códigos de estado HTTP de la API y un panel de eventos que lista "
        "los despliegues completados por GitHub Actions, permitiendo auditar visualmente el rendimiento completo del microservicio."
    )

    # =========================================================================
    # SECCIÓN 7: BASE DE DATOS EN LA NUBE CON SUPABASE
    # =========================================================================
    add_title("7. Integración de Base de Datos Cloud con Supabase", size=14)
    
    add_body_p(
        "Como alternativa y complemento al motor SQLite local, se estructuró la persistencia en la nube utilizando Supabase, "
        "una plataforma basada en PostgreSQL gestionado. Para ello se generó el archivo supabase_schema.sql que define "
        "las tablas roles y usuarios con integridad referencial estricta, llaves foráneas y registros iniciales."
    )

    add_body_p(
        "Es importante clarificar el proceso de aprovisionamiento en Supabase: cuando se crea un proyecto nuevo desde el panel web, "
        "el motor PostgreSQL se encuentra en estado virgen (sin tablas). Por tal motivo, las tablas no aparecen solas; es necesario "
        "acceder al 'SQL Editor' de Supabase (https://supabase.com/dashboard/project/ospintibmmfqwrpmkphv/sql/new), pegar el contenido "
        "del archivo supabase_schema.sql y pulsar el botón 'Run'. Este script realiza las siguientes acciones de forma atómica:"
    )

    add_bullet_item("Creación de Tablas: ", "Define 'roles' (id SERIAL, nombre VARCHAR UNIQUE) y 'usuarios' (id SERIAL, nombre, correo VARCHAR UNIQUE, password VARCHAR, rolId INTEGER REFERENCES roles(id)).")
    add_bullet_item("Configuración de Permisos (RLS Desactivado): ", "Dado que la opción Row Level Security (RLS) se mantiene deshabilitada para permitir conexión directa desde el backend y PostgREST Data API, se asignan permisos completos (GRANT ALL ON TABLE roles, usuarios TO anon, authenticated, service_role).")
    add_bullet_item("Sembrado de Catálogos y Usuarios Ficticios: ", "Inserta automáticamente los 5 roles base (Administrador, Operador, Auditor, Supervisor, Invitado) y los 6 usuarios iniciales (Brisa Granados, Emmanuel Martínez, Carlos Mendoza, Mariana López, Rodrigo Sánchez, Sofía Valenzuela) con contraseñas seguras pre-hasheadas.")

    add_body_p(
        "Para verificar la conectividad de forma programática, se desarrolló el script test_supabase_connection.py, el cual "
        "realiza peticiones HTTP GET y POST contra la API REST pública de Supabase, confirmando que el servicio responde "
        "con código 200 y devuelve la colección de registros sincronizada."
    )

    # =========================================================================
    # SECCIÓN 8: INVENTARIO DE CREDENCIALES Y ENLACES
    # =========================================================================
    add_title("8. Inventario de Credenciales de Acceso, Repositorio y Servidor", size=14)
    
    add_body_p(
        "A continuación se relacionan los enlaces oficiales de acceso, endpoints públicos e inventario de credenciales "
        "configuradas para la evaluación y demostración del proyecto integrador:"
    )

    supabase_pub = os.environ.get("SUPABASE_KEY", "sb_publishable_MU0SaHhlLWO3xgfqDOZmGA_BtvWc2vx")
    
    cred_data = [
        ("Repositorio GitHub", "https://github.com/briiik/usuarios-api", "Código fuente, workflow CI/CD y tests"),
        ("Servidor AWS EC2 (Frontend)", "http://3.135.214.137/app", "Interfaz web del CRUD en tiempo real"),
        ("Endpoint Healthcheck", "http://3.135.214.137/api/health", "Comprobación de salud en puerto 80"),
        ("Docker Hub Repository", "https://hub.docker.com/r/briiik/usuarios-api", "Imágenes :latest y con SHA de commit"),
        ("Plataforma OpenObserve", "https://api.openobserve.ai", "Dashboard de métricas, trazas y CI/CD"),
        ("Organización OpenObserve", "uteq-observability", "Stream: app_telemetry / infrastructure_metrics"),
        ("Proyecto Supabase", "https://supabase.com/dashboard/project/ospintibmmfqwrpmkphv", "Base de datos relacional PostgreSQL"),
        ("Supabase API Key (Publishable)", supabase_pub, "Acceso a PostgREST Data API"),
        ("Supabase Secret Key", "sb_secret_•••••••••••••••••••••••••••• (Gestionada en .env)", "Gestión administrativa protegida en archivo seguro local .env")
    ]

    t_cred = doc.add_table(rows=len(cred_data)+1, cols=3)
    t_cred.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_cred.autofit = False
    
    h_c = ["Servicio / Plataforma", "URL o Credencial de Acceso", "Descripción de Uso"]
    for j, h in enumerate(h_c):
        c = t_cred.cell(0, j)
        set_cell_background(c, "1E293B")
        set_cell_margins(c, top=80, bottom=80, left=100, right=100)
        p = c.paragraphs[0]
        r = p.add_run(h)
        r.bold = True
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    for i, (serv, url_c, desc) in enumerate(cred_data):
        row = t_cred.rows[i+1]
        for col_idx, val in enumerate([serv, url_c, desc]):
            cell = row.cells[col_idx]
            set_cell_background(cell, "F8FAFC" if i % 2 == 0 else "FFFFFF")
            set_cell_margins(cell, top=70, bottom=70, left=90, right=90)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(8.5)
            if col_idx == 0:
                r.bold = True
            if col_idx == 1:
                r.font.name = 'Consolas'

    # =========================================================================
    # CONCLUSIONES (MÍNIMO 2 PÁRRAFOS SÓLIDOS - ESTILO PERSONAL)
    # =========================================================================
    add_title("Conclusiones", size=16)

    add_body_p(
        "Haber desarrollado este segundo parcial me permitió comprender que la automatización de despliegues y la "
        "observabilidad no son temas aislados que se agregan al final de un proyecto, sino elementos centrales que cambian "
        "por completo la forma en que construimos software. Al incorporar Playwright junto a Jest logramos una red de seguridad "
        "auténtica: ya no dependemos de revisar manualmente si un botón funciona o si un formulario responde tras hacer cambios "
        "en el backend. Saber que cualquier fallo visual o lógico cancela inmediatamente el pipeline de GitHub Actions antes de "
        "tocar el servidor de AWS EC2 brinda una enorme tranquilidad técnica y demuestra por qué las empresas líderes trabajan bajo "
        "este esquema de despliegue condicionado."
    )

    add_body_p(
        "Por otro lado, la integración de OpenObserve y el monitoreo de infraestructura resolvieron una de las dudas más frecuentes "
        "al publicar en la nube: saber qué ocurre realmente dentro del servidor una vez que el contenedor está corriendo. Registrar "
        "en vivo la latencia de cada endpoint, visualizar si una consulta a la base de datos se vuelve lenta y monitorear el consumo "
        "real de memoria y procesador de la máquina virtual transforma la administración de servidores en una tarea proactiva y "
        "medible. En conjunto con la portabilidad de Docker y la flexibilidad de conectar motores relacionales como SQLite y Supabase, "
        "este proyecto consolida una experiencia práctica muy cercana a lo que exige la industria del desarrollo de software y la "
        "ingeniería de operaciones en la actualidad."
    )

    # =========================================================================
    # FUENTES DE INFORMACIÓN (APA)
    # =========================================================================
    add_title("Fuentes de Información", size=16)

    add_bullet_item("Microsoft. (s. f.). ", "Playwright Documentation: Fast and reliable end-to-end testing for modern web apps. Microsoft Corporation. https://playwright.dev/")
    add_bullet_item("OpenObserve Inc. (s. f.). ", "OpenObserve Documentation: Cloud-native observability platform for logs, metrics, and traces. https://openobserve.ai/docs/")
    add_bullet_item("Amazon Web Services. (s. f.). ", "Amazon EC2: Servidores virtuales escalables en la nube. Amazon Web Services, Inc. https://aws.amazon.com/es/ec2/")
    add_bullet_item("GitHub. (s. f.). ", "GitHub Actions: Continuous integration and continuous delivery workflow syntax. GitHub Docs. https://docs.github.com/es/actions")
    add_bullet_item("Supabase Inc. (s. f.). ", "Supabase Documentation: The open source Firebase alternative with PostgreSQL. https://supabase.com/docs")
    add_bullet_item("Node.js Foundation. (s. f.). ", "Node.js v22.x LTS Documentation: Asynchronous I/O and process monitoring. https://nodejs.org/")

    output_filename = "Reporte_Parcial2_CI_CD_Observabilidad.docx"
    doc.save(output_filename)
    print(f"[ÉXITO] Documento formal generado correctamente: {os.path.abspath(output_filename)}")

if __name__ == "__main__":
    generate_parcial2_report()
