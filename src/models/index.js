const Rol = require("./rol");
const Usuario = require("./usuario");

Rol.hasMany(Usuario, {
  foreignKey: "rolId",
  as: "usuarios"
});

Usuario.belongsTo(Rol, {
  foreignKey: "rolId",
  as: "rol"
});

module.exports = {
  Rol,
  Usuario
};