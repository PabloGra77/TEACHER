import streamlit as st
import streamlit.components.v1 as components

# --- INYECCIÓN CSS: ESTILO PIZARRA (Blackboard) y Tarjetas de Nota ---
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
    /* 3. Estilo de la Tarjeta de Nota (para el contenedor) */
    .note-card {
        background-color: #FFFFF0; /* Color de papel claro */
        color: black; 
        padding: 20px; 
        border-radius: 8px; 
        box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.5); /* Sombra para simular elevación */
        margin-bottom: 25px;
        border: 1px solid #ccc;
    }
    /* 4. Color general del texto (elementos fuera de las tarjetas) */
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

# --- Función Modificada para Tarjetas Estilo Nota y Presentaciones ---
def blog_card(title, category, date, excerpt, content_type="article", embed_code=None):
    
    # Creamos un contenedor nativo
    with st.container():
        # Asignamos la clase CSS 'note-card' al contenido
        st.markdown(f'<div class="note-card">', unsafe_allow_html=True)
        
        # Título y metadatos (en color negro para el fondo claro)
        st.markdown(f"**<span style='color: black; font-size: 1.5em;'>{title}</span>**", unsafe_allow_html=True) 
        st.markdown(f"<span style='color: #4CAF50;'>{category}</span> | <span style='color: #777777;'>{date}</span>", unsafe_allow_html=True)
        st.markdown("<hr style='border-top: 1px solid #ccc;'>", unsafe_allow_html=True)
        
        # Contenido: Artículo o Presentación
        if content_type == "presentation" and embed_code:
            st.markdown("### 📽️ Presentación Incrustada", unsafe_allow_html=True)
            # Usamos st.components.v1.html para incrustar el iframe de la presentación
            components.html(embed_code, height=400, scrolling=False)
            st.markdown(f"<span style='color: black;'>{excerpt}</span>", unsafe_allow_html=True)
        else:
            # Contenido de artículo normal
            st.markdown(f"<span style='color: black;'>{excerpt}</span>", unsafe_allow_html=True)
            st.markdown(
                f'<p style="text-align: right;"><a href="#" style="color: #007BFF;">Leer el artículo completo >></a></p>', 
                unsafe_allow_html=True
            )
            
        st.markdown('</div>', unsafe_allow_html=True)


# --- EJEMPLOS DE USO DE TARJETAS ---

# 1. Tarjeta de Artículo (La que ya tenías)
blog_card(
    "5 Estrategias para Fomentar el Pensamiento Crítico en Primaria",
    "Didáctica",
    "24 de Noviembre, 2025",
    "Aprende técnicas sencillas y efectivas para que tus alumnos dejen de memorizar y comiencen a cuestionar y analizar la información por sí mismos."
)

# 2. Tarjeta con Presentación Incrustada (¡NUEVO!)
# NOTA: Debes obtener el código iframe de "Compartir" de Google Slides o SlideShare.
# Este es un EJEMPLO de código iframe. Reemplázalo por tu presentación real.
presentacion_ejemplo = """
<iframe src="https://docs.google.com/presentation/d/e/2PACX-1vT1gB2S5f.../embed?start=false&loop=false&delayms=3000" frameborder="0" width="100%" height="300" allowfullscreen="true" mozallowfullscreen="true" webkitallowfullscreen="true"></iframe>
"""

blog_card(
    "Tutorial de Gamificación para el Aula",
    "Tecnología Educativa",
    "18 de Noviembre, 2025",
    "Esta es la presentación que compartí sobre cómo usar elementos de juego en la clase para aumentar la motivación. ¡Espero que te sea útil!",
    content_type="presentation",
    embed_code=presentacion_ejemplo
)


# 3. Tarjeta de Artículo
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
    st.button("¡Quiero Mi Guía Ahora!", type="primary", use_container_width=True)

st.markdown("<hr style='border: 1px solid #FFFF99;'>", unsafe_allow_html=True)
st.markdown("<div style='text-align: center; color: #B0C4DE;'>© 2025 El Rincón Educativo de la Profe. Enseñar es dejar una huella para siempre.</div>", unsafe_allow_html=True)
