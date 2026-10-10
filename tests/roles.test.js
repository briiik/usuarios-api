const request = require("supertest");
const app = require("../src/app");
const { Rol, Usuario } = require("../src/models");
const { sequelize } = require("../src/config/database");

require("./setup");

describe("Endpoints de Roles (/api/roles)", () => {
  beforeEach(async () => {
    await Usuario.destroy({ where: {}, truncate: false });
    await Rol.destroy({ where: {}, truncate: false });
  });

  const crearRolPrueba = async (nombre = "Administrador") => {
    const rol = await Rol.create({ nombre: `${nombre}-${Date.now()}-${Math.random().toString(36).substring(2, 6)}` });
    return rol;
  };

  test("GET /api/roles debe retornar 200 y la lista de roles", async () => {
    await crearRolPrueba("Editor");

    const res = await request(app).get("/api/roles");

    expect(res.statusCode).toBe(200);
    expect(res.body.statusCode).toBe(200);
    expect(Array.isArray(res.body.data)).toBe(true);
    expect(res.body.data.length).toBeGreaterThanOrEqual(1);
  });

  test("POST /api/roles debe crear un rol válido y retornar 201", async () => {
    const res = await request(app)
      .post("/api/roles")
      .send({ nombre: `Supervisor-${Date.now()}` });

    expect(res.statusCode).toBe(201);
    expect(res.body.statusCode).toBe(201);
    expect(res.body.data[0]).toHaveProperty("id");
    expect(res.body.message).toContain("creado correctamente");
  });

  test("GET /api/roles/:id debe retornar 200 y el rol consultado", async () => {
    const rol = await crearRolPrueba("Contador");

    const res = await request(app).get(`/api/roles/${rol.id}`);

    expect(res.statusCode).toBe(200);
    expect(res.body.statusCode).toBe(200);
    expect(res.body.data[0].id).toBe(rol.id);
  });

  test("PUT /api/roles/:id debe actualizar el rol existente y retornar 200", async () => {
    const rol = await crearRolPrueba("Analista");

    const res = await request(app)
      .put(`/api/roles/${rol.id}`)
      .send({ nombre: `Analista Senior-${Date.now()}` });

    expect(res.statusCode).toBe(200);
    expect(res.body.statusCode).toBe(200);
    expect(res.body.data[0].nombre).toContain("Analista Senior");
  });

  test("DELETE /api/roles/:id debe eliminar el rol y retornar 200", async () => {
    const rol = await crearRolPrueba("Temporal");

    const res = await request(app).delete(`/api/roles/${rol.id}`);

    expect(res.statusCode).toBe(200);
    expect(res.body.statusCode).toBe(200);
    expect(res.body.message).toContain("eliminado correctamente");

    const buscado = await Rol.findByPk(rol.id);
    expect(buscado).toBeNull();
  });

  test("GET /api/roles/:id con ID inexistente debe retornar 404", async () => {
    const res = await request(app).get("/api/roles/999999");

    expect(res.statusCode).toBe(404);
    expect(res.body.statusCode).toBe(404);
    expect(res.body.message).toContain("no encontrado");
  });

  test("POST /api/roles con nombre vacío debe retornar 400", async () => {
    const res = await request(app)
      .post("/api/roles")
      .send({ nombre: "" });

    expect(res.statusCode).toBe(400);
    expect(res.body.statusCode).toBe(400);
    expect(res.body.message).toContain("obligatorio");
  });

  test("POST /api/roles con solo espacios en blanco debe retornar 400", async () => {
    const res = await request(app)
      .post("/api/roles")
      .send({ nombre: "     " });

    expect(res.statusCode).toBe(400);
    expect(res.body.statusCode).toBe(400);
    expect(res.body.message).toContain("obligatorio");
  });

  test("POST /api/roles con nombre duplicado debe retornar 409", async () => {
    const nombreUnico = `Exclusivo-${Date.now()}`;
    await Rol.create({ nombre: nombreUnico });

    const res = await request(app)
      .post("/api/roles")
      .send({ nombre: nombreUnico });

    expect(res.statusCode).toBe(409);
    expect(res.body.statusCode).toBe(409);
    expect(res.body.message).toContain("ya existe");
  });

  test("PUT /api/roles/:id con ID inexistente debe retornar 404", async () => {
    const res = await request(app)
      .put("/api/roles/999999")
      .send({ nombre: "Nuevo Rol" });

    expect(res.statusCode).toBe(404);
    expect(res.body.statusCode).toBe(404);
  });

  test("PUT /api/roles/:id con nombre vacío debe retornar 400", async () => {
    const rol = await crearRolPrueba("ParaEditar");

    const res = await request(app)
      .put(`/api/roles/${rol.id}`)
      .send({ nombre: "" });

    expect(res.statusCode).toBe(400);
    expect(res.body.statusCode).toBe(400);
  });

  test("DELETE /api/roles/:id con ID inexistente debe retornar 404", async () => {
    const res = await request(app).delete("/api/roles/999999");

    expect(res.statusCode).toBe(404);
    expect(res.body.statusCode).toBe(404);
  });

  test("DELETE /api/roles/:id cuando tiene usuarios asociados debe retornar 409", async () => {
    const rol = await crearRolPrueba("RolConUsuarios");
    await Usuario.create({
      nombre: "Juan Perez",
      correo: `juan-${Date.now()}@test.com`,
      passwordHash: "hash123",
      rolId: rol.id
    });

    const res = await request(app).delete(`/api/roles/${rol.id}`);

    expect(res.statusCode).toBe(409);
    expect(res.body.statusCode).toBe(409);
    expect(res.body.message).toContain("tiene usuarios");
  });
});
