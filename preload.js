const { contextBridge, ipcRenderer } = require('electron');
contextBridge.exposeInMainWorld('appConfig', { get: () => ipcRenderer.invoke('cfg') });
