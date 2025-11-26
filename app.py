import streamlit as st
import json
import os
from pathlib import Path

# --- CONFIGURACIÓN Y ARCHIVOS ---
ADMIN_USER = "admin"      # Tu usuario
ADMIN_PASS = "clave123"   # Tu contraseña
DATA_FILE = "recursos.json"
PROFILE_FILE = "profile.json" # Archivo para guardar tu perfil
UPLOAD_DIR = "uploaded_files" # Carpeta para guardar PPTs/PDFs

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

# --- ESTILOS VISUALES ---
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #36454F; color: white; }
    [data-testid="stSidebar"] { background-color: #2F4F4F; color: white; }
    .resource-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(100px, 1fr)); gap: 15px; padding: 20px; justify-items: center; }
    .tile { display: flex; flex-direction: column; align-items: center; justify-content: center; width: 100px; height: 100px; border-radius: 15px; text-decoration: none; color: white; font-weight: bold; font-size: 12px; text-align: center; transition: transform 0.2s; box-shadow: 3px 3px 10px rgba(0,0,0,0.4); }
    .tile:hover { transform: scale(1.1); box-shadow: 0px 0px 15px yellow; z-index: 10; }
    .bg-green { background-color: #4CAF50; } .bg-red { background-color: #E53935; }
    .bg-blue { background-color: #2196F3; } .bg-orange { background-color: #FF9800; } .bg-purple { background-color: #9C27B0; }
    </style>
    """, unsafe_allow_html=True)

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
        link = c2.text_input("Enlace (URL)")
        icon = c1.text_input("Icono (Emoji)", value="🔗")
        color = c2.selectbox("Color", ["bg-green","bg-red","bg-blue","bg-orange","bg-purple"])
        if st.form_submit_button("Guardar Enlace"):
            if name and link:
                st.session_state['recursos'].append({"name": name, "icon": icon, "color": color, "link": link})
                save_data(st.session_state['recursos'])
                st.success("Enlace guardado!"); st.rerun()

    st.subheader("🗑️ Opciones Rápidas")
    if st.button("Borrar último botón añadido"):
        if st.session_state['recursos']:
            st.session_state['recursos'].pop()
            save_data(st.session_state['recursos'])
            st.warning("Borrado."); st.rerun()

def file_uploader_view():
    st.header("📤 Subir Archivos (PPT, PDF, etc.)")
    st.warning("⚠️ Nota Importante: La aplicación no puede 'proyectar' archivos PPT directamente. Al subir el archivo, se crea un botón de DESCARGA.")
    st.info("Si deseas que se vea como presentación, debes usar un servicio como Google Drive/OneDrive, compartir el archivo públicamente y pegar el enlace de DESCARGA directa o EMBED en la sección de 'Agregar Enlaces'.")
    
    uploaded_file = st.file_uploader("Selecciona un archivo:", type=['pdf', 'ppt', 'pptx', 'doc', 'docx'])
    
    if uploaded_file is not None:
        file_path = Path(UPLOAD_DIR) / uploaded_file.name
        
        # Guardar el archivo en la carpeta del servidor
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Crear un recurso con el enlace de descarga (solo funciona si el archivo está en la misma carpeta raíz del Streamlit)
        # Como Streamlit sirve archivos desde su carpeta raíz, el link es el nombre del archivo.
        download_link = uploaded_file.name 
        
        st.success(f"Archivo '{uploaded_file.name}' guardado.")
        
        with st.form("add_file_res"):
            st.subheader("Añadir como Recurso de Descarga")
            c1, c2 = st.columns(2)
            name = c1.text_input("Nombre del Botón de Descarga", value=uploaded_file.name.split('.')[0])
            icon = c2.text_input("Icono", value="💾")
            color = st.selectbox("Color", ["bg-orange","bg-purple","bg-blue"])
            
            if st.form_submit_button("Añadir Botón de Descarga"):
                new_resource = {"name": name, "icon": icon, "color": color, "link": download_link}
                st.session_state['recursos'].append(new_resource)
                save_data(st.session_state['recursos'])
                st.success("Botón de descarga añadido a la página principal.")
                st.rerun()

# --- VISTA PÚBLICA (ALUMNOS) ---
def public_view():
    st.markdown("<h1 style='text-align: center; color: #FFFF99;'>🧩 Zona de Aprendizaje</h1>", unsafe_allow_html=True)
    st.markdown("""<div style="display:flex;justify-content:center;margin-bottom:20px;"><input style="padding:10px;border-radius:20px;border:none;width:50%;text-align:center;" placeholder="🔍 Busca aquí..."></div>""", unsafe_allow_html=True)

    grid_html = '<div class="resource-grid">'
    for res in st.session_state['recursos']:
        # Verifica si es un archivo local para el target
        target = "_blank" if res['link'].startswith('http') else "_self"
        tile = f"""<a href="{res['link']}" class="tile {res['color']}" target="{target}"><div style="font-size: 30px;">{res['icon']}</div><div>{res['name']}</div></a>"""
        grid_html += tile
    grid_html += '</div>'
    
    st.markdown(grid_html, unsafe_allow_html=True)


# --- BARRA LATERAL (MAIN LOGIC) ---
with st.sidebar:
    # Muestra la información del perfil
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

if st.session_state['logged_in']:
    tab1, tab2, tab3 = st.tabs(["📝 Perfil", "🔗 Recursos", "💾 Archivos"])
    with tab1: profile_editor()
    with tab2: resource_manager()
    with tab3: file_uploader_view()
else:
    public_view()
