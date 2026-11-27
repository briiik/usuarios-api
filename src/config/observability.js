// src/config/observability.js - Instrumentación de Observabilidad (Logs, Métricas y Trazas)
const http = require("http");
const https = require("https");

const OPENOBSERVE_ENDPOINT = process.env.OPENOBSERVE_ENDPOINT || "";
const OPENOBSERVE_ORG = process.env.OPENOBSERVE_ORG || "default";
const OPENOBSERVE_STREAM = process.env.OPENOBSERVE_STREAM || "app_telemetry";
const OPENOBSERVE_AUTH = process.env.OPENOBSERVE_AUTH || "";

/**
 * Envío asíncrono no bloqueante de eventos a OpenObserve
 */
function enviarAOpenObserve(datos) {
  if (!OPENOBSERVE_ENDPOINT || !OPENOBSERVE_AUTH) return;

  try {
    const url = new URL(`${OPENOBSERVE_ENDPOINT}/api/${OPENOBSERVE_ORG}/${OPENOBSERVE_STREAM}/_json`);
    const payload = JSON.stringify(Array.isArray(datos) ? datos : [datos]);
    const esHttps = url.protocol === "https:";
    const cliente = esHttps ? https : http;

    const req = cliente.request(
      url,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": OPENOBSERVE_AUTH.startsWith("Basic ") ? OPENOBSERVE_AUTH : `Basic ${OPENOBSERVE_AUTH}`,
          "Content-Length": Buffer.byteLength(payload)
        },
        timeout: 2500
      },
      (res) => {
        res.resume(); // Consumir respuesta para liberar memoria
      }
    );

    req.on("error", () => {
      // Silenciar errores de red hacia observabilidad para no interrumpir la API
    });

    req.write(payload);
    req.end();
  } catch (err) {
    // Silencioso
  }
}

/**
 * Middleware de telemetría HTTP: registra latencia, códigos de estado, timestamp y métricas
 */
function observabilityMiddleware(req, res, next) {
  const inicio = process.hrtime();

  res.on("finish", () => {
    const diff = process.hrtime(inicio);
    const duracionMs = Number((diff[0] * 1e3 + diff[1] * 1e-6).toFixed(2));

    const registro = {
      tipo: "HTTP_REQUEST",
      metodo: req.method,
      ruta: req.originalUrl || req.url,
      statusCode: res.statusCode,
      latenciaMs: duracionMs,
      ip: req.ip || req.socket.remoteAddress || "127.0.0.1",
      timestamp: new Date().toISOString(),
      servicio: "usuarios-api",
      entorno: process.env.NODE_ENV || "development"
    };

    // Imprimir log estructurado (recolectable por Docker y OpenObserve)
    if (process.env.NODE_ENV !== "test") {
      console.log(JSON.stringify(registro));
    }

    // Enviar a OpenObserve en background
    enviarAOpenObserve(registro);
  });

  next();
}

module.exports = {
  observabilityMiddleware,
  enviarAOpenObserve
};
