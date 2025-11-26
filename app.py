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

# --- ESTILOS VISUALES (Mantenemos ocultamiento) ---
st.markdown(f"""
    <style>
    [data-testid="stAppViewContainer"] {{ background-color: #36454F; color: white; }}
    [data-testid="stSidebar"] {{ background-color: #2F4F4F; color: white; }}
    .resource-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(100px, 1fr)); gap: 15px; padding: 20px; justify-items: center; }}
    
    .tile-wrapper {{ position: relative; width: 100px; height: 100px; }}
    .tile-container {{ width: 100%; height: 100%; border-radius: 15px; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; font-weight: bold; font-size: 12px; transition: transform 0.2s; box-shadow: 3px 3px 10px rgba(0,0,0,0.4); cursor: pointer; position: relative; z-index: 1; }}
    .tile-container:hover {{ transform: scale(1.05); box-shadow: 0px 0px 15px yellow; }}
    .tile-container div {{ color: black; }} 
    .bg-green {{ background-color: #4CAF50; }} .bg-red {{ background-color: #E53935; }} .bg-blue {{ background-color: #2196F3; }} .bg-orange {{ background-color: #FF9800; }} .bg-purple {{ background-color: #9C27B0; }}

    /* OCULTAMIENTO TOTAL DEL BOTÓN Y ESPACIO */
    .tile-wrapper .stButton {{
        position: absolute; 
        top: 0;
        left: 0;
        width: 100%; 
        height: 100%;
        margin: 0 !important;
        padding: 0 !important;
        z-index: 2; 
    }}
    .tile-wrapper .stButton>button {{
        width: 100% !important;
        height: 100% !important;
        opacity: 0 !important; 
        cursor: pointer;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- VISOR DE PDF (ELIMINADO Y REEMPLAZADO POR DESCARGA) ---
# Se elimina la función display_pdf ya que no funciona de forma estable.

# --- VISTAS DEL PANEL ADMIN (Sin cambios) ---
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
    st.info("Sube archivos PDF. **El archivo se descargará directamente** para que pueda ser proyectado en el dispositivo del usuario.")
    
    uploaded_file = st.file_uploader("Archivo (SOLO PDF):", type=['pdf'])
    
    if uploaded_file is not None:
        file_ext = Path(uploaded_file.name).suffix.lower()
        file_name = f"{Path(uploaded_file.name).stem}-{os.urandom(4).hex()}{file_ext}"
        file_path = Path(UPLOAD_DIR) / file_name
        
        with open(file_path, "wb") as f: f.write(uploaded_file.getbuffer())
        st.success(f"Archivo '{uploaded_file.name}' guardado.")
        
        with st.form("add_file_res"):
            st.subheader("Añadir como Botón")
            c1, c2 = st.columns(2)
            name = c1.text_input("Título de la Tarjeta", value=Path(uploaded_file.name).stem)
            icon = c2.text_input("Icono", value="💾")
            color = st.selectbox("Color", ["bg-orange","bg-purple","bg-blue"])
            
            if st.form_submit_button("Añadir Botón al Aula"):
                # Ahora link_type 'local_download' para todos los archivos subidos
                new_resource = {"name": name, "icon": icon, "color": color, "link_type": 'local_download', "link": str(file_path)}
                st.session_state['recursos'].append(new_resource)
                save_data(st.session_state['recursos']); st.success("Botón añadido."); st.rerun()

    st.markdown("---")
    st.subheader("🧹 Gestionar Botones Existentes")
    if st.session_state['recursos']:
        if st.button("Borrar ÚLTIMO botón añadido"):
            last_res = st.session_state['recursos'].pop()
            if last_res.get('link_type') == 'local_download':
                try: Path(last_res['link']).unlink()
                except FileNotFoundError: pass
                
            save_data(st.session_state['recursos']); st.warning(f"Botón '{last_res['name']}' y archivo asociado borrados.")
            st.rerun()

# --- VISTA PÚBLICA (ALUMNOS) ---
def public_view():
    st.markdown("<h1 style='text-align: center; color: #FFFF99;'>🧩 Zona de Aprendizaje</h1>", unsafe_allow_html=True)
    st.markdown("""<div style="display:flex;justify-content:center;margin-bottom:20px;"><input style="padding:10px;border-radius:20px;border-none;width:50%;text-align:center;" placeholder="🔍 Busca aquí..."></div>""", unsafe_allow_html=True)

    grid_html = '<div class="resource-grid">'
    st.markdown(grid_html, unsafe_allow_html=True) 

    cols = st.columns(len(st.session_state['recursos']))

    for idx, res in enumerate(st.session_state['recursos']):
        with cols[idx]:
            # Contenedor para manejar la superposición
            st.markdown('<div class="tile-wrapper">', unsafe_allow_html=True)
            
            # 1. Contenedor visual (la tarjeta)
            tile_html = f"""
            <div class="tile-container {res['color']}">
                <div style="font-size: 30px;">{res['icon']}</div>
                <div>{res['name']}</div>
            </div>
            """
            st.markdown(tile_html, unsafe_allow_html=True)
            
            # 2. Botón invisible de Streamlit para detectar el click
            clicked = st.button("Abrir", key=f"btn_tile_{idx}", help=f"Abrir {res['name']}", use_container_width=True)
            
            st.markdown('</div>', unsafe_allow_html=True) # Cierra el contenedor wrapper

            if clicked:
                if res.get('link_type') == 'local_download':
                    # Lee el archivo y lo sirve para descarga
                    file_path = Path(res['link'])
                    if file_path.exists():
                        st.download_button(
                            label=f"Descargar {res['name']} 💾", 
                            data=file_path.read_bytes(), 
                            file_name=file_path.name,
                            mime="application/octet-stream",
                            key=f"dl_final_{idx}"
                        )
                        st.info("La descarga comenzará automáticamente.")
                    else:
                        st.error("El archivo no existe en el servidor. Contacte al administrador.")
                else:
                    st.error("Recurso no proyectable. El archivo se debe descargar.")

# --- ROUTER PRINCIPAL (Sin cambios) ---
# Lógica del Sidebar
with st.sidebar:
    st.image(st.session_state['profile']['photo_url'], width=100)
    st.markdown(f"### {st.session_state['profile']['name']}")
    st.markdown(f"**Materia:** {st.session_state['profile']['subject']}")
    st.markdown("---") 

    if not st.session_state['logged_in']:
        with st.expander("🔑 Ingreso Docente"):
            u = st.text_input("Usuario", key='login_user'); p = st.text_input("Contraseña", type="password", key='login_pass')
            if st.button("Entrar", key='login_btn'):
                if u == ADMIN_USER and p == ADMIN_PASS:
                    st.session_state['logged_in'] = True; st.rerun()
                else:
                    st.error("Credenciales incorrectas.")
    else:
        if st.button("Cerrar Sesión"): st.session_state['logged_in'] = False; st.rerun()

# Lógica de Vistas (Router)
if st.session_state['logged_in']:
    tab1, tab2 = st.tabs(["📝 Perfil", "🖼️ Presentaciones"])
    with tab1: profile_editor()
    with tab2: presentation_manager()
else:
    # Mostramos solo la vista pública. El visor fue eliminado por inestabilidad.
    public_view()
