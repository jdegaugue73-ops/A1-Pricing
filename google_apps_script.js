// =========================================================================
// SCRIPT GOOGLE APPS SCRIPT - GÉNÉRATEUR DE PLANNING
// =========================================================================

// Constantes
const SENIORS = ["Julien", "Damien"];
const MIDDLES = ["Pierre V", "Pierre D", "Benoit", "Quentin"];
const ALL_MEMBERS = [...SENIORS, ...MIDDLES];
const DAYS = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi"];
const PERIODS = ["Matin", "Après-midi"];

const SENIOR_TASKS = ["out PF seniors", "PF"];
const MIDDLE_TASKS = ["Pricing", "Out PF middle", "On PF"];

// Cette fonction crée un menu spécial dans Google Sheets à l'ouverture du fichier
function onOpen() {
  var ui = SpreadsheetApp.getUi();
  ui.createMenu('📅 Planning Équipe')
      .addItem('1. Initialiser la grille', 'initGrid')
      .addItem('2. Générer le planning', 'generatePlanning')
      .addToUi();
}

// Fonction pour préparer la grille vide
function initGrid() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  sheet.clear();

  // En-têtes fixes
  sheet.getRange(1, 1).setValue("Jour").setBackground("#f8f9fa").setFontWeight("bold");
  sheet.getRange(1, 2).setValue("Période").setBackground("#f8f9fa").setFontWeight("bold");

  // Seniors
  sheet.getRange(1, 3, 1, 2).merge().setValue("Seniors").setBackground("#dbe4eb").setHorizontalAlignment("center").setFontWeight("bold");
  sheet.getRange(2, 3).setValue("Julien").setBackground("#e6f2ff").setHorizontalAlignment("center").setFontWeight("bold");
  sheet.getRange(2, 4).setValue("Damien").setBackground("#e6f2ff").setHorizontalAlignment("center").setFontWeight("bold");

  // Middles
  sheet.getRange(1, 5, 1, 4).merge().setValue("Middles").setBackground("#e9ecef").setHorizontalAlignment("center").setFontWeight("bold");
  sheet.getRange(2, 5).setValue("Pierre V").setBackground("#f8f9fa").setHorizontalAlignment("center").setFontWeight("bold");
  sheet.getRange(2, 6).setValue("Pierre D").setBackground("#f8f9fa").setHorizontalAlignment("center").setFontWeight("bold");
  sheet.getRange(2, 7).setValue("Benoit").setBackground("#f8f9fa").setHorizontalAlignment("center").setFontWeight("bold");
  sheet.getRange(2, 8).setValue("Quentin").setBackground("#f8f9fa").setHorizontalAlignment("center").setFontWeight("bold");

  var row = 3;
  for (var d = 0; d < DAYS.length; d++) {
    sheet.getRange(row, 1, 2, 1).merge().setValue(DAYS[d]).setVerticalAlignment("middle").setHorizontalAlignment("center").setFontWeight("bold").setBackground("#f8f9fa");
    sheet.getRange(row, 2).setValue("Matin").setBackground("#f8f9fa");
    sheet.getRange(row + 1, 2).setValue("Après-midi").setBackground("#f8f9fa");
    row += 2;
  }

  // Mise en forme
  sheet.getRange(1, 1, row - 1, 8).setBorder(true, true, true, true, true, true);
  sheet.setColumnWidth(1, 100);
  sheet.setColumnWidth(2, 100);
  for (var c = 3; c <= 8; c++) {
    sheet.setColumnWidth(c, 130);
  }

  // Appliquer le fond bleu clair pour les colonnes seniors par défaut
  sheet.getRange(3, 3, 12, 2).setBackground("#f1f8ff");

  SpreadsheetApp.getUi().alert("Grille initialisée !\n\nVous pouvez maintenant écrire 'OFF' dans les cases où les collaborateurs sont absents.\nUne fois terminé, utilisez le menu '📅 Planning Équipe > 2. Générer le planning'.");
}

// Fonction pour calculer et afficher le planning
function generatePlanning() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  var data = sheet.getRange(3, 3, 12, 6).getValues();

  // 1. Lire les OFF
  var offSlots = {};
  ALL_MEMBERS.forEach(function(person) { offSlots[person] = []; });

  for (var r = 0; r < 12; r++) {
    var dayIdx = Math.floor(r / 2);
    var periodIdx = r % 2;
    var pid = DAYS[dayIdx] + "_" + PERIODS[periodIdx];

    for (var c = 0; c < 6; c++) {
      var val = String(data[r][c]).trim().toUpperCase();
      if (val === "OFF") {
        offSlots[ALL_MEMBERS[c]].push(pid);
      }
    }
  }

  // 2. Initialiser les compteurs
  var taskCounts = {};
  ALL_MEMBERS.forEach(function(p) {
    taskCounts[p] = {};
    SENIOR_TASKS.forEach(function(t) { taskCounts[p][t] = 0; });
    MIDDLE_TASKS.forEach(function(t) { taskCounts[p][t] = 0; });
  });

  var schedule = {};

  // 3. Assigner les tâches
  DAYS.forEach(function(day) {
    PERIODS.forEach(function(period) {
      var pid = day + "_" + period;
      schedule[pid] = {};
      ALL_MEMBERS.forEach(function(p) { schedule[pid][p] = []; });

      // Seniors
      var availableSeniors = SENIORS.filter(function(s) { return offSlots[s].indexOf(pid) === -1; });
      if (availableSeniors.length > 0) {
        shuffleArray(availableSeniors);
        SENIOR_TASKS.forEach(function(task) {
          availableSeniors.sort(function(a, b) {
            if (schedule[pid][a].length !== schedule[pid][b].length) {
              return schedule[pid][a].length - schedule[pid][b].length;
            }
            if (taskCounts[a][task] !== taskCounts[b][task]) {
              return taskCounts[a][task] - taskCounts[b][task];
            }
            var totalA = Object.keys(taskCounts[a]).reduce(function(sum, key) { return sum + taskCounts[a][key]; }, 0);
            var totalB = Object.keys(taskCounts[b]).reduce(function(sum, key) { return sum + taskCounts[b][key]; }, 0);
            return totalA - totalB;
          });
          var chosen = availableSeniors[0];
          schedule[pid][chosen].push(task);
          taskCounts[chosen][task]++;
        });
      }

      // Middles
      var availableMiddles = MIDDLES.filter(function(m) { return offSlots[m].indexOf(pid) === -1; });
      if (availableMiddles.length > 0) {
        shuffleArray(availableMiddles);
        MIDDLE_TASKS.forEach(function(task) {
          availableMiddles.sort(function(a, b) {
            if (schedule[pid][a].length !== schedule[pid][b].length) {
              return schedule[pid][a].length - schedule[pid][b].length;
            }
            if (taskCounts[a][task] !== taskCounts[b][task]) {
              return taskCounts[a][task] - taskCounts[b][task];
            }
            var totalA = Object.keys(taskCounts[a]).reduce(function(sum, key) { return sum + taskCounts[a][key]; }, 0);
            var totalB = Object.keys(taskCounts[b]).reduce(function(sum, key) { return sum + taskCounts[b][key]; }, 0);
            return totalA - totalB;
          });
          var chosen = availableMiddles[0];
          schedule[pid][chosen].push(task);
          taskCounts[chosen][task]++;
        });

        // Fallback Pricing pour le middle restant
        availableMiddles.forEach(function(m) {
          if (schedule[pid][m].length === 0) {
            schedule[pid][m].push("Pricing");
            taskCounts[m]["Pricing"]++;
          }
        });
      }
    });
  });

  // 4. Mettre à jour la grille
  var outData = [];
  var outColors = [];
  var outFonts = [];

  for (var r = 0; r < 12; r++) {
    var rowData = [];
    var rowColors = [];
    var rowFonts = [];
    var dayIdx = Math.floor(r / 2);
    var periodIdx = r % 2;
    var pid = DAYS[dayIdx] + "_" + PERIODS[periodIdx];

    for (var c = 0; c < 6; c++) {
      var person = ALL_MEMBERS[c];
      var isSenior = c < 2;
      var defaultBg = isSenior ? "#f1f8ff" : "#ffffff";

      if (offSlots[person].indexOf(pid) !== -1) {
        rowData.push("OFF");
        rowColors.push("#e9ecef");
        rowFonts.push("italic");
      } else {
        var tasks = schedule[pid][person];
        if (tasks.length === 0) {
          rowData.push("-");
          rowColors.push(defaultBg);
          rowFonts.push("normal");
        } else {
          rowData.push(tasks.join(" + "));
          rowColors.push(defaultBg);
          rowFonts.push("normal");
        }
      }
    }
    outData.push(rowData);
    outColors.push(rowColors);
    outFonts.push(rowFonts);
  }

  var gridRange = sheet.getRange(3, 3, 12, 6);
  gridRange.setValues(outData);
  gridRange.setBackgrounds(outColors);
  gridRange.setFontStyles(outFonts);
  gridRange.setHorizontalAlignment("center").setVerticalAlignment("middle");

  // 5. Afficher les compteurs détaillés
  var totalRow = 16;
  sheet.getRange(totalRow, 1, 2, 8).clear(); // Nettoyer
  sheet.getRange(totalRow, 1, 1, 2).merge().setValue("Détail des tâches :").setHorizontalAlignment("right").setFontWeight("bold").setBackground("#f8f9fa").setVerticalAlignment("top");

  for (var c = 0; c < 6; c++) {
    var person = ALL_MEMBERS[c];
    var isSenior = c < 2;
    var bg = isSenior ? "#f1f8ff" : "#f8f9fa";

    var details = [];
    var counts = taskCounts[person];
    var sortedKeys = Object.keys(counts).sort(function(a,b) { return counts[b] - counts[a]; });

    for (var i = 0; i < sortedKeys.length; i++) {
      var k = sortedKeys[i];
      if (counts[k] > 0) {
        details.push(counts[k] + " : " + k);
      }
    }
    var detailStr = details.length > 0 ? details.join("\n") : "Aucune tâche";

    var cell = sheet.getRange(totalRow, c + 3);
    cell.setValue(detailStr).setBackground(bg).setVerticalAlignment("top").setHorizontalAlignment("left");
  }

  sheet.setRowHeight(totalRow, 80);

  // Bordure globale
  sheet.getRange(1, 1, 14, 8).setBorder(true, true, true, true, true, true);
  sheet.getRange(totalRow, 1, 1, 8).setBorder(true, true, true, true, true, true);
}

// Fonction utilitaire pour mélanger un tableau
function shuffleArray(array) {
  for (var i = array.length - 1; i > 0; i--) {
    var j = Math.floor(Math.random() * (i + 1));
    var temp = array[i];
    array[i] = array[j];
    array[j] = temp;
  }
}
