import streamlit as st
import numpy as np
from PIL import Image, ImageDraw
from sklearn.cluster import KMeans
import io


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

def create_palette_image(hex_colors):
    swatch_width = 100
    swatch_height = 200
    img_width = swatch_width * len(hex_colors)
    img_height = swatch_height
    
    palette_img = Image.new("RGB", (img_width, img_height))
    draw = ImageDraw.Draw(palette_img)
    
    for i, color in enumerate(hex_colors):
        # Convertir le hex en RGB
        r = int(color[1:3], 16)
        g = int(color[3:5], 16)
        b = int(color[5:7], 16)
        
        box = (i * swatch_width, 0, (i + 1) * swatch_width, swatch_height)
        draw.rectangle(box, fill=(r, g, b))
        
    return palette_img

uploaded_file = st.file_uploader("Choisissez une image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Image source")
        st.image(uploaded_file, use_container_width=True)

    n_colors = st.slider("Nombre de couleurs dans la palette", min_value=3, max_value=10, value=5)
    palette = get_color_palette(uploaded_file, n_colors=n_colors)

    with col2:
        st.subheader("")

    st.markdown("### Codes Héxadécimaux :")
    cols = st.columns(len(palette))
    for i, color in enumerate(palette):
        with cols[i]:
            st.markdown(
                f'<div style="background-color: {color}; height: 80px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);"></div>',
                unsafe_allow_html=True
            )
            st.code(color, language="")

    st.markdown("---")
    st.subheader("📥 Télécharger la palette")

    txt_content = "\n".join(palette)
    st.download_button(
        label="📄 Télécharger les codes (TXT)",
        data=txt_content,
        file_name="palette.txt",
        mime="text/plain"
    )

    buffer = io.BytesIO()
    palette_img = create_palette_image(palette)
    palette_img.save(buffer, format="PNG")
    byte_im = buffer.getvalue()

    st.download_button(
        label="🖼️ Télécharger l'image de la palette (PNG)",
        data=byte_im,
        file_name="palette.png",
        mime="image/png"
    )