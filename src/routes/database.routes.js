const express = require("express");

const {
  crearBackup,
  vaciarDatabase
} = require("../controllers/database.controller");

const router = express.Router();

router.post("/backup", crearBackup);
router.get("/backup", crearBackup);
router.delete("/vaciar", vaciarDatabase);
router.post("/vaciar", vaciarDatabase);

module.exports = router;