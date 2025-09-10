const { contextBridge, ipcRenderer } = require('electron')

// Expose protected methods that allow the renderer process to use
// the ipcRenderer without exposing the entire object
contextBridge.exposeInMainWorld('electronAPI', {
  // AI Assistant APIs
  sendAIRequest: (message) => ipcRenderer.invoke('ai-request', message),
  
  // System APIs
  getAppVersion: () => ipcRenderer.invoke('get-app-version'),
  
  // Window controls (if needed)
  minimizeWindow: () => ipcRenderer.invoke('minimize-window'),
  maximizeWindow: () => ipcRenderer.invoke('maximize-window'),
  closeWindow: () => ipcRenderer.invoke('close-window'),
  
  // File system (for future use)
  openFileDialog: () => ipcRenderer.invoke('open-file-dialog'),
  saveFileDialog: (content) => ipcRenderer.invoke('save-file-dialog', content),
  
  // Notifications
  showNotification: (title, body) => ipcRenderer.invoke('show-notification', title, body)
})

// Listen for theme changes or other app events
window.addEventListener('DOMContentLoaded', () => {
  console.log('Arise AI Electron App Loaded')
})
