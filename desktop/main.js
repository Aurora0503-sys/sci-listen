const { app, BrowserWindow, ipcMain, desktopCapturer, dialog } = require('electron');
const path = require('path');

let mainWindow;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1400,
    height: 900,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
      enableRemoteModule: true
    },
    title: '学术会议陪听助手 - 桌面版',
    icon: path.join(__dirname, 'icon.png') // 可选图标
  });

  mainWindow.loadFile('web/enhanced_sci_listen.html');

  // 开发模式下打开开发者工具
  if (process.env.NODE_ENV === 'development') {
    mainWindow.webContents.openDevTools();
  }
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});

// 获取音频源列表
ipcMain.handle('get-audio-sources', async () => {
  const sources = await desktopCapturer.getSources({
    types: ['audio', 'window', 'screen']
  });
  
  return sources.map(source => ({
    id: source.id,
    name: source.name,
    type: source.id.startsWith('screen:') ? 'screen' : 
          source.id.startsWith('window:') ? 'window' : 'audio'
  }));
});

// 获取音频流
ipcMain.handle('get-audio-stream', async (event, sourceId) => {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({
      audio: {
        mandatory: {
          chromeMediaSource: 'desktop',
          chromeMediaSourceId: sourceId
        }
      }
    });
    return stream;
  } catch (error) {
    console.error('获取音频流失败:', error);
    throw error;
  }
});

// 处理文件保存
ipcMain.handle('save-file', async (event, content, filename) => {
  const result = await dialog.showSaveDialog(mainWindow, {
    defaultPath: filename,
    filters: [
      { name: 'Text Files', extensions: ['txt'] },
      { name: 'Markdown Files', extensions: ['md'] },
      { name: 'All Files', extensions: ['*'] }
    ]
  });

  if (!result.canceled) {
    const fs = require('fs').promises;
    await fs.writeFile(result.filePath, content, 'utf8');
    return result.filePath;
  }
  return null;
});