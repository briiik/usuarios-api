const app = require("./app"); // (Ojo aquí dependiendo de dónde esté ubicado tu server.js con respecto a src)

app.iniciarServidor().catch((error) => {
  console.error("Fallo crítico al iniciar el servidor:", error);
  process.exit(1);
});