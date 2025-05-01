window.addEventListener('DOMContentLoaded', () => {
  // File Upload Elements
  const uploadBox = document.getElementById('file-upload-box');
  const fileInput = document.getElementById('file-input');
  const uploadedFiles = document.getElementById('uploaded-files');

  uploadBox.addEventListener('click', () => fileInput.click());
  uploadBox.addEventListener('dragover', e => { e.preventDefault(); uploadBox.classList.add('dragover'); });
  uploadBox.addEventListener('dragleave', () => uploadBox.classList.remove('dragover'));
  uploadBox.addEventListener('drop', e => { e.preventDefault(); uploadBox.classList.remove('dragover'); handleFiles(e.dataTransfer.files); });
  fileInput.addEventListener('change', () => handleFiles(fileInput.files));

  // Load existing uploads
  loadUploadedFiles();

  // Socket.IO Logs
  const socket = io();
  let logs = JSON.parse(localStorage.getItem('printerLogs') || '[]');
  const logDiv = document.getElementById('log-output');

  // Restore logs
  logs.forEach(entry => {
    const p = document.createElement('p');
    p.innerText = entry;
    logDiv.appendChild(p);
  });

  socket.on('new_log', data => {
    const logEntry = `[${data.timestamp}] Layer ${data.layer} | Z: ${data.position_z} | Scan: ${data.scan}`;
    logs.push(logEntry);
    if (logs.length > 500) logs.shift();
    localStorage.setItem('printerLogs', JSON.stringify(logs));

    const p = document.createElement('p');
    p.innerText = logEntry;
    logDiv.appendChild(p);
    logDiv.scrollTop = logDiv.scrollHeight;
  });

  // Expose clearLogs globally
  window.clearLogs = () => {
    logs = [];
    localStorage.setItem('printerLogs', JSON.stringify([]));  // overwrite with empty array
    logDiv.innerHTML = '';
  };

  
  function handleFiles(files) {
    const formData = new FormData();
    for (const file of files) formData.append(file.name, file);
    fetch('/upload', { method: 'POST', body: formData })
      .then(res => res.json())
      .then(loadUploadedFiles)
      .catch(() => { uploadedFiles.textContent = 'Error uploading files.'; });
  }

  function loadUploadedFiles() {
    fetch('/uploaded-files')
      .then(res => res.json())
      .then(data => {
        if (!uploadedFiles) return;
        if (!data.files.length) { uploadedFiles.innerHTML = ''; return; }

        let html = '<strong>Uploaded Files:</strong><ul>';
        data.files.forEach(fname => {
          const cls = fname.endsWith('.gcode') ? 'gcode' : fname.endsWith('.stl') ? 'stl' : '';
          html += `<li class="${cls}">${fname} <button class="delete-file" data-filename="${fname}">×</button></li>`;
        });
        html += '</ul>';
        uploadedFiles.innerHTML = html;

        document.querySelectorAll('.delete-file').forEach(btn => {
          btn.addEventListener('click', () => {
            fetch(`/delete-file/${encodeURIComponent(btn.dataset.filename)}`, { method: 'POST' })
              .then(loadUploadedFiles);
          });
        });

        const changeBtn = document.getElementById('change-printer-btn');
        const printerForm = document.getElementById('printer-form');
        const currentPrinterWrapper = changeBtn ? changeBtn.parentElement : null;

        if (changeBtn && printerForm && currentPrinterWrapper) {
          changeBtn.addEventListener('click', () => {
          printerForm.style.display = 'block';
          currentPrinterWrapper.style.display = 'none';
    });
  }

      });
  }
});