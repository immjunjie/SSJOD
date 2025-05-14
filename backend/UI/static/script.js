window.addEventListener('DOMContentLoaded', () => {
  const uploadBox = document.getElementById('file-upload-box');
  const fileInput = document.getElementById('file-input');
  const uploadedFiles = document.getElementById('uploaded-files');
  const logDiv = document.getElementById('log-output');
  const timerDisplay = document.getElementById('timer-display');
  const socket = io();

  uploadBox.addEventListener('click', () => fileInput.click());
  uploadBox.addEventListener('dragover', e => { e.preventDefault(); uploadBox.classList.add('dragover'); });
  uploadBox.addEventListener('dragleave', () => uploadBox.classList.remove('dragover'));
  uploadBox.addEventListener('drop', e => { e.preventDefault(); uploadBox.classList.remove('dragover'); handleFiles(e.dataTransfer.files); });
  fileInput.addEventListener('change', () => handleFiles(fileInput.files));

  // timer input, no limit button
  const checkbox = document.getElementById("unlimitedDuration");
  const durationInputGroup = document.querySelector(".duration-input");

  checkbox.addEventListener("change", function () {
    durationInputGroup.style.display = this.checked ? "none" : "flex";
  });


  // Load existing uploads
  loadUploadedFiles();

  // Socket.IO Logs

  let logs = JSON.parse(localStorage.getItem('printerLogs') || '[]');
  logs.forEach(entry => {
    const p = document.createElement('p');
    p.innerText = entry;
    logDiv?.appendChild(p);
  });


  socket.on('new_log', data => {
    let logEntry = `[${data.timestamp}] Layer ${data.layer} | Scan: ${data.scan}`;

    if (data.endpoint_data) {
      for (const [key, value] of Object.entries(data.endpoint_data)) {
        logEntry += ` | ${key}: ${value}`;
      }
    }
    logs.push(logEntry);
    if (logs.length > 500) logs.shift(); // Keep max 500
    localStorage.setItem('printerLogs', JSON.stringify(logs));

    const p = document.createElement('p');
    p.innerText = logEntry;
    const isAtBottom = logDiv.scrollHeight - logDiv.scrollTop <= logDiv.clientHeight + 5;
    logDiv.appendChild(p);
    if (isAtBottom) logDiv.scrollTop = logDiv.scrollHeight;
  });

  window.clearLogs = () => {
    logs = [];
    localStorage.setItem('printerLogs', JSON.stringify([]));
    if (logDiv) logDiv.innerHTML = '';
  };

  function updateTimerDisplay() {
    const hrs = String(Math.floor(secondsLeft / 3600)).padStart(2, '0');
    const mins = String(Math.floor((secondsLeft % 3600) / 60)).padStart(2, '0');
    const secs = String(secondsLeft % 60).padStart(2, '0');
    timerDisplay.textContent = `${hrs}:${mins}:${secs}`;
  }

  let secondsLeft = 0;
  if (timerDisplay && timerDisplay.dataset.seconds) {
    secondsLeft = parseInt(timerDisplay.dataset.seconds, 10);
  }

  updateTimerDisplay();
  const countdownInterval = setInterval(() => {
    secondsLeft -= 1;
    if (secondsLeft < 0) {
      clearInterval(countdownInterval);
      window.location.reload();
    } else {
      updateTimerDisplay();
    }
  }, 1000);

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

        let html = '<strong>Uploaded Files:</strong><ul>';
        let hasGcode = false, hasStl = false;

        data.files.forEach(fname => {
          const cls = fname.endsWith('.gcode') ? 'gcode' : fname.endsWith('.stl') ? 'stl' : '';
          if (cls === 'gcode') hasGcode = true;
          if (cls === 'stl') hasStl = true;
          html += `<li class="${cls}">${fname} <button class="delete-file" data-filename="${fname}">×</button></li>`;
        });

        if (!hasGcode) html += `<li class="gcode placeholder">G-code file required.</li>`;
        if (!hasStl) html += `<li class="stl placeholder">STL file required.</li>`;
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

  loadUploadedFiles(); // Initial call
});

socket.on('logging_stopped', function () {
  window.location.reload();
});