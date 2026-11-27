const bcrypt = require("bcryptjs");
const { Usuario, Rol } = require("../models");

const DOMINIOS_PERMITIDOS = [
  "gmail.com",
  "uteq.edu.mx",
  "hotmail.com",
  "outlook.com",
  "empresa.com",
  "test.com"
];

const CARACTERES_ESPECIALES_REGEX = /[#$@!%*?&_\-]/;

// POST /api/usuarios
const crearUsuario = async (req, res) => {
  try {
    const { nombre, correo, password, confirmPassword, rolId } = req.body;

    // 1. Verificación de campos obligatorios
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

    const correoLimpio = correo.trim().toLowerCase();

    // 2. Validación de existencia del rol
    const rol = await Rol.findByPk(rolId);
    if (!rol) {
      return res.status(400).json({
        statusCode: 400,
        data: [],
        message: "El rol indicado no existe"
      });
    }

    // 3. Validación de correo duplicado
    const usuarioExistente = await Usuario.findOne({
      where: { correo: correoLimpio }
    });

    if (usuarioExistente) {
      return res.status(409).json({
        statusCode: 409,
        data: [],
        message: "El correo ya está registrado"
      });
    }

    // 4. Validación de formato de correo y dominios permitidos
    const partesCorreo = correoLimpio.split("@");
    if (partesCorreo.length !== 2 || !partesCorreo[0] || !partesCorreo[1]) {
      return res.status(400).json({
        statusCode: 400,
        data: [],
        message: "El correo electrónico debe incluir un '@' y un formato válido"
      });
    }

    const dominio = partesCorreo[1];
    if (!DOMINIOS_PERMITIDOS.includes(dominio)) {
      return res.status(400).json({
        statusCode: 400,
        data: [],
        message: `Dominio '@${dominio}' no permitido. Debe pertenecer a: gmail.com, uteq.edu.mx, hotmail.com, outlook.com o empresa.com`
      });
    }

    // 5. Validación de contraseña: mínimo 8 caracteres
    if (password.length < 8) {
      return res.status(400).json({
        statusCode: 400,
        data: [],
        message: "La contraseña debe tener una longitud mínima de 8 caracteres"
      });
    }

    // 6. Validación de contraseña: al menos un carácter especial (#, $, @, !, %, *, &, _, -)
    if (!CARACTERES_ESPECIALES_REGEX.test(password)) {
      return res.status(400).json({
        statusCode: 400,
        data: [],
        message: "La contraseña debe contener al menos un carácter especial (#, $, @, !, %, *, &, _, -)"
      });
    }

    // 7. Validación de confirmación idéntica de contraseña (si se envía)
    if (confirmPassword !== undefined && confirmPassword !== password) {
      return res.status(400).json({
        statusCode: 400,
        data: [],
        message: "Las contraseñas no coinciden. Deben ser idénticas"
      });
    }

    const passwordHash = await bcrypt.hash(password, 10);

    const usuario = await Usuario.create({
      nombre: nombre.trim(),
      correo: correoLimpio,
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
      },
      order: [["id", "ASC"]]
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
    const { nombre, correo, password, confirmPassword, rolId } = req.body;

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

    if (correo) {
      const correoLimpio = correo.trim().toLowerCase();
      const partes = correoLimpio.split("@");
      if (partes.length !== 2 || !partes[0] || !partes[1]) {
        return res.status(400).json({
          statusCode: 400,
          data: [],
          message: "El correo electrónico debe incluir un '@' y un formato válido"
        });
      }
      const dom = partes[1];
      if (!DOMINIOS_PERMITIDOS.includes(dom)) {
        return res.status(400).json({
          statusCode: 400,
          data: [],
          message: `Dominio '@${dom}' no permitido. Debe ser gmail.com, uteq.edu.mx, hotmail.com o empresa.com`
        });
      }

      if (correoLimpio !== usuario.correo.toLowerCase()) {
        const correoExistente = await Usuario.findOne({ where: { correo: correoLimpio } });
        if (correoExistente) {
          return res.status(409).json({
            statusCode: 409,
            data: [],
            message: "El correo ya está registrado"
          });
        }
        usuario.correo = correoLimpio;
      }
    }

    if (password !== undefined) {
      if (typeof password !== "string" || !password.trim()) {
        return res.status(400).json({
          statusCode: 400,
          data: [],
          message: "La contraseña no puede estar vacía"
        });
      }
      if (password.length < 8) {
        return res.status(400).json({
          statusCode: 400,
          data: [],
          message: "La contraseña debe tener una longitud mínima de 8 caracteres"
        });
      }
      if (!CARACTERES_ESPECIALES_REGEX.test(password)) {
        return res.status(400).json({
          statusCode: 400,
          data: [],
          message: "La contraseña debe contener al menos un carácter especial (#, $, @, !, %, *, &, _, -)"
        });
      }
      if (confirmPassword !== undefined && confirmPassword !== password) {
        return res.status(400).json({
          statusCode: 400,
          data: [],
          message: "Las contraseñas no coinciden. Deben ser idénticas"
        });
      }
      usuario.passwordHash = await bcrypt.hash(password.trim(), 10);
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

    if (nombre) {
      usuario.nombre = nombre.trim();
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
