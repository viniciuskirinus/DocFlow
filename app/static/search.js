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

document.getElementById("submitButton").addEventListener("click", function() {
    var formData = new FormData(document.getElementById("info"));

    fetch('/edit_data', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.type === 'success') {
            Swal.fire({
                icon: 'success',
                title: 'Sucesso!',
                text: data.message
            });
        } else {
            Swal.fire({
                icon: 'error',
                title: 'Erro!',
                text: data.message
            });
        }
    })
    .catch(error => {
        console.error('Erro:', error);
    });
});