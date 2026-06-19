import streamlit as st

# 1. CONFIGURACIÓN DE LA INTERFAZ ORIGINAL (DISEÑO ESTILIZADO)
st.set_page_config(page_title="Simulador Clínico Híbrido 2.0", layout="wide")

st.title("🤖 Simulador Clínico Híbrido 2.0")
st.subheader("Panel de Control Docente e Interfaz del Alumno")

# Formulario original para el docente
with st.expander("🛠️ Configuración del Caso Clínico (Docente)", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        nombre = st.text_input("Nombre del Paciente Virtual:", value="Carlos Gómez")
        edad = st.number_input("Edad:", value=28)
        genero = st.selectbox("Género:", ["Masculino", "Femenino", "Otro"])
    with col2:
        ansiedad = st.select_slider("Nivel de Ansiedad:", options=["Bajo", "Moderado", "Crítico"], value="Crítico")
        disnea = st.slider("Dificultad Respiratoria (%):", 0, 100, 85)

# Signos vitales originales
st.markdown("### 📊 Signos Vitales Iniciales")
col_sv1, col_sv2, col_sv3, col_sv4 = st.columns(4)
fc = col_sv1.number_input("FC (lpm):", value=115)
fr = col_sv2.number_input("FR (rpm):", value=28)
ta = col_sv3.text_input("Presión Arterial (mmHg):", value="140/90")
sat = col_sv4.number_input("Saturación Oxígeno (%):", value=88)

# Instrucciones del sistema clínicas
instruccion_sistema = (
    f"Actúa estrictamente como un paciente llamado {nombre} de {edad} años, género {genero}. "
    f"Tienes un nivel de ansiedad {ansiedad} y una dificultad respiratoria del {disnea}%. "
    f"Tus signos vitales iniciales son: FC {fc} lpm, FR {fr} rpm, TA {ta}, Saturación {sat}%. "
    "Habla con frases muy cortas (máximo 4 palabras), simula que te falta el aire y estás asustado. "
    "No uses lenguaje médico. Si te ponen oxígeno o te dan salbutamol, empieza a mejorar tu respiración gradualmente."
)

# 2. INTERFAZ DEL ALUMNO (ORIGINAL)
st.markdown("---")
st.header("🎙️ Interfaz del Alumno: Simulación de Voz Live")
st.write("Presiona 'Iniciar Paciente Virtual' para activar el micrófono e iniciar el interrogatorio clínico.")

api_key_env = st.secrets["GEMINI_API_KEY"]

col_audio_1, col_audio_2 = st.columns([1, 2])
with col_audio_1:
    conectar_voz = st.button("▶️ Iniciar Paciente Virtual", use_container_width=True)
with col_audio_2:
    status_placeholder = st.empty()
    status_placeholder.info("🔌 Sistema listo. Esperando inicio del alumno...")

if conectar_voz:
    status_placeholder.success("🟢 Modo Híbrido Activo - Conectando canales de audio...")
    
    # Pasamos la instrucción usando un div invisible para evitar romper las llaves de JavaScript con Python
    st.markdown(f'<div id="prompt-clinico" style="display:none;">{instruccion_sistema}</div>', unsafe_allow_html=True)
    st.markdown(f'<div id="api-key-hidden" style="display:none;">{api_key_env}</div>', unsafe_allow_html=True)
    
    # Inyección de código limpio. No usa f-strings de Python, eliminando errores de llaves simples/dobles.
    st.components.v1.html("""
        <div style="background-color: #f8fafc; padding: 15px; border-radius: 8px; border: 1px solid #e2e8f0; text-align: center; font-family: sans-serif;">
            <p style="color: #0f172a; margin: 0 0 5px 0;">🎙️ <strong>Canal de Voz Conectado Exitosamente</strong></p>
            <p style="font-size: 13px; color: #64748b; margin: 0;">El simulador está escuchando e interactuando de forma bidireccional.</p>
        </div>
        
        <script>
            const API_KEY = document.parentWindow ? null : window.parent.document.getElementById('api-key-hidden').innerText;
            const PROMPT = document.parentWindow ? null : window.parent.document.getElementById('prompt-clinico').innerText;
            
            const HOST = "generativelanguage.googleapis.com";
            const PATH = "/ws/google.ai.generativelanguage.v1alpha.GenerativeService.BidiGenerateContent?key=" + API_KEY;
            
            const ws = new WebSocket("wss://" + HOST + PATH);
            let audioCtx;
            
            function abrirSalidaAudio() {
                audioCtx = new (window.AudioContext || window.webkitAudioContext)({ sampleRate: 24000 });
            }

            ws.onopen = () => {
                abrirSalidaAudio();
                const setup = {
                    setup: {
                        model: "models/gemini-2.0-flash-exp",
                        generationConfig: {
                            responseModalities: ["AUDIO"],
                            speechConfig: {
                                voiceConfig: { prebuiltVoiceConfig: { voiceName: "Puck" } }
                            }
                        },
                        systemInstruction: {
                            parts: [{ text: PROMPT }]
                        }
                    }
                };
                ws.send(JSON.stringify(setup));
                activarMicrofono();
            };

            async function activarMicrofono() {
                try {
                    const stream = await navigator.mediaDevices.getUserMedia({ audio: { channelCount: 1, sampleRate: 16000 } });
                    const micCtx = new AudioContext({ sampleRate: 16000 });
                    const source = micCtx.createMediaStreamSource(stream);
                    const processor = micCtx.createScriptProcessor(2048, 1, 1);

                    processor.onaudioprocess = (e) => {
                        const input = e.inputBuffer.getChannelData(0);
                        const pcm = new Int16Array(input.length);
                        for (let i = 0; i < input.length; i++) {
                            pcm[i] = Math.max(-1, Math.min(1, input[i])) * 0x7FFF;
                        }
                        const base64Audio = btoa(String.fromCharCode(...new Uint8Array(pcm.buffer)));
                        
                        if (ws.readyState === WebSocket.OPEN) {
                            ws.send(JSON.stringify({
                                realtimeInput: { mediaChunks: [{ mimeType: "audio/pcm", data: base64Audio }] }
                            }));
                        }
                    };
                    source.connect(processor);
                    processor.connect(micCtx.destination);
                } catch (err) {
                    console.error("Error al acceder al micrófono:", err);
                }
            }

            ws.onmessage = async (event) => {
                const msg = JSON.parse(event.data);
                if (msg.serverContent && msg.serverContent.modelTurn) {
                    const parts = msg.serverContent.modelTurn.parts;
                    for (const part of parts) {
                        if (part.inlineData && part.inlineData.mimeType.startsWith("audio/pcm")) {
                            const raw = atob(part.inlineData.data);
                            const array = new Uint8Array(raw.length);
                            for(let i=0; i<raw.length; i++) { array[i] = raw.charCodeAt(i); }
                            const pcm16 = new Int16Array(array.buffer);
                            
                            const float32 = new Float32Array(pcm16.length);
                            for(let i=0; i<pcm16.length; i++) { float32[i] = pcm16[i] / 0x7FFF; }
                            
                            const audioBuffer = audioCtx.createBuffer(1, float32.length, 24000);
                            audioBuffer.getChannelData(0).set(float32);
                            const bufferSource = audioCtx.createBufferSource();
                            bufferSource.buffer = audioBuffer;
                            bufferSource.connect(audioCtx.destination);
                            bufferSource.start();
                        }
                    }
                }
            };
        </script>
    """, height=100)