
let currentPdfId = null;

function showChat(clickedElement, pdfId, pdfName, pdfCategory, pdfSector) {
    
    var chatContainer = document.getElementById('chatContainer');
    currentPdfId = pdfId;

    if (!chatContainer) {
        console.error('Elemento chatContainer não encontrado.');
        return;
    }

    chatContainer.style.display = 'none';

    // Atualize todos os elementos para remover a seleção
    document.querySelectorAll('.card-body a').forEach(link => {
        link.classList.remove('bg-gradient-primary', 'selected');
    });

    // Adiciona a classe 'selected' ao elemento clicado
    clickedElement.classList.add('bg-gradient-primary', 'selected');

    chatContainer.style.display = 'block';
    document.getElementById('selectChatMessage').style.display = 'none';

    updateChatInfo(pdfId, pdfName, pdfCategory, pdfSector);
    updateTextStyle();
    clearChat();
    addWelcomeMessage();
    openChat(pdfId);
    window.pdfId = pdfId;
}

function updateTextStyle() {
    // Remove a classe 'selected' do texto de todos os links
    document.querySelectorAll('.card-body a .justify-content-between.align-items-center h4, .card-body a .justify-content-between.align-items-center h6').forEach(text => {
        text.style.color = 'black'; // Define a cor padrão para preto
    });

    // Adiciona a classe 'selected' ao texto do link selecionado e muda a cor para branco
    var selectedLink = document.querySelector('.card-body a.selected');
    if (selectedLink) {
        selectedLink.querySelector('.justify-content-between.align-items-center h4').style.color = 'white';
        selectedLink.querySelector('.justify-content-between.align-items-center h6').style.color = 'white';
    }
}

function updateChatInfo(pdfId, pdfName, pdfCategory, pdfSector) {
    // Obtém os elementos com os IDs correspondentes
    var chatTitle = document.querySelector('#chatContainer .card-header h2');
    var chatSector = document.querySelector('#chatContainer .card-header span.text-muted');
    var chatId = document.querySelector('#chatContainer .card-header span.chat-id');

    // Verifica se os elementos foram encontrados
    if (!chatTitle || !chatSector || !chatId) {
        console.error('Elementos do chat não encontrados.');
        return;
    }

    // Atualiza os elementos com os valores do banco de dados
    chatTitle.textContent = pdfName;
    chatSector.textContent = pdfSector;
    chatId.textContent = pdfId;
}
setInterval(function () {
    // Obtém a hora atual
    var currentTime = new Date();

    // Formata a hora no formato desejado (hh:mm am/pm)
    var formattedTime = currentTime.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

    // Obtém todos os elementos com a classe 'chat-time'
    var chatTimeElements = document.getElementsByClassName('chat-time');

    // Atualiza cada elemento com a hora formatada
    for(var i = 0; i < chatTimeElements.length; i++) {
        chatTimeElements[i].textContent = formattedTime;
    }
}, 1000); // Atualiza a cada segundo

function addWelcomeMessage() {
    var welcomeMessageDiv = document.createElement("div");
    welcomeMessageDiv.className = "row justify-content-start mb-4";
    welcomeMessageDiv.innerHTML = '<div class="col-auto">' +
                                  '<div class="card ">' +
                                  '<div class="card-body p-2">' +
                                  '<p class="mb-1">Olá, em que posso ajudar hoje?</p>' +
                                  '<div class="d-flex align-items-center text-sm opacity-6">'+
                                  '<i class="far fa-clock mr-1" aria-hidden="true"></i>'+
                                  '<small class="chat-time"></small>'+                             
                                  '</div></div></div></div>';
    document.getElementById("bodychat").appendChild(welcomeMessageDiv);
}

function handleSubmit() {
    sendMessage();
    return false; // Isso impede a atualização da página
}

let chats = {};

function openChat(pdfId) {
    if (!chats[pdfId]) {
        chats[pdfId] = []; // Inicializa um novo chat se ainda não existir
    }
    chats[pdfId].forEach(message => {
        addNewUserMessage(message);
    });
}


var botTypingMessageDiv = null; // Variável para manter a referência à div de "Digitando..."
var typingDotsInterval; // Variável para manter a referência ao intervalo de pontos

function sendMessage() {
    var userMessage = document.getElementById('chatInput').value;

    if (userMessage.trim() !== '') {
        addNewUserMessage(userMessage);

        // Iniciar a animação de "Digitando..."
        startBotTypingAnimation();

        // Enviar a mensagem para o servidor para processamento
        fetch('/process_chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: userMessage, pdfid: currentPdfId }),
        })
        .then(response => response.json())
        .then(data => {
            // Parar a animação de "Digitando..." quando a resposta do bot chegar
            stopBotTypingAnimation();
            addNewBotMessage(data.response);
        });

        document.getElementById('chatInput').value = "";
    }
}

function startBotTypingAnimation() {
    if (!botTypingMessageDiv) {
        botTypingMessageDiv = document.createElement("div");
        botTypingMessageDiv.className = "row justify-content-start text-left mb-4";
        document.getElementById("bodychat").appendChild(botTypingMessageDiv);
    }

    // Iniciar a animação de pontos
    var typingDots = 1;
    botTypingMessageDiv.innerHTML = '<div class="col-auto">' +
        '<div class="card bg-gradient-light text-dark">' +
        '<div class="card-body p-2">' +
        '<p class="mb-1">Pensando' + '.'.repeat(typingDots) + '<br></p>' +
        '</div></div></div>';

    // Atualizar os pontos a cada segundo (limitado a 3)
    typingDotsInterval = setInterval(function () {
        typingDots = (typingDots % 3) + 1;
        botTypingMessageDiv.innerHTML = '<div class="col-auto">' +
            '<div class="card bg-gradient-light text-dark">' +
            '<div class="card-body p-2">' +
            '<p class="mb-1">Pensando' + '.'.repeat(typingDots) + '<br></p>' +
            '</div></div></div>';
    }, 1000);
}

function stopBotTypingAnimation() {
    // Parar a animação de pontos e remover a mensagem de "Digitando..."
    if (botTypingMessageDiv) {
        clearInterval(typingDotsInterval);
        botTypingMessageDiv.remove();
        botTypingMessageDiv = null;
    }
}


function clearChat() {
    var chatBody = document.getElementById("bodychat");
    while (chatBody.firstChild) {
        chatBody.removeChild(chatBody.firstChild);
    }
}

function addNewUserMessage(message) {
    var newUserMessageDiv = document.createElement("div");
    newUserMessageDiv.className = "row justify-content-end text-right mb-4";
    newUserMessageDiv.innerHTML = '<div class="col-auto">' +
                                '<div class="card bg-gradient-primary text-white">' +
                                '<div class="card-body p-2">' +
                                '<p class="mb-1">' + message + '<br></p>' +
                                '<div class="d-flex align-items-center justify-content-end text-sm opacity-6">' +
                                '<i class="fa fa-check-double mr-1 text-xs" aria-hidden="true"></i>' +
                                '<small class="chat-time">.</small>' +
                                '</div></div></div></div>';
    document.getElementById("bodychat").appendChild(newUserMessageDiv);
}

function addNewBotMessage(message) {
    var newBotMessageDiv = document.createElement("div");
    newBotMessageDiv.className = "row justify-content-start";
    newBotMessageDiv.innerHTML = '<div class="col-auto">' +
                                '<div class="card">' +
                                '<div class="card-body p-2">' +
                                '<p class="mb-0 text-sm">' + message + '<br></p>' +
                                '<div class="d-flex align-items-center justify-content-end text-sm opacity-6">' +
                                '<i class="fa fa-check-double mr-1 text-xs" aria-hidden="true"></i>' +
                                '<small class="chat-time">.</small>' +
                                '</div></div></div></div>';
    document.getElementById("bodychat").appendChild(newBotMessageDiv);
}

function openPDFModal(pdfImagesBase64List) {
    // Inicializar o modal
    $('#pdfModal').modal('show');

    // Renderizar o PDF como imagem
    var pdfViewer = document.getElementById('pdfViewer');
    pdfViewer.innerHTML = ''; // Limpa o conteúdo anterior

    pdfImagesBase64List.forEach(function(imageBase64) {
        var imgElement = document.createElement('img');
        imgElement.src = 'data:image/png;base64,' + imageBase64;
        pdfViewer.appendChild(imgElement);
    });
}

function showPDF(pdfId) {
    // Mostrar o loader
    document.querySelector('.loader').style.display = 'block';

    $.ajax({
        url: '/showpdf',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ 'pdf_id': pdfId }),
        success: function(data) {
            if (data && data.pdf_images_base64) {
                openPDFModal(data.pdf_images_base64);
                // Ocultar o loader quando o modal está pronto para ser exibido
                document.querySelector('.loader').style.display = 'none';
            } else {
                alert("Não foi possível encontrar o conteúdo do PDF.");
                // Ocultar o loader se não conseguir encontrar o conteúdo do PDF
                document.querySelector('.loader').style.display = 'none';
            }
        },
        error: function(xhr, status, error) {
            console.error("Erro ao obter o conteúdo do PDF:", error);
            alert("Erro ao obter o conteúdo do PDF. Por favor, tente novamente mais tarde.");
            // Ocultar o loader em caso de erro
            document.querySelector('.loader').style.display = 'none';
        }
    });
}

document.addEventListener("DOMContentLoaded", function() {
    // Outras inicializações que já existem
    updateChatInfo();
    ordenarElementosPorNome();
});

function ordenarElementosPorNome() {
    var container = document.querySelector(".card-body.p-2");
    if (!container) return;

    var elementos = Array.from(container.querySelectorAll('a'));
    elementos.sort(function(a, b) {
        var nomeA = extrairNumero(a.querySelector('h4').textContent.trim());
        var nomeB = extrairNumero(b.querySelector('h4').textContent.trim());
        return nomeA - nomeB;
    });

    elementos.forEach(function(elemento) {
        container.appendChild(elemento);
    });
}

function extrairNumero(texto) {
    var matches = texto.match(/\d+/);
    return matches ? parseInt(matches[0], 10) : 0;
}