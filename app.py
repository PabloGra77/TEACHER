import streamlit as st

# --- Configuración de la Página ---
st.set_page_config(
    page_title="El Rincón Educativo de la Profe",
    page_icon="👩‍🏫",
    layout="wide"
)

# --- Header y Bienvenida ---
st.header("📚 El Rincón Educativo de la Profe [Nombre]")
st.markdown("""
**"Donde las ideas florecen y el aprendizaje nunca se detiene."**
---
""")

# --- Contenido Principal (Últimas Publicaciones) ---
st.title("Últimas Publicaciones 📝")

# Usamos columnas para simular tarjetas de blog
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Post 1: Estrategias de Pensamiento Crítico")
    st.caption("24 de Noviembre, 2025 | Categoría: Didáctica")
    st.write("Aprende 5 técnicas sencillas para que tus alumnos cuestionen y analicen información.")
    st.button("Leer más >>", key="p1")

with col2:
    st.subheader("Post 2: Apps para Quizzes Interactivos")
    st.caption("15 de Noviembre, 2025 | Categoría: Tecnología")
    st.write("Mis 3 herramientas favoritas para evaluar de forma divertida y rápida.")
    st.button("Leer más >>", key="p2")

with col3:
    st.subheader("Post 3: Cómo Ayudar con la Organización")
    st.caption("1 de Noviembre, 2025 | Categoría: Padres")
    st.write("Consejos prácticos para que las familias apoyen las rutinas de estudio.")
    st.button("Leer más >>", key="p3")

st.markdown("---")

# --- Recursos Destacados (CTA) ---
st.subheader("🎁 ¡Descarga la Guía GRATUITA para la Gestión del Aula!")
st.text_input("Ingresa tu email aquí para recibirla:", value="", key="email")
st.button("¡Quiero Mi Guía!", type="primary")

# --- Barra Lateral (Simulada) ---
st.sidebar.title("Menú")
st.sidebar.button("Inicio")
st.sidebar.button("Sobre Mí")
st.sidebar.button("Recursos")
st.sidebar.button("Contacto")

st.sidebar.markdown("---")
st.sidebar.subheader("Categorías")
st.sidebar.write("* Didáctica (5)")
st.sidebar.write("* Consejos para Padres (12)")
st.sidebar.write("* Tecnología Educativa (8)")
