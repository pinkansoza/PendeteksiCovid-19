// DOM Elements
const dropZone = document.getElementById('drop-zone');
const fileInput = document.getElementById('file-input');
const previewSection = document.getElementById('preview-section');
const previewWrap = document.getElementById('preview-wrap');
const imagePreview = document.getElementById('image-preview');
const removeBtn = document.getElementById('remove-btn');
const analyzeBtn = document.getElementById('analyze-btn');
const btnText = document.getElementById('btn-text');
const btnLoader = document.getElementById('btn-loader');
const resultSection = document.getElementById('result-section');
const resultCard = document.getElementById('result-card');
const resultIcon = document.getElementById('result-icon');
const statusBadge = document.getElementById('status-badge');

let currentFile = null;

// --- Drag & Drop ---
['dragenter', 'dragover', 'dragleave', 'drop'].forEach(evt =>
    dropZone.addEventListener(evt, e => { e.preventDefault(); e.stopPropagation(); })
);
['dragenter', 'dragover'].forEach(evt =>
    dropZone.addEventListener(evt, () => dropZone.classList.add('dragover'))
);
['dragleave', 'drop'].forEach(evt =>
    dropZone.addEventListener(evt, () => dropZone.classList.remove('dragover'))
);
dropZone.addEventListener('drop', e => handleFiles(e.dataTransfer.files));
fileInput.addEventListener('change', function () { handleFiles(this.files); });

// --- File Handler ---
function handleFiles(files) {
    if (files.length === 0) return;
    const file = files[0];
    if (!file.type.startsWith('image/')) {
        alert('Mohon unggah file gambar yang valid (JPG/PNG).');
        return;
    }
    currentFile = file;
    const reader = new FileReader();
    reader.onload = e => {
        imagePreview.src = e.target.result;
        dropZone.style.display = 'none';
        previewSection.style.display = 'block';
        analyzeBtn.style.display = 'block';
        resultSection.style.display = 'none';
    };
    reader.readAsDataURL(file);
}

// --- Remove / Reset ---
removeBtn.addEventListener('click', e => {
    e.stopPropagation();
    currentFile = null;
    fileInput.value = '';
    previewSection.style.display = 'none';
    analyzeBtn.style.display = 'none';
    resultSection.style.display = 'none';
    dropZone.style.display = 'block';
    previewWrap.classList.remove('scanning');
});

// --- Analyze ---
analyzeBtn.addEventListener('click', async () => {
    if (!currentFile) return;

    // Start scan animation
    previewWrap.classList.add('scanning');

    // Loading state
    btnText.style.display = 'none';
    btnLoader.style.display = 'flex';
    analyzeBtn.disabled = true;
    resultSection.style.display = 'none';

    const formData = new FormData();
    formData.append('file', currentFile);
    formData.append('mode', 'covid19');

    try {
        const res = await fetch('/predict', { method: 'POST', body: formData });
        const data = await res.json();

        if (res.ok) {
            previewWrap.classList.remove('scanning');

            const isDanger = data.status_type === 'danger';
            resultCard.className = `result__card ${isDanger ? 'is-danger' : 'is-safe'}`;
            resultIcon.className = isDanger
                ? 'result__icon fa-solid fa-triangle-exclamation'
                : 'result__icon fa-solid fa-circle-check';

            statusBadge.textContent = data.status;

            // Confidence bar
            const conf = data.confidence;
            document.getElementById('confidence-text').textContent = `${conf}%`;
            document.getElementById('confidence-bar').style.width = '0%';
            requestAnimationFrame(() => {
                document.getElementById('confidence-bar').style.width = `${conf}%`;
            });

            // Interpretation
            const el = document.getElementById('interpretation-text');
            const score = data.raw_score.toFixed(4);
            if (isDanger) {
                el.innerHTML = `Model AI mendeteksi adanya pola abnormalitas pada citra rontgen yang konsisten dengan infeksi COVID-19 <em>(Skor: ${score})</em>.<br><br><strong style="color:var(--danger-light)">Saran:</strong> Segera konsultasikan dengan tenaga medis profesional untuk pemeriksaan lebih lanjut.`;
            } else {
                el.innerHTML = `Citra rontgen tidak menunjukkan pola infeksi COVID-19 yang signifikan <em>(Skor: ${score})</em>. Paru-paru terdeteksi normal.<br><br><strong style="color:var(--safe-light)">Saran:</strong> Tetap jaga kesehatan dan patuhi protokol yang berlaku.`;
            }

            resultSection.style.display = 'block';
            setTimeout(() => resultSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' }), 100);
        } else {
            alert('Error: ' + data.error);
            previewWrap.classList.remove('scanning');
        }
    } catch (err) {
        console.error(err);
        alert('Terjadi kesalahan saat menghubungi server.');
        previewWrap.classList.remove('scanning');
    } finally {
        btnText.style.display = 'block';
        btnLoader.style.display = 'none';
        analyzeBtn.disabled = false;
    }
});
