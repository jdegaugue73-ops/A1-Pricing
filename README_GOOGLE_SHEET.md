# Générateur de Planning d'Équipe (Version Google Sheets)

Ce guide explique comment installer et utiliser le générateur de planning directement dans **Google Sheets**. Cette solution permet d'avoir tout au même endroit, avec un bouton pour générer automatiquement le planning.

## 1. Installation (À faire une seule fois)

1. Ouvrez un nouveau fichier **Google Sheets** (ou un fichier existant).
2. Dans le menu en haut, cliquez sur **Extensions** > **Apps Script**.
3. Un nouvel onglet s'ouvre. Supprimez tout le code existant dans l'éditeur.
4. Ouvrez le fichier `google_apps_script.js` (fourni dans ce dossier), copiez tout son contenu, et collez-le dans l'éditeur Apps Script.
5. Cliquez sur l'icône de disquette 💾 (Enregistrer le projet) en haut.
6. Vous pouvez fermer l'onglet Apps Script et retourner sur votre Google Sheet.
7. **Rafraîchissez la page** de votre Google Sheet (F5).

*Note : Lors de la première exécution, Google vous demandera des autorisations. Cliquez sur "Continuer", choisissez votre compte Google, cliquez sur "Paramètres avancés", puis sur "Aller à [Nom du script] (non sécurisé)" et enfin sur "Autoriser".*

## 2. Utilisation

Après avoir rafraîchi la page, vous verrez un nouveau menu en haut de votre Google Sheet appelé **📅 Planning Équipe**.

### Étape 1 : Préparer la grille
1. Cliquez sur **📅 Planning Équipe** > **1. Initialiser la grille**.
2. Le script va créer automatiquement le tableau avec les jours de la semaine (Lundi à Samedi, Matin et Après-midi) et les noms de l'équipe (Seniors et Middles).
   * Les colonnes des Seniors sont grisées/bleutées pour les distinguer facilement.

### Étape 2 : Indiquer les jours OFF
1. Dans la grille qui vient d'être générée, tapez simplement le mot **OFF** dans les cases où une personne est absente.
   * *Par exemple : Si Damien est absent mardi après-midi, tapez "OFF" dans la case correspondante à Damien.*

### Étape 3 : Générer le planning
1. Une fois tous les "OFF" renseignés, cliquez sur **📅 Planning Équipe** > **2. Générer le planning**.
2. Le script va automatiquement :
   * Distribuer les tâches de manière équitable.
   * Assigner "Pricing" comme tâche par défaut pour le 4ème Middle s'il n'a pas de tâche principale ce jour-là.
   * Respecter les jours OFF (qui s'afficheront en gris italique).
   * Afficher un récapitulatif détaillé des tâches assignées (compteurs) tout en bas de la grille.

Vous pouvez modifier manuellement les cases générées si besoin. Si vous changez les "OFF", vous pouvez simplement re-cliquer sur "2. Générer le planning" pour calculer une nouvelle répartition.