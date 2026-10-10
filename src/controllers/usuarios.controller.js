const bcrypt = require("bcryptjs");
const { Usuario, Rol } = require("../models");

// POST /api/usuarios
const crearUsuario = async (req, res) => {
  try {
    const { nombre, correo, password, rolId } = req.body;

    if (
      !nombre || typeof nombre !== "string" || !nombre.trim() ||
      !correo || typeof correo !== "string" || !correo.trim() ||
      !password || typeof password !== "string" || !password.trim() ||
      !rolId
    ) {
      return res.status(400).json({
        statusCode: 400,
        data: [],
        message: "Nombre, correo, contraseña y rolId son obligatorios"
      });
    }

    const rol = await Rol.findByPk(rolId);

    if (!rol) {
      return res.status(400).json({
        statusCode: 400,
        data: [],
        message: "El rol indicado no existe"
      });
    }

    const usuarioExistente = await Usuario.findOne({
      where: { correo }
    });

    if (usuarioExistente) {
      return res.status(409).json({
        statusCode: 409,
        data: [],
        message: "El correo ya está registrado"
      });
    }

    const passwordHash = await bcrypt.hash(password, 10);

    const usuario = await Usuario.create({
      nombre,
      correo,
      passwordHash,
      rolId
    });

    const usuarioCreado = await Usuario.findByPk(usuario.id, {
      attributes: { exclude: ["passwordHash"] },
      include: {
        model: Rol,
        as: "rol",
        attributes: ["id", "nombre"]
      }
    });

    return res.status(201).json({
      statusCode: 201,
      data: [usuarioCreado],
      message: "Usuario registrado correctamente"
    });
  } catch (error) {
    return res.status(500).json({
      statusCode: 500,
      data: [],
      message: error.message
    });
  }
};

// GET /api/usuarios
const obtenerUsuarios = async (req, res) => {
  try {
    const usuarios = await Usuario.findAll({
      attributes: { exclude: ["passwordHash"] },
      include: {
        model: Rol,
        as: "rol",
        attributes: ["id", "nombre"]
      }
    });

    return res.status(200).json({
      statusCode: 200,
      data: usuarios
    });
  } catch (error) {
    return res.status(500).json({
      statusCode: 500,
      data: [],
      message: error.message
    });
  }
};

// GET /api/usuarios/:id
const obtenerUsuarioPorId = async (req, res) => {
  try {
    const usuario = await Usuario.findByPk(req.params.id, {
      attributes: { exclude: ["passwordHash"] },
      include: {
        model: Rol,
        as: "rol",
        attributes: ["id", "nombre"]
      }
    });

    if (!usuario) {
      return res.status(404).json({
        statusCode: 404,
        data: [],
        message: "Usuario no encontrado"
      });
    }

    return res.status(200).json({
      statusCode: 200,
      data: [usuario]
    });
  } catch (error) {
    return res.status(500).json({
      statusCode: 500,
      data: [],
      message: error.message
    });
  }
};

// DELETE /api/usuarios/:id
const eliminarUsuario = async (req, res) => {
  try {
    const usuario = await Usuario.findByPk(req.params.id);

    if (!usuario) {
      return res.status(404).json({
        statusCode: 404,
        data: [],
        message: "Usuario no encontrado"
      });
    }

    await usuario.destroy();

    return res.status(200).json({
      statusCode: 200,
      data: [],
      message: "Usuario eliminado correctamente"
    });
  } catch (error) {
    return res.status(500).json({
      statusCode: 500,
      data: [],
      message: error.message
    });
  }
};

// PUT /api/usuarios/:id
const actualizarUsuario = async (req, res) => {
  try {
    const { nombre, correo, password, rolId } = req.body;

    const usuario = await Usuario.findByPk(req.params.id);

    if (!usuario) {
      return res.status(404).json({
        statusCode: 404,
        data: [],
        message: "Usuario no encontrado"
      });
    }

    if (nombre !== undefined && (typeof nombre !== "string" || !nombre.trim())) {
      return res.status(400).json({
        statusCode: 400,
        data: [],
        message: "El nombre no puede estar vacío"
      });
    }

    if (correo !== undefined && (typeof correo !== "string" || !correo.trim())) {
      return res.status(400).json({
        statusCode: 400,
        data: [],
        message: "El correo no puede estar vacío"
      });
    }

    if (password !== undefined && (typeof password !== "string" || !password.trim())) {
      return res.status(400).json({
        statusCode: 400,
        data: [],
        message: "La contraseña no puede estar vacía"
      });
    }

    if (rolId !== undefined) {
      const rol = await Rol.findByPk(rolId);
      if (!rol) {
        return res.status(400).json({
          statusCode: 400,
          data: [],
          message: "El rol indicado no existe"
        });
      }
      usuario.rolId = rolId;
    }

    if (correo && correo.trim().toLowerCase() !== usuario.correo.toLowerCase()) {
      const correoExistente = await Usuario.findOne({
        where: { correo: correo.trim() }
      });
      if (correoExistente) {
        return res.status(409).json({
          statusCode: 409,
          data: [],
          message: "El correo ya está registrado"
        });
      }
      usuario.correo = correo.trim();
    }

    if (nombre) {
      usuario.nombre = nombre.trim();
    }

    if (password) {
      usuario.passwordHash = await bcrypt.hash(password.trim(), 10);
    }

    await usuario.save();

    const usuarioActualizado = await Usuario.findByPk(usuario.id, {
      attributes: { exclude: ["passwordHash"] },
      include: {
        model: Rol,
        as: "rol",
        attributes: ["id", "nombre"]
      }
    });

    return res.status(200).json({
      statusCode: 200,
      data: [usuarioActualizado],
      message: "Usuario actualizado correctamente"
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
  crearUsuario,
  obtenerUsuarios,
  obtenerUsuarioPorId,
  actualizarUsuario,
  eliminarUsuario
};