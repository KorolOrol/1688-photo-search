document.getElementById('register-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const name = document.getElementById('name').value;
    const password = document.getElementById('password').value;
    const data = {
        username: username,
        password: password
    };
    fetch('https://example.com/api/register', { // Замените URL на ваш бэкенд
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data) // Преобразуем объект в JSON
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Ошибка сети');
        }
        return response.json();
    })
    .then(data => {
        document.getElementById('message').innerText = 'Регистрация прошла успешно!';
        console.log(data);
    })
    .catch(error => {
        document.getElementById('message').innerText = 'Ошибка регистрации: ' + error.message;
        console.error('Ошибка:', error);
    });
});