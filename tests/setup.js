process.env.NODE_ENV = "test";

const { sequelize } = require("../src/config/database");
require("../src/models");

beforeAll(async () => {
  await sequelize.authenticate();
  await sequelize.sync({ force: true });
});

afterAll(async () => {
  await sequelize.close();
});
