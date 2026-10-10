const request = require("supertest");
const app = require("../src/app");
const { Rol, Usuario } = require("../src/models");

require("./setup");

describe("Endpoints de Usuarios (/api/usuarios)", () => {
  let rolIdDefault;

  beforeEach(async () => {
    await Usuario.destroy({ where: {}, truncate: false });
    await Rol.destroy({ where: {}, truncate: false });

    const rol = await Rol.create({ nombre: `RolBase-${Date.now()}` });
    rolIdDefault = rol.id;
  });

  const crearUsuarioPrueba = async (rolId = rolIdDefault) => {
    const sufijo = `${Date.now()}-${Math.random().toString(36).substring(2, 6)}`;
    const usuario = await Usuario.create({
      nombre: `Usuario ${sufijo}`,
      correo: `user-${sufijo}@test.com`,
      passwordHash: "hashPrueba",
      rolId
    });
    return usuario;
  };

  test("GET /api/usuarios debe retornar 200 y la lista de usuarios", async () => {
    await crearUsuarioPrueba();

    const res = await request(app).get("/api/usuarios");

    expect(res.statusCode).toBe(200);
    expect(res.body.statusCode).toBe(200);
    expect(Array.isArray(res.body.data)).toBe(true);
    expect(res.body.data.length).toBeGreaterThanOrEqual(1);
  });

  test("POST /api/usuarios debe registrar un usuario válido y retornar 201", async () => {
    const sufijo = `${Date.now()}`;
    const res = await request(app)
      .post("/api/usuarios")
      .send({
        nombre: "Carlos Gomez",
        correo: `carlos-${sufijo}@empresa.com`,
        password: "passwordSeguro123",
        rolId: rolIdDefault
      });

    expect(res.statusCode).toBe(201);
    expect(res.body.statusCode).toBe(201);
    expect(res.body.data[0]).toHaveProperty("id");
    expect(res.body.data[0].correo).toContain("carlos");
    expect(res.body.data[0]).not.toHaveProperty("passwordHash");
  });

  test("GET /api/usuarios/:id debe retornar 200 y el usuario correspondiente", async () => {
    const usuario = await crearUsuarioPrueba();

    const res = await request(app).get(`/api/usuarios/${usuario.id}`);

    expect(res.statusCode).toBe(200);
    expect(res.body.statusCode).toBe(200);
    expect(res.body.data[0].id).toBe(usuario.id);
  });

  test("PUT /api/usuarios/:id debe actualizar el usuario y retornar 200", async () => {
    const usuario = await crearUsuarioPrueba();

    const res = await request(app)
      .put(`/api/usuarios/${usuario.id}`)
      .send({
        nombre: "Nombre Modificado",
        correo: `modificado-${Date.now()}@test.com`
      });

    expect(res.statusCode).toBe(200);
    expect(res.body.statusCode).toBe(200);
    expect(res.body.data[0].nombre).toBe("Nombre Modificado");
  });

  test("DELETE /api/usuarios/:id debe eliminar el usuario y retornar 200", async () => {
    const usuario = await crearUsuarioPrueba();

    const res = await request(app).delete(`/api/usuarios/${usuario.id}`);

    expect(res.statusCode).toBe(200);
    expect(res.body.statusCode).toBe(200);
    expect(res.body.message).toContain("eliminado correctamente");

    const buscado = await Usuario.findByPk(usuario.id);
    expect(buscado).toBeNull();
  });

  test("GET /api/usuarios/:id con ID inexistente debe retornar 404", async () => {
    const res = await request(app).get("/api/usuarios/999999");

    expect(res.statusCode).toBe(404);
    expect(res.body.statusCode).toBe(404);
    expect(res.body.message).toContain("no encontrado");
  });

  test("POST /api/usuarios con nombre vacío debe retornar 400", async () => {
    const res = await request(app)
      .post("/api/usuarios")
      .send({
        nombre: "",
        correo: `test-${Date.now()}@test.com`,
        password: "123",
        rolId: rolIdDefault
      });

    expect(res.statusCode).toBe(400);
    expect(res.body.statusCode).toBe(400);
    expect(res.body.message).toContain("obligatorios");
  });

  test("POST /api/usuarios con correo faltante o vacío debe retornar 400", async () => {
    const res = await request(app)
      .post("/api/usuarios")
      .send({
        nombre: "Test",
        correo: "   ",
        password: "123",
        rolId: rolIdDefault
      });

    expect(res.statusCode).toBe(400);
    expect(res.body.statusCode).toBe(400);
  });

  test("POST /api/usuarios con rolId inexistente debe retornar 400", async () => {
    const res = await request(app)
      .post("/api/usuarios")
      .send({
        nombre: "Test Invalido",
        correo: `invalido-${Date.now()}@test.com`,
        password: "123",
        rolId: 999999
      });

    expect(res.statusCode).toBe(400);
    expect(res.body.statusCode).toBe(400);
    expect(res.body.message).toContain("El rol indicado no existe");
  });

  test("POST /api/usuarios con correo duplicado debe retornar 409", async () => {
    const correoExistente = `duplicado-${Date.now()}@test.com`;
    await Usuario.create({
      nombre: "Original",
      correo: correoExistente,
      passwordHash: "hash",
      rolId: rolIdDefault
    });

    const res = await request(app)
      .post("/api/usuarios")
      .send({
        nombre: "Copia",
        correo: correoExistente,
        password: "123",
        rolId: rolIdDefault
      });

    expect(res.statusCode).toBe(409);
    expect(res.body.statusCode).toBe(409);
    expect(res.body.message).toContain("ya está registrado");
  });

  test("PUT /api/usuarios/:id con ID inexistente debe retornar 404", async () => {
    const res = await request(app)
      .put("/api/usuarios/999999")
      .send({ nombre: "Nuevo" });

    expect(res.statusCode).toBe(404);
    expect(res.body.statusCode).toBe(404);
  });

  test("PUT /api/usuarios/:id con nombre vacío debe retornar 400", async () => {
    const usuario = await crearUsuarioPrueba();

    const res = await request(app)
      .put(`/api/usuarios/${usuario.id}`)
      .send({ nombre: "" });

    expect(res.statusCode).toBe(400);
    expect(res.body.statusCode).toBe(400);
  });

  test("PUT /api/usuarios/:id con rolId inexistente debe retornar 400", async () => {
    const usuario = await crearUsuarioPrueba();

    const res = await request(app)
      .put(`/api/usuarios/${usuario.id}`)
      .send({ rolId: 999999 });

    expect(res.statusCode).toBe(400);
    expect(res.body.statusCode).toBe(400);
    expect(res.body.message).toContain("El rol indicado no existe");
  });

  test("DELETE /api/usuarios/:id con ID inexistente debe retornar 404", async () => {
    const res = await request(app).delete("/api/usuarios/999999");

    expect(res.statusCode).toBe(404);
    expect(res.body.statusCode).toBe(404);
  });
});
