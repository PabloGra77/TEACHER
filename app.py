import streamlit as st
import json
import os
from pathlib import Path
import base64 

# --- CONFIGURACIÓN Y ARCHIVOS ---
ADMIN_USER = "admin"      
ADMIN_PASS = "clave123"   
DATA_FILE = "recursos.json"
PROFILE_FILE = "profile.json"
UPLOAD_DIR = "uploaded_files" 

Path(UPLOAD_DIR).mkdir(parents=True, exist_ok=True) 

st.set_page_config(
    page_title="Aula Virtual",
    page_icon="🎓",
    layout="wide"
)

# --- GESTIÓN DE DATOS ---
def load_profile():
    if os.path.exists(PROFILE_FILE):
        with open(PROFILE_FILE, "r") as f: return json.load(f)
    return {"name": "Profesor(a) Tutor", "subject": "Educación", "photo_url": "https://cdn-icons-png.flaticon.com/512/3429/3429149.png"}
def save_profile(data):
    with open(PROFILE_FILE, "w") as f: json.dump(data, f, indent=4)
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f: return json.load(f)
    return []
def save_data(data):
    with open(DATA_FILE, "w") as f: json.dump(data, f, indent=4)

# Inicialización
if 'recursos' not in st.session_state: st.session_state['recursos'] = load_data()
if 'profile' not in st.session_state: st.session_state['profile'] = load_profile()
if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False
if 'view_file' not in st.session_state: st.session_state['view_file'] = None

# --- ESTILOS VISUALES ---
st.markdown(f"""
    <style>
    [data-testid="stAppViewContainer"] {{ background-color: #36454F; color: white; }}
    [data-testid="stSidebar"] {{ background-color: #2F4F4F; color: white; }}
    .resource-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(100px, 1fr)); gap: 15px; padding: 20px; justify-items: center; }}
    /* CONTENEDOR DE LA TARJETA */
    .tile-container {{ width: 100px; height: 100px; border-radius: 15px; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; font-weight: bold; font-size: 12px; transition: transform 0.2s; box-shadow: 3px 3px 10px rgba(0,0,0,0.4); cursor: pointer; }}
    .tile-container:hover {{ transform: scale(1.1); box-shadow: 0px 0px 15px yellow; z-index: 10; }}
    .tile-container div {{ color: black; }} /* TEXTO NEGRO FIJO */
    .bg-green {{ background-color: #4CAF50; }} .bg-red {{ background-color: #E53935; }}
    .bg-blue {{ background-color: #2196F3; }} .bg-orange {{ background-color: #FF9800; }} .bg-purple {{ background-color: #9C27B0; }}
    /* ESTILO PARA EL BOTÓN INVISIBLE */
    .stButton>button {{ visibility: hidden; height: 0; }} 
    .stButton {{ margin-top: -100px; }}
    </style>
    """, unsafe_allow_html=True)

# --- VISOR DE PDF (INCRUSTACIÓN) ---
def display_pdf(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="700px" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

# --- VISTAS DEL PANEL ADMIN ---
def profile_editor():
    st.header("✏️ Editar Perfil del Profesor(a)")
    st.markdown("---")
    with st.form("profile_form"):
        name = st.text_input("Nombre Completo", value=st.session_state['profile']['name'])
        subject = st.text_input("Materia/Asignatura", value=st.session_state['profile']['subject'])
        photo_url = st.text_input("URL de la Foto (link público)", value=st.session_state['profile']['photo_url'])
        
        if st.form_submit_button("Guardar Cambios del Perfil"):
            st.session_state['profile'].update({'name': name, 'subject': subject, 'photo_url': photo_url})
            save_profile(st.session_state['profile']); st.success("Perfil actualizado."); st.rerun()

def presentation_manager():
    st.header("🖼️ Subir Presentaciones PDF")
    st.info("Sube solo archivos **PDF** para que se puedan proyectar directamente en la página.")
    
    uploaded_file = st.file_uploader("Archivo (SOLO PDF):", type=['pdf'])
    
    if uploaded_file is not None:
        file_ext = Path(uploaded_file.name).suffix.
