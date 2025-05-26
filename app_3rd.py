import pandas as pd
import streamlit as st
# Importation du module
from streamlit_option_menu import option_menu
from streamlit_authenticator import Authenticate


# Définition du Menu en sidebar
with st.sidebar:
    selection = option_menu(menu_title=None, options = [":pink_heart: Home :pink_heart:", 
                                                        "Catounets :camera:")


# On indique au programme quoi faire en fonction du choix
if selection == ":pink_heart: Home :pink_heart:":
    st.write("Welcome at Home !")


elif selection == "Catounets :camera:":
    st.write("Catounets's Pictures :camera:")
        # Création de 3 colonnes 
    col1, col2, col3 = st.columns(3)
        # Contenu de la première colonne : 
    with col1:
        st.image("https://www.reddit.com/r/aww/comments/hoa5p2/if_youve_ever_wondered_what_a_mainecoon_kitten/?tl=fr#lightbox")
        # Contenu de la deuxième colonne :
    with col2:
        st.image("https://www.zooplus.fr/magazine/wp-content/uploads/2018/07/maine-coon-2-1024x683.webp")
    # Contenu de la troisième colonne : 
    with col3:
        st.image("https://www.atavik.fr/wp-content/uploads/2022/02/portraits-maine-coon-x5.jpeg")

# Nos données utilisateurs doivent respecter ce format
lesDonneesDesComptes = {
    'usernames': {
        'utilisateur': {
            'name': 'utilisateur',
            'password': 'utilisateurMDP',
            'email': 'utilisateur@gmail.com',
            'failed_login_attemps': 0,  # Sera géré automatiquement
            'logged_in': False,          # Sera géré automatiquement
            'role': 'utilisateur'
        },
        'root': {
            'name': 'root',
            'password': 'rootMDP',
            'email': 'admin@gmail.com',
            'failed_login_attemps': 0,  # Sera géré automatiquement
            'logged_in': False,          # Sera géré automatiquement
            'role': 'administrateur'
        }
    }
}

authenticator = Authenticate(
    lesDonneesDesComptes,  # Les données des comptes
    "cookie name",         # Le nom du cookie, un str quelconque
    "cookie key",          # La clé du cookie, un str quelconque
    30,                    # Le nombre de jours avant que le cookie expire
)

def accueil():
      st.title("Bienvenue sur le contenu réservé aux utilisateurs connectés")

with st.sidebar:
    if st.session_state["authentication_status"]:
    accueil()
    # Le bouton de déconnexion
    authenticator.logout("Déconnexion")

    elif st.session_state["authentication_status"] is False:
        st.error("L'username ou le password est/sont incorrect")
    elif st.session_state["authentication_status"] is None:
        st.warning('Les champs username et mot de passe doivent être remplie')
