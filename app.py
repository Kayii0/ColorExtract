import streamlit as st
import numpy as np
from PIL import Image
from sklearn.cluster import KMeans

st.set_page_config(page_title="Générateur de Palette", page_icon="🎨", layout="centered")

st.title("🎨 Générateur de Palette de Couleurs")
st.write("Glissez-déposez une image ci-dessous pour extraire automatiquement ses couleurs dominantes !")

# Fonction d'extraction de la palette de couleurs
def get_color_palette(image_file, n_colors=5):
    image = Image.open(image_file)
    image = image.resize((150, 150))

    pixels = np.array(image)
    pixels = pixels.reshape(-1, 3)

    kmeans = KMeans(n_clusters=n_colors, n_init=10)
    kmeans.fit(pixels)

    colors = kmeans.cluster_centers_.astype(int)
    hex_colors = ['#{:02x}{:02x}{:02x}'.format(r, g, b) for r, g, b in colors]
    return hex_colors

uploaded_file = st.file_uploader("Choisissez une image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Image source")
        st.image(uploaded_file, use_container_width=True)

    n_colors = st.slider("Nombre de couleurs dans la palette", min_value=3, max_value=10, value=5)
    palette = get_color_palette(uploaded_file, n_colors=n_colors)

    with col2:
        st.subheader("Palette extraite")

    st.markdown("### Codes Héxadécimaux :")
    cols = st.columns(len(palette))
    for i, color in enumerate(palette):
        with cols[i]:
            st.markdown(
                f'<div style="background-color: {color}; height: 80px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);"></div>',
                unsafe_allow_html=True
            )
            st.code(color, language="")
