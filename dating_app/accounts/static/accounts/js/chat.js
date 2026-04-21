document.addEventListener('DOMContentLoaded', function() {
    const chatWindow = document.getElementById('chat-window');
    const chatForm = document.getElementById('chat-form');

    if (!chatWindow || !chatForm) return;

    const currentUser = chatWindow.dataset.currentUser;
    const chatUrl = chatWindow.dataset.chatUrl;

    const scrollToBottom = () => {
        chatWindow.scrollTop = chatWindow.scrollHeight;
    };
    scrollToBottom();

    chatForm.addEventListener('submit', function(e) {
        e.preventDefault();
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

    function appendMessage(data, isMe) {
        // Убираем блок "История пуста", если это первое сообщение
        const emptyMsg = document.getElementById('empty-chat-msg');
        if (emptyMsg) emptyMsg.remove();

        const alignClass = isMe ? 'justify-content-end' : 'justify-content-start';
        const bgClass = isMe ? 'bg-danger text-white' : 'bg-secondary text-white';
        const imageHtml = data.image_url ? `<img src="${data.image_url}" class="img-fluid mb-2" style="max-height: 250px; width: auto; clip-path: polygon(2% 2%, 98% 0%, 100% 98%, 0% 100%);">` : '';

        // ВЕРНУЛИ РВАНЫЙ СТИЛЬ СЮДА ТОЖЕ
        const html = `
            <div class="message-box w-100 d-flex ${alignClass} mb-3" data-id="${data.id}">
                <div class="p-3 shadow-sm ${bgClass}" style="max-width: 75%; position: relative; clip-path: polygon(0 5%, 100% 0, 98% 95%, 2% 100%);">
                    ${imageHtml}
                    <p class="mb-1 fw-bold" style="font-size: 1rem; word-wrap: break-word; letter-spacing: 0.5px;">${data.text || ''}</p>
                    <div class="text-end mt-1" style="font-size: 0.7rem; opacity: 0.8; font-weight: bold;">${data.created_at}</div>
                </div>
            </div>`;
        chatWindow.insertAdjacentHTML('beforeend', html);
        scrollToBottom();
    }

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