document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.querySelector('form');
    const nameInput = document.getElementById('name');
    const passwordInput = document.getElementById('password');
    const submitButton = loginForm.querySelector('button[type="submit"]');
  
    // Функция показа ошибки (можно улучшить стилизацию)
    function showError(message) {
        // Удаляем предыдущие ошибки
        const existingError = document.querySelector('.error-message');
        if (existingError) existingError.remove();
  
        // Создаем элемент ошибки
        const errorElement = document.createElement('div');
        errorElement.classList.add('error-message');
        errorElement.style.color = 'red';
        errorElement.style.marginBottom = '10px';
        errorElement.textContent = message;
  
        // Вставляем перед формой
        loginForm.insertBefore(errorElement, loginForm.firstChild);
    }
  
    loginForm.addEventListener('submit', function(e) {
        e.preventDefault();
  
        // Получаем значения
        const username = nameInput.value.trim();
        const password = passwordInput.value;
  
        // Базовая валидация
        if (!username) {
            showError('Введите логин');
            return;
        }
  
        if (password.length < 4) {
            showError('Пароль слишком короткий');
            return;
        }
  
        // Блокируем кнопку во время отправки
        submitButton.disabled = true;
        submitButton.textContent = 'Вход...';
  
        // Подготавливаем данные для отправк
        const loginData = {
            username: username,
            password: password
        };
  
        // Отправка на backend
        fetch('/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(loginData)
        })
        .then(response => {
            // Проверка ответа
            if (!response.ok) {
                switch(response.status) {
                    case 401:
                        throw new Error('Неверный логин или пароль');
                    case 429:
                        throw new Error('Слишком много попыток. Попробуйте позже');
                    default:
                        throw new Error('Ошибка входа');
                }
            }
            return response.json();
        })
        .then(data => {
            // Успешная авторизация
            // Сохраняем токен и данные пользователя
            localStorage.setItem('token', data.token);
            
            // Редирект на главную или личный кабинет
            window.location.href = '/';
        })
        .catch(error => {
            // Обработка ошибок
            console.error('Login Error:', error);
            showError(error.message);
        })
        .finally(() => {
            // Разблокируем кнопку
            submitButton.disabled = false;
            submitButton.textContent = 'Войти';
        });
    });
  
    // Дополнительные улучшения безопасности
    // Отключаем автозаполнение
    nameInput.setAttribute('autocomplete', 'off');
    passwordInput.setAttribute('autocomplete', 'off');
  });