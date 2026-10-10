const fs = require("fs");
const path = require("path");

const { sequelize, databasePath } = require("../config/database");
const { Usuario, Rol } = require("../models");

// POST /api/database/backup
const crearBackup = async (req, res) => {
  try {
    await sequelize.authenticate();

    const backupDirectory = path.join(__dirname, "../../backups");

    if (!fs.existsSync(backupDirectory)) {
      fs.mkdirSync(backupDirectory, { recursive: true });
    }

    const fecha = new Date()
      .toISOString()
      .replace(/:/g, "-")
      .replace(/\./g, "-");

    const nombreArchivo = `backup-${fecha}.sqlite`;
    const rutaBackup = path.join(backupDirectory, nombreArchivo);

    fs.copyFileSync(databasePath, rutaBackup);

    // Envía el archivo como descarga
    return res.download(rutaBackup, nombreArchivo, (error) => {
      if (error) {
        console.error("Error al descargar el backup:", error);

        if (!res.headersSent) {
          res.status(500).json({
            statusCode: 500,
            data: [],
            message: "El backup fue creado, pero no pudo descargarse"
          });
        }
      }
    });
  } catch (error) {
    return res.status(500).json({
      statusCode: 500,
      data: [],
      message: error.message
    });
  }
};

// DELETE /api/database/vaciar
const vaciarDatabase = async (req, res) => {
  const transaction = await sequelize.transaction();

  try {
    // Primero usuarios por la llave foránea rolId
    await Usuario.destroy({
      where: {},
      truncate: false,
      transaction
    });

    await Rol.destroy({
      where: {},
      truncate: false,
      transaction
    });

    await transaction.commit();

    return res.status(200).json({
      statusCode: 200,
      data: [],
      message: "Base de datos vaciada correctamente"
    });
  } catch (error) {
    await transaction.rollback();

    return res.status(500).json({
      statusCode: 500,
      data: [],
      message: error.message
    });
  }
};

module.exports = {
  crearBackup,
  vaciarDatabase
};