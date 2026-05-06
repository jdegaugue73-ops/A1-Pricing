import streamlit as st

# Base de données simulée (Mock API)
MOCK_DATABASE = {
    "AB-123-CD": {
        "marque": "Peugeot",
        "modele": "208",
        "motorisation": "1.2 PureTech 100",
        "boite": "Manuelle 6 rapports",
        "generation": "Génération 2 (P21)",
        "phase": "Phase 1 (2019-2023)",
        "annee": 2021,
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/4/4b/Peugeot_208_II_Genf_2019_1Y7A5581.jpg"
    },
    "EF-456-GH": {
        "marque": "Renault",
        "modele": "Clio",
        "motorisation": "1.5 Blue dCi 115",
        "boite": "Manuelle 6 rapports",
        "generation": "Génération 5",
        "phase": "Phase 1 (2019-2023)",
        "annee": 2020,
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/5/58/Renault_Clio_V_Genf_2019_1Y7A5550.jpg"
    },
    "VF1RJA00000000001": {
        "marque": "Renault",
        "modele": "Megane E-Tech",
        "motorisation": "EV60 220ch",
        "boite": "Automatique",
        "generation": "Génération 1",
        "phase": "Phase 1 (2022-)",
        "annee": 2023,
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/2/23/Renault_Megane_E-Tech_IAA_2021_1Y7A0065.jpg"
    }
}

def get_vehicle_info(search_term):
    """Recherche un véhicule dans la base de données simulée (insensible à la casse)."""
    search_term = search_term.upper().replace(" ", "")
    if search_term in MOCK_DATABASE:
        return MOCK_DATABASE[search_term]
    
    # Recherche partielle pour faciliter les tests
    for key, data in MOCK_DATABASE.items():
        if search_term in key:
            return data
            
    return None

def main():
    st.set_page_config(page_title="Outil d'Analyse Pricing Auto", page_icon="🚗", layout="wide")
    
    st.title("🚗 Outil d'Analyse Pricing Automobile")
    st.markdown("Recherchez un véhicule par **Immatriculation** ou **Numéro de série (VIN)** pour obtenir ses caractéristiques détaillées.")
    
    # Formulaire de recherche
    search_term = st.text_input("Immatriculation ou VIN", placeholder="Ex: AB-123-CD ou VF1...")
    
    # Bouton de recherche
    if st.button("Rechercher", type="primary"):
        if search_term:
            with st.spinner("Recherche en cours..."):
                vehicle_data = get_vehicle_info(search_term)
                
                if vehicle_data:
                    st.success(f"Véhicule trouvé ! ({search_term.upper()})")
                    
                    # Mise en page avec 2 colonnes : Informations | Image
                    col1, col2 = st.columns([1, 1])
                    
                    with col1:
                        st.subheader("Caractéristiques techniques")
                        st.write(f"**Marque :** {vehicle_data['marque']}")
                        st.write(f"**Modèle :** {vehicle_data['modele']}")
                        st.write(f"**Motorisation :** {vehicle_data['motorisation']}")
                        st.write(f"**Boîte de vitesse :** {vehicle_data['boite']}")
                        st.write(f"**Année de fabrication :** {vehicle_data['annee']}")
                        
                        st.subheader("Génération & Phase")
                        st.info(f"**Génération :** {vehicle_data['generation']}\n\n**Phase :** {vehicle_data['phase']}")
                        
                    with col2:
                        st.subheader("Illustration")
                        st.image(vehicle_data['image_url'], caption=f"{vehicle_data['marque']} {vehicle_data['modele']} - {vehicle_data['phase']}", use_column_width=True)
                        
                else:
                    st.error("Véhicule introuvable. Veuillez vérifier l'immatriculation ou le VIN.")
                    st.info("Pour le test, essayez 'AB-123-CD', 'EF-456-GH' ou 'VF1RJA00000000001'.")
        else:
            st.warning("Veuillez saisir une immatriculation ou un VIN.")

if __name__ == "__main__":
    main()
