document.addEventListener('DOMContentLoaded', function() {
    const pasteArea = document.getElementById('pasteArea');
    const previewImage = document.getElementById('previewImage');
    const uploadBtn = document.getElementById('uploadBtn');
  
    // Обработчик вставки
    document.addEventListener('paste', function(event) {
        const items = event.clipboardData.items;
        
        for (let i = 0; i < items.length; i++) {
            if (items[i].type.indexOf('image') !== -1) {
                const blob = items[i].getAsFile();
                const reader = new FileReader();
  
                reader.onload = function(e) {
                    previewImage.src = e.target.result;
                    previewImage.style.display = 'block';
                    uploadBtn.disabled = false;
                };
  
                reader.readAsDataURL(blob);
                break;
            }
        }
    });
  
    // Обработчик загрузки
    uploadBtn.addEventListener('click', function() {
        const imageData = previewImage.src;
        
        // Здесь можно реализовать логику отправки на сервер
        chrome.storage.local.set({lastUploadedImage: imageData}, function() {
            alert('Изображение сохранено');
        });
    });
  });