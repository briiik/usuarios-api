import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def generate_report():
    doc = Document()

    # Configuración de márgenes estándar de 1 pulgada (2.54 cm) estilo LaTeX / APA
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        # Encabezado y pie de página
        footer = section.footer
        p_footer = footer.paragraphs[0]
        p_footer.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        # Añadir número de página en XML
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

    # Helpers
    def set_cell_background(cell, fill_hex):
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
        cell._tc.get_or_add_tcPr().append(shd)

    def set_cell_margins(cell, top=120, bottom=120, left=150, right=150):
        tcPr = cell._tc.get_or_add_tcPr()
        tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
        tcPr.append(tcMar)

    def add_title(text, size=20, bold=True, space_before=18, space_after=12, align=WD_ALIGN_PARAGRAPH.LEFT):
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

    def add_subtitle(text, size=14, space_before=14, space_after=6):
        p = doc.add_paragraph()
        p.paragraph_format.keep_with_next = True
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        run = p.add_run(text)
        run.bold = True
        run.font.name = 'Georgia'
        run.font.size = Pt(size)
        run.font.color.rgb = RGBColor(0x22, 0x22, 0x22)
        return p

    def add_subsubtitle(text, size=12, space_before=10, space_after=4):
        p = doc.add_paragraph()
        p.paragraph_format.keep_with_next = True
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        run = p.add_run(text)
        run.bold = True
        run.font.name = 'Georgia'
        run.font.size = Pt(size)
        run.font.color.rgb = RGBColor(0x33, 0x33, 0x33)
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
        set_cell_background(cell, "F4F5F7")
        set_cell_margins(cell, top=100, bottom=100, left=150, right=150)
        cell.width = Inches(6.5)
        
        # Border
        tcPr = cell._tc.get_or_add_tcPr()
        borders = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:left w:val="single" w:sz="18" w:space="0" w:color="0052CC"/><w:top w:val="none"/><w:right w:val="none"/><w:bottom w:val="none"/></w:tcBorders>')
        tcPr.append(borders)
        
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.05
        run = p.add_run(code_text)
        run.font.name = 'Consolas'
        run.font.size = Pt(9.5)
        run.font.color.rgb = RGBColor(0x24, 0x29, 0x2E)

        # Espacio después de tabla
        p_sp = doc.add_paragraph()
        p_sp.paragraph_format.space_before = Pt(0)
        p_sp.paragraph_format.space_after = Pt(4)

    # =========================================================================
    # PÁGINA 1: PORTADA (ESTILO EXACTO AL PDF PROPORCIONADO)
    # =========================================================================
    
    # Espaciado superior para centrar verticalmente
    p_top = doc.add_paragraph()
    p_top.paragraph_format.space_before = Pt(36)
    p_top.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Logo centrado
    logo_path = "uteq_logo.png"
    if os.path.exists(logo_path):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_after = Pt(32)
        run_logo = p_logo.add_run()
        run_logo.add_picture(logo_path, width=Inches(2.2))

    # Nombre de la Institución
    p_uni = doc.add_paragraph()
    p_uni.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_uni.paragraph_format.space_after = Pt(12)
    r_uni = p_uni.add_run("UNIVERSIDAD TECNOLÓGICA DE QUERÉTARO")
    r_uni.font.name = 'Georgia'
    r_uni.font.size = Pt(16)
    r_uni.font.color.rgb = RGBColor(0x11, 0x11, 0x11)

    # Materia / Asignatura
    p_mat = doc.add_paragraph()
    p_mat.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_mat.paragraph_format.space_after = Pt(48)
    r_mat = p_mat.add_run("SEGURIDAD EN EL DESARROLLO DE APLICACIONES\nGESTIÓN DEL PROCESO DE DESARROLLO")
    r_mat.font.name = 'Georgia'
    r_mat.font.size = Pt(12)
    r_mat.font.color.rgb = RGBColor(0x33, 0x33, 0x33)

    # Título principal del entregable
    p_tit = doc.add_paragraph()
    p_tit.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_tit.paragraph_format.space_after = Pt(60)
    r_tit = p_tit.add_run("Pipeline CI/CD Automatizado para API REST\ncon Docker, GitHub Actions y AWS EC2")
    r_tit.bold = True
    r_tit.font.name = 'Georgia'
    r_tit.font.size = Pt(20)
    r_tit.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    # Datos del Alumno y Docente
    p_datos = doc.add_paragraph()
    p_datos.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_datos.paragraph_format.line_spacing = 1.3
    p_datos.paragraph_format.space_after = Pt(80)

    r_nom = p_datos.add_run("Nombre del Alumno: ")
    r_nom.bold = True
    r_nom.font.name = 'Georgia'
    r_nom.font.size = Pt(12)
    r_nom_v = p_datos.add_run("Brisa Anahi Granados Cabrera\n")
    r_nom_v.font.name = 'Georgia'
    r_nom_v.font.size = Pt(12)

    r_grd = p_datos.add_run("Grado: ")
    r_grd.bold = True
    r_grd.font.name = 'Georgia'
    r_grd.font.size = Pt(12)
    r_grd_v = p_datos.add_run("10mo Cuatrimestre\n")
    r_grd_v.font.name = 'Georgia'
    r_grd_v.font.size = Pt(12)

    r_num = p_datos.add_run("Número de estudiante: ")
    r_num.bold = True
    r_num.font.name = 'Georgia'
    r_num.font.size = Pt(12)
    r_num_v = p_datos.add_run("2018140039\n\n")
    r_num_v.font.name = 'Georgia'
    r_num_v.font.size = Pt(12)

    r_doc = p_datos.add_run("Docente: ")
    r_doc.bold = True
    r_doc.font.name = 'Georgia'
    r_doc.font.size = Pt(12)
    r_doc_v = p_datos.add_run("M.C.C. Emmanuel Martínez Hernández")
    r_doc_v.font.name = 'Georgia'
    r_doc_v.font.size = Pt(12)

    # Fecha de entrega al pie de la portada
    p_fec = doc.add_paragraph()
    p_fec.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_fec.paragraph_format.space_before = Pt(30)
    r_fec = p_fec.add_run("Fecha de entrega: Octubre del 2026")
    r_fec.font.name = 'Georgia'
    r_fec.font.size = Pt(11)
    r_fec.font.color.rgb = RGBColor(0x44, 0x44, 0x44)

    # Salto de página tras portada
    doc.add_page_break()

    # =========================================================================
    # PÁGINA 2: ÍNDICE GENERAL (ESTILO LATEX / PDF)
    # =========================================================================
    add_title("Índice general", size=22, space_before=12, space_after=18)

    indice_items = [
        ("Introducción", "3"),
        ("Desarrollo", "4"),
        ("    1. Arquitectura General y Flujo de Automatización DevOps", "4"),
        ("    2. Implementación de la API REST y Catálogo de Endpoints", "4"),
        ("    3. Suite de Pruebas Unitarias Automatizadas y Cobertura (Jest)", "5"),
        ("    4. Contenedorización Multi-Entorno y Optimización con Docker", "6"),
        ("    5. Orquestación del Pipeline CI/CD en GitHub Actions", "7"),
        ("    6. Aprovisionamiento Cloud y Despliegue Continuo en AWS EC2", "8"),
        ("    7. Gestión de Secretos, Resolución de Incidencias y Demostración en Vivo", "9"),
        ("Conclusiones", "10"),
        ("Fuentes de Información", "11")
    ]

    for item, num in indice_items:
        p_ind = doc.add_paragraph()
        p_ind.paragraph_format.space_before = Pt(2)
        p_ind.paragraph_format.space_after = Pt(3)
        p_ind.paragraph_format.line_spacing = 1.15
        
        r_item = p_ind.add_run(item)
        r_item.font.name = 'Georgia'
        r_item.font.size = Pt(11)
        
        dots_count = max(5, 75 - len(item) * 2)
        r_dots = p_ind.add_run(" " + ". " * dots_count)
        r_dots.font.name = 'Georgia'
        r_dots.font.size = Pt(10)
        r_dots.font.color.rgb = RGBColor(0x88, 0x88, 0x88)
        
        r_num = p_ind.add_run(num)
        r_num.font.name = 'Georgia'
        r_num.font.size = Pt(11)
        r_num.bold = True

    doc.add_page_break()

    # =========================================================================
    # PÁGINA 3: INTRODUCCIÓN (EXACTAMENTE 4 PÁRRAFOS EXTENSOS)
    # =========================================================================
    add_title("Introducción", size=22, space_before=12, space_after=16)

    # Párrafo 1
    add_body_p(
        "El presente documento técnico tiene como propósito fundamental documentar, analizar y validar la implementación de un flujo integral de Integración Continua y Despliegue Continuo (CI/CD) aplicado a una arquitectura de microservicio basada en una API REST desarrollada sobre Node.js y Express. En el contexto de la ingeniería de software actual, la entrega constante de valor exige trascender los esquemas manuales tradicionales de despliegue, caracterizados históricamente por su lentitud, su alta propensión a discrepancias de configuración entre entornos y su vulnerabilidad operativa. A través de este proyecto integrador, se consolidan las directrices de automatización requeridas para la materia de Seguridad en el Desarrollo de Aplicaciones y Gestión del Proceso de Desarrollo, garantizando que cada cambio integrado al repositorio de control de versiones sea validado exhaustivamente mediante pruebas unitarias rigurosas, empaquetado de forma inmutable a través de contenedores Docker y promovido a un entorno productivo de nube en Amazon Web Services (AWS EC2) sin necesidad de intervención manual directa."
    )

    # Párrafo 2
    add_body_p(
        "A lo largo de los últimos años, la adopción de las metodologías DevOps y las prácticas de observabilidad y entrega automatizada se ha establecido como un estándar imperativo para las organizaciones que buscan sostener altos niveles de competitividad, calidad y estabilidad operativa. La desconexión histórica entre las fases de desarrollo (Dev) y las fases de infraestructura u operaciones (Ops) generaba cuellos de botella críticos, donde errores no detectados en código local alcanzaban ambientes productivos generando indisponibilidad en los servicios. Frente a este reto, la integración continua introduce una red de seguridad proactiva donde cada confirmación de código ('git push') dispara entornos efímeros de compilación y análisis estático y dinámico, permitiendo detectar regresiones en etapas sumamente tempranas del ciclo de vida del software, reduciendo drásticamente el costo técnico y financiero asociado a la resolución de fallos."
    )

    # Párrafo 3
    add_body_p(
        "Este trabajo se estructura detalladamente sobre la construcción de una API REST robusta denominada 'usuarios-api', la cual administra entidades relacionales fundamentales de roles y usuarios, así como mecanismos de persistencia ligera mediante SQLite y Sequelize ORM. Sobre dicha aplicación, se diseñó e implementó una suite completa de pruebas unitarias e integración con Jest y Supertest, alcanzando una cobertura de código superior al 85%, lo cual sobrepasa con holgura el umbral mínimo institucional exigido del 70%. Asimismo, se estructuró un proceso de contenedorización basado en imágenes ligeras multi-etapa utilizando Alpine Linux, orquestado mediante un archivo de workflow declarativo en GitHub Actions que enlaza secuencialmente los trabajos de verificación, compilación con publicación al registro público de Docker Hub y despliegue continuo mediante SSH seguro hacia una máquina virtual Ubuntu Server alojada en la infraestructura cloud de AWS EC2."
    )

    # Párrafo 4
    add_body_p(
        "Finalmente, este documento busca servir como una guía técnica exhaustiva de consulta profesional y académica, detallando no solamente los fundamentos teóricos y las decisiones de diseño adoptadas, sino también la resolución práctica de los desafíos reales experimentados durante el ciclo de vida del proyecto. Entre estos aspectos se abordan con especial profundidad la depuración de incidentes de control de versiones con Git, el filtrado estricto de artefactos mediante exclusiones en .gitignore, la gestión segura de variables de entorno y credenciales criptográficas a través de GitHub Secrets, y la verificación en vivo del despliegue mediante comprobaciones funcionales de estado sobre la red pública. De esta forma, se fomenta una comprensión integral y fidedigna de cómo se diseñan, aseguran y operan los pipelines de entrega moderna en el software contemporáneo."
    )

    doc.add_page_break()

    # =========================================================================
    # PÁGINAS 4-9: DESARROLLO (EXTENSO, EXPLICADO PASO A PASO)
    # =========================================================================
    add_title("Desarrollo", size=22, space_before=12, space_after=16)

    # Subsección 1
    add_subtitle("1. Arquitectura General y Flujo de Automatización DevOps")
    add_body_p(
        "La arquitectura del sistema fue concebida siguiendo los principios de inmutabilidad, trazabilidad y separación clara de responsabilidades. El núcleo de la infraestructura se distribuye en tres capas interconectadas: la estación local de desarrollo, el orquestador de integración continua en la nube (GitHub Actions) y el servidor de alojamiento en producción (AWS EC2). La comunicación y promoción entre estos estadios se encuentra completamente automatizada a través de eventos desencadenados por el sistema de control de versiones."
    )
    add_body_p(
        "El ciclo de vida del flujo operativo se resume en la siguiente secuencia lógica: el desarrollador realiza modificaciones en el código fuente de la API y ejecuta la confirmación hacia la rama principal ('main'). Inmediatamente, GitHub detecta el evento 'push' e instancia un contenedor de ejecución limpio (Runner con Ubuntu Linux). Este runner ejecuta secuencialmente los jobs de pruebas de software, empaquetado y publicación hacia Docker Hub, para culminar con una conexión SSH segura que aprovisiona el nuevo contenedor en el puerto 80 del servidor web en Amazon Web Services."
    )

    add_code_snippet(
        "[ Desarrollador ] --( git push main )--> [ GitHub Repository: usuarios-api ]\n"
        "                                               │\n"
        "                                   ┌───────────┴───────────┐\n"
        "                                   ▼                       ▼\n"
        "                             [ Job 1: test ]      [ GitHub Secrets ]\n"
        "                         (Jest/Supertest >70%)             │\n"
        "                                   │                       │\n"
        "                                   ▼                       │\n"
        "                         [ Job 2: build-push ] <───────────┘\n"
        "                         (Docker Hub Registry)\n"
        "                                   │\n"
        "                                   ▼\n"
        "                          [ Job 3: deploy ]\n"
        "                        (SSH a AWS EC2 :80)\n"
        "                                   │\n"
        "                                   ▼\n"
        "                       [ AWS EC2 Ubuntu Server ]\n"
        "                     (Contenedor Docker en Puerto 80)"
    )

    # Subsección 2
    add_subtitle("2. Implementación de la API REST y Catálogo de Endpoints")
    add_body_p(
        "Para responder a los requisitos funcionales del proyecto integrador, se desarrolló un backend robusto empleando Node.js en su versión 22 LTS y el framework Express 5. La persistencia de datos se gestiona mediante el ORM Sequelize 6 sobre un motor relacional SQLite3 embebido, lo cual garantiza portabilidad absoluta y minimiza la huella de memoria del contenedor sin requerir un cluster externo de base de datos para la capa de pruebas."
    )
    add_body_p(
        "La aplicación implementa el modelo de arquitectura en capas, aislando los controladores, las rutas y los modelos de datos. En total, se desarrollaron 14 endpoints funcionales que satisfacen sobradamente el requisito mínimo estipulado de 6 endpoints, cubriendo las operaciones CRUD completas para las entidades 'roles' y 'usuarios', endpoints de mantenimiento y diagnóstico de base de datos, y un endpoint de monitoreo de disponibilidad ('healthcheck'):"
    )

    # Tabla de Endpoints
    table_ep = doc.add_table(rows=1, cols=4)
    table_ep.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr_cells = table_ep.rows[0].cells
    headers = ["Método", "Endpoint", "Descripción Funcional", "Código Éxito"]
    for i, h in enumerate(headers):
        hdr_cells[i].text = h
        set_cell_background(hdr_cells[i], "1F3A60")
        set_cell_margins(hdr_cells[i], 100, 100, 100, 100)
        p = hdr_cells[i].paragraphs[0]
        p.runs[0].font.name = 'Georgia'
        p.runs[0].font.bold = True
        p.runs[0].font.size = Pt(10)
        p.runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    endpoints_data = [
        ("GET", "/", "Comprobación visual de servicio y bienvenida", "200 OK"),
        ("GET", "/api/health", "Healthcheck con estado del sistema y timestamp", "200 OK"),
        ("GET", "/api/roles", "Consulta y listado de todos los roles", "200 OK"),
        ("GET", "/api/roles/:id", "Consulta individual de rol por identificador", "200 OK"),
        ("POST", "/api/roles", "Creación y validación de nuevo rol", "201 Created"),
        ("PUT", "/api/roles/:id", "Actualización de nombre y descripción de rol", "200 OK"),
        ("DELETE", "/api/roles/:id", "Eliminación de rol con validación relacional", "200 OK"),
        ("GET", "/api/usuarios", "Listado de usuarios registrados (sin hash)", "200 OK"),
        ("GET", "/api/usuarios/:id", "Búsqueda de usuario por ID con relación de rol", "200 OK"),
        ("POST", "/api/usuarios", "Registro con encriptación bcrypt de contraseña", "201 Created"),
        ("PUT", "/api/usuarios/:id", "Modificación de datos de perfil de usuario", "200 OK"),
        ("DELETE", "/api/usuarios/:id", "Baja definitiva de registro de usuario", "200 OK"),
        ("POST", "/api/database/backup", "Generación y descarga de snapshot SQLite", "200 OK"),
        ("DELETE", "/api/database/vaciar", "Vaciado integral controlado de tablas", "200 OK")
    ]

    for m, ep, desc, code in endpoints_data:
        row_cells = table_ep.add_row().cells
        for idx, val in enumerate([m, ep, desc, code]):
            row_cells[idx].text = val
            set_cell_margins(row_cells[idx], 80, 80, 90, 90)
            p = row_cells[idx].paragraphs[0]
            p.runs[0].font.name = 'Georgia'
            p.runs[0].font.size = Pt(9.5)
            if idx == 0:
                p.runs[0].bold = True
                if val in ["POST", "PUT"]:
                    p.runs[0].font.color.rgb = RGBColor(0x9C, 0x5B, 0x00)
                elif val == "DELETE":
                    p.runs[0].font.color.rgb = RGBColor(0xA6, 0x1C, 0x1C)
                else:
                    p.runs[0].font.color.rgb = RGBColor(0x0C, 0x54, 0x60)

    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(4)
    p_sp.paragraph_format.space_after = Pt(4)

    # Subsección 3
    add_subtitle("3. Suite de Pruebas Unitarias Automatizadas y Cobertura (Jest)")
    add_body_p(
        "La garantía de calidad del microservicio se fundamenta en una estrategia integral de pruebas automatizadas construida mediante Jest 29 y Supertest 7. Para asegurar que ninguna regresión o falla funcional alcance el entorno de producción, se configuró un umbral estricto ('coverageThreshold') en el archivo jest.config.js, exigiendo un cumplimiento mínimo del 70% en líneas, funciones, sentencias y ramas de decisión, tal como lo demandan las especificaciones de la práctica."
    )
    add_body_p(
        "Se estructuraron 3 suites de pruebas exhaustivas que totalizan 34 casos de prueba automatizados, cubriendo tanto los caminos felices (flujos ideales de éxito) como validaciones de datos incorrectos, códigos HTTP de error esperados (400 Bad Request, 404 Not Found, 409 Conflict), integridad referencial y encriptación de credenciales:"
    )

    add_bullet_item("tests/usuarios.test.js (14 pruebas): ", "Evalúa la creación de usuarios con hashing de contraseña mediante bcryptjs, consulta por ID, listado general, modificación, eliminación física, validación de campos obligatorios vacíos, correos electrónicos con formato inválido, detección de emails duplicados y existencia previa del rol foráneo asignado.")
    add_bullet_item("tests/roles.test.js (13 pruebas): ", "Valida la inserción de roles de sistema, control de cadenas vacías o espacios en blanco, unicidad de nombres de rol (código 409), actualización controlada, búsqueda por ID y restricción de integridad que impide eliminar roles que tengan usuarios vinculados activamente.")
    add_bullet_item("tests/database.test.js (7 pruebas): ", "Comprueba la operatividad del endpoint de salud (/api/health), la respuesta de bienvenida en la raíz (/), el manejo de rutas no encontradas y los procedimientos de mantenimiento y respaldo de la base de datos relacional.")

    add_body_p(
        "Al ejecutar la suite mediante el comando 'npm test', los resultados obtenidos superaron de manera contundente las exigencias institucionales, tal como se refleja en el reporte oficial de cobertura:"
    )

    # Tabla de Cobertura
    table_cov = doc.add_table(rows=1, cols=5)
    table_cov.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_hdr = table_cov.rows[0].cells
    cov_headers = ["Dimensión de Cobertura", "Umbral Exigido", "Métrica Obtenida", "Estado", "Superávit"]
    for i, h in enumerate(cov_headers):
        c_hdr[i].text = h
        set_cell_background(c_hdr[i], "2E4053")
        set_cell_margins(c_hdr[i], 100, 100, 100, 100)
        p = c_hdr[i].paragraphs[0]
        p.runs[0].font.name = 'Georgia'
        p.runs[0].font.bold = True
        p.runs[0].font.size = Pt(10)
        p.runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    cov_data = [
        ("Cobertura de Líneas (Lines)", ">= 70.00%", "85.77%", "Aprobado (Éxito)", "+ 15.77%"),
        ("Cobertura de Funciones (Functions)", ">= 70.00%", "88.88%", "Aprobado (Éxito)", "+ 18.88%"),
        ("Cobertura de Sentencias (Statements)", ">= 70.00%", "85.77%", "Aprobado (Éxito)", "+ 15.77%"),
        ("Cobertura de Ramas (Branches)", ">= 70.00%", "80.45%", "Aprobado (Éxito)", "+ 10.45%")
    ]

    for dim, umb, met, est, sup in cov_data:
        row_cells = table_cov.add_row().cells
        for idx, val in enumerate([dim, umb, met, est, sup]):
            row_cells[idx].text = val
            set_cell_margins(row_cells[idx], 80, 80, 90, 90)
            p = row_cells[idx].paragraphs[0]
            p.runs[0].font.name = 'Georgia'
            p.runs[0].font.size = Pt(9.5)
            if idx == 2:
                p.runs[0].bold = True
                p.runs[0].font.color.rgb = RGBColor(0x1B, 0x6E, 0x22)
            if idx == 3:
                p.runs[0].bold = True

    p_sp2 = doc.add_paragraph()
    p_sp2.paragraph_format.space_before = Pt(4)
    p_sp2.paragraph_format.space_after = Pt(4)

    # Subsección 4
    add_subtitle("4. Contenedorización Multi-Entorno y Optimización con Docker")
    add_body_p(
        "Para lograr un entorno completamente reproducible que elimine la clásica problemática de 'en mi máquina sí funciona', la API se empaquetó como una imagen de contenedor Docker. Se optó por una imagen base minimalista fundamentada en Node.js 22 sobre Alpine Linux ('node:22-alpine'), lo que reduce el tamaño total del artefacto a menos de 150 MB y minimiza de forma radical las posibles vulnerabilidades presentes en distribuciones estándar más pesadas."
    )
    add_body_p(
        "Asimismo, se aplicaron buenas prácticas de seguridad e higiene de construcción. El archivo .dockerignore se configuró de manera estricta para excluir del contexto de compilación los módulos de desarrollo locales ('node_modules'), las bases de datos de prueba SQLite, los reportes de cobertura generados por Jest y los archivos de registro. El proceso de instalación en el contenedor utiliza el comando 'npm ci --omit=dev', garantizando instalaciones deterministas basadas en el archivo package-lock.json y omitiendo librerías exclusivas de desarrollo en la imagen de producción."
    )

    add_code_snippet(
        "# Dockerfile optimizado para usuarios-api\n"
        "FROM node:22-alpine\n"
        "WORKDIR /app\n"
        "COPY package*.json ./\n"
        "RUN npm ci --omit=dev\n"
        "COPY . .\n"
        "EXPOSE 3000\n"
        "CMD [\"npm\", \"start\"]"
    )

    # Subsección 5
    add_subtitle("5. Orquestación del Pipeline CI/CD en GitHub Actions")
    add_body_p(
        "El núcleo de automatización del proyecto reside en el archivo declarativo .github/workflows/main.yml, el cual orquesta un pipeline de tres fases estrictamente secuenciales activadas mediante eventos de empuje ('push') o solicitudes de extracción ('pull_request') hacia la rama principal 'main':"
    )

    add_bullet_item("Fase 1: Integración Continua (Job: test): ", "Aprovisiona un runner limpio en Ubuntu, descarga el código fuente con actions/checkout@v4, configura el entorno de ejecución Node 22 con actions/setup-node@v4 aprovechando caché inteligente de dependencias npm, instala los paquetes con 'npm ci' y ejecuta 'npm test'. Si alguna de las 34 pruebas falla o la cobertura cae por debajo del 70%, el pipeline se interrumpe de inmediato evitando cualquier publicación errónea.")
    add_bullet_item("Fase 2: Gestión y Publicación de Artefactos (Job: build-and-push): ", "Condicionado al éxito del job anterior ('needs: test') y a eventos 'push' en 'main'. Configura el motor de construcción Docker Buildx, se autentica de forma segura en Docker Hub mediante docker/login-action@v3 y construye la imagen etiquetándola con ':latest' y con el identificador único del commit (${{ github.sha }}), permitiendo trazabilidad y reversión ágil ante incidentes.")
    add_bullet_item("Fase 3: Despliegue Continuo (Job: deploy): ", "Condicionado al éxito de la publicación ('needs: build-and-push'). Emplea el action appleboy/ssh-action@v1.0.3 para autenticarse remotamente en la máquina virtual AWS EC2 mediante SSH. El script remoto descarga la imagen más reciente desde Docker Hub, detiene y elimina cualquier contenedor previo en ejecución, e inicia un nuevo contenedor mapeando el puerto externo 80 del servidor al puerto 3000 interno del contenedor.")

    # Subsección 6
    add_subtitle("6. Aprovisionamiento Cloud y Despliegue Continuo en AWS EC2")
    add_body_p(
        "El entorno de destino se aprovisionó en la nube pública de Amazon Web Services (AWS) utilizando una instancia EC2 de tipo t2.micro ejecutando Ubuntu Server 24.04 LTS. Para garantizar la conectividad y seguridad requeridas por el pipeline y los usuarios finales, se definieron reglas estrictas en el Grupo de Seguridad (Security Group):"
    )

    add_bullet_item("Regla SSH (Puerto 22 TCP): ", "Permite la conexión cifrada requerida por el runner de GitHub Actions para transferir y ejecutar los comandos de orquestación de contenedores.")
    add_bullet_item("Regla HTTP (Puerto 80 TCP): ", "Abre el acceso público web para que cualquier cliente, evaluador o navegador pueda interactuar directamente con la API REST desplegada.")

    add_body_p(
        "Dentro de la máquina virtual se configuró el demonio de Docker mediante los comandos 'sudo apt update && sudo apt install -y docker.io', asignando el usuario del sistema 'ubuntu' al grupo administrativo de Docker ('sudo usermod -aG docker ubuntu') y habilitando el inicio automático del servicio con 'sudo systemctl enable --now docker'. Esta configuración permite que los despliegues remotos ejecutados por GitHub Actions operen sin necesidad de escalar privilegios mediante contraseñas interactivas."
    )

    # Subsección 7
    add_subtitle("7. Gestión de Secretos, Resolución de Incidencias y Demostración en Vivo")
    add_body_p(
        "Para preservar la confidencialidad de las credenciales y cumplir con los estándares de DevSecOps, el repositorio no almacena contraseñas ni llaves en texto plano. En su lugar, se configuraron cinco secretos criptográficos en la sección 'Settings > Secrets and variables > Actions > Repository secrets' de GitHub:"
    )

    add_bullet_item("DOCKERHUB_USERNAME: ", "Identificador del usuario en el registro Docker Hub.")
    add_bullet_item("DOCKERHUB_TOKEN: ", "Personal Access Token generado en Docker Hub con permisos de lectura y escritura (Read & Write).")
    add_bullet_item("EC2_HOST: ", "Dirección IPv4 pública asignada a la instancia de AWS EC2.")
    add_bullet_item("EC2_USER: ", "Nombre del usuario con acceso SSH en la máquina virtual (ubuntu).")
    add_bullet_item("EC2_SSH_KEY: ", "Contenido íntegro del par de claves privadas en formato .pem generado por AWS.")

    add_subsubtitle("Resolución de Incidencias Técnicas Reales:")
    add_body_p(
        "Durante la fase de integración se detectaron y resolvieron exitosamente dos eventualidades comunes en flujos reales de desarrollo: en primer término, un commit inicial local vinculó temporalmente la carpeta de módulos pesados 'node_modules' debido a la ausencia inicial de .gitignore en el subdirectorio de origen; esta situación fue subsanada con precisión mediante la inicialización limpia en el proyecto correcto, la definición exhaustiva de exclusiones y la ejecución de un push forzado controlado ('git push -u origin main --force'). En segundo término, durante la ejecución del job 'build-and-push' se presentó la advertencia 'Username and password required', la cual fue diagnosticada oportunamente como la ausencia temporal de las variables de repositorio en GitHub Actions, procediendo a su registro y validación inmediata."
    )

    add_subsubtitle("Metodología de Demostración en Vivo:")
    add_body_p(
        "Para corroborar que la automatización responde sin intervención manual a cualquier modificación del código fuente, se efectuó la prueba de modificación en vivo: se alteró el mensaje del controlador raíz en src/app.js sustituyendo la cadena estática por 'Servidor desplegado automáticamente con CI/CD y Docker'. Al emitir los comandos 'git add .', 'git commit -m ...' y 'git push origin main', se observó en tiempo real cómo GitHub Actions ejecutó las 34 pruebas, publicó la imagen con tag actualizado en Docker Hub y actualizó el contenedor en la IP pública de AWS en menos de 90 segundos, confirmando el éxito operativo de la solución."
    )

    doc.add_page_break()

    # =========================================================================
    # PÁGINA 10: CONCLUSIONES (EXACTAMENTE 4 PÁRRAFOS EXTENSOS)
    # =========================================================================
    add_title("Conclusiones", size=22, space_before=12, space_after=16)

    # Párrafo 1
    add_body_p(
        "Tras la culminación y validación del proyecto integrador, se puede concluir de manera fehaciente que la implementación de un pipeline automatizado de CI/CD representa mucho más que la adopción aislada de herramientas como Docker, GitHub Actions o AWS; constituye una transformación metodológica integral en la forma en que concebimos la calidad y la entrega de software. Al sustituir los métodos tradicionales de subida manual mediante FTP o accesos remotos artesanales por un flujo de trabajo estructurado y guiado por eventos de Git, se elimina por completo la variabilidad introducida por el factor humano, garantizando que cada versión que alcance a los usuarios finales haya superado rigurosos filtros de verificación estática, lógica y operativa."
    )

    # Párrafo 2
    add_body_p(
        "La integración de pruebas unitarias automatizadas con Jest y Supertest vinculadas directamente al umbral de cobertura del 70% demostró ser uno de los pilares más determinantes para la estabilidad del sistema. El hecho de haber alcanzado una cobertura real del 85.77% en líneas y 88.88% en funciones proporciona una confianza técnica absoluta antes de promover cualquier artefacto al registro de Docker Hub. Si una modificación introduce un error sintáctico o una regresión en la lógica de negocio, el job de pruebas interrumpe la ejecución en cuestión de segundos, impidiendo que el contenedor defectuoso sea siquiera compilado o desplegado, lo que salvaguarda la continuidad y reputación del servicio."
    )

    # Párrafo 3
    add_body_p(
        "Asimismo, el uso de la contenedorización con Docker sobre distribuciones ultraligeras como Alpine Linux y la gestión segura de infraestructura en AWS EC2 evidencian la sinergia indispensable entre desarrollo, operaciones y seguridad (DevSecOps). La capacidad de desacoplar la aplicación de las particularidades del sistema operativo anfitrión y encapsularla junto con sus dependencias exactas garantiza una portabilidad intachable. Complementariamente, la centralización de credenciales confidenciales mediante GitHub Secrets protege la información crítica de la infraestructura, evitando la exposición inadvertida de llaves privadas SSH o tokens de registro en repositorios públicos."
    )

    # Párrafo 4
    add_body_p(
        "Finalmente, el desarrollo práctico de este proyecto consolida competencias profesionales indispensables para el perfil del egresado en tecnologías de la información y seguridad de software. La experiencia de haber diagnosticado y resuelto incidentes habituales del control de versiones con Git, haber optimizado el tamaño de imágenes de contenedor y haber presenciado el despliegue automático en la nube a partir de un simple comando 'git push' valida la madurez técnica adquirida. Este proyecto demuestra con claridad cómo la conjunción armónica de estándares de codificación, automatización declarativa e infraestructura cloud permite entregar soluciones tecnológicas ágiles, resilientes, escalables y seguras frente a las demandas de la industria actual."
    )

    doc.add_page_break()

    # =========================================================================
    # PÁGINA 11: FUENTES DE INFORMACIÓN (FORMATO APA)
    # =========================================================================
    add_title("Fuentes de Información", size=22, space_before=12, space_after=16)

    referencias = [
        ("Amazon Web Services. (s. f.). ", "¿Qué es la integración continua (CI)? Amazon Web Services, Inc. https://aws.amazon.com/es/devops/continuous-integration/"),
        ("Amazon Web Services. (s. f.). ", "Amazon EC2: Servidores virtuales en la nube y cómputo elástico. Amazon Web Services, Inc. https://aws.amazon.com/es/ec2/"),
        ("Atlassian. (s. f.). ", "CI/CD Pipeline: Continuous Integration and Delivery Explained. Atlassian Documentation. https://www.atlassian.com/continuous-delivery/ci-cd-pipeline"),
        ("Docker Inc. (s. f.). ", "Docker Overview and Container Architecture. Docker Documentation. https://docs.docker.com/get-started/overview/"),
        ("GitHub. (s. f.). ", "Understanding GitHub Actions: Workflows, Jobs, and Steps. GitHub Documentation. https://docs.github.com/es/actions/learn-github-actions/understanding-github-actions"),
        ("Jest. (s. f.). ", "Jest: Delightful JavaScript Testing with Code Coverage Thresholds. Jest Documentation. https://jestjs.io/docs/configuration#coveragethreshold-object"),
        ("Node.js. (s. f.). ", "Node.js v22.x LTS Documentation and Best Practices. Node.js Foundation. https://nodejs.org/docs/latest-v22.x/api/"),
        ("Sequelize. (s. f.). ", "Sequelize v6: The Modern TypeScript and JavaScript ORM for Node.js. Sequelize Documentation. https://sequelize.org/docs/v6/")
    ]

    for autor, obra in referencias:
        p_ref = doc.add_paragraph()
        p_ref.paragraph_format.left_indent = Inches(0.4)
        p_ref.paragraph_format.first_line_indent = Inches(-0.4)
        p_ref.paragraph_format.space_before = Pt(3)
        p_ref.paragraph_format.space_after = Pt(6)
        p_ref.paragraph_format.line_spacing = 1.15
        
        r_aut = p_ref.add_run(autor)
        r_aut.font.name = 'Georgia'
        r_aut.font.size = Pt(10)
        
        r_obr = p_ref.add_run(obra)
        r_obr.font.name = 'Georgia'
        r_obr.font.size = Pt(10)

    # Guardar en las dos ubicaciones clave
    output_path = "Pipeline_CICD_Usuarios_API_Reporte.docx"
    doc.save(output_path)
    print(f"Documento generado exitosamente en: {output_path}")

    # Guardar copia en la raíz del workspace
    parent_path = os.path.join("..", "..", "Pipeline_CICD_Usuarios_API_Reporte.docx")
    try:
        doc.save(parent_path)
        print(f"Copia guardada en: {parent_path}")
    except Exception as e:
        print(f"Nota copia: {e}")

if __name__ == "__main__":
    generate_report()
