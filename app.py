import streamlit as st

# --- INYECCIÓN CSS: ESTILO PIZARRA (Blackboard) ---
# Se inyecta CSS para cambiar el fondo y el color de texto en toda la aplicación
# NOTA: Los estilos de texto globales son ahora menos intrusivos, ya que las tarjetas tienen su propio fondo.
st.markdown(
    """
    <style>
    /* 1. Fondo principal de la aplicación: Pizarra */
    [data-testid="stAppViewContainer"] {
        background-color: #36454F; /* Gris oscuro para el efecto pizarra */
        color: white; 
    }
    /* 2. Barra lateral */
    [data-testid="stSidebar"] {
        background-color: #2F4F4F; 
        color: white;
    }
    /* 3. Color general del texto (afecta elementos fuera de las tarjetas) */
    * {
        color: white;
    }
    /* Excepciones: Botones y Inputs */
    .stButton>button {
        background-color: #556B2F; 
        color: white !important;
        border: 1px solid white;
    }
    .stTextInput>div>div>input {
        background-color: white;
        color: black !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# --- Configuración de la Página ---
st.set_page_config(
    page_title="El Rincón Educativo de la Profe",
    page_icon="📚",
    layout="wide"
)

# --- Contenedor de la Barra Lateral (Perfil y Menú) ---
with st.sidebar:
    # PERFIL DEL PROFESOR
    st.markdown(
        """
        <div style='text-align: center; margin-bottom: 20px;'>
            <img src="https://via.placeholder.com/150/FFFFFF/000000?text=Profe+Foto" 
                 style='border-radius: 50%; width: 100px; height: 100px; object-fit: cover; border: 3px solid #FFFF99;'>
        </div>
        """, unsafe_allow_html=True
    )
    st.markdown("<h2 style='text-align: center; color: white;'>👩‍🏫 Profa. Ana Rodríguez</h2>", unsafe_allow_html=True)
    st.caption("Especialista en Didáctica y Tecnología Educativa")
    
    st.markdown("---")
    
    # Resto del menú
    st.title("Menú Principal")
    st.button("🏠 Inicio", use_container_width=True)
    st.button("💡 Sobre Mí / Mi Filosofía", use_container_width=True)
    st.button("🎁 Recursos Descargables", use_container_width=True)
    st.button("📧 Contacto", use_container_width=True)
    
    st.markdown("---")
    st.subheader("🏷️ Categorías")
    st.caption("Filtra por tema")
    st.write("* Didáctica y Metodología (5)")
    st.write("* Consejos para Padres (12)")
    st.write("* Tecnología Educativa (8)")
    st.write("* Reflexiones y Experiencias (15)")

    st.markdown("---")
    st.subheader("📲 Sígueme")
    st.write("[Instagram] | [Pinterest] | [YouTube]")


# --- Contenedor del Contenido Principal ---
st.title("El Blog de la Profe")
# Cita de Bienvenida con color de tiza
st.markdown(
    """
    <p style='font-size: 18px; color: #FFFF99;'>
        "Donde las ideas florecen y el aprendizaje nunca se detiene. 
        Encuentra inspiración para transformar tu aula o tu hogar."
    </p>
    """, unsafe_allow_html=True
)

st.markdown("<hr style='border: 1px solid #FFFF99;'>", unsafe_allow_html=True)

## Sección de Artículos (Simulación de Tarjetas estilo Notas)

st.subheader("✨ Últimas Publicaciones")

# --- Función Modificada para Tarjetas Estilo Nota ---
def blog_card(title, category, date, excerpt):
    # CSS para el contenedor de la tarjeta (simula una nota o papel)
    note_style = """
    background-color: #FFFFF0; /* Color de papel o Post-it */
    color: black; 
    padding: 20px; 
    border-radius: 8px; 
    box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.5); /* Sombra para simular elevación */
    margin-bottom: 25px;
    """
    
    # Inicia el contenedor HTML para la tarjeta
    st.markdown(f'<div style="{note_style}">', unsafe_allow_html=True)
    
    # Contenido de la tarjeta (todo dentro de la tarjeta debe ser negro)
    st.markdown(f"**<span style='color: black; font-size: 1.5em;'>{title}</span>**", unsafe_allow_html=True) 
    st.markdown(f"<span style='color: #4CAF50;'>{category}</span> | <span style='color: #777777;'>{date}</span>", unsafe_allow_html=True)
    st.markdown(f"<span style='color: black;'>{excerpt}</span>", unsafe_allow_html=True)
    
    # Botón de lectura (usamos un truco con markdown/html para el color)
    st.markdown(
        f'<p style="text-align: right;"><a href="#" style="color: #007BFF;">Leer el artículo completo >></a></p>', 
        unsafe_allow_html=True
    )
    
    # Cierra el contenedor HTML
    st.markdown('</div>', unsafe_allow_html=True)

# Tarjeta 1
blog_card(
    "5 Estrategias para Fomentar el Pensamiento Crítico en Primaria",
    "Didáctica",
    "24 de Noviembre, 2025",
    "Aprende técnicas sencillas y efectivas para que tus alumnos dejen de memorizar y comiencen a cuestionar y analizar la información por sí mismos."
)

# Tarjeta 2
blog_card(
    "Mis 3 Apps Favoritas para Crear Quizzes Interactivos",
    "Tecnología Educativa",
    "15 de Noviembre, 2025",
    "Descubre herramientas que hacen que la evaluación sea un juego, ahorrándote tiempo de corrección y manteniendo a tus estudiantes motivados."
)

# Tarjeta 3
blog_card(
    "Cómo Ayudar a tu Hijo a Organizar su Mochila sin Estresarse",
    "Consejos para Padres",
    "1 de Noviembre, 2025",
    "Una guía práctica para establecer rutinas de organización en casa. Fomenta la autonomía y reduce el caos matutino de la familia."
)

# --- Call to Action (CTA) al pie de página ---
st.subheader("📧 Únete a la Comunidad Educativa")
col_email, col_button = st.columns([2, 1])

with col_email:
    st.text_input("Ingresa tu email para descargar la 'Guía GRATUITA de Gestión del Aula'", label_visibility="collapsed") 

with col_button:
    # Usamos el botón nativo de Streamlit
    st.button("¡Quiero Mi Guía Ahora!", type="primary", use_container_width=True)

st.markdown("<hr style='border: 1px solid #FFFF99;'>", unsafe_allow_html=True)
st.markdown("<div style='text-align: center; color: #B0C4DE;'>© 2025 El Rincón Educativo de la Profe. Enseñar es dejar una huella para siempre.</div>", unsafe_allow_html=True)
