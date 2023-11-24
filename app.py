import streamlit as st
import pandas as pd
import requests
from st_click_detector import click_detector

# Config de la page.
st.set_page_config(
    page_title = "Calendrier de l'avent",
    page_icon = "🎁",
    layout = "wide"
)

# Instanciation des session_state.
if "clicked" not in st.session_state:
    st.session_state["clicked"] = None
if "button_clicked" not in st.session_state:
    st.session_state["button_clicked"] = False
if "jours" not in st.session_state:
    st.session_state["jours"] = 0

# Importation des dataframes.
# # Images Cadeaux :
link = "datasets/images_cadeaux.parquet"
df_images = pd.read_parquet(link)

# Films de Noel :
link = "datasets/24_movies.parquet"
df_film = pd.read_parquet(link)

# Playlist deezer :
url = "https://api.deezer.com/playlist/12002102981"
r_music = requests.get(url)
df_music = pd.json_normalize(r_music.json()["tracks"]["data"])
df_music = df_music[[
    "title",
    "link",
    "album.cover",
    "album.cover_medium"
]]

# Cadeaux Tech :
link = "datasets/cadeaux_tech.parquet"
df_cadeaux = pd.read_parquet(link)

# Recette de cuisine :
link = "datasets/dessert.parquet"
df_dessert = pd.read_parquet(link)
link2 = "datasets/moins_30_min.parquet"
df_moins_30 = pd.read_parquet(link2)
link3 = "datasets/plat_principal.parquet"
df_plat_principal = pd.read_parquet(link3)

# Citations :
link = "datasets/citations.parquet"
df_citations = pd.read_parquet(link)

def get_info(
        df: pd.DataFrame,
        info_type: str
    ):
    """
    Récupère les infos demandées sur le dataframe sélectionné.
    ---
    Paramètres :
    df : pd.DataFrame : DataFrame contenant l'information pour le jour sélectionné.
    info_type : str : Type d'info demandé.
    ---
    Retourne :
    La valeur de l'info demandée.
    """
    info = df[info_type].iloc[0]
    return info

def afficher_info_recette(
        df: pd.DataFrame
):
    """
    Affiche les informations de la recette du jour.
    ---
    Paramètres :
    df : pd.DataFrame : DataFrame contenant la recette pour le jour sélectionné.
    ---
    Retourne :
    L'affichage du nom de la recette et de l'image contenant le lien vers la recette.
    """
    st.subheader(get_info(df, "Nom de la recette"), anchor = False)
    link = get_info(df, "Lien vers la recette")
    image_url = get_info(df, "Lien vers la photo")
    st.markdown(f'<a href="{link}" target="_blank"><img width="450px" height="225px" style="border_radius: 5%" src="{image_url}" alt="Clickable Image"></a>', unsafe_allow_html=True)

def afficher_info_cadeau(
        df: pd.DataFrame
):
    """
    Affiche les informations du cadeau du jour.
    ---
    Paramètres :
    df : pd.DataFrame : DataFrame contenant la recette pour le jour sélectionné.
    ---
    Retourne :
    L'affichage du nom du cadeau et de l'image contenant le lien vers le cadeau.
    """
    st.subheader(get_info(df, "Cadeau_nom"), anchor = False)
    link = get_info(df, 'cadeau_url')
    image_url = get_info(df, 'cadeau_image')
    st.markdown(f'<a href="{link}" target="_blank"><img width="400px" height="225px" style="border_radius: 5%" src="{image_url}" alt="Clickable Image"></a>', unsafe_allow_html=True)

def afficher_info_film(
        df: pd.DataFrame
):
    """
    Affiche les informations du film du jour.
    ---
    Paramètres :
    df : pd.DataFrame : DataFrame contenant la recette pour le jour sélectionné.
    ---
    Retourne :
    L'affichage du nom du film et de l'affiche contenant le lien allociné.
    """
    st.subheader(get_info(df, "Titre"), anchor = False)
    link = get_info(df, 'lien_allocine')
    image_url = get_info(df, "image")
    st.markdown(f'<a href="{link}" target="_blank"><img width="200px" height="275px" style="border_radius: 5%" src="{image_url}" alt="Clickable Image"></a>', unsafe_allow_html=True)

def afficher_info_musique(
        df: pd.DataFrame
):
    """
    Affiche les informations de la musique du jour.
    ---
    Paramètres :
    df : pd.DataFrame : DataFrame contenant la recette pour le jour sélectionné.
    ---
    Retourne :
    L'affichage du nom de la musique et de l'image contenant le lien vers deezer.
    """
    st.subheader(get_info(df, "title"), anchor = False)
    link = get_info(df, "link")
    st.markdown(f"[![Link]({get_info(df, 'album.cover_medium')})]({link})")

def choix_item_du_jour(
        df: pd.DataFrame,
        jour: int,
        col: str,
):
    """
    Récupère l'item demandé pour le jour sélectionné.
    ---
    Paramètres :
    df : pd.DataFrame : DataFrame contenant la recette pour le jour sélectionné.
    jour : int : Le jour qui a été sélectionné.
    col : str : La colonne dans laquelle chercher l'information.
    ---
    Retourne :
    Un DataFrame avec une seule ligne contenant l'élement demandé pour le jour sélectionné.
    """
    liste_titre = df[col].tolist()
    element_du_jour = liste_titre[jour-1]
    return df[df[col] == element_du_jour]

def get_clicked(
        jour: int
):
    """
    Affiche une image cliquable pour chaque jour du calendrier.
    ---
    Paramètre :
    jour : int : Le jour pour lequel afficher une image
    ---
    Retourne :
    Un component 'click_detector' affichant une image avec une clé unique.
    """
    img_link = df_images.iloc[jour][0]
    content = f'''<a href="#" id="{jour}"><img width="165px" heigth="80px" src="{img_link}" style="border-radius: 20%"></a>'''
    unique_key = f"click_detector_{jour}"
    return click_detector(content, key=unique_key)

# Début de la page.
# Si aucun bouton n'a été cliqué.
if st.session_state["button_clicked"] == False:
    st.markdown("<h1 style='text-align: center; color: white;'>Calendrier de l'avent            </h1>", unsafe_allow_html=True)
    cols = st.columns(6)
    for index in range(24):
        with cols[index % 6]:
            clicked = get_clicked(index)
            if clicked:
                st.session_state["button_clicked"] = True
                st.session_state["jours"] = index+1
                st.rerun()
# Si un bouton a été cliqué.
else:
    # Détermine le jour qui a été sélectionné.
    jour = st.session_state["jours"]
    er = "er" if jour == 1 else ""
    st.markdown(f"<h2 style='text-align: center; color: white;'>{jour}{er} Décembre</h2>", unsafe_allow_html=True)
    if st.button("⬅️ Retour"):
        st.session_state["button_clicked"] = False
        st.rerun()
    st.divider()
    if jour != 24:
        st.markdown("<h3 style='text-align: center; color: white;'>Citation du jour :</h3>", unsafe_allow_html=True)
        text = f'"{df_citations["Citation"].loc[jour]}"'
        auteur = f'-{df_citations["Auteur Nom"].loc[jour]}'
        st.markdown(f"<h3 style='text-align: center; color: white; font-size: 1.25em; font-style: italic;'>{text}</h3>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='text-align: center; color: white; font-size: 1.25em; font-style: italic;'>{auteur}</h3>", unsafe_allow_html=True)
        st.divider()
        col6, col7, col8, = st.columns(3)
        with col6:
            st.header("Film : ", anchor = False)
            movie_du_jour = choix_item_du_jour(df_film, jour, "Titre")
            afficher_info_film(movie_du_jour)
        with col7:
            st.header("Musique : ", anchor = False)
            musique_du_jour = choix_item_du_jour(df_music, jour, "title")
            afficher_info_musique(musique_du_jour)
        with col8:
            st.header("Idée cadeaux :", anchor = False)
            cadeau_du_jour = choix_item_du_jour(df_cadeaux, jour, "Cadeau_nom")
            afficher_info_cadeau(cadeau_du_jour)
        st.divider()
        st.markdown("<h3 style='text-align: center; color: white;'>Suggestion de recettes</h3>", unsafe_allow_html=True)
        col9, col10, col11 = st.columns(3)
        with col9:
            moins_30_du_jour = choix_item_du_jour(df_moins_30, jour, "Nom de la recette")
            afficher_info_recette(moins_30_du_jour)
        with col10:
            plat_du_jour = choix_item_du_jour(df_plat_principal, jour, "Nom de la recette")
            afficher_info_recette(plat_du_jour)
        with col11:
            dessert_du_jour = choix_item_du_jour(df_dessert, jour, "Nom de la recette")
            afficher_info_recette(dessert_du_jour)
        st.divider()
    else :
        # Vidéo spéciale pour le 24 décembre.
        st.video("hackathon24112023.mp4")