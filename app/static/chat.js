// SISTEMA CURRICULO FACIL VERSÃO 2.0
// AUTOR: FRANCISCO NEVES
// DATA: 27/06/2025
// Versão do arquivo chat.js: V1.005
// Descrição: Lida com a lógica do frontend. A exibição automática do IP local foi removida
//            para dar lugar à consulta via IA.
// -----------------------------------------------------------------------------

'use strict';
document.addEventListener('DOMContentLoaded', () => {

    const checkRefreshAndReset = () => {
        if (window.performance && performance.getEntriesByType) {
            const navEntries = performance.getEntriesByType("navigation");
            if (navEntries.length > 0 && navEntries[0].type === 'reload') {
                if (sessionStorage.getItem('isReloadingForReset')) {
                    sessionStorage.removeItem('isReloadingForReset');
                    return false;
                } else {
                    sessionStorage.setItem('isReloadingForReset', 'true');
                    fetch('/reset_chat_history', { method: 'POST', headers: { 'Content-Type': 'application/json' }})
                    .then(response => {
                        if (response.ok) { window.location.reload(); }
                        else { sessionStorage.removeItem('isReloadingForReset'); }
                    })
                    .catch(() => sessionStorage.removeItem('isReloadingForReset'));
                    return true;
                }
            }
        }
        return false;
    };

    if (checkRefreshAndReset()) {
        return;
    }

    const chatHistoryContainer = document.getElementById('chat-history-container');
    const promptForm = document.getElementById('prompt-form');
    const promptInput = document.getElementById('prompt-input');
    const sendButton = document.getElementById('send-button');

    function addMessageToHistory(sender, text, isHtml = false) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', `${sender}-message`);
        const paragraph = document.createElement('p');

        if (isHtml) {
            paragraph.innerHTML = DOMPurify.sanitize(text, { USE_PROFILES: { html: true } });
        } else {
            const rawHtml = marked.parse(text);
            paragraph.innerHTML = DOMPurify.sanitize(rawHtml, { USE_PROFILES: { html: true } });
        }

        messageDiv.appendChild(paragraph);
        chatHistoryContainer.appendChild(messageDiv);
        chatHistoryContainer.scrollTop = chatHistoryContainer.scrollHeight;
    }

    // A função showIpMessage foi completamente removida.

    const showInitialSetupMessage = () => {
        if (typeof NEEDS_API_KEY !== 'undefined' && NEEDS_API_KEY === true) {
            const welcomeMessage = `Obrigado por instalar o Currículo Fácil!\n\nPara começar, por favor, insira sua Chave de API (API Key) do Gemini. Você pode criar sua chave gratuitamente no site [https://aistudio.google.com/](https://aistudio.google.com/).\n\nDepois de criar, é só copiar o código e colar aqui como sua primeira mensagem para gente começar.`;
            addMessageToHistory('assistant', welcomeMessage);
        }
    };

    async function submitPrompt() {
        const promptText = promptInput.value.trim();
        if (!promptText) return;

        addMessageToHistory('user', promptText);
        promptInput.value = '';
        sendButton.disabled = true;
        promptInput.disabled = true;

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ prompt: promptText }),
            });

            const data = await response.json();

            if (response.ok && data.status === 'sucesso') {
                addMessageToHistory('assistant', data.resposta_assistente);
            } else {
                const errorMessage = data.mensagem || "Ocorreu um erro.";
                addMessageToHistory('assistant', `<b>[ERRO NO SERVIDOR]</b> ${errorMessage}`, true);
            }
        } catch (error) {
            console.error('Erro na requisição de chat:', error);
            addMessageToHistory('assistant', '<b>[ERRO DE CONEXÃO]</b> Não foi possível conectar ao servidor. Verifique sua rede e tente novamente.', true);
        } finally {
            sendButton.disabled = false;
            promptInput.disabled = false;
            promptInput.focus();
        }
    }

    promptForm.addEventListener('submit', (event) => {
        event.preventDefault();
        submitPrompt();
    });

    promptInput.addEventListener('keydown', (event) => {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault();
            submitPrompt();
        }
    });

    showInitialSetupMessage();
    promptInput.focus();
});