const express = require("express");

const {
  crearRol,
  obtenerRoles,
  obtenerRolPorId,
  actualizarRol,
  eliminarRol
} = require("../controllers/roles.controller");

const router = express.Router();

router.post("/", crearRol);
router.get("/", obtenerRoles);
router.get("/:id", obtenerRolPorId);
router.put("/:id", actualizarRol);
router.delete("/:id", eliminarRol);

module.exports = router;