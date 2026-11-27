// public/app.js - Lógica interactiva del Frontend para usuarios-api
let listaUsuariosGlobal = [];
let listaRolesGlobal = [];

document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("host-info").textContent = window.location.origin;
  cargarTodo();
  // Monitoreo periódico del healthcheck cada 15 segundos
  setInterval(comprobarSalud, 15000);
});

async function cargarTodo() {
  await Promise.all([comprobarSalud(), cargarRoles(), cargarUsuarios()]);
}

// ==========================================
// 1. HEALTHCHECK Y OBSERVABILIDAD DEL SERVIDOR
// ==========================================
async function comprobarSalud() {
  const pill = document.getElementById("health-pill");
  const statusTxt = document.getElementById("health-status");
  const latencyTxt = document.getElementById("health-latency");
  const statHealth = document.getElementById("stat-health");
  const statTimestamp = document.getElementById("stat-timestamp");
  const footerStatus = document.getElementById("footer-status");

  const inicio = performance.now();
  try {
    const res = await fetch("/api/health");
    const duracion = Math.round(performance.now() - inicio);
    const data = await res.json();

    if (res.ok) {
      pill.classList.remove("error");
      statusTxt.textContent = `Saludable (${data.status || "OK"})`;
      latencyTxt.textContent = `${duracion}ms`;
      statHealth.textContent = "OK";
      statHealth.className = "stat-value text-success";
      statTimestamp.textContent = `Comprobado: ${new Date(data.timestamp).toLocaleTimeString()}`;
      footerStatus.textContent = "En línea";
      footerStatus.className = "text-success";
    } else {
      throw new Error(`Código ${res.status}`);
    }
  } catch (error) {
    pill.classList.add("error");
    statusTxt.textContent = "Sin conexión";
    latencyTxt.textContent = "--";
    statHealth.textContent = "Falla";
    statHealth.className = "stat-value text-danger";
    statTimestamp.textContent = "Servidor no responde";
    footerStatus.textContent = "Desconectado";
    footerStatus.className = "text-danger";
  }
}

// ==========================================
// 2. GESTIÓN DE ROLES
// ==========================================
async function cargarRoles() {
  const tbody = document.getElementById("cuerpo-tabla-roles");
  const selectRol = document.getElementById("select-usuario-rol");
  const editSelectRol = document.getElementById("edit-rolId");
  const badgeTotal = document.getElementById("badge-total-roles");
  const statRoles = document.getElementById("stat-roles");

  try {
    const res = await fetch("/api/roles");
    const json = await res.json();
    const roles = json.data || [];
    listaRolesGlobal = roles;

    badgeTotal.textContent = `${roles.length} roles`;
    statRoles.textContent = roles.length;

    // Actualizar Selects
    let opciones = '<option value="">Seleccione un rol...</option>';
    roles.forEach((r) => {
      opciones += `<option value="${r.id}">${r.nombre}</option>`;
    });
    selectRol.innerHTML = opciones;
    if (editSelectRol) editSelectRol.innerHTML = opciones;

    // Actualizar Tabla
    if (roles.length === 0) {
      tbody.innerHTML = `<tr><td colspan="3" class="text-center text-muted">No hay roles registrados aún.</td></tr>`;
      return;
    }

    tbody.innerHTML = roles
      .map(
        (r) => `
      <tr data-rol-id="${r.id}">
        <td><strong>#${r.id}</strong></td>
        <td><span class="badge badge-role">${r.nombre}</span></td>
        <td class="text-center">
          <button class="btn-danger-sm" onclick="eliminarRol(${r.id}, '${r.nombre}')" title="Eliminar rol">
            Eliminar
          </button>
        </td>
      </tr>
    `
      )
      .join("");
  } catch (error) {
    tbody.innerHTML = `<tr><td colspan="3" class="text-center text-muted">Error al cargar roles: ${error.message}</td></tr>`;
  }
}

async function crearNuevoRol(event) {
  event.preventDefault();
  const input = document.getElementById("input-rol-nombre");
  const nombre = input.value.trim();

  if (!nombre) return;

  try {
    const res = await fetch("/api/roles", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ nombre })
    });
    const json = await res.json();

    if (!res.ok) {
      throw new Error(json.message || "Error al crear rol");
    }

    input.value = "";
    mostrarToast("Rol creado exitosamente", "success");
    await cargarRoles();
  } catch (error) {
    mostrarToast(error.message, "error");
  }
}

async function eliminarRol(id, nombre) {
  if (!confirm(`¿Deseas eliminar el rol "${nombre}" (ID: ${id})?`)) return;

  try {
    const res = await fetch(`/api/roles/${id}`, { method: "DELETE" });
    const json = await res.json();

    if (!res.ok) {
      throw new Error(json.message || "Error al eliminar rol");
    }

    mostrarToast("Rol eliminado con éxito", "success");
    await cargarRoles();
  } catch (error) {
    mostrarToast(error.message, "error");
  }
}

// ==========================================
// 3. GESTIÓN DE USUARIOS
// ==========================================
async function cargarUsuarios() {
  const tbody = document.getElementById("cuerpo-tabla-usuarios");
  const statUsuarios = document.getElementById("stat-usuarios");

  try {
    const res = await fetch("/api/usuarios");
    const json = await res.json();
    const usuarios = json.data || [];
    listaUsuariosGlobal = usuarios;

    statUsuarios.textContent = usuarios.length;
    renderizarTablaUsuarios(usuarios);
  } catch (error) {
    tbody.innerHTML = `<tr><td colspan="6" class="text-center text-muted">Error al cargar usuarios: ${error.message}</td></tr>`;
  }
}

function renderizarTablaUsuarios(usuarios) {
  const tbody = document.getElementById("cuerpo-tabla-usuarios");

  if (!usuarios || usuarios.length === 0) {
    tbody.innerHTML = `<tr><td colspan="6" class="text-center text-muted">No hay usuarios registrados en la base de datos.</td></tr>`;
    return;
  }

  tbody.innerHTML = usuarios
    .map((u) => {
      const nombreRol = u.rol ? u.rol.nombre : "Sin Rol";
      const fecha = u.createdAt ? new Date(u.createdAt).toLocaleDateString() : "--";
      return `
      <tr data-usuario-id="${u.id}">
        <td><strong>#${u.id}</strong></td>
        <td><strong class="user-name">${u.nombre}</strong></td>
        <td><code>${u.correo}</code></td>
        <td><span class="badge badge-role">${nombreRol}</span></td>
        <td><small class="text-muted">${fecha}</small></td>
        <td class="text-center">
          <button class="btn-edit-sm" onclick="abrirModalEdicion(${u.id})">Editar</button>
          <button class="btn-danger-sm" onclick="eliminarUsuario(${u.id}, '${u.nombre}')">Eliminar</button>
        </td>
      </tr>
    `;
    })
    .join("");
}

function filtrarUsuarios(query) {
  const q = query.toLowerCase().trim();
  if (!q) {
    renderizarTablaUsuarios(listaUsuariosGlobal);
    return;
  }
  const filtrados = listaUsuariosGlobal.filter(
    (u) => u.nombre.toLowerCase().includes(q) || u.correo.toLowerCase().includes(q)
  );
  renderizarTablaUsuarios(filtrados);
}

async function crearNuevoUsuario(event) {
  event.preventDefault();
  const nombre = document.getElementById("input-usuario-nombre").value.trim();
  const correo = document.getElementById("input-usuario-correo").value.trim();
  const password = document.getElementById("input-usuario-password").value.trim();
  const confirmInput = document.getElementById("input-usuario-confirm-password");
  const confirmPassword = confirmInput ? confirmInput.value.trim() : password;
  const rolId = parseInt(document.getElementById("select-usuario-rol").value, 10);

  if (!nombre || !correo || !password || !rolId) {
    mostrarToast("Por favor llena todos los campos", "error");
    return;
  }

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(correo)) {
    mostrarToast("El correo electrónico no tiene un formato válido (debe incluir @ y dominio)", "error");
    return;
  }

  const dominiosPermitidos = ["gmail.com", "uteq.edu.mx", "hotmail.com", "outlook.com", "empresa.com", "test.com"];
  const partesCorreo = correo.split("@");
  const dominio = partesCorreo[partesCorreo.length - 1].toLowerCase();
  if (!dominiosPermitidos.includes(dominio)) {
    mostrarToast(`Dominio @${dominio} no permitido. Dominios autorizados: gmail.com, uteq.edu.mx, hotmail.com, outlook.com`, "error");
    return;
  }

  if (password.length < 8) {
    mostrarToast("La contraseña debe tener al menos 8 caracteres", "error");
    return;
  }

  if (!/[#$@!%*?&_\-]/.test(password)) {
    mostrarToast("La contraseña debe incluir al menos un carácter especial (#, $, @, !, %, *, &, _)", "error");
    return;
  }

  if (confirmPassword !== password) {
    mostrarToast("Las contraseñas no coinciden. Deben ser idénticas", "error");
    return;
  }

  try {
    const res = await fetch("/api/usuarios", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ nombre, correo, password, confirmPassword, rolId })
    });
    const json = await res.json();

    if (!res.ok) {
      throw new Error(json.message || "Error al registrar usuario");
    }

    document.getElementById("form-usuario").reset();
    mostrarToast("Usuario registrado con éxito", "success");
    await cargarUsuarios();
  } catch (error) {
    mostrarToast(error.message, "error");
  }
}

async function sembrarDatosFicticios() {
  try {
    mostrarToast("Cargando usuarios y roles iniciales...", "success");
    const res = await fetch("/api/database/seed", { method: "POST" });
    const json = await res.json();
    if (!res.ok) throw new Error(json.message || "Error al sembrar");
    mostrarToast("Datos ficticios cargados con éxito", "success");
    await cargarTodo();
  } catch (error) {
    mostrarToast(error.message, "error");
  }
}

function abrirModalEdicion(id) {
  const u = listaUsuariosGlobal.find((item) => item.id === id);
  if (!u) return;

  document.getElementById("edit-id").value = u.id;
  document.getElementById("edit-nombre").value = u.nombre;
  document.getElementById("edit-correo").value = u.correo;
  document.getElementById("edit-rolId").value = u.rolId || (u.rol ? u.rol.id : "");
  document.getElementById("edit-password").value = "";

  document.getElementById("modal-editar").classList.remove("hidden");
}

function cerrarModalEdicion() {
  document.getElementById("modal-editar").classList.add("hidden");
}

async function guardarEdicionUsuario(event) {
  event.preventDefault();
  const id = document.getElementById("edit-id").value;
  const nombre = document.getElementById("edit-nombre").value.trim();
  const correo = document.getElementById("edit-correo").value.trim();
  const rolId = parseInt(document.getElementById("edit-rolId").value, 10);
  const password = document.getElementById("edit-password").value.trim();

  const payload = { nombre, correo, rolId };
  if (password) payload.password = password;

  try {
    const res = await fetch(`/api/usuarios/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    const json = await res.json();

    if (!res.ok) {
      throw new Error(json.message || "Error al actualizar usuario");
    }

    cerrarModalEdicion();
    mostrarToast("Usuario actualizado con éxito", "success");
    await cargarUsuarios();
  } catch (error) {
    mostrarToast(error.message, "error");
  }
}

async function eliminarUsuario(id, nombre) {
  if (!confirm(`¿Estás seguro de eliminar al usuario "${nombre}" (ID: ${id})?`)) return;

  try {
    const res = await fetch(`/api/usuarios/${id}`, { method: "DELETE" });
    const json = await res.json();

    if (!res.ok) {
      throw new Error(json.message || "Error al eliminar usuario");
    }

    mostrarToast("Usuario eliminado con éxito", "success");
    await cargarUsuarios();
  } catch (error) {
    mostrarToast(error.message, "error");
  }
}

// ==========================================
// 4. MANTENIMIENTO Y RESPALDOS
// ==========================================
async function descargarBackup() {
  try {
    mostrarToast("Generando respaldo de base de datos...", "success");
    const res = await fetch("/api/database/backup", { method: "POST" });
    if (!res.ok) throw new Error("No se pudo generar el respaldo");

    const blob = await res.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `backup-${new Date().toISOString().slice(0, 10)}.sqlite`;
    document.body.appendChild(a);
    a.click();
    a.remove();
    window.URL.revokeObjectURL(url);
    mostrarToast("Respaldo descargado exitosamente", "success");
  } catch (error) {
    mostrarToast(error.message, "error");
  }
}

async function confirmarVaciarBD() {
  const confirmacion = prompt("Escribe 'VACIAR' para confirmar el borrado total de las tablas:");
  if (confirmacion !== "VACIAR") {
    if (confirmacion !== null) mostrarToast("Operación cancelada: palabra incorrecta", "error");
    return;
  }

  try {
    const res = await fetch("/api/database/vaciar", { method: "DELETE" });
    const json = await res.json();

    if (!res.ok) throw new Error(json.message || "Error al vaciar BD");

    mostrarToast("Base de datos vaciada", "success");
    await cargarTodo();
  } catch (error) {
    mostrarToast(error.message, "error");
  }
}

// ==========================================
// 5. UTILIDAD TOAST
// ==========================================
function mostrarToast(mensaje, tipo = "success") {
  const toast = document.getElementById("toast");
  toast.textContent = mensaje;
  toast.className = `toast ${tipo}`;
  toast.classList.remove("hidden");

  setTimeout(() => {
    toast.classList.add("hidden");
  }, 3500);
}
