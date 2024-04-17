
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
            // Se a inserção for bem-sucedida, exibir um alerta de sucesso
            Swal.fire({
                icon: 'success',
                title: 'Sucesso!',
                text: 'Os dados foram inseridos com sucesso.',
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
                text: 'Ocorreu um erro ao inserir o documento. Por favor, atualize a página e tente novamente. Caso o problema persistir contate um administrador',
            });
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
$(document).ready(function() {
    $('#deleteModal').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget); // Botão que acionou o modal
        var documentName = button.data('name'); // Extrair informações dos atributos de dados
        var idPdf = button.data('id_pdf');
        var modal = $(this);
        modal.find('.modal-body #delete_document_name').text(documentName); // Atualizar o texto no modal
        modal.find('.modal-footer form').attr('action', "{{ url_for('delete.delete') }}"); // Atualizar a ação do formulário
        modal.find('.modal-footer form input[name="id_pdf"]').attr('value', idPdf); // Atualizar o valor do campo oculto
    });

    // Evento de clique no botão de exclusão dentro do modal
    $('#deleteButton').click(function(event) {
        var form = $('#deleteForm')[0]; // Obter o formulário de exclusão
        var formData = new FormData(form); // Obter dados do formulário

        // Enviar solicitação AJAX
        $.ajax({
            url: form.action,
            type: form.method,
            data: formData,
            cache: false,
            contentType: false,
            processData: false,
            success: function(response) {
                // Se a exclusão for bem-sucedida, exibir um alerta de sucesso
                Swal.fire({
                    icon: 'success',
                    title: 'Sucesso!',
                    text: 'Documento excluído com sucesso!',
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

        // Impede o envio padrão do formulário
        event.preventDefault();
    });
});