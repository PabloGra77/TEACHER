import streamlit as st
import streamlit.components.v1 as components

# --- INYECCIÓN CSS: ESTILO PIZARRA Y GRID TIPO SYMBALOO ---
st.markdown(
    """
    <style>
    /* 1. Fondo Pizarra */
    [data-testid="stAppViewContainer"] {
        background-color: #36454F;
        color: white; 
    }
    [data-testid="stSidebar"] {
        background-color: #2F4F4F; 
        color: white;
    }
    
    /* 2. Estilo para la BARRA DE BÚSQUEDA CENTRAL */
    .search-container {
        display: flex;
        justify-content: center;
        margin-bottom: 30px;
    }
    .search-box {
        width: 60%;
        padding: 15px;
        border-radius: 30px;
        border: none;
        outline: none;
        text-align: center;
        font-size: 18px;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.3);
    }

    /* 3. Estilo para el GRID DE RECURSOS (Tipo Symbaloo) */
    .resource-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
        gap: 15px;
        padding: 20px;
        justify-items: center;
    }
    
    .tile {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        width: 100px;
        height: 100px;
        border-radius: 15px;
        text-decoration: none;
        color: white;
        font-weight: bold;
        font-size: 12px;
        text-align: center;
        transition: transform 0.2s;
        box-shadow: 3px 3px 10px rgba(0,0,0,0.4);
        padding: 5px;
    }
    
    .tile:hover {
        transform: scale(1.1);
        z-index: 10;
        box-shadow: 0px 0px 15px yellow; /* Resplandor al pasar el mouse */
    }

    .tile img {
        width: 50px;
        height: 50px;
        margin-bottom: 5px;
        filter: drop-shadow(2px 2px 2px rgba(0,0,0,0.5));
    }
    
    /* Colores de las baldosas */
    .bg-green { background-color: #4CAF50; }
    .bg-red { background-color: #E53935; }
    .bg-blue { background-color: #2196F3; }
    .bg-orange { background-color: #FF9800; }
    .bg-purple { background-color: #9C27B0; }
    
    </style>
    """,
    unsafe_allow_html=True
)

# --- Configuración de la Página ---
st.set_page_config(page_title="Aula Virtual Interactiva", page_icon="🧩", layout="wide")

# --- Barra Lateral (Perfil) ---
with st.sidebar:
    st.markdown(
        """
        <div style='text-align: center;'>
            <img src="https://via.placeholder.com/150/FFFFFF/000000?text=Profe" 
                 style='border-radius: 50%; width: 90px; border: 3px solid #FFFF99;'>
            <h3>Profa. Ana</h3>
        </div>
        """, unsafe_allow_html=True
    )
    st.write("---")
    st.button("🏠 Inicio / Tablero", use_container_width=True)
    st.button("📝 Blog de Notas", use_container_width=True)
    st.button("📺 Videos", use_container_width=True)

# --- TÍTULO PRINCIPAL ---
st.markdown("<h1 style='text-align: center; color: #FFFF99;'>🧩 Zona de Aprendizaje</h1>", unsafe_allow_html=True)

# --- BARRA DE BÚSQUEDA (Visual) ---
st.markdown(
    """
    <div class="search-container">
        <input type="text" class="search-box" placeholder="🔍 ¿Qué quieres aprender hoy? (Ej: Vocales, Cuentos...)">
    </div>
    """, unsafe_allow_html=True
)

# --- GENERACIÓN DEL GRID TIPO SYMBALOO ---
# Definimos los recursos como una lista de diccionarios para facilitar la edición
resources = [
    {"name": "Praxias", "icon": "👅", "color": "bg-green", "link": "#"},
    {"name": "Caperucita", "icon": "🐺", "color": "bg-red", "link": "#"},
    {"name": "Sílabas", "icon": "🗣️", "color": "bg-blue", "link": "#"},
    {"name": "Cuentos", "icon": "📖", "color": "bg-purple", "link": "#"},
    {"name": "Colores", "icon": "🎨", "color": "bg-orange", "link": "#"},
    {"name": "Trabalenguas", "icon": "🤪", "color": "bg-green", "link": "#"},
    {"name": "Fonemas", "icon": "🔊", "color": "bg-blue", "link": "#"},
    {"name": "Granja", "icon": "🐮", "color": "bg-orange", "link": "#"},
    {"name": "Adivinanzas", "icon": "❓", "color": "bg-purple", "link": "#"},
    {"name": "Letra L", "icon": "L", "color": "bg-green", "link": "#"},
    {"name": "Letra R", "icon": "R", "color": "bg-green", "link": "#"},
    {"name": "Juegos", "icon": "🎲", "color": "bg-red", "link": "#"},
]

# Creamos el HTML para el Grid
grid_html = '<div class="resource-grid">'
for res in resources:
    # Usamos emojis como iconos por simplicidad, pero podrías usar URLs de imágenes reales
    # Si el icono es un emoji, lo mostramos grande. Si es texto (L/R), también.
    
    tile = f"""
    <a href="{res['link']}" class="tile {res['color']}" target="_blank">
        <div style="font-size: 40px;">{res['icon']}</div>
        <div class="label">{res['name']}</div>
    </a>
    """
    grid_html += tile
grid_html += '</div>'

# Renderizamos el Grid
st.markdown(grid_html, unsafe_allow_html=True)

st.write("---")

# --- SECCIÓN INFERIOR (BLOG RÁPIDO) ---
st.subheader("📌 Notas de Clase")
col1, col2 = st.columns(2)

with col1:
    with st.container():
        st.info("📢 **Tarea para mañana:** Traer el cuaderno de caligrafía y repasar los sonidos de la R.")

with col2:
     # Ejemplo de presentación incrustada pequeña
    st.markdown("**📽️ Repaso de la semana:**")
    st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ") # Video ejemplo
