import pandas as pd
import streamlit as st
# Importation du module
from streamlit_option_menu import option_menu

import os
from PIL import Image

# Liste des noms des chats
cats = ["Kiwi", "Lenka", "Keiko", "Flokie", "Loken"]

# Chargement des utilisateurs
@st.cache_data
def load_users():
    return pd.read_csv("users.csv")

# Authentification
def authenticate(username, password, users_df):
    user_row = users_df[users_df["name"] == username]
    if not user_row.empty and user_row.iloc[0]["password"] == password:
        return True, user_row.iloc[0]
    return False, None

# Affichage de 3 images d'un chat
def show_cat_images(cat_name):
    image_dir = "images"
    images = [f"{cat_name}{i}.jpg" for i in range(1, 4)]  # ex: Kiwi1.jpg, Kiwi2.jpg, Kiwi3.jpg
    cols = st.columns(3)
    for i in range(3):
        img_path = os.path.join(image_dir, images[i])
        if os.path.exists(img_path):
            img = Image.open(img_path)
            cols[i].image(img, use_column_width=True, caption=images[i])
        else:
            cols[i].warning(f"{images[i]} non trouvée")

# Application principale
def main():
    st.set_page_config(page_title="Album Chats", layout="wide")
    users_df = load_users()

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.username = ""

    if not st.session_state.authenticated:
        st.title("Connexion")
        username = st.text_input("Nom d'utilisateur")
        password = st.text_input("Mot de passe", type="password")
        if st.button("Se connecter"):
            valid, user_data = authenticate(username, password, users_df)
            if valid:
                st.session_state.authenticated = True
                st.session_state.username = user_data["name"]
                st.success(f"Bienvenue {st.session_state.username} !")
                st.rerun()
            else:
                st.error("Nom d'utilisateur ou mot de passe incorrect.")
    else:
        st.sidebar.title("Menu")
        st.sidebar.markdown(f"👤 Bienvenue **{st.session_state.username}**")

        pages = ["🖤 Home 🖤"] + cats
        selected_page = st.sidebar.radio("Navigation", pages)

        if st.sidebar.button("Déconnexion"):
            st.session_state.authenticated = False
            st.session_state.username = ""
            st.experimental_rerun()

        st.title(selected_page)

        if selected_page == "🖤 Home 🖤":
            st.markdown("Bienvenue dans l'album photo des chats 🐾 !\nChoisissez un chat dans le menu pour voir ses photos.")
        else:
            show_cat_images(selected_page)

if __name__ == "__main__":
    main()
