const socket = new WebSocket("ws://127.0.0.1:8000/ws");

socket.onopen = (event) => {
    console.log('Соединение установлено.');
};

socket.onmessage = (event) => {
    const message = event.data;
    console.log('Получено сообщение: ', message);
};

socket.onclose = (event) => {
    if (event.wasClean) {
        console.log(`Пользователь отключился, код=${event.code} причина=${event.reason}`);
    } else {
        console.error('Обрыв соединения');
    }
};

socket.onerror = (error) => {
    console.error(`Ошибка ${error.message}`);
};