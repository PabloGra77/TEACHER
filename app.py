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

# --- ESTILOS VISUALES (TEXTO DE TARJETAS NEGRO) ---
st.markdown(f"""
    <style>
    [data-testid="stAppViewContainer"] {{ background-color: #36454F; color: white; }}
    [data-testid="stSidebar"] {{ background-color: #2F4F4F; color: white; }}
    .resource-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(100px, 1fr)); gap: 15px; padding: 20px; justify-items: center; }}
    .tile {{ display: flex; flex-direction: column; align-items: center; justify-content: center; width: 100px; height: 100px; border-radius: 15px; text-decoration: none; font-weight: bold; font-size: 12px; text-align: center; transition: transform 0.2s; box-shadow: 3px 3px 10px rgba(0,0,0,0.4); }}
    .tile:hover {{ transform: scale(1.1); box-shadow: 0px 0px 15px yellow; z-index: 10; }}
    .tile div {{ color: black; }} /* TEXTO NEGRO FIJO */
    .bg-green {{ background-color: #4CAF50; }} .bg-red {{ background-color: #E53935; }}
    .bg-blue {{ background-color: #2196F3; }} .bg-orange {{ background-color: #FF9800; }} .bg-purple {{ background-color: #9C27B0; }}
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
            save_profile(st.session_state['profile'])
            st.success("Perfil actualizado."); st.rerun()

def presentation_manager():
    st.header("🖼️ Subir y Gestionar Presentaciones")
    st.info("Sube tus archivos PDF o PPTX. Los PDFs se proyectarán directamente; los PPTX se descargarán.")
    
    uploaded_file = st.file_uploader("Archivo (PDF o PPTX):", type=['pdf', 'pptx', 'ppt'])
    
    if uploaded_file is not None:
        file_ext = Path(uploaded_file.name).suffix.lower()
        file_name = f"{Path(uploaded_file.name).stem}-{os.urandom(4).hex()}{file_ext}" # Nombre único
        file_path = Path(UPLOAD_DIR) / file_name
        
        with open(file_path, "wb") as f: f.write(uploaded_file.getbuffer())
        st.success(f"Archivo '{uploaded_file.name}' guardado.")
        
        with st.form("add_file_res"):
            st.subheader("Añadir como Botón")
            c1, c2 = st.columns(2)
            name = c1.text_input("Título de la Tarjeta", value=Path(uploaded_file.name).stem)
            icon = c2.text_input("Icono", value="🎥" if file_ext == '.pdf' else "🗃️")
            color = st.selectbox("Color", ["bg-orange","bg-purple","bg-blue"])
            
            if st.form_submit_button("Añadir Botón al Aula"):
                link_type = 'local_pdf' if file_ext == '.pdf' else 'local_download'
                
                new_resource = {"name": name, "icon": icon, "color": color, "link_type": link_type, "link": str(file_path)}
                st.session_state['recursos'].append(new_resource)
                save_data(st.session_state['recursos'])
                st.success("Botón añadido."); st.rerun()

    st.markdown("---")
    st.subheader("🧹 Gestionar Botones Existentes")
    if st.session_state['recursos']:
        if st.button("Borrar ÚLTIMO botón añadido"):
            last_res = st.session_state['recursos'].pop()
            if last_res.get('link_type') in ['local_pdf', 'local_download']:
                try: Path(last_res['link']).unlink()
                except FileNotFoundError: pass
                
            save_data(st.session_state['recursos'])
            st.warning(f"Botón '{last_res['name']}' y archivo asociado borrados.")
            st.rerun()

# --- VISTA PÚBLICA (ALUMNOS) ---
def public_view():
    st.markdown("<h1 style='text-align: center; color: #FFFF99;'>🧩 Zona de Aprendizaje</h1>", unsafe_allow_html=True)
    st.markdown("""<div style="display:flex;justify-content:center;margin-bottom:20px;"><input style="padding:10px;border-radius:20px;border:none;width:50%;text-align:center;" placeholder="🔍 Busca aquí..."></div>""", unsafe_allow_html=True)

    grid_html = '<div class="resource-grid">'
    for idx, res in enumerate(st.session_state['recursos']):
        form_key = f"tile_form_{idx}"
        with st.form(form_key, clear_on_submit=False):
            tile_html = f"""
            <a href='javascript:void(0);' class="tile {res['color']}">
                <div style="font-size: 30px;">{res['icon']}</div>
                <div>{res['name']}</div>
            </a>
            """
            st.markdown(tile_html, unsafe_allow_html=True)
            
            if st.form_submit_button("Abrir", help="Abrir recurso", use_container_width=True):
                if res.get('link_type') == 'local_pdf':
                    st.session_state['view_file'] = res['link']
                elif res.get('link_type') == 'local_download':
                    st.download_button(
                        label="Descargar", 
                        data=Path(res['link']).read_bytes(), 
                        file_name=Path(res['link']).name,
                        mime="application/octet-stream",
                        key=f"dl_{form_key}"
                    )
                    st.info("Archivo listo para descargar. Clic en el botón azul de descarga.")
            
    st.markdown("</div>", unsafe_allow_html=True)


# --- ROUTER PRINCIPAL ---

# Lógica del Sidebar (Restaurada)
with st.sidebar:
    st.image(st.session_state['profile']['photo_url'], width=100)
    st.markdown(f"### {st.session_state['profile']['name']}")
    st.markdown(f"**Materia:** {st.session_state['profile']['subject']}")
    st.markdown("---") # Separador para el login

    if not st.session_state['logged_in']:
        # Restaurar la sección de Login para que se vea
        with st.expander("🔑 Ingreso Docente"):
            u = st.text_input("Usuario", key='login_user'); p = st.text_input("Contraseña", type="password", key='login_pass')
            if st.button("Entrar", key='login_btn'):
                if u == ADMIN_USER and p == ADMIN_PASS:
                    st.session_state['logged_in'] = True; st.rerun()
                else:
                    st.error("Credenciales incorrectas.")
    else:
        # Si está logueado, mostrar el botón de salir
        if st.button("Cerrar Sesión"): st.session_state['logged_in'] = False; st.rerun()

# Lógica de Vistas (Router)
if st.session_state['logged_in']:
    tab1, tab2 = st.tabs(["📝 Perfil", "🖼️ Presentaciones"])
    with tab1: profile_editor()
    with tab2: presentation_manager()
else:
    # Si no está logueado, verifica si debe mostrar el visor de PDF
    if st.session_state.get('view_file'):
        file_path = Path(st.session_state['view_file'])
        if file_path.exists():
            st.header(f"Proyectando: {file_path.name}")
            display_pdf(file_path)
            if st.button("Volver al Aula"):
                st.session_state['view_file'] = None
                st.rerun()
        else:
            st.error("Archivo no encontrado.")
            st.session_state['view_file'] = None 
            public_view()
    else:
        # Muestra la vista pública normal con los botones
        public_view()
