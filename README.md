# Pipeline CI/CD Automatizado para Usuarios API

Proyecto Integrador de Gestión del Proceso de Desarrollo: API REST implementada con Node.js y Express, pruebas automatizadas y cobertura de código con Jest/Supertest, contenedorizada con Docker y desplegada continuamente en AWS EC2 mediante GitHub Actions.

---

## 1. Arquitectura del Proyecto

```
[ Desarrollador ] --( git push main )--> [ GitHub Repository ]
                                                │
                                    ┌───────────┴───────────┐
                                    ▼                       ▼
                              [ Job: test ]          [ GitHub Secrets ]
                          (Jest + Supertest 70%+)           │
                                    │                       │
                                    ▼                       │
                            [ Job: build-push ] <───────────┘
                           (Docker Hub Registry)
                                    │
                                    ▼
                             [ Job: deploy ]
                           (SSH a AWS EC2 :80)
                                    │
                                    ▼
                         [ AWS EC2 Ubuntu Server ]
                         (Contenedor Docker Activo)
```

- **Backend**: Node.js 22 + Express 5
- **ORM & Base de Datos**: Sequelize 6 + SQLite3
- **Seguridad**: Hash de contraseñas con bcryptjs
- **Testing**: Jest 29 + Supertest 7 (34 pruebas automatizadas con >70% de cobertura)
- **Contenedorización**: Docker (Node Alpine)
- **CI/CD**: GitHub Actions (.github/workflows/main.yml)
- **Infraestructura Cloud**: AWS EC2 (Ubuntu Server) en puerto 80

---

## 2. Endpoints de la API

La API expone los 4 verbos HTTP (GET, POST, PUT, DELETE) para todas sus entidades y mantenimiento:

| Método | Endpoint | Descripción | Código Éxito |
|---|---|---|---|
| `GET` | `/` | Comprobación de estado del servicio | 200 OK |
| `GET` | `/api/health` | Healthcheck con timestamp | 200 OK |
| `GET` | `/api/roles` | Listar todos los roles | 200 OK |
| `GET` | `/api/roles/:id` | Consultar rol por ID | 200 OK |
| `POST` | `/api/roles` | Crear nuevo rol | 201 Created |
| `PUT` | `/api/roles/:id` | Actualizar rol existente | 200 OK |
| `DELETE` | `/api/roles/:id` | Eliminar rol | 200 OK |
| `GET` | `/api/usuarios` | Listar usuarios (sin hash) | 200 OK |
| `GET` | `/api/usuarios/:id` | Consultar usuario por ID | 200 OK |
| `POST` | `/api/usuarios` | Registrar nuevo usuario | 201 Created |
| `PUT` | `/api/usuarios/:id` | Actualizar datos de usuario | 200 OK |
| `DELETE` | `/api/usuarios/:id` | Eliminar usuario | 200 OK |
| `POST` | `/api/database/backup` | Descargar respaldo SQLite | 200 OK |
| `DELETE` | `/api/database/vaciar` | Vaciar todas las tablas | 200 OK |

---

## 3. Ejecución Local

### Prerrequisitos
- Node.js >= 20.x
- npm >= 10.x

### Instalación y arranque
```bash
# Instalar dependencias
npm install

# Iniciar en modo producción
npm start

# Iniciar en modo desarrollo (con nodemon)
npm run dev
```

El servidor quedará escuchando en `http://localhost:3000`.

---

## 4. Pruebas Automatizadas y Cobertura

Para ejecutar las 34 pruebas automatizadas y verificar el umbral de cobertura mínimo del 70%:

```bash
npm test
```

El reporte de cobertura se generará en la consola y dentro del directorio `coverage/`.

---

## 5. Construcción y Ejecución en Docker Local

```bash
# Construir la imagen Docker
docker build -t usuarios-api:latest .

# Ejecutar el contenedor mapeando el puerto 3000
docker run -d --name usuarios-api -p 3000:3000 usuarios-api:latest

# Probar funcionamiento
curl http://localhost:3000/api/health
```

---

## 6. Configuración del Pipeline CI/CD en GitHub

El pipeline se encuentra en `.github/workflows/main.yml` y consta de tres fases:
1. **test**: Clona el código, instala dependencias y ejecuta la suite de pruebas validando el 70% de cobertura.
2. **build-and-push**: Compila la imagen Docker y la publica en Docker Hub con tags `:latest` y `:${{ github.sha }}`.
3. **deploy**: Conecta por SSH a la instancia EC2, descarga la imagen de Docker Hub y refresca el contenedor en el puerto 80.

### Secretos requeridos en el repositorio (`Settings > Secrets and variables > Actions`):
- `DOCKERHUB_USERNAME`: Nombre de usuario en Docker Hub.
- `DOCKERHUB_TOKEN`: Personal Access Token (PAT) de Docker Hub con permisos de Read & Write.
- `EC2_HOST`: Dirección IP pública o DNS de tu instancia AWS EC2.
- `EC2_USER`: Usuario SSH de la máquina virtual (generalmente `ubuntu`).
- `EC2_SSH_KEY`: Contenido completo de tu archivo de clave privada `.pem`.
