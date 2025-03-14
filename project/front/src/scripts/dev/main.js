document.addEventListener('DOMContentLoaded', function() {
    const registerForm = document.querySelector('form');
    const nameInput = document.getElementById('name');
    const passwordInput = document.getElementById('password');
    const submitButton = registerForm.querySelector('button[type="submit"]');
  
    // Функция показа ошибки
    function showError(message) {
        // Удаляем предыдущие ошибки
        const existingError = document.querySelector('.error-message');
        if (existingError) existingError.remove();
  
        // Создаем элемент ошибки
        const errorElement = document.createElement('div');
        errorElement.classList.add('error-message');
        errorElement.style.cssText = `
            color: red;
            background-color: #ffeeee;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 15px;
            width: 100%;
            text-align: center;
        `;
        errorElement.textContent = message;
  
        // Вставляем перед формой
        registerForm.insertBefore(errorElement, registerForm.firstChild);
    }
  
    // Улучшенная валидация
    function validateInputs() {
        const username = nameInput.value.trim();
        const password = passwordInput.value;
  
        // Проверка логина
        if (username.length < 3) {
            showError('Логин должен быть не короче 3 символов');
            return false;
        }
  
        // Проверка сложности пароля
        const passwordRegex = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}$/;
        if (!passwordRegex.test(password)) {
            showError('Пароль должен содержать буквы и цифры, минимум 6 символов');
            return false;
        }
  
        return true;
    }
  
    // Настройка инпутов
    nameInput.setAttribute('minlength', '3');
    nameInput.setAttribute('maxlength', '20');
    nameInput.setAttribute('pattern', '[A-Za-zА-Яа-я0-9_]+');
    nameInput.setAttribute('title', 'Используйте буквы, цифры и нижнее подчеркивание');
    nameInput.setAttribute('placeholder', 'Введите логин');
    nameInput.setAttribute('autocomplete', 'off');
  
    passwordInput.setAttribute('minlength', '6');
    passwordInput.setAttribute('maxlength', '30');
    passwordInput.setAttribute('placeholder', 'Введите пароль');
    passwordInput.setAttribute('autocomplete', 'new-password');
  
    // Обработчик отправки формы
    registerForm.addEventListener('submit', function(e) {
        e.preventDefault();
  
        // Валидация
        if (!validateInputs()) {
            return;
        }
  
        // Блокируем кнопку
        submitButton.disabled = true;
        submitButton.textContent = 'Регистрация...';
  
        // Подготавливаем данные
        const registrationData = {
            username: nameInput.value.trim(),
            password: passwordInput.value
        };
  
        // Отправка на сервер
        fetch('http://127.0.0.1:8000/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(registrationData)
        })
        .then(response => {
            if (!response.ok) {
                switch(response.status) {
                    case 409:
                        throw new Error('Пользователь с таким логином уже существует');
                    case 400:
                        throw new Error('Некорректные данные');
                    default:
                        throw new Error('Ошибка регистрации');
                }
            }
            return response.json();
        })
        .then(data => {
            // Успешная регистрация
            alert('Регистрация прошла успешно!');
            // Редирект на страницу входа
            window.location.href = '/login.html';
        })
        .catch(error => {
            console.error('Registration Error:', error);
            showError(error.message);
        })
        .finally(() => {
            // Разблокируем кнопку
            submitButton.disabled = false;
            submitButton.textContent = 'Зарегистрироваться';
        });
    });
  
    // Динамическая проверка логина
    let usernameTimeout;
    nameInput.addEventListener('input', function() {
        clearTimeout(usernameTimeout);
        usernameTimeout = setTimeout(() => {
            const username = nameInput.value.trim();
            if (username.length >= 3) {
                // Проверка доступности логина
                fetch(`/api/check-username?username=${username}`)
                    .then(response => response.json())
                    .then(data => {
                        if (!data.available) {
                            showError('Этот логин уже занят');
                        }
                    })
                    .catch(error => {
                        console.error('Username check error:', error);
                    });
            }
        }, 500);
    });
  
    // Показ/скрытие пароля
    const togglePasswordBtn = document.createElement('button');
    togglePasswordBtn.type = 'button';
    togglePasswordBtn.textContent = '👁️';
    togglePasswordBtn.style.cssText = `
        font-size: 20px;
        position: absolute;
        right: 10px;
        top: 50%;
        transform: translateY(-50%);
        background: none;
        border: none;
        cursor: pointer;
        z-index: 10;
    `;
    
    const passwordWrapper = passwordInput.closest('.form-group');
    passwordWrapper.style.position = 'relative';
    passwordWrapper.appendChild(togglePasswordBtn);
  
    togglePasswordBtn.addEventListener('click', function() {
        if (passwordInput.type === 'password') {
            passwordInput.type = 'text';
            togglePasswordBtn.textContent = '🙈';
        } else {
            passwordInput.type = 'password';
            togglePasswordBtn.textContent = '👁️';
        }
    });
});
