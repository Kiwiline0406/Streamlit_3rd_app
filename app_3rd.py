import streamlit as st
import pandas as pd
import os
from PIL import Image, ExifTags

cats = ["Kiwi", "Lenka", "Keiko", "Flokie", "Loken"]

@st.cache_data
def load_users():
    return pd.read_csv("users.csv")

def tips_connexion(users_df):
    if st.checkbox("💡 Besoin d'un indice de connexion ?"):
        st.markdown("Voici quelques exemples d'identifiants pour tester :")
        examples = users_df[["name", "password"]].rename(columns={"name": "Utilisateur", "password": "Mot de passe"})
        st.dataframe(examples, use_container_width=True)

def authenticate(username, password, users_df):
    user_row = users_df[users_df["name"] == username]
    if not user_row.empty and user_row.iloc[0]["password"] == password:
        return True, user_row.iloc[0]
    return False, None

def load_and_correct_image(path):
    img = Image.open(path)
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        exif = img._getexif()
        if exif is not None:
            orientation_value = exif.get(orientation, None)
            if orientation_value == 3:
                img = img.rotate(180, expand=True)
            elif orientation_value == 6:
                img = img.rotate(270, expand=True)
            elif orientation_value == 8:
                img = img.rotate(90, expand=True)
    except (AttributeError, KeyError, IndexError):
        pass
    return img

def show_cat_images(cat_name):
    image_dir = "images"
    images = [f"{cat_name}{i}.jpg" for i in range(1, 4)]
    cols = st.columns(3)
    for i in range(3):
        img_path = os.path.join(image_dir, images[i])
        if os.path.exists(img_path):
            img = load_and_correct_image(img_path)
            cols[i].image(img, use_container_width=True, caption=images[i])
        else:
            cols[i].warning(f"{images[i]} non trouvée")

def main():
    st.set_page_config(page_title="Album Chats", layout="wide")
    users_df = load_users()

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.username = ""
    if "current_page" not in st.session_state:
        st.session_state.current_page = "🖤 Home 🖤"

    if not st.session_state.authenticated:
        st.title("Connexion")
        username = st.text_input("Nom d'utilisateur")
        password = st.text_input("Mot de passe", type="password")

        if st.button("Se connecter"):
            valid, user_data = authenticate(username, password, users_df)
            if valid:
                st.session_state.authenticated = True
                st.session_state.username = user_data["name"]
                st.rerun()
            else:
                st.error("Nom d'utilisateur ou mot de passe incorrect.")

        tips_connexion(users_df)  # 💡 Ajouté au bon endroit

    else:
        st.sidebar.markdown(f"👋 Bienvenue **{st.session_state.username}**")
        menu_items = ["🖤 Home 🖤"] + cats

        st.sidebar.markdown("---")
        for item in menu_items:
            if st.sidebar.button(item):
                st.session_state.current_page = item
                st.rerun()

        st.sidebar.markdown("---")
        if st.sidebar.button("🚪 Déconnexion"):
            st.session_state.authenticated = False
            st.session_state.username = ""
            st.rerun()

        st.title(st.session_state.current_page)
        if st.session_state.current_page == "🖤 Home 🖤":
            st.markdown("Bienvenue dans l'album photo des chats 🐾 !\n\nClique sur un nom à gauche pour voir les photos.")
            st.image("https://ladiesgamers.com/wp-content/uploads/2024/03/20240316211631_1-1536x960.jpg",
                    caption="Un moment de détente? Check les jeux Hidden Cats 🎮🐱",
                    use_container_width=True)
            
        else:
            show_cat_images(st.session_state.current_page)

if __name__ == "__main__":
    main()
