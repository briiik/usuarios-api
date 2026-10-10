const app = require("./app");

app.iniciarServidor().catch((error) => {
  console.error("Fallo crítico al iniciar el servidor:", error);
  process.exit(1);
});
