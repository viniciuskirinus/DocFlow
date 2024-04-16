document.addEventListener("DOMContentLoaded", function() {
    var searchInput = document.getElementById('searchInput');
    var searchOption = "nome"; // Por padrão, a pesquisa é por nome

    // Adicionando evento de mudança aos botões de rádio para atualizar a opção de pesquisa
    document.querySelectorAll('input[name="opcao"]').forEach(function(radio) {
        radio.addEventListener('change', function() {
            searchOption = this.value;
            search(); // Chama a função de pesquisa cada vez que a opção de pesquisa muda
        });
    });

    // Adicionando evento de digitação ao campo de busca para realizar a pesquisa em tempo real
    searchInput.addEventListener('keyup', search);

    function search() {
        var searchValue = searchInput.value.trim().toLowerCase();

        var items = document.querySelectorAll('.card-body.p-2 a');

        items.forEach(item => {
            // Determina se está buscando por nome ou setor e obtém o texto relevante
            var itemText = searchOption === "nome" ?
                item.querySelector('h4').textContent.trim().toLowerCase() :
                item.querySelector('h6').textContent.trim().toLowerCase();

            if (itemText.includes(searchValue)) {
                item.style.display = ''; // Mostra o item se corresponder
            } else {
                // Usa setProperty para adicionar !important ao estilo de display
                item.style.setProperty('display', 'none', 'important'); // Esconde o item se não corresponder
            }
        });
    }
});

window.onload = function() {
    document.getElementById('selectChatMessage').classList.add('active');
};

document.addEventListener("DOMContentLoaded", function() {
    // Captura o formulário dentro do modal
    var form = document.getElementById("info-form");

    // Adiciona um event listener para o envio do formulário
    form.addEventListener("submit", function(event) {
        // Previne o envio padrão do formulário
        event.preventDefault();

        // Captura os valores dos campos de senha
        var password = document.getElementById("password").value;
        var confirm_password = document.getElementById("confirm_password").value;

        // Verifica se as senhas são iguais
        if (password !== confirm_password) {
            Swal.fire({
                icon: 'error',
                title: 'Erro!',
                text: 'As senhas não são iguais'
            });
            return; // Interrompe o envio do formulário
        }

        // Verifica se a senha atende aos critérios de segurança
        if (!isStrongPassword(password)) {
            Swal.fire({
                icon: 'error',
                title: 'Erro!',
                text: 'A senha deve conter pelo menos 8 caracteres, incluindo letras maiúsculas, minúsculas, números e caracteres especiais.'
            });
            return; // Interrompe o envio do formulário
        }

        // Se todas as validações passaram, envia o formulário para a rota /edit_data
        form.submit();
    });

    // Função para verificar se a senha é forte
    function isStrongPassword(password) {
        // Verifica se a senha tem pelo menos 8 caracteres, incluindo letras maiúsculas, minúsculas, números e caracteres especiais
        if (password.length < 8 || !/[A-Z]/.test(password) || !/[a-z]/.test(password) || !/\d/.test(password) || !/[!@#$%^&*()-_=+{};:,<.>]/.test(password)) {
            return false;
        }
        return true;
    }
});