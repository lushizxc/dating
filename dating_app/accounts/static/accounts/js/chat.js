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

    // 1. ОТПРАВКА
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
            if (data.error) {
                alert(data.message);
            } else {
                chatForm.reset();
                // Удаляем надпись "сообщений нет", если она есть
                const emptyMsg = document.getElementById('empty-chat-msg');
                if (emptyMsg) emptyMsg.remove();

                appendMessage(data, true);
            }
        })
        .catch(err => console.error('Ошибка отправки:', err));
    });

    // 2. ПОЛЛИНГ (Обновление каждые 3 сек)
    setInterval(() => {
        // Ищем последний элемент, у которого точно есть атрибут data-id
        const messages = chatWindow.querySelectorAll('.message-box[data-id]');
        const lastId = messages.length > 0 ? messages[messages.length - 1].dataset.id : 0;

        fetch(`${chatUrl}?last_msg_id=${lastId}`)
        .then(res => res.json())
        .then(data => {
            if (data.messages && data.messages.length > 0) {
                data.messages.forEach(msg => {
                    if (!document.querySelector(`[data-id="${msg.id}"]`)) {
                        appendMessage(msg, msg.sender === currentUser);
                    }
                });
            }
        });
    }, 3000);

    // Функция отрисовки
    function appendMessage(data, isMe) {
        const alignClass = isMe ? 'justify-content-end' : 'justify-content-start';
        const bgClass = isMe ? 'bg-danger text-white' : 'bg-secondary text-light';
        const infoClass = isMe ? 'text-white' : 'text-info';

        const imageHtml = data.image_url
            ? `<div class="mb-2"><a href="${data.image_url}" target="_blank">
               <img src="${data.image_url}" class="img-fluid rounded border border-light" style="max-height: 250px; width: 100%; object-fit: cover;">
               </a></div>`
            : '';

        const html = `
            <div class="message-box" data-id="${data.id}">
                <div class="d-flex ${alignClass} mb-4">
                    <div class="p-3 shadow-sm ${bgClass}"
                         style="max-width: 75%; position: relative; clip-path: polygon(0 5%, 100% 0, 98% 95%, 2% 100%);">
                        ${imageHtml}
                        ${data.text ? `<p class="mb-1 fw-bold">${data.text}</p>` : ''}
                        <div class="small mt-1 opacity-75 ${infoClass}" style="font-size: 0.65rem;">
                            ${data.created_at}
                        </div>
                    </div>
                </div>
            </div>`;

        // Вставляем ВНУТРЬ chat-window
        chatWindow.insertAdjacentHTML('beforeend', html);
        scrollToBottom();
    }
});