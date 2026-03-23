    const chatWindow = document.getElementById('chat-window');
    const chatForm = document.getElementById('chat-form');
    const currentUser = "{{ request.user.username }}";

    const scrollToBottom = () => {
        chatWindow.scrollTop = chatWindow.scrollHeight;
    };

    scrollToBottom();

    chatForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(this);

        fetch(window.location.href, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            }
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(data => { alert(data.message); throw new Error(data.error); });
            }
            return response.json();
        })
        .then(data => {
            chatForm.reset();
            appendMessage(data, true);
        })
        .catch(error => console.error('Ошибка отправки:', error));
    });

    setInterval(() => {

        const allMessages = document.querySelectorAll('.message-box[data-id]');
        const lastId = allMessages.length > 0 ? allMessages[allMessages.length - 1].getAttribute('data-id') : 0;

        fetch(`${window.location.href}?last_msg_id=${lastId}`)
        .then(response => response.json())
        .then(data => {
            if (data.messages && data.messages.length > 0) {
                data.messages.forEach(msg => {
                    // Добавляем сообщение, только если его еще нет (на случай лагов)
                    if (!document.querySelector(`[data-id="${msg.id}"]`)) {
                        appendMessage(msg, msg.sender === currentUser);
                    }
                });
            }
        });
    }, 3000);

    function appendMessage(data, isMe) {
        const alignClass = isMe ? 'justify-content-end' : 'justify-content-start';
        const bgClass = isMe ? 'bg-danger text-white' : 'bg-secondary text-light';
        const infoClass = isMe ? 'text-white' : 'text-info';

        const imageHtml = data.image_url
            ? `<div class="mb-2"><a href="${data.image_url}" target="_blank">
               <img src="${data.image_url}" class="img-fluid rounded border border-light" style="max-height: 250px; width: 100%; object-fit: cover;">
               </a></div>`
            : '';

        const messageHtml = `
            <div class="message-box" data-id="${data.id}">
                <div class="d-flex ${alignClass} mb-4">
                    <div class="p-3 shadow-sm message-box ${bgClass}"
                         style="max-width: 75%; position: relative; clip-path: polygon(0 5%, 100% 0, 98% 95%, 2% 100%);">
                        ${imageHtml}
                        ${data.text ? `<p class="mb-1 fw-bold">${data.text}</p>` : ''}
                        <div class="small mt-1 opacity-75 ${infoClass}" style="font-size: 0.65rem;">
                            ${data.created_at}
                        </div>
                    </div>
                </div>
            </div>
        `;

        chatWindow.insertAdjacentHTML('beforeend', messageHtml);
        scrollToBottom();
    }
