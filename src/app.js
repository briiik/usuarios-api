const express = require("express");
const cors = require("cors");

const { sequelize } = require("./config/database");
require("./models");

const usuariosRoutes = require("./routes/usuarios.routes");
const rolesRoutes = require("./routes/roles.routes");
const databaseRoutes = require("./routes/database.routes");

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());

app.get("/", (req, res) => {
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

app.get("/api/health", (req, res) => {
  return res.status(200).json({
    statusCode: 200,
    status: "OK",
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

    return app.listen(PORT, () => {
      console.log(`Servidor ejecutándose en http://localhost:${PORT}`);
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