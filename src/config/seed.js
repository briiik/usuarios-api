// src/config/seed.js - Carga de roles y usuarios ficticios iniciales
const bcrypt = require("bcryptjs");
const { Rol, Usuario } = require("../models");

const ROLES_INICIALES = [
  "Administrador",
  "Supervisor",
  "Operador",
  "Auditor",
  "Invitado"
];

const USUARIOS_FICTICIOS = [
  {
    nombre: "Brisa Granados",
    correo: "brisa.granados@uteq.edu.mx",
    password: "PasswordSeguro123@",
    rolNombre: "Administrador"
  },
  {
    nombre: "Emmanuel Martínez",
    correo: "emmanuel.docente@uteq.edu.mx",
    password: "PasswordSeguro123@",
    rolNombre: "Supervisor"
  },
  {
    nombre: "Carlos Mendoza",
    correo: "carlos.mendoza@gmail.com",
    password: "PasswordSeguro123@",
    rolNombre: "Operador"
  },
  {
    nombre: "Mariana López",
    correo: "mariana.lopez@hotmail.com",
    password: "PasswordSeguro123@",
    rolNombre: "Auditor"
  },
  {
    nombre: "Rodrigo Sánchez",
    correo: "rodrigo.sanchez@empresa.com",
    password: "PasswordSeguro123@",
    rolNombre: "Operador"
  },
  {
    nombre: "Sofía Valenzuela",
    correo: "sofia.valenzuela@outlook.com",
    password: "PasswordSeguro123@",
    rolNombre: "Invitado"
  }
];

async function sembrarDatosIniciales() {
  try {
    const conteoRoles = await Rol.count();
    if (conteoRoles === 0) {
      console.log("[SEED] Sembrando catálogo inicial de roles...");
      for (const r of ROLES_INICIALES) {
        await Rol.findOrCreate({ where: { nombre: r } });
      }
    }

    const conteoUsuarios = await Usuario.count();
    if (conteoUsuarios === 0) {
      console.log("[SEED] Sembrando usuarios ficticios de prueba...");
      for (const u of USUARIOS_FICTICIOS) {
        const rol = await Rol.findOne({ where: { nombre: u.rolNombre } });
        if (rol) {
          const hash = await bcrypt.hash(u.password, 10);
          await Usuario.create({
            nombre: u.nombre,
            correo: u.correo,
            passwordHash: hash,
            rolId: rol.id
          });
        }
      }
      console.log("[SEED] Datos iniciales cargados con éxito.");
    }
  } catch (error) {
    console.error("[SEED] Error al sembrar datos:", error.message);
  }
}

module.exports = {
  sembrarDatosIniciales,
  ROLES_INICIALES,
  USUARIOS_FICTICIOS
};
