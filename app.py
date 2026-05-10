import streamlit as st
import pandas as pd

def calculate_variable(row):
    try:
        ventes = float(row["Ventes (%)"])
        conversion = float(row["Conversion (%)"])
        marges_neg = float(row["Marges Négatives (%)"])
    except (ValueError, TypeError):
        return pd.Series([0, 0, 0, 0, 0])

    # Nouveaux Poids: Ventes 30% (300), Conversion 50% (500), Marges neg 20% (200)
    
    # 1. Ventes (Obj 90%)
    bonus_ventes = (ventes / 90.0) * 300

    # 2. Conversion (Obj 11%)
    bonus_conv = (conversion / 11.0) * 500

    # 3. Marges négatives (Obj <= 20%)
    # Formule : 200 + (20 - marges_neg) * 20
    bonus_marges = 200 + (20 - marges_neg) * 20
    if bonus_marges < 0:
        bonus_marges = 0

    total = bonus_ventes + bonus_conv + bonus_marges

    # Plafond à 1300
    total_plafonne = min(total, 1300.0)

    return pd.Series([
        round(bonus_ventes),
        round(bonus_conv),
        round(bonus_marges),
        round(total),
        round(total_plafonne)
    ])

def main():
    st.set_page_config(page_title="Calculateur de Rémunération Variable", page_icon="💰", layout="wide")

    st.title("💰 Calculateur de Rémunération Variable (Équipe de 9)")
    st.markdown("""
    Cet outil permet de calculer la part variable du salaire pour vos collaborateurs.

    **Règles de calcul (Base 1000€) :**
    - **Conversion** (Objectif 11%) : Poids **50%** (500€)
    - **Ventes** (Objectif 90%) : Poids **30%** (300€)
    - **Marges Négatives** (Objectif ≤ 20%) : Poids **20%** (200€)

    *Le total est déplafonné mais **limité à 1300€ maximum**.*
    """)

    # Initialisation des données pour 9 personnes
    if "data" not in st.session_state:
        st.session_state.data = pd.DataFrame({
            "Nom du collaborateur": [f"Collaborateur {i+1}" for i in range(9)],
            "Ventes (%)": [90.0, 70.0, 80.0, 85.0, 95.0, 100.0, 110.0, 90.0, 85.0],
            "Conversion (%)": [11.0, 8.0, 13.0, 10.0, 12.0, 13.0, 15.0, 11.0, 10.0],
            "Marges Négatives (%)": [20.0, 25.0, 20.0, 5.0, 30.0, 10.0, 0.0, 15.0, 10.0]
        })

    st.subheader("Saisie des performances")
    st.info("Modifiez directement les valeurs dans le tableau ci-dessous. Les calculs se mettront à jour automatiquement.")

    # Tableau éditable
    edited_df = st.data_editor(
        st.session_state.data,
        num_rows="fixed",
        width="stretch",
        hide_index=True,
        column_config={
            "Nom du collaborateur": st.column_config.TextColumn("Nom"),
            "Ventes (%)": st.column_config.NumberColumn("Ventes (%)", min_value=0.0, format="%.1f %%"),
            "Conversion (%)": st.column_config.NumberColumn("Conversion (%)", min_value=0.0, format="%.1f %%"),
            "Marges Négatives (%)": st.column_config.NumberColumn("Marges Négatives (%)", min_value=0.0, format="%.1f %%"),
        }
    )

    # Sauvegarde des modifications
    st.session_state.data = edited_df

    st.subheader("Résultats : Montants des Variables")
    
    # Application du calcul
    results_df = edited_df.copy()
    results_df[["Bonus Ventes (€)", "Bonus Conv. (€)", "Bonus Marges (€)", "Total Brut (€)", "Total à Payer (€)"]] = results_df.apply(calculate_variable, axis=1)
    
    # Formatage des colonnes de résultats
    st.dataframe(
        results_df,
        width="stretch",
        hide_index=True,
        column_config={
            "Nom du collaborateur": st.column_config.TextColumn("Nom"),
            "Ventes (%)": st.column_config.NumberColumn(format="%.1f %%"),
            "Conversion (%)": st.column_config.NumberColumn(format="%.1f %%"),
            "Marges Négatives (%)": st.column_config.NumberColumn(format="%.1f %%"),
            "Bonus Ventes (€)": st.column_config.NumberColumn("Bonus Ventes", format="%d €"),
            "Bonus Conv. (€)": st.column_config.NumberColumn("Bonus Conv.", format="%d €"),
            "Bonus Marges (€)": st.column_config.NumberColumn("Bonus Marges", format="%d €"),
            "Total Brut (€)": st.column_config.NumberColumn("Total Brut", format="%d €"),
            "Total à Payer (€)": st.column_config.NumberColumn("Total à Payer (Max 1300€)", format="%d €", width="medium"),
        }
    )
    
    # Export CSV
    csv = results_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Télécharger les résultats (CSV)",
        data=csv,
        file_name='calcul_variables_equipe.csv',
        mime='text/csv',
    )

if __name__ == "__main__":
    main()
