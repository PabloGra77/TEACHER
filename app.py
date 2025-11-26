import streamlit as st
import json
import os

# --- 1. CONFIGURACIÓN GENERAL (CAMBIA ESTO) ---
# Aquí defines tu usuario y contraseña para entrar al panel
ADMIN_USER = "admin"      # <--- Cambia "admin" por tu usuario
ADMIN_PASS = "clave123"   # <--- Cambia "clave123" por tu contraseña
DATA_FILE = "recursos.json"

# Configuración de la pestaña del navegador (lo que se ve arriba en Chrome)
st.set_page_config(
    page_title="Aula Virtual 2.0",  # <--- Cambia el nombre de la pestaña
    page_icon="🎓",                 # <--- Cambia el icono (emoji)
    layout="wide"
)

# --- FUNCIONES DE MEMORIA (NO TOCAR) ---
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return [
        {"name": "Google", "icon": "🔍", "color": "bg-blue", "link": "https://google.com"},
        {"name": "Juegos", "icon": "🎮", "color": "bg-green", "link": "#"}
    ]

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

if 'recursos' not in st.session_state:
    st.session_state['recursos'] = load_data()
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# --- ESTILOS CSS (NO TOCAR - DA EL COLOR Y FORMA) ---
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

# --- VISTA PÚBLICA (LO QUE VEN LOS ALUMNOS) ---
def public_view():
    # 2. CAMBIA ESTO: El Título Grande Principal
    st.markdown("<h1 style='text-align: center; color: #FFFF99;'>🎓 Aula de Matemáticas</h1>", unsafe_allow_html=True) # <--- Cambia el título aquí
    
    # 3. CAMBIA ESTO: El texto dentro de la barra de búsqueda
    st.markdown("""<div style="display:flex;justify-content:center;margin-bottom:20px;"><input style="padding:10px;border-radius:20px;border:none;width:50%;text-align:center;" placeholder="🔍 Busca tu tarea o juego aquí..."></div>""", unsafe_allow_html=True)

    grid_html = '<div class="resource-grid">'
    for res in st.session_state['recursos']:
        tile = f"""<a href="{res['link']}" class="tile {res['color']}" target="_blank"><div style="font-size: 30px;">{res['icon']}</div><div>{res['name']}</div></a>"""
        grid_html += tile
    grid_html += '</div>'
    
    st.markdown(grid_html, unsafe_allow_html=True)

# --- VISTA PRIVADA (LO QUE VES TÚ) ---
def admin_view():
    st.title("Panel de Control 🎛️")
    st.info("Modo Edición Activado")
    with st.form("add_res"):
        c1, c2 = st.columns(2)
        name = c1.text_input("Nombre del botón")
        link = c2.text_input("Enlace (URL)")
        icon = c1.text_input("Icono (Emoji)", value="🔗")
        color = c2.selectbox("Color", ["bg-green","bg-red","bg-blue","bg-orange","bg-purple"])
        if st.form_submit_button("Guardar"):
            if name and link:
                st.session_state['recursos'].append({"name": name, "icon": icon, "color": color, "link": link})
                save_data(st.session_state['recursos'])
                st.success("Guardado!"); st.rerun()

    if st.button("Borrar último"):
        if st.session_state['recursos']:
            st.session_state['recursos'].pop()
            save_data(st.session_state['recursos'])
            st.warning("Borrado."); st.rerun()

# --- BARRA LATERAL (FOTO Y NOMBRE PROFESOR) ---
with st.sidebar:
    # Puedes cambiar la URL de la imagen por una foto tuya si tienes el link
    st.image("https://cdn-icons-png.flaticon.com/512/3429/3429149.png", width=100)
    
    # 4. CAMBIA ESTO: Tu Nombre en la barra lateral
    st.markdown("### Profesor Juan Pérez") # <--- Pon tu nombre real aquí
    
    if not st.session_state['logged_in']:
        with st.expander("Ingreso Docente"):
            u = st.text_input("Usuario"); p = st.text_input("Contraseña", type="password")
            if st.button("Entrar") and u == ADMIN_USER and p == ADMIN_PASS:
                st.session_state['logged_in'] = True; st.rerun()
    else:
        if st.button("Salir"): st.session_state['logged_in'] = False; st.rerun()

if st.session_state['logged_in']: admin_view()
else: public_view()
