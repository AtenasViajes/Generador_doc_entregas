import streamlit as st
from fpdf import FPDF
from datetime import datetime
from zoneinfo import ZoneInfo

# --- LÓGICA DEL PDF (Intacta para impresión oficial) ---
class AtenasPDF(FPDF):
    def header(self):
        self.image('membrete.png', 0, 0, 210, 297)
        self.set_y(55)

    def footer(self):
        pass

def generar_pdf(nombre_cliente, items_seleccionados, fecha_texto):
    pdf = AtenasPDF()
    pdf.set_auto_page_break(auto=True, margin=40)
    pdf.add_page()
    
    pdf.set_text_color(12, 24, 60) 
    pdf.set_font('Helvetica', 'B', 14)
    pdf.cell(0, 10, 'FORMATO DE RECEPCION DE DOCUMENTACION', ln=True, align='C')
    pdf.ln(5)
    
    pdf.set_text_color(0, 0, 0)
    pdf.set_font('Helvetica', '', 11)
    pdf.cell(0, 7, f'Fecha: {fecha_texto}', ln=True)
    pdf.cell(0, 7, f'Titular de la reserva: {nombre_cliente}', ln=True)
    pdf.ln(8) 
    
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 10, 'Servicios y documentos entregados:', ln=True)
    pdf.set_font('Helvetica', '', 11)
    
    for item in items_seleccionados:
        pdf.cell(10, 6, '-', align='C')
        pdf.cell(0, 6, item, ln=True)
    
    pdf.ln(10)
    pdf.set_font('Helvetica', 'I', 9)
    disclaimer = (
        "Declaracion de Conformidad: Hago constar que he recibido la documentacion detallada anteriormente. "
        "Declaro tener conocimiento de que el itinerario final (tanto en sus segmentos aereos como terrestres) "
        "puede estar sujeto a modificaciones por causas ajenas a la agencia Atenas, tales como condiciones climaticas, "
        "disposiciones gubernamentales, retrasos operativos de transportistas o situaciones de fuerza mayor. "
        "Acepto los terminos de servicio y la gestion de la agencia ante dichas eventualidades. "
        "Es responsabilidad del pasajero contar con pasaporte vigente, asi como visados, vacunas y requisitos necesarios para realizar su viaje."
    )
    pdf.multi_cell(0, 5, disclaimer)
    
    pdf.ln(15)
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 10, '________________________________________', ln=True, align='C')
    pdf.cell(0, 5, 'Nombre y firma del cliente', ln=True, align='C')
    
    return bytes(pdf.output())


# ==========================================
# --- UI PREMIUM, RESPONSIVA Y MODO OSCURO ---
# ==========================================

st.set_page_config(page_title="Atenas | Recepción de Docs", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    /* Ocultar elementos de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* ☀️ MODO CLARO (Por defecto) */
    .stApp { background-color: #f4f6f9; }
    .block-container { padding-top: 2rem !important; padding-bottom: 2rem !important; max-width: 800px; }
    div[data-testid="stForm"] {
        background-color: #ffffff;
        border-radius: 20px;
        padding: 40px;
        box-shadow: 0 10px 30px rgba(12, 24, 60, 0.08);
        border: 1px solid rgba(12, 24, 60, 0.05);
    }
    .section-title {
        text-align: center; color: #0c183c; font-size: 1.1rem; font-weight: 700;
        letter-spacing: 1px; text-transform: uppercase; margin-top: 10px;
        margin-bottom: 25px; border-bottom: 1px solid #e2e8f0; padding-bottom: 15px;
    }
    .stTextInput input, .stDateInput input {
        border-radius: 8px !important; border: 1px solid #cbd5e1 !important;
        padding: 0.6rem 1rem !important; background-color: #f8fafc !important;
    }
    .stTextInput input:focus, .stDateInput input:focus {
        border-color: #0c183c !important; box-shadow: 0 0 0 2px rgba(12, 24, 60, 0.1) !important;
        background-color: #ffffff !important;
    }
    div.stButton > button {
        background-color: #0c183c; color: #ffffff !important; border: none;
        border-radius: 10px; padding: 0.8rem 2rem; font-size: 1.1rem;
        font-weight: 600; letter-spacing: 1px; width: 100%; transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(12, 24, 60, 0.2); margin-top: 10px;
    }
    div.stButton > button:hover { background-color: #1a2a5c; transform: translateY(-2px); }
    .main-subtitle {
        text-align: center; font-weight: 400; letter-spacing: 1px; 
        margin-top: -20px; margin-bottom: 30px; color: #64748b; font-size: 1.15rem;
    }

    /* 🌙 MODO OSCURO (NIGHT MODE) */
    @media (prefers-color-scheme: dark) {
        .stApp { background-color: #0b0f19 !important; }
        div[data-testid="stForm"] {
            background-color: #111827 !important;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.8) !important;
            border: 1px solid rgba(255, 255, 255, 0.05) !important;
        }
        .section-title {
            color: #f1f5f9 !important;
            border-bottom: 1px solid #334155 !important;
        }
        .main-subtitle { color: #94a3b8 !important; }
        .stTextInput input, .stDateInput input {
            background-color: #1e293b !important;
            border: 1px solid #334155 !important;
            color: #f8fafc !important;
        }
        .stTextInput input:focus, .stDateInput input:focus {
            border-color: #3b82f6 !important;
            background-color: #0f172a !important;
        }
        /* Rescatamos el texto de los checkboxes */
        .stCheckbox label p, .stCheckbox label span {
            color: #cbd5e1 !important;
        }
        /* Botón más vibrante en la oscuridad */
        div.stButton > button {
            background-color: #1e3a8a !important;
            border: 1px solid #1e3a8a !important;
        }
        div.stButton > button:hover { background-color: #2563eb !important; }
        /* MAGIA: Convertimos el logo azul a color blanco para que contraste */
        img { filter: brightness(0) invert(1); }
    }

    /* 📱 DISEÑO RESPONSIVO (MÓVILES) */
    @media (max-width: 768px) {
        .block-container { padding-top: 1.5rem !important; padding-left: 1rem !important; padding-right: 1rem !important; }
        div[data-testid="stForm"] { padding: 20px 15px !important; border-radius: 15px !important; }
        .main-subtitle { font-size: 1rem !important; margin-top: -10px !important; margin-bottom: 20px !important; }
        .section-title { font-size: 0.95rem !important; padding-bottom: 10px !important; margin-bottom: 15px !important; }
    }
    </style>
""", unsafe_allow_html=True)

# Encabezado
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    try:
        st.image("Logo_con_Marca_Registrada.png", use_container_width=True)
    except Exception as e:
        st.error("No se encontró el logo.")

st.markdown("<div class='main-subtitle'>Generador de documentos entregados</div>", unsafe_allow_html=True)

# Formulario
with st.form("generador", clear_on_submit=False):
    st.markdown("<div class='section-title'>INFORMACIÓN DEL PASAJERO</div>", unsafe_allow_html=True)
    
    col_input1, col_input2 = st.columns(2)
    with col_input1:
        nombre = st.text_input("Nombre completo del Titular")
    with col_input2:
        zona_mx = ZoneInfo("America/Mexico_City")
        fecha_actual = datetime.now(zona_mx).date()
        fecha_seleccionada = st.date_input("Fecha de emisión", fecha_actual)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>SERVICIOS INCLUIDOS</div>", unsafe_allow_html=True)
    
    opciones = [
        "Boletos de Estrella Roja", "Reserva de vuelos", "Cupón de hospedaje",
        "Cupón de traslados", "Cupón de servicios", "Cupón de tours adicionales",
        "Itinerario personalizado", "Visa, ETAs y registros de entrada",
        "Póliza de seguro de asistencia de viaje", "Kit de viaje"
    ]
    
    col_chk1, col_chk2 = st.columns(2)
    seleccionados = []
    
    for i, item in enumerate(opciones):
        if i < 5:
            with col_chk1:
                if st.checkbox(item): seleccionados.append(item)
        else:
            with col_chk2:
                if st.checkbox(item): seleccionados.append(item)
    
    st.markdown("<br>", unsafe_allow_html=True)
    submitted = st.form_submit_button("GENERAR DOCUMENTO PDF")

# Lógica
if submitted:
    if nombre and seleccionados:
        try:
            meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
            fecha_elegante = f"{fecha_seleccionada.day:02d} de {meses[fecha_seleccionada.month - 1]} de {fecha_seleccionada.year}"
            
            pdf_bytes = generar_pdf(nombre, seleccionados, fecha_elegante)
            st.success("✨ ¡Documento procesado correctamente! Listo para imprimir o enviar.")
            st.download_button(
                label="⬇️ DESCARGAR PDF OFICIAL",
                data=pdf_bytes,
                file_name=f"Recepcion_{nombre.replace(' ', '_')}.pdf",
                mime="application/pdf",
                type="primary"
            )
        except Exception as e:
            st.error(f"Hubo un error al generar el PDF: {e}")
    else:
        st.warning("⚠️ Por favor ingresa el nombre del titular y selecciona al menos un servicio.")
