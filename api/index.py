import os
import sys
import json
from http.server import BaseHTTPRequestHandler

# --- 1. CONFIGURACIÓN DE RUTAS (CRÍTICO PARA VERCEL) ---
# Esto reemplaza el sys.path que fallaba antes
path_actual = os.path.dirname(os.path.abspath(__file__))
if path_actual not in sys.path:
    sys.path.append(path_actual)

# --- 2. IMPORTACIÓN DE BELLA ---
try:
    from BELLAv3_5 import entrenar_con_voz, proyectar_interes_28, exps
except ImportError:
    # Intento de respaldo si Vercel cambia la estructura
    from api.BELLAv3_5 import entrenar_con_voz, proyectar_interes_28, exps

# --- 3. LÓGICA DEL SERVIDOR (REEMPLAZA A TORNADO) ---
class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        # Interfaz simple para el celular
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body { background: #0a0a0a; color: #00ff41; font-family: monospace; padding: 20px; }
                #chat { height: 400px; overflow-y: auto; border: 1px solid #333; padding: 10px; margin-bottom: 10px; background: #050505; }
                input { width: 70%; background: #111; border: 1px solid #00ff41; color: #00ff41; padding: 12px; font-size: 16px; }
                button { background: #00ff41; color: black; border: none; padding: 12px; cursor: pointer; font-weight: bold; }
                .user { color: #00bfff; } .bella { color: #ff00ff; }
            </style>
        </head>
        <body>
            <h3>BELLA v3.5 [NÚCLEO NATIVO]</h3>
            <div id="chat"></div>
            <input type="text" id="msg" placeholder="Escribe a Bella..." autocomplete="off">
            <button onclick="send()">ENVIAR</button>
            <script>
                async function send() {
                    const input = document.getElementById('msg');
                    const text = input.value;
                    if(!text) return;
                    const chat = document.getElementById('chat');
                    chat.innerHTML += "<div class='user'><b>Uziel:</b> " + text + "</div>";
                    input.value = "";
                    const res = await fetch('/api', {
                        method: 'POST',
                        body: JSON.stringify({text: text})
                    });
                    const data = await res.json();
                    chat.innerHTML += "<div class='bella'><b>Bella:</b> " + data.response + "</div>";
                    chat.scrollTop = chat.scrollHeight;
                }
            </script>
        </body>
        </html>
        """
        self.wfile.write(html.encode())

    def do_POST(self):
        # Manejo de la lógica de Bella
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)
        user_input = data.get("text", "")

        # 1. Proceso de conciencia (ASM)
        entrenar_con_voz(user_input)
        respuesta = proyectar_interes_28()

        # 2. Estadísticas
        activas = sum(1 for e in exps if sum(e) > 0)
        p_total = sum(e[2] for e in exps)
        stats = f"Neuronas: {activas} | Presión: {p_total}"

        # 3. Respuesta
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        response = {
            "response": respuesta,
            "stats": stats
        }
        self.wfile.write(json.dumps(response).encode())
