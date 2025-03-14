// Константы для backend
const BACKEND_URL = 'http://127.0.0.1:8000/products/search-by-photo';

// Функция конвертации Base64 в Blob
function base64ToBlob(base64, mimeType) {
  const byteCharacters = atob(base64.split(',')[1]);
  const byteNumbers = new Array(byteCharacters.length);
  
  for (let i = 0; i < byteCharacters.length; i++) {
      byteNumbers[i] = byteCharacters.charCodeAt(i);
  }
  
  const byteArray = new Uint8Array(byteNumbers);
  return new Blob([byteArray], { type: mimeType });
}

// Основная функция загрузки
async function uploadImage() {
  const previewImage = document.getElementById('previewImage');
  const uploadBtn = document.getElementById('uploadBtn');
  
  try {
      // Получаем Base64 изображения
      const base64Image = previewImage.src;
      
      // Создаем FormData
      const formData = new FormData();
      
      // Конвертируем Base64 в Blob
      const imageBlob = base64ToBlob(base64Image, 'image/png');
      
      // Добавляем файл в FormData
      formData.append('image', imageBlob, 'uploaded_image.png');
      
      // Опционально: добавить дополнительные данные
      formData.append('userId', 'example_user_id');
      formData.append('timestamp', new Date().toISOString());

      // Отправка на backend
      const response = await fetch(BACKEND_URL, {
          method: 'POST',
          body: formData,
          // Если нужна авторизация
          headers: {
              'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
      });

      // Обработка ответа
      if (!response.ok) {
          throw new Error('Ошибка загрузки');
      }

      const result = await response.json();
      
      // Показываем успешный результат
      alert('Изображение успешно загружено');
      
      // Сохраняем результат в локальное хранилище
      chrome.storage.local.set({
          lastUploadedImage: {
              url: result.imageUrl,
              uploadedAt: new Date().toISOString()
          }
      });

  } catch (error) {
      console.error('Ошибка:', error);
      alert(`Не удалось загрузить изображение: ${error.message}`);
  }
}

// Навешиваем обработчик на кнопку
document.getElementById('uploadBtn').addEventListener('click', uploadImage);