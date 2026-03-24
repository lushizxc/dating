document.addEventListener('DOMContentLoaded', function() {
    const chatWindow = document.getElementById('chat-window');
    const chatForm = document.getElementById('chat-form');

    // Если скрипт загрузится, ты увидишь это в консоли (F12)
    console.log("JS файл успешно загружен!");

    if (!chatWindow || !chatForm) return;

    // Берем данные из HTML-атрибутов (dataset)
    const currentUser = chatWindow.dataset.currentUser;
    const chatUrl = chatWindow.dataset.chatUrl;

    const scrollToBottom = () => {
        chatWindow.scrollTop = chatWindow.scrollHeight;
    };
    scrollToBottom();

    // Перехват отправки сообщения
    chatForm.addEventListener('submit', function(e) {
        e.preventDefault(); // Отменяет переход на страницу с JSON

        const formData = new FormData(this);
        fetch(chatUrl, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            }
        })
        .then(response => response.json())
        .then(data => {
            chatForm.reset();
            appendMessage(data, true);
        })
        .catch(error => console.error('Ошибка отправки:', error));
    });

    // Функция отрисовки сообщения (используй те же классы, что в HTML)
    function appendMessage(data, isMe) {
        const alignClass = isMe ? 'justify-content-end' : 'justify-content-start';
        const bgClass = isMe ? 'bg-danger text-white' : 'bg-secondary text-light';
        const imageHtml = data.image_url ? `<img src="${data.image_url}" class="img-fluid rounded mb-2" style="max-height: 250px; width: 100%; object-fit: cover;">` : '';

        const html = `
            <div class="message-box" data-id="${data.id}">
                <div class="d-flex ${alignClass} mb-4">
                    <div class="p-3 ${bgClass}" style="max-width: 75%; clip-path: polygon(0 5%, 100% 0, 98% 95%, 2% 100%);">
                        ${imageHtml}
                        <p class="mb-1 fw-bold">${data.text || ''}</p>
                        <div class="small opacity-75">${data.created_at}</div>
                    </div>
                </div>
            </div>`;
        chatWindow.insertAdjacentHTML('beforeend', html);
        scrollToBottom();
    }

    // Обновление чата раз в 3 секунды
    setInterval(() => {
        const lastId = document.querySelector('.message-box:last-child')?.dataset.id || 0;
        fetch(`${chatUrl}?last_msg_id=${lastId}`)
            .then(res => res.json())
            .then(data => {
                data.messages?.forEach(msg => {
                    if (!document.querySelector(`[data-id="${msg.id}"]`)) {
                        appendMessage(msg, msg.sender === currentUser);
                    }
                });
            });
    }, 3000);
});