const { app, BrowserWindow, ipcMain } = require('electron/main');
const path = require('node:path');

const createWindow = () => {
  const win = new BrowserWindow({
    title: "Pattern Pilot",
    width: 800,
    height: 600
  });

  const appURL = "http://127.0.0.1:8000/";

  win.loadURL(appURL)
}

app.whenReady().then(() => {
    createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  })
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});