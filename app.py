import streamlit as st
import json
import os
from pathlib import Path
import base64 # Para mostrar PDFs directamente

# --- CONFIGURACIÓN Y ARCHIVOS ---
ADMIN_USER = "admin"      # Tu usuario
ADMIN_PASS = "clave123"   # Tu contraseña
DATA_FILE = "recursos.json"
PROFILE_FILE = "profile.json" # Archivo para guardar tu perfil
UPLOAD_DIR = "uploaded_files" # Carpeta para guardar PPTs/PDFs

# Asegurarse de que la carpeta de subidas exista
Path(UPLOAD_DIR).mkdir(parents=True, exist_ok=True)

st.set_page_config(
    page_title="Aula Virtual",
    page_icon="🎓",
    layout="wide"
)

# --- GESTIÓN DE PERFIL ---
def load_profile():
    if os.path.exists(PROFILE_FILE):
        with open(PROFILE_FILE, "r") as f:
            return json.load(f)
    return {"name": "Profesor(a) Tutor", "subject": "Educación", "photo_url": "https://cdn-icons-png.flaticon.com/512/3429/3429149.png"}

def save_profile(data):
    with open(PROFILE_FILE, "w") as f:
        json.dump(data, f, indent=4)

# --- GESTIÓN DE RECURSOS (JSON) ---
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Inicialización de la sesión
if 'recursos' not in st.session_state: st.session_state['recursos'] = load_data()
if 'profile' not in st.session_state: st.session_state['profile'] = load_profile()
if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False
if 'current_file_viewer' not in st.session_state: st.session_state['current_file_viewer'] = None

# --- ESTILOS VISUALES (MODIFICADO: TEXTO DE TARJETAS NEGRO) ---
st.markdown(f"""
    <style>
    [data-testid="stAppViewContainer"] {{ background-color: #36454F; color: white; }}
    [data-testid="stSidebar"] {{ background-color: #2F4F4F; color: white; }}
    .resource-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(100px, 1fr)); gap: 15px; padding: 20px; justify-items: center; }}
    .tile {{ display: flex; flex-direction: column; align-items: center; justify-content: center; width: 100px; height: 100px; border-radius: 15px; text-decoration: none; font-weight: bold; font-size: 12px; text-align: center; transition: transform 0.2s; box-shadow: 3px 3px 10px rgba(0,0,0,0.4); }}
    .tile:hover {{ transform: scale(1.1); box-shadow: 0px 0px 15px yellow; z-index: 10; }}
    .tile div {{ color: black; }} /* <--- ¡TEXTO NEGRO PARA TODAS LAS TARJETAS! */
    .bg-green {{ background-color: #4CAF50; }} .bg-red {{ background-color: #E53935; }}
    .bg-blue {{ background-color: #2196F3; }} .bg-orange {{ background-color: #FF9800; }} .bg-purple {{ background-color: #9C27B0; }}
    </style>
    """, unsafe_allow_html=True)

# --- VISOR DE ARCHIVOS ---
def display_pdf(file_path):
    # Función para mostrar un PDF directamente en el navegador
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="700px" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

# --- VISTAS DEL PANEL ADMIN ---

def profile_editor():
    st.header("✏️ Editar Perfil del Profesor(a)")
    with st.form("profile_form"):
        name = st.text_input("Nombre Completo", value=st.session_state['profile']['name'])
        subject = st.text_input("Materia/Asignatura", value=st.session_state['profile']['subject'])
        photo_url = st.text_input("URL de la Foto (Debe ser un enlace público)", value=st.session_state['profile']['photo_url'])
        
        if st.form_submit_button("Guardar Cambios del Perfil"):
            st.session_state['profile']['name'] = name
            st.session_state['profile']['subject'] = subject
            st.session_state['profile']['photo_url'] = photo_url
            save_profile(st.session_state['profile'])
            st.success("Perfil actualizado y guardado.")
            st.rerun()

def resource_manager():
    st.header("➕ Agregar Enlaces Externos")
    with st.form("add_res"):
        c1, c2 = st.columns(2)
        name = c1.text_input("Nombre del botón")
        link = c2.text_input("Enlace (URL) - Ej: https://youtube.com/...")
        icon = c1.text_input("Icono (Emoji)", value="🔗")
        color = c2.selectbox("Color", ["bg-green","bg-red","bg-blue","bg-orange","bg-purple"])
        if st.form_submit_button("Guardar Enlace"):
            if name and link:
                st.session_state['recursos'].append({"name": name, "icon": icon, "color": color, "link_type": "external", "link": link})
                save_data(st.session_state['recursos'])
                st.success("Enlace guardado!"); st.rerun()

    st.subheader("🗑️ Opciones Rápidas")
    if st.button("Borrar último botón añadido"):
        if st.session_state['recursos']:
            st.session_state['recursos'].pop()
            save_data(st.session_state['recursos'])
            st.warning("Borrado."); st.rerun()

def file_uploader_view():
    st.header("📤 Subir Archivos (PPT, PDF)")
    st.info("Sube aquí tus archivos. Al hacer clic, se abrirán en una nueva pestaña (PDFs intentarán visualizarse, PPTs se descargarán).")
    
    uploaded_file = st.file_uploader("Selecciona un archivo:", type=['pdf', 'ppt', 'pptx'])
    
    if uploaded_file is not None:
        file_path = Path(UPLOAD_DIR) / uploaded_file.name
        
        # Guardar el archivo en la carpeta del servidor
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.success(f"Archivo '{uploaded_file.name}' guardado en el servidor.")
        
        with st.form("add_file_res"):
            st.subheader("Añadir como Recurso de Archivo")
            c1, c2 = st.columns(2)
            name = c1.text_input("Nombre del Botón", value=uploaded_file.name.split('.')[0])
            icon = c2.text_input("Icono", value="📄")
            color = st.selectbox("Color", ["bg-orange","bg-purple","bg-blue"])
            
            if st.form_submit_button("Añadir Botón de Archivo"):
                new_resource = {"name": name, "icon": icon, "color": color, "link_type": "local_file", "link": str(file_path)}
                st.session_state['recursos'].append(new_resource)
                save_data(st.session_state['recursos'])
                st.success("Botón de archivo añadido a la página principal.")
                st.rerun()

# --- VISTA PÚBLICA (ALUMNOS) ---
def public_view():
    st.markdown("<h1 style='text-align: center; color: #FFFF99;'>🧩 Zona de Aprendizaje</h1>", unsafe_allow_html=True)
    st.markdown("""<div style="display:flex;justify-content:center;margin-bottom:20px;"><input style="padding:10px;border-radius:20px;border:none;width:50%;text-align:center;" placeholder="🔍 Busca aquí..."></div>""", unsafe_allow_html=True)

    grid_html = '<div class="resource-grid">'
    for res in st.session_state['recursos']:
        # Determinar el enlace real y si debe abrir en nueva pestaña
        final_link = res['link']
        target_attr = 'target="_blank"' # Por defecto abre en nueva pestaña

        if res.get('link_type') == 'local_file':
            # Para archivos locales, generamos un enlace directo para que el navegador lo maneje
            # Necesitamos servir los archivos a través de Streamlit
            # Nota: Streamlit por defecto sirve archivos en la raíz o subdirectorios simples
            # Para un control más robusto, se usaría Nginx
            file_extension = Path(res['link']).suffix.lower()
            if file_extension == ".pdf":
                # Para PDFs locales, creamos un enlace a una ruta especial para visualizarlos
                # Esto es un truco, el link real se procesa en `main`
                final_link = f"/view_file/{res['link']}" 
                target_attr = '' # Abre en la misma pestaña si es un PDF para visualización
            else:
                # Para otros tipos de archivos locales (PPTX), se descarga
                final_link = f"/files/{res['link']}" # Ruta para descarga directa
                target_attr = '_blank'
            
        tile = f"""
        <a href="{final_link}" class="tile {res['color']}" {target_attr}>
            <div style="font-size: 30px;">{res['icon']}</div>
            <div>{res['name']}</div>
        </a>
        """
        grid_html += tile
    grid_html += '</div>'
    
    st.markdown(grid_html, unsafe_allow_html=True)

# --- BARRA LATERAL (MAIN LOGIC) ---
with st.sidebar:
    st.image(st.session_state['profile']['photo_url'], width=100)
    st.markdown(f"### {st.session_state['profile']['name']}")
    st.markdown(f"**Materia:** {st.session_state['profile']['subject']}")
    
    if not st.session_state['logged_in']:
        with st.expander("Ingreso Docente"):
            u = st.text_input("Usuario"); p = st.text_input("Contraseña", type="password")
            if st.button("Entrar") and u == ADMIN_USER and p == ADMIN_PASS:
                st.session_state['logged_in'] = True; st.rerun()
    else:
        if st.button("Cerrar Sesión"): st.session_state['logged_in'] = False; st.rerun()

# --- RUTAS Y VISTAS PRINCIPALES ---
if st.session_state['logged_in']:
    tab1, tab2, tab3 = st.tabs(["📝 Perfil", "🔗 Recursos", "💾 Archivos"])
    with tab1: profile_editor()
    with tab2: resource_manager()
    with tab3: file_uploader_view()
else:
    # Si no está logueado, se muestra la vista pública o el visor de archivos
    # Esto es un workaround para Streamlit que no maneja bien las rutas
    path_parts = st.query_params.get("path", "").split('/')
    if path_parts and path_parts[0] == "view_file" and len(path_parts) > 1:
        file_to_view = "/".join(path_parts[1:])
        full_file_path = Path(UPLOAD_DIR) / file_to_view
        if full_file_path.exists() and full_file_path.suffix.lower() == ".pdf":
            st.header(f"Visualizando: {file_to_view}")
            display_pdf(full_file_path)
            if st.button("Volver al Aula"):
                st.session_state['current_file_viewer'] = None
                st.query_params.clear()
                st.rerun()
        else:
            st.error("Archivo no encontrado o formato no soportado para visualización directa.")
            public_view()
    elif path_parts and path_parts[0] == "files" and len(path_parts) > 1:
        file_to_download = "/".join(path_parts[1:])
        full_file_path = Path(UPLOAD_DIR) / file_to_download
        if full_file_path.exists():
            # Streamlit no tiene un mecanismo directo para servir archivos para descarga
            # Deberías usar Nginx para servir la carpeta 'uploaded_files' directamente
            # Por ahora, solo indicamos que el navegador debería manejarlo.
            st.download_button(
                label=f"Descargar {file_to_download}",
                data=full_file_path.read_bytes(),
                file_name=file_to_download,
                mime="application/octet-stream"
            )
        else:
            st.error("Archivo no encontrado para descarga.")
        public_view()
    else:
        public_view()
