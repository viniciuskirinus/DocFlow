
$(document).ready(function(){
    // Ativar a função de pesquisa
    $("#searchInput").on("keyup", function() {
        var value = $(this).val().toLowerCase();
        $("#myTable tbody tr").filter(function() {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
    });
});

$(document).on('click', '.botao-edit', function()  {
    var id_pdf = $(this).data('id_pdf');
    var name = $(this).data('name');
    var category = $(this).data('category');
    var sector = $(this).data('sector');
    var version = $(this).data('version');
    var date = $(this).data('date');

    // Preencher os campos do modal de edição com os dados
    $('#edit_nome').val(name);
    $('#edit_categoria').val(category);
    $('#edit_version').val(version);
    $('#edit_setor').val(sector);
    $('#edit_data').val(date);
    $('#edit_id_pdf').val(id_pdf);

    // Abrir o modal de edição
    $('#editModal').modal('show');
});

function ordenarTabela() {
    var tbody = document.querySelector("#myTable tbody");
    var linhas = Array.from(tbody.querySelectorAll("tr"));
    
    linhas.sort(function(a, b) {
        var nomeA = a.dataset.nome.toUpperCase();
        var nomeB = b.dataset.nome.toUpperCase();
        
        // Ordenar pelo nome
        if (nomeA < nomeB) {
            return -1;
        }
        if (nomeA > nomeB) {
            return 1;
        }
        
        // Se os nomes são iguais, ordenar pelo número
        var numeroA = extrairNumero(nomeA);
        var numeroB = extrairNumero(nomeB);
        return numeroA - numeroB;
    });
    
    linhas.forEach(function(linha) {
        tbody.appendChild(linha);
    });
}

// Função auxiliar para extrair o número do nome
function extrairNumero(nome) {
    var matches = nome.match(/\d+/);
    return matches ? parseInt(matches[0]) : 0;
}

// Chamar a função de ordenação quando a página for carregada
document.addEventListener("DOMContentLoaded", function() {
    ordenarTabela();
});

function logout() {
    window.location.href = "{{ url_for('logout.logout') }}";
}