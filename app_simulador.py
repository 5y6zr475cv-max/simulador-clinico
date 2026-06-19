import streamlit as st
import json
import os  # <-- CORRECCIÓN: Añadido para resolver el NameError de raíz

# Configuración de página de Streamlit
st.set_page_config(
    page_title="Simulador Clínico Híbrido 2.0 - Panel Docente",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos personalizados para un look clínico, limpio y profesional (Teal & Navy)
st.markdown("""
    <style>
    .main {
        background-color: #f8fafc;
    }
    .stApp header {
        background-color: #003366;
    }
    h1, h2, h3 {
        color: #003366;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    .clinical-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #008080;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .status-badge {
        background-color: #e2e8f0;
        padding: 5px 10px;
        border-radius: 15px;
        font-weight: bold;
        color: #003366;
    }
    </style>
""", unsafe_allow_html=True)

# TÍTULO DE LA APLICACIÓN
st.title("🩺 Simulador Clínico Híbrido 2.0")
st.subheader("Panel de Configuración de Casos Clínicos para Docentes")
st.markdown("---")

# BARRA LATERAL: Selección de Plantillas Predefinidas
with st.sidebar:
    st.header("📋 Plantillas Rápidas")
    st.write("Selecciona un caso predefinido para cargar los parámetros iniciales:")
    
    plantilla = st.selectbox(
        "Escenarios Disponibles",
        ["Vacío (Personalizado)", "Crisis Asmática Severa", "Infarto Agudo (SCASEST)", "Crisis de Ansiedad / Pánico"]
    )
    
    st.markdown("---")
    st.write("🔌 **Estado del Maniquí:**")
    st.markdown("<span class='status-badge'>🟢 Modo Híbrido Activo (Audio Vía Web)</span>", unsafe_allow_html=True)

# Inicializar variables de sesión para las plantillas
if plantilla == "Crisis Asmática Severa":
    default_nombre = "Carlos Gómez"
    default_edad = 28
    default_genero = "Masculino"
    default_motivo = "Dificultad respiratoria extrema que comenzó hace 1 hora después de barrer un almacén con polvo."
    default_ansiedad = "Crítico"
    default_disnea = 85
    default_fc = 118
    default_fr = 28
    default_ta_sis = 135
    default_ta_dia = 85
    default_sato2 = 88
    default_keyword_1 = "oxigeno"
    default_reaccion_1 = "Siente alivio en el pecho, pero sigue agitado. Su SatO2 sube a 94%."
    default_keyword_2 = "salbutamol"
    default_reaccion_2 = "La respiración mejora notablemente, disminuyen las sibilancias orales y puede hablar más corrido."
elif plantilla == "Infarto Agudo (SCASEST)":
    default_nombre = "Elena Rodríguez"
    default_edad = 62
    default_genero = "Femenino"
    default_motivo = "Dolor opresivo retroesternal de intensidad 8/10, irradiado a mandíbula y brazo izquierdo, acompañado de diaforesis."
    default_ansiedad = "Crítico"
    default_disnea = 30
    default_fc = 95
    default_fr = 18
    default_ta_sis = 150
    default_ta_dia = 95
    default_sato2 = 95
    default_keyword_1 = "aspirina"
    default_reaccion_1 = "Menciona que el dolor disminuye levemente a 6/10, pero sigue asustada."
    default_keyword_2 = "nitroglicerina"
    default_reaccion_2 = "El dolor disminuye significativamente a 3/10 y la presión arterial baja a niveles normales."
else:
    default_nombre = "Paciente Anónimo"
    default_edad = 30
    default_genero = "Masculino"
    default_motivo = ""
    default_ansiedad = "Moderado"
    default_disnea = 0
    default_fc = 80
    default_fr = 16
    default_ta_sis = 120
    default_ta_dia = 80
    default_sato2 = 98
    default_keyword_1 = ""
    default_reaccion_1 = ""
    default_keyword_2 = ""
    default_reaccion_2 = ""

# DISEÑO DE LA INTERFAZ EN DOS COLUMNAS DE CONFIGURACIÓN
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("<div class='clinical-card'><h3>👤 1. Datos del Paciente</h3></div>", unsafe_allow_html=True)
    nombre = st.text_input("Nombre Completo (Ficticio)", value=default_nombre)
    
    col_demog = st.columns(2)
    with col_demog[0]:
        edad = st.number_input("Edad (Años)", min_value=0, max_value=120, value=default_edad)
    with col_demog[1]:
        genero = st.selectbox("Género Fisiológico", ["Masculino", "Femenino", "Otro"], index=["Masculino", "Femenino", "Otro"].index(default_genero))
        
    motivo_consulta = st.text_area("Motivo de Consulta (Contexto Clínico)", value=default_motivo, placeholder="Ej: Dolor abdominal difuso que inició hace 4 horas...")

    st.markdown("<div class='clinical-card'><h3>🎭 2. Estado Emocional y Respiratorio</h3></div>", unsafe_allow_html=True)
    ansiedad = st.select_slider(
        "Nivel de Ansiedad / Miedo",
        options=["Bajo", "Moderado", "Crítico"],
        value=default_ansiedad
    )
    disnea = st.slider("Dificultad para Respirar (Disnea %)", 0, 100, default_disnea, help="A mayor porcentaje, el modelo hablará con oraciones más cortas e interrumpidas.")

with col2:
    st.markdown("<div class='clinical-card'><h3>📊 3. Signos Vitales Iniciales</h3></div>", unsafe_allow_html=True)
    
    col_vitals_1 = st.columns(2)
    with col_vitals_1[0]:
        fc = st.number_input("Frecuencia Cardíaca (lpm)", 30, 220, default_fc)
    with col_vitals_1[1]:
        fr = st.number_input("Frecuencia Respiratoria (rpm)", 8, 50, default_fr)
        
    col_vitals_2 = st.columns(3)
    with col_vitals_2[0]:
        ta_sis = st.number_input("TA Sistólica (mmHg)", 50, 250, default_ta_sis)
    with col_vitals_2[1]:
        ta_dia = st.number_input("TA Diastólica (mmHg)", 30, 150, default_ta_dia)
    with col_vitals_2[2]:
        sato2 = st.number_input("Saturación O2 (%)", 50, 100, default_sato2)

    st.markdown("<div class='clinical-card'><h3>🎯 4. Reglas de Intervención (Palabras Clave)</h3></div>", unsafe_allow_html=True)
    st.write("Define qué acciones del alumno aliviarán o alterarán el estado del paciente:")
    
    col_rule_1 = st.columns([1, 2])
    with col_rule_1[0]:
        kw1 = st.text_input("Acción / Palabra Clave 1", value=default_keyword_1, placeholder="ej. oxigeno")
    with col_rule_1[1]:
        reac1 = st.text_input("Reacción del Paciente 1", value=default_reaccion_1, placeholder="ej. Siente alivio parcial...")
        
    col_rule_2 = st.columns([1, 2])
    with col_rule_2[0]:
        kw2 = st.text_input("Acción / Palabra Clave 2", value=default_keyword_2, placeholder="ej. salbutamol")
    with col_rule_2[1]:
        reac2 = st.text_input("Reacción del Paciente 2", value=default_reaccion_2, placeholder="ej. Su respiración mejora...")

st.markdown("---")

# PROCESAMIENTO: Generación automática de las "System Instructions" de Gemini
instruccion_sistema = f"""[ROL Y CONTEXTO]
Actúa rigurosamente como un paciente de simulación clínica.
- Nombre: {nombre}
- Edad: {edad} años
- Género: {genero}
- Motivo de consulta principal: {motivo_consulta}

[ESTADO FÍSICO Y EMOCIONAL]
- Nivel de Ansiedad: {ansiedad}. Si es Crítico, tu tono de voz debe denotar pánico, miedo a morir o desesperación.
- Dificultad Respiratoria (Disnea): {disnea}%. 
  * REGLA DE VOZ: Si este valor es mayor a 50%, debes simular fatiga de manera muy marcada. Habla con frases de máximo 4 palabras. Haz pausas frecuentes usando puntos suspensivos ("...").
- Si el alumno te hace preguntas irrelevantes o largas, reacciona cansado, diciendo que no tienes aire para responder tanto.

[SIGNOS VITALES INICIALES]
Si el alumno dice explícitamente que te va a colocar o conectar a un monitor de signos vitales, describe verbalmente estos valores exactos:
- Frecuencia Cardíaca: {fc} lpm
- Frecuencia Respiratoria: {fr} rpm
- Presión Arterial: {ta_sis}/{ta_dia} mmHg
- Saturación de Oxígeno: {sato2}%

[DINÁMICA DE TRATAMIENTO (MEJORÍA)]
Debes reaccionar con cambios lógicos en tu voz y actitud solo ante los siguientes desencadenantes verbales del alumno:
"""

if kw1:
    instruccion_sistema += f"- Si detectas la acción o mención de '{kw1}': Modifica tu estado a: {reac1}. Tu dificultad respiratoria percibida disminuye a la mitad.\n"
if kw2:
    instruccion_sistema += f"- Si detectas la acción o mención de '{kw2}': Modifica tu estado a: {reac2}. Tu ansiedad pasa a ser 'Baja' y respiras de forma fluida.\n"

# VISUALIZACIÓN DEL PROMPT FINAL PARA EL DOCENTE
st.header("⚙️ Prompt Generated (System Instructions)")
st.write("Este es el texto técnico estructurado que la plataforma enviará en segundo plano a la API de Gemini:")

with st.expander("👁️ Ver instrucciones del sistema completas"):
    st.code(instruccion_sistema, language="markdown")

# SECCIÓN DE INTEGRACIÓN CON EL BLOG (EMBED DE GOOGLE SITES)
st.markdown("---")
st.header("🌐 Despliegue en Google Sites")

col_sites_1, col_sites_2 = st.columns(2)
with col_sites_1:
    st.write("""
    ### ¿Cómo usar este simulador en tu Blog de Sites?
    1. **Sube este script a la nube:** Alójalo gratis en **Streamlit Community Cloud** vinculando tu repositorio de GitHub.
    2. **Copia el enlace público:** Obtendrás una URL tipo `https://tu-simulador.streamlit.app`.
    3. **Insértalo en Google Sites:** Usa el botón de **Incorporar (Embed)** mediante URL.
    """)
with col_sites_2:
    st.info("""
    💡 **Ventaja de Streamlit:**
    Al estar embebido en Google Sites mediante un iframe, los alumnos podrán acceder a la interfaz directamente desde la web escolar y hablar con el maniquí virtual usando la laptop en el laboratorio.
    """)

# 2. INTERFAZ DEL ALUMNO (ORIGINAL)
st.markdown("---")
st.header("🎙️ Interfaz del Alumno: Simulación de Voz Live")
st.write("Presiona 'Iniciar Paciente Virtual' para activar el micrófono e iniciar el interrogatorio clínico.")

# Lectura segura de la API KEY desde los Secrets
api_key_env = st.secrets["GEMINI_API_KEY"]

col_audio_1, col_audio_2 = st.columns([1, 2])
with col_audio_1:
    conectar_voz = st.button("▶️ Iniciar Paciente Virtual", use_container_width=True)
with col_audio_2:
    status_placeholder = st.empty()
    status_placeholder.info("🔌 Sistema listo. Esperando inicio del alumno...")

if conectar_voz:
    status_placeholder.success("🟢 Modo Híbrido Activo - Conectando canales de audio...")
    
    # Estructura del cliente de audio independiente (Escapando las llaves del JS para Python)
    html_raw = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body style="margin:0; padding:0; background-color: transparent;">
    <div id="status-box" style="background-color: #f8fafc; padding: 15px; border-radius: 8px; border: 1px solid #e2e8f0; text-align: center; font-family: sans-serif;">
        <p id="status-text" style="color: #0f172a; margin: 0 0 5px 0;">⏳ <strong>Conectando con el Paciente Virtual...</strong></p>
        <p style="font-size: 13px; color: #64748b; margin: 0;">Acepta los permisos de micrófono si el navegador lo solicita.</p>
    </div>
    <script>
        const API_KEY = "{api_key_env}";
        const PROMPT = "{instruccion_sistema.replace(chr(10), ' ').replace('"', '\\"')}";
        const HOST = "generativelanguage.googleapis.com";
        const PATH = "/ws/google.ai.generativelanguage.v1alpha.GenerativeService.BidiGenerateContent?key=" + API_KEY;
        let ws; let audioCtx;
        try {{
            ws = new WebSocket("wss://" + HOST + PATH);
            ws.onopen = () => {{
                document.getElementById("status-text").innerHTML = "🟢 <strong>Paciente en línea: ¡Puedes hablar ahora!</strong>";
                audioCtx = new (window.AudioContext || window.webkitAudioContext)({{ sampleRate: 24000 }});
                const setup = {{
                    setup: {{
                        model: "models/gemini-2.0-flash-exp",
                        generationConfig: {{ responseModalities: ["AUDIO"], speechConfig: {{ voiceConfig: {{ prebuiltVoiceConfig: {{ voiceName: "Puck" }} }} }} }},
                        systemInstruction: {{ parts: [{{ text: PROMPT }}] }}
                    }}
                }};
                ws.send(JSON.stringify(setup));
                activarMicrofono();
            }};
            ws.onmessage = async (event) => {{
                const msg = JSON.parse(event.data);
                if (msg.serverContent && msg.serverContent.modelTurn) {{
                    const parts = msg.serverContent.modelTurn.parts;
                    for (const part of parts) {{
                        if (part.inlineData && part.inlineData.mimeType.startsWith("audio/pcm")) {{
                            const raw = atob(part.inlineData.data);
                            const array = new Uint8Array(raw.length);
                            for(let i=0; i<raw.length; i++) {{ array[i] = raw.charCodeAt(i); }}
                            const pcm16 = new Int16Array(array.buffer);
                            const float32 = new Float32Array(pcm16.length);
                            for(let i=0; i<pcm16.length; i++) {{ float32[i] = pcm16[i] / 0x7FFF; }}
                            const audioBuffer = audioCtx.createBuffer(1, float32.length, 24000);
                            audioBuffer.getChannelData(0).set(float32);
                            const bufferSource = audioCtx.createBufferSource();
                            bufferSource.buffer = audioBuffer;
                            bufferSource.connect(audioCtx.destination);
                            bufferSource.start();
                        }}
                    }}
                }}
            }};
            ws.onerror = () => {{ document.getElementById("status-text").innerHTML = "❌ <strong>Error de conexión con la API de Google</strong>"; }};
        }} catch(err) {{ document.getElementById("status-text").innerHTML = "❌ <strong>Error de inicialización</strong>"; }}
        async function activarMicrofono() {{
            try {{
                const stream = await navigator.mediaDevices.getUserMedia({{ audio: {{ channelCount: 1, sampleRate: 16000 }} }});
                const micCtx = new AudioContext({{ sampleRate: 16000 }});
                const source = micCtx.createMediaStreamSource(stream);
                const processor = micCtx.createScriptProcessor(2048, 1, 1);
                processor.onaudioprocess = (e) => {{
                    const input = e.inputBuffer.getChannelData(0);
                    const pcm = new Int16Array(input.length);
                    for (let i = 0; i < input.length; i++) {{ pcm[i] = Math.max(-1, Math.min(1, input[i])) * 0x7FFF; }}
                    const base64Audio = btoa(String.fromCharCode(...new Uint8Array(pcm.buffer)));
                    if (ws && ws.readyState === WebSocket.OPEN) {{
                        ws.send(JSON.stringify({{ realtimeInput: {{ mediaChunks: [{{ mimeType: "audio/pcm", data: base64Audio }}] }} }}));
                    }}
                }};
                source.connect(processor); processor.connect(micCtx.destination);
            }} catch (err) {{ document.getElementById("status-text").innerHTML = "❌ <strong>Permiso de micrófono denegado</strong>"; }}
        }}
    </script>
</body>
</html>"""

    # Guardamos el cliente de audio en el directorio estático
    static_path = "static"
    if not os.path.exists(static_path):
        os.makedirs(static_path)
        
    with open(os.path.join(static_path, "audio_client.html"), "w", encoding="utf-8") as f:
        f.write(html_raw)

    # Inyección final limpia usando el HTML nativo con permisos explícitos heredados
    st.write('<iframe src="static/audio_client.html" height="130" width="100%" allow="microphone" style="border:none;"></iframe>', unsafe_allow_html=True)
