const express = require("express");
const cors = require("cors");
const path = require("path");

const { sequelize } = require("./config/database");
const { observabilityMiddleware } = require("./config/observability");
require("./models");

const usuariosRoutes = require("./routes/usuarios.routes");
const rolesRoutes = require("./routes/roles.routes");
const databaseRoutes = require("./routes/database.routes");

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());
app.use(observabilityMiddleware);

// Endpoint raíz de bienvenida (requerido por tests de Jest)
app.get("/", (req, res) => {
  const accept = req.headers.accept || "";
  // Navegador web solicitando la página principal
  if (accept.includes("text/html") && !accept.includes("application/json") && accept !== "*/*") {
    return res.sendFile(path.join(__dirname, "../public/index.html"));
  }

  // Respuesta JSON estándar de API
  return res.status(200).json({
    statusCode: 200,
    data: [
      {
        nombre: "API de usuarios",
        estado: "Servidor funcionando"
      }
    ]
  });
});

// Ruta explícita para la aplicación web Frontend
app.get("/app", (req, res) => {
  return res.sendFile(path.join(__dirname, "../public/index.html"));
});

// Servir archivos estáticos del frontend (index: false para que no sobrescriba GET /)
app.use(express.static(path.join(__dirname, "../public"), { index: false }));

app.get("/api/health", (req, res) => {
  return res.status(200).json({
    statusCode: 200,
    status: "OK 2",
    mensaje: "Servidor funcionando correctamente",
    timestamp: new Date().toISOString()
  });
});

app.use("/api/usuarios", usuariosRoutes);
app.use("/api/roles", rolesRoutes);
app.use("/api/database", databaseRoutes);

app.use((req, res) => {
  return res.status(404).json({
    statusCode: 404,
    data: [],
    message: "Endpoint no encontrado"
  });
});

const iniciarServidor = async () => {
  try {
    await sequelize.authenticate();
    console.log("Conexión con SQLite establecida");

    await sequelize.sync();
    console.log("Tablas creadas correctamente");

    if (process.env.NODE_ENV !== "test") {
      const { sembrarDatosIniciales } = require("./config/seed");
      await sembrarDatosIniciales();
    }

    // IMPORTANTE: Agregamos '0.0.0.0' para permitir tráfico externo desde AWS
    return app.listen(PORT, '0.0.0.0', () => {
      console.log(`Servidor ejecutándose en http://0.0.0.0:${PORT}`);
    });
  } catch (error) {
    console.error("Error al iniciar el servidor:", error.message);
    throw error;
  }
};

if (require.main === module) {
  iniciarServidor();
}

app.iniciarServidor = iniciarServidor;
module.exports = app;
