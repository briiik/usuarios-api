const request = require("supertest");
const app = require("../src/app");
const { Rol, Usuario } = require("../src/models");
const fs = require("fs");
const path = require("path");

require("./setup");

describe("Endpoints de Mantenimiento de Base de Datos (/api/database)", () => {
  beforeEach(async () => {
    await Usuario.destroy({ where: {}, truncate: false });
    await Rol.destroy({ where: {}, truncate: false });
  });

  test("DELETE /api/database/vaciar debe eliminar todos los registros y retornar 200", async () => {
    // Arrange: Crear registros previos
    const rol = await Rol.create({ nombre: "RolTemporal" });
    await Usuario.create({
      nombre: "UsuarioPrueba",
      correo: "temporal@test.com",
      passwordHash: "hash123",
      rolId: rol.id
    });

    // Act: Llamar a vaciar
    const res = await request(app).delete("/api/database/vaciar");

    // Assert
    expect(res.statusCode).toBe(200);
    expect(res.body.statusCode).toBe(200);
    expect(res.body.message).toContain("vaciada correctamente");

    const countUsuarios = await Usuario.count();
    const countRoles = await Rol.count();

    expect(countUsuarios).toBe(0);
    expect(countRoles).toBe(0);
  });

  test("POST /api/database/vaciar también debe funcionar como método alternativo y retornar 200", async () => {
    const res = await request(app).post("/api/database/vaciar");

    expect(res.statusCode).toBe(200);
    expect(res.body.statusCode).toBe(200);
  });

  test("DELETE /api/database/vaciar cuando ya está vacía no debe fallar y retornar 200", async () => {
    const res1 = await request(app).delete("/api/database/vaciar");
    expect(res1.statusCode).toBe(200);

    const res2 = await request(app).delete("/api/database/vaciar");
    expect(res2.statusCode).toBe(200);
  });

  test("POST /api/database/backup debe generar el archivo de respaldo", async () => {
    // Asegurar que exista el archivo de BD en disco para copiar
    const { databasePath } = require("../src/config/database");
    if (!fs.existsSync(databasePath)) {
      fs.writeFileSync(databasePath, "");
    }

    const res = await request(app).post("/api/database/backup");

    expect(res.statusCode).toBe(200);
    expect(res.headers["content-disposition"]).toContain("attachment");
  });

  test("GET / debe retornar 200 y mensaje de servidor funcionando", async () => {
    const res = await request(app).get("/");
    expect(res.statusCode).toBe(200);
    expect(res.body.statusCode).toBe(200);
    expect(res.body.data[0].estado).toContain("funcionando");
  });

  test("GET /api/health debe retornar 200 con status OK", async () => {
    const res = await request(app).get("/api/health");
    expect(res.statusCode).toBe(200);
    expect(res.body.status).toBe("OK");
  });

  test("GET ruta inexistente debe retornar 404", async () => {
    const res = await request(app).get("/api/ruta-que-no-existe");
    expect(res.statusCode).toBe(404);
    expect(res.body.statusCode).toBe(404);
  });
});
