const express = require("express");

const {
  crearBackup,
  vaciarDatabase,
  sembrarDatabase
} = require("../controllers/database.controller");

const router = express.Router();

router.post("/backup", crearBackup);
router.get("/backup", crearBackup);
router.delete("/vaciar", vaciarDatabase);
router.post("/vaciar", vaciarDatabase);
router.post("/seed", sembrarDatabase);

module.exports = router;
