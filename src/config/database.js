const path = require("path");
const { Sequelize } = require("sequelize");

const isTest = process.env.NODE_ENV === "test";
const databasePath = isTest
  ? path.join(__dirname, "../../database.test.sqlite")
  : path.join(__dirname, "../../database.sqlite");

const sequelize = new Sequelize({
  dialect: "sqlite",
  storage: databasePath,
  logging: false
});

module.exports = {
  sequelize,
  databasePath
};