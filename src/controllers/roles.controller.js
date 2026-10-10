const { Rol, Usuario } = require("../models");

// POST /api/roles
const crearRol = async (req, res) => {
  try {
    const { nombre } = req.body;

    if (!nombre || typeof nombre !== "string" || !nombre.trim()) {
      return res.status(400).json({
        statusCode: 400,
        data: [],
        message: "El nombre del rol es obligatorio"
      });
    }

    const nombreLimpio = nombre.trim();
    const rolExistente = await Rol.findOne({
      where: { nombre: nombreLimpio }
    });

    if (rolExistente) {
      return res.status(409).json({
        statusCode: 409,
        data: [],
        message: "El rol ya existe"
      });
    }

    const rol = await Rol.create({ nombre: nombreLimpio });

    return res.status(201).json({
      statusCode: 201,
      data: [rol],
      message: "Rol creado correctamente"
    });
  } catch (error) {
    return res.status(500).json({
      statusCode: 500,
      data: [],
      message: error.message
    });
  }
};

// GET /api/roles
const obtenerRoles = async (req, res) => {
  try {
    const roles = await Rol.findAll();

    return res.status(200).json({
      statusCode: 200,
      data: roles
    });
  } catch (error) {
    return res.status(500).json({
      statusCode: 500,
      data: [],
      message: error.message
    });
  }
};

// GET /api/roles/:id
const obtenerRolPorId = async (req, res) => {
  try {
    const rol = await Rol.findByPk(req.params.id, {
      include: {
        model: Usuario,
        as: "usuarios",
        attributes: ["id", "nombre", "correo"]
      }
    });

    if (!rol) {
      return res.status(404).json({
        statusCode: 404,
        data: [],
        message: "Rol no encontrado"
      });
    }

    return res.status(200).json({
      statusCode: 200,
      data: [rol]
    });
  } catch (error) {
    return res.status(500).json({
      statusCode: 500,
      data: [],
      message: error.message
    });
  }
};

// DELETE /api/roles/:id
const eliminarRol = async (req, res) => {
  try {
    const rol = await Rol.findByPk(req.params.id);

    if (!rol) {
      return res.status(404).json({
        statusCode: 404,
        data: [],
        message: "Rol no encontrado"
      });
    }

    const usuariosConRol = await Usuario.count({
      where: { rolId: rol.id }
    });

    if (usuariosConRol > 0) {
      return res.status(409).json({
        statusCode: 409,
        data: [],
        message: "No se puede eliminar el rol porque tiene usuarios"
      });
    }

    await rol.destroy();

    return res.status(200).json({
      statusCode: 200,
      data: [],
      message: "Rol eliminado correctamente"
    });
  } catch (error) {
    return res.status(500).json({
      statusCode: 500,
      data: [],
      message: error.message
    });
  }
};

// PUT /api/roles/:id
const actualizarRol = async (req, res) => {
  try {
    const { nombre } = req.body;

    if (!nombre || typeof nombre !== "string" || !nombre.trim()) {
      return res.status(400).json({
        statusCode: 400,
        data: [],
        message: "El nombre del rol es obligatorio"
      });
    }

    const rol = await Rol.findByPk(req.params.id);

    if (!rol) {
      return res.status(404).json({
        statusCode: 404,
        data: [],
        message: "Rol no encontrado"
      });
    }

    const nombreLimpio = nombre.trim();
    if (nombreLimpio !== rol.nombre) {
      const rolExistente = await Rol.findOne({
        where: { nombre: nombreLimpio }
      });

      if (rolExistente) {
        return res.status(409).json({
          statusCode: 409,
          data: [],
          message: "El rol ya existe"
        });
      }
    }

    rol.nombre = nombreLimpio;
    await rol.save();

    return res.status(200).json({
      statusCode: 200,
      data: [rol],
      message: "Rol actualizado correctamente"
    });
  } catch (error) {
    return res.status(500).json({
      statusCode: 500,
      data: [],
      message: error.message
    });
  }
};

module.exports = {
  crearRol,
  obtenerRoles,
  obtenerRolPorId,
  actualizarRol,
  eliminarRol
};