const uploadBox = document.getElementById('file-upload-box');
const fileInput = document.getElementById('file-input');
const uploadedFiles = document.getElementById('uploaded-files');

uploadBox.addEventListener('click', () => fileInput.click());

uploadBox.addEventListener('dragover', (e) => {
  e.preventDefault();
  uploadBox.classList.add('dragover');
});

uploadBox.addEventListener('dragleave', () => {
  uploadBox.classList.remove('dragover');
});

uploadBox.addEventListener('drop', (e) => {
  e.preventDefault();
  uploadBox.classList.remove('dragover');
  handleFiles(e.dataTransfer.files);
});

fileInput.addEventListener('change', () => {
  handleFiles(fileInput.files);
});

window.addEventListener('DOMContentLoaded', () => {
  loadUploadedFiles();
});

function handleFiles(files) {
  const formData = new FormData();
  for (const file of files) {
    formData.append(file.name, file);
  }

  fetch('/upload', {
    method: 'POST',
    body: formData
  })
    .then(res => res.json())
    .then(() => {
      loadUploadedFiles();
    })
    .catch(err => {
      console.error(err);
      uploadedFiles.textContent = "Error uploading files.";
    });
}

function loadUploadedFiles() {
  fetch('/uploaded-files')
    .then(response => response.json())
    .then(data => {
      if (!uploadedFiles) return;

      if (data.files.length === 0) {
        uploadedFiles.innerHTML = '';
        return;
      }

      let html = "<strong>Uploaded Files:</strong><ul>";
      data.files.forEach(filename => {
        const typeClass = filename.endsWith('.gcode') ? 'gcode' :
                          filename.endsWith('.stl') ? 'stl' : '';
        html += `<li class="${typeClass}">
          ${filename}
          <button class="delete-file" data-filename="${filename}">clear</button>
        </li>`;
      });
      html += "</ul>";
      uploadedFiles.innerHTML = html;

      document.querySelectorAll('.delete-file').forEach(btn => {
        btn.addEventListener('click', () => {
          const filename = btn.dataset.filename;
          fetch(`/delete-file/${encodeURIComponent(filename)}`, {
            method: 'POST'
          }).then(() => loadUploadedFiles());
        });
      });
    });
}