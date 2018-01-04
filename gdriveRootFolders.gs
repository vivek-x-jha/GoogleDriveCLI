/**
 * The function in this script will be called by the Apps Script Execution API.
 */

/**
 * Return the set of folder names contained in the user's root folder as an
 * object (with folder IDs as keys).
 *
 * @return {Object} A set of folder names keyed by folder ID.
 */
function getFoldersUnderRoot() {
  
  var root = DriveApp.getRootFolder();
  var folders = root.getFolders();
  var folderSet = {};
  
  while (folders.hasNext()) {
    
    var folder = folders.next();
    folderSet[folder.getId()] = folder.getName();
    Logger.log(folder.getId());
    Logger.log(folderSet[folder.getId()]);
    
  }
  
  return folderSet;
  
}
