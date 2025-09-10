const { app, BrowserWindow, ipcMain } = require('electron')
const path = require('path')
const isDev = !app.isPackaged

let mainWindow

function createWindow() {
  // Create the browser window
  mainWindow = new BrowserWindow({
    width: 1400,
    height: 900,
    minWidth: 800,
    minHeight: 600,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      enableRemoteModule: false,
      preload: path.join(__dirname, 'preload.js')
    },
    frame: true,
    titleBarStyle: 'default',
    backgroundColor: '#0f172a',
    show: false,
    icon: path.join(__dirname, 'assets/icon.png') // Add icon if available
  })

  // Load the app
  if (isDev) {
    mainWindow.loadURL('http://localhost:5174')
    // Open DevTools in development
    mainWindow.webContents.openDevTools()
  } else {
    mainWindow.loadFile(path.join(__dirname, '../dist/index.html'))
  }

  // Show window when ready
  mainWindow.once('ready-to-show', () => {
    mainWindow.show()
    
    if (isDev) {
      mainWindow.webContents.openDevTools()
    }
  })

  // Handle window closed
  mainWindow.on('closed', () => {
    mainWindow = null
  })
}

// This method will be called when Electron has finished initialization
app.whenReady().then(() => {
  createWindow()

  app.on('activate', () => {
    // On macOS it's common to re-create a window in the app when the
    // dock icon is clicked and there are no other windows open
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow()
    }
  })
})

// Quit when all windows are closed, except on macOS
app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
  }
})

// Security: Prevent navigation to external websites
app.on('web-contents-created', (event, contents) => {
  contents.on('new-window', (navigationEvent, url) => {
    navigationEvent.preventDefault()
  })

  contents.on('will-navigate', (navigationEvent, url) => {
    if (url !== mainWindow.webContents.getURL()) {
      navigationEvent.preventDefault()
    }
  })
})

// Handle IPC messages (for future AI integration)
ipcMain.handle('ai-request', async (event, message) => {
  // Placeholder for AI API calls
  return { response: `Echo: ${message}` }
})

// Handle app protocol for custom schemes (if needed)
if (isDev) {
  app.setAsDefaultProtocolClient('arise-ai', process.execPath, [
    path.resolve(process.argv[1])
  ])
} else {
  app.setAsDefaultProtocolClient('arise-ai')
}
