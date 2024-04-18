
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

// Evento de adição de pdf
$('#addForm').submit(function(event) {
    event.preventDefault(); // Impede o envio padrão do formulário

    var formData = new FormData($(this)[0]); // Obter dados do formulário

    // Enviar solicitação AJAX
    $.ajax({
        url: '/generate',
        type: 'POST',
        data: formData,
        cache: false,
        contentType: false,
        processData: false,
        success: function(response) {
            if (response.success) {
                // Se a inserção for bem-sucedida, exibir um alerta de sucesso
                Swal.fire({
                    icon: 'success',
                    title: 'Sucesso!',
                    text: 'Os dados foram inseridos com sucesso.',
                }).then((result) => {
                    // Redirecionar para a página de PDF após o alerta ser fechado
                    window.location.href = '/pdf';
                });
            } else {
                // Se o servidor retornar erro, exibir alerta de erro com a mensagem específica
                Swal.fire({
                    icon: 'error',
                    title: 'Erro!',
                    text: response.error || 'Erro ao inserir o documento.',
                });
            }
        },
        error: function(xhr, status, error) {
            // Checa se o status é 400 para erro de negócio específico
            if (xhr.status === 400) {
                var response = JSON.parse(xhr.responseText);
                Swal.fire({
                    icon: 'error',
                    title: 'Erro!',
                    text: response.error || 'Erro desconhecido ao inserir documento.',
                });
            } else {
                // Trata erros gerais de comunicação ou de servidor
                Swal.fire({
                    icon: 'error',
                    title: 'Erro de Comunicação!',
                    text: 'Não foi possível completar a operação. Verifique sua conexão e tente novamente. Se o problema persistir, contate o suporte.',
                });
            }
        }
    });
});



// Evento de edição do pdf
$('#editForm').submit(function(event) {
    event.preventDefault(); // Impede o envio padrão do formulário

    var formData = new FormData($(this)[0]); // Obter dados do formulário

    // Enviar solicitação AJAX
    $.ajax({
        url: '/edit',
        type: 'POST',
        data: formData,
        cache: false,
        contentType: false,
        processData: false,
        success: function(response) {
            // Se a edição for bem-sucedida, exibir um alerta de sucesso
            Swal.fire({
                icon: 'success',
                title: 'Sucesso!',
                text: 'Os dados foram alterados com sucesso.',
            }).then((result) => {
                // Redirecionar para a página de PDF após o alerta ser fechado
                window.location.href = '/pdf';
            });
        },
        error: function(xhr, status, error) {
            // Se ocorrer um erro, exibir um alerta de erro
            Swal.fire({
                icon: 'error',
                title: 'Erro!',
                text: 'Ocorreu um erro ao alterar o documento. Por favor, atualize a página e tente novamente. Caso o problema persistir contate um administrador',
            });
        }
    });
});

// Evento de apagar o pdf
$(document).on('click', '.botao-delete', function()  {
    var id_pdf = $(this).data('id_pdf');
    var name = $(this).data('name');

    // Preencher o texto do span com o nome do documento
    $('#delete_document_name').text(name);
    $('#delete_id_pdf').val(id_pdf);

    // Abrir o modal de exclusão
    $('#deleteModal').modal('show');
});

// Evento de delete do pdf
$('#deleteForm').submit(function(event) {
    event.preventDefault(); // Impede o envio padrão do formulário

    var formData = new FormData($(this)[0]); // Obter dados do formulário

    // Enviar solicitação AJAX
    $.ajax({
        url: '/delete',
        type: 'POST',
        data: formData,
        cache: false,
        contentType: false,
        processData: false,
        success: function(response) {
            // Se a edição for bem-sucedida, exibir um alerta de sucesso
            Swal.fire({
                icon: 'success',
                title: 'Sucesso!',
                text: 'Os dados foram excluídos com sucesso.',
            }).then((result) => {
                // Redirecionar para a página de PDF após o alerta ser fechado
                window.location.href = '/pdf';
            });
        },
        error: function(xhr, status, error) {
            // Se ocorrer um erro, exibir um alerta de erro
            Swal.fire({
                icon: 'error',
                title: 'Erro!',
                text: 'Ocorreu um erro ao apagar o documento. Por favor, atualize a página e tente novamente. Caso o problema persistir contate um administrador',
            });
        }
    });
});
