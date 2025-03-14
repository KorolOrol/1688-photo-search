
    document.getElementById('registr-form').addEventListener('submit', function(event) {
        event.preventDefault(); // Предотвращает стандартную отправку формы

        const name = document.getElementById('name').value;
        const password = document.getElementById('password').value;

        const data = {
            name: name,
            password: password
        };

        fetch('/your-backend-endpoint', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'  // Указываем, что отправляем JSON
            },
            body: JSON.stringify(data) // Преобразуем данные в JSON
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json(); // Или response.text(), если бэкенд возвращает текст
        })
        .then(data => {
            console.log('Success:', data);
            // Здесь можно обработать успешный ответ от сервера (например, показать сообщение)
        })
        .catch(error => {
            console.error('Error:', error);
            // Здесь можно обработать ошибку (например, показать сообщение об ошибке)
        });
    });
