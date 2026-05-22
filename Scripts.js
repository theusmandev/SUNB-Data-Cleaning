function checkLinksInBatches() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  
  if (sheet.getRange("C1").isBlank()) {
    sheet.getRange("C1").setValue("Status");
  }
  
  var properties = PropertiesService.getScriptProperties();
  var startRow = parseInt(properties.getProperty('LAST_ROW_PROCESSED')) || 2;
  var totalRows = sheet.getLastRow();
  
  if (startRow > totalRows) {
    Logger.log("✅ Saara data check ho chuka hai!");
    return;
  }

  var batchSize = 500; 
  var endRow = Math.min(startRow + batchSize - 1, totalRows);
  var numRowsToFetch = endRow - startRow + 1;
  
  Logger.log("Row " + startRow + " se " + endRow + " tak fetch ho raha hai...");
  
  var range = sheet.getRange(startRow, 1, numRowsToFetch, 3);
  var data = range.getValues();
  
  var linkColIndex = 1;  
  var statusColIndex = 2; 

  for (var i = 0; i < data.length; i++) {
    var link = data[i][linkColIndex];
    var currentStatus = data[i][statusColIndex] || ""; 
    var actualRowNumber = startRow + i;
    
    if (currentStatus !== "" || !link || link.toString().trim() === "") {
      continue; 
    }
    
    var isWorking = checkSingleLink(link);
    
    if (isWorking) {
      sheet.getRange(actualRowNumber, statusColIndex + 1).setValue("Working");
      sheet.getRange(actualRowNumber, statusColIndex + 1).setBackground("#d9ead3"); 
    } else {
      sheet.getRange(actualRowNumber, statusColIndex + 1).setValue("Dead Link");
      sheet.getRange(actualRowNumber, statusColIndex + 1).setBackground("#f4cccc"); 
    }
  }
  
  properties.setProperty('LAST_ROW_PROCESSED', endRow + 1);
  Logger.log("Batch complete! Agli baar Row " + (endRow + 1) + " se start hoga.");
}

function checkSingleLink(url) {
  try {
    if (url.indexOf("drive.google.com") !== -1) {
      var fileId = "";
      var match = url.match(/\/file\/d\/([a-zA-Z0-9_-]+)/) || url.match(/id=([a-zA-Z0-9_-]+)/);
      if (match) {
        fileId = match[1];
      } else {
        return false; 
      }
      
      try {
        DriveApp.getFileById(fileId);
        return true; 
      } catch (e) {
        return false; 
      }
    }
    
    if (url.indexOf("mediafire.com") !== -1) {
      var mfOptions = { muteHttpExceptions: true, followRedirects: true };
      var mfResponse = UrlFetchApp.fetch(url, mfOptions);
      var mfStatusCode = mfResponse.getResponseCode();
      var mfContent = mfResponse.getContentText().toLowerCase();
      
      if (mfStatusCode === 404) return false;
      
      if (mfContent.indexOf("file has been removed") !== -1 || 
          mfContent.indexOf("invalid or deleted file") !== -1 || 
          mfContent.indexOf("permission denied") !== -1) {
        return false;
      }
      return true;
    }
    
    var genericOptions = { muteHttpExceptions: true, followRedirects: true };
    var genericResponse = UrlFetchApp.fetch(url, genericOptions);
    if (genericResponse.getResponseCode() >= 400) return false;
    
    return true;
    
  } catch (e) {
    return false; 
  }
}

function CLEAR_ALL_STATUS() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  var lastRow = sheet.getLastRow();
  
  if (lastRow > 1) {
    var range = sheet.getRange(2, 3, lastRow - 1, 1);
    range.clearContent();
    range.setBackground(null); 
  }
  
  PropertiesService.getScriptProperties().setProperty('LAST_ROW_PROCESSED', 2);
  Logger.log("✅ Saara purana status clear ho gaya hai!");
}

function RESET_COUNTER() {
  PropertiesService.getScriptProperties().setProperty('LAST_ROW_PROCESSED', 2);
  Logger.log("Counter reset ho gaya hai.");
}


// =============== NAYA AUR BEHTAREEN SEPARATE FUNCTION ===============
function SEPARATE_DEAD_LINKS() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sourceSheet = ss.getActiveSheet(); 
  
  // Progress Toast: Start
  ss.toast("Data scan ho raha hai. Kripya thoda intezar karein...", "Step 1/4", 10);
  
  var fullRange = sourceSheet.getDataRange();
  var data = fullRange.getValues();
  var backgrounds = fullRange.getBackgrounds(); // Colors bhi ek sath copy kar liye (Fastest way)
  
  var workingRows = [];
  var workingBgs = [];
  var deadRows = [];
  var deadBgs = [];
  
  // Headers add karna
  workingRows.push(data[0]); 
  workingBgs.push(backgrounds[0]);
  
  for (var i = 1; i < data.length; i++) {
    var status = data[i][2]; // Column C
    
    if (status === "Dead Link") {
      deadRows.push(data[i]); 
      deadBgs.push(backgrounds[i]);
    } else {
      workingRows.push(data[i]); 
      workingBgs.push(backgrounds[i]);
    }
  }
  
  if (deadRows.length === 0) {
    SpreadsheetApp.getUi().alert("Koi 'Dead Link' nahi mila!");
    return;
  }
  
  // Progress Toast: Result mila
  ss.toast("Total " + deadRows.length + " dead links milay. Unhe archive mein transfer kar rahe hain...", "Step 2/4", 10);
  
  var targetSheetName = "Dead_Links_Archive";
  var targetSheet = ss.getSheetByName(targetSheetName);
  
  if (!targetSheet) {
    targetSheet = ss.insertSheet(targetSheetName);
    var headers = sourceSheet.getRange(1, 1, 1, sourceSheet.getLastColumn()).getValues();
    targetSheet.getRange(1, 1, 1, headers[0].length).setValues(headers);
    targetSheet.getRange(1, 1, 1, headers[0].length).setFontWeight("bold");
  }
  
  // Dead Rows Transfer (Sirf 2 bulk operations = zero crash chance)
  var nextRow = targetSheet.getLastRow() + 1;
  targetSheet.getRange(nextRow, 1, deadRows.length, deadRows[0].length).setValues(deadRows);
  targetSheet.getRange(nextRow, 1, deadBgs.length, deadBgs[0].length).setBackgrounds(deadBgs); 
  
  // Progress Toast: Original saaf ho rahi hai
  ss.toast("Dead links transfer ho gaye. Ab original sheet saaf ki ja rahi hai...", "Step 3/4", 10);
  
  // Original Sheet Safai aur Rewrite
  sourceSheet.getDataRange().clearContent();
  sourceSheet.getDataRange().setBackground(null);
  
  if (workingRows.length > 0) {
    sourceSheet.getRange(1, 1, workingRows.length, workingRows[0].length).setValues(workingRows);
    sourceSheet.getRange(1, 1, workingBgs.length, workingBgs[0].length).setBackgrounds(workingBgs);
  }
  
  // Progress Toast: Mukammal
  ss.toast("Kamyabi! Process mukammal ho gaya.", "Step 4/4", 5);
  SpreadsheetApp.getUi().alert("Kamyabi!\n\nTotal " + deadRows.length + " Dead Links 'Dead_Links_Archive' sheet mein move kar diye gaye hain.");
}