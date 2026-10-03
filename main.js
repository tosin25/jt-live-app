const { app, BrowserWindow, screen, ipcMain } = require('electron');
const path = require('path'), fs = require('fs');
let op = null, out = null;

// Optional default settings (config.json sits next to this file; never committed to GitHub).
let cfg = {};
try { cfg = JSON.parse(fs.readFileSync(path.join(__dirname, 'config.json'), 'utf8')); } catch { }
ipcMain.handle('cfg', () => cfg);

const prefs = { backgroundThrottling: false, preload: path.join(__dirname, 'preload.js') };

// Projector = the first non-primary display if one is connected, otherwise the main screen.
function targetDisplay() {
  const prim = screen.getPrimaryDisplay();
  return screen.getAllDisplays().find(d => d.id !== prim.id) || prim;
}

function openOverlay() {
  if (out && !out.isDestroyed()) { out.show(); return; }
  const d = targetDisplay(), h = Math.round(d.bounds.height * 0.24);
  out = new BrowserWindow({
    x: d.bounds.x, y: d.bounds.y + d.bounds.height - h, width: d.bounds.width, height: h,
    frame: false, resizable: true, alwaysOnTop: true, skipTaskbar: true, hasShadow: false,
    backgroundColor: '#000000', webPreferences: prefs
  });
  out.setAlwaysOnTop(true, 'screen-saver');   // stay above EasyWorship's output window
  out.loadFile('index.html', { hash: 'display' });
  out.on('closed', () => { out = null; });
}

app.whenReady().then(() => {
  op = new BrowserWindow({ width: 1280, height: 800, title: 'Jesus Tabernacle', webPreferences: prefs });
  op.setMenuBarVisibility(false);
  op.loadFile('index.html');
  op.webContents.setWindowOpenHandler(({ url }) => {
    if (url.includes('#display')) openOverlay();
    return { action: 'deny' };
  });
  op.on('closed', () => app.quit());
});
app.on('window-all-closed', () => app.quit());
