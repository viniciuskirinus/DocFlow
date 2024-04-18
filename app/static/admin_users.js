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
    var id_user = $(this).data('id_user');
    var name = $(this).data('name');
    var office = $(this).data('office');
    var role = $(this).data('role');

    // Preencher os campos do modal de edição com os dados
    $('#edit_nome').val(name);
    $('#edit_cargo').val(office);
    $('#edit_role').val(role);
    $('#edit_id_user').val(id_user);

    // Abrir o modal de edição
    $('#editModal').modal('show');
});

function exportToExcel() {
    const rows = document.querySelectorAll("#myTable tbody tr");
    const data = [];
    rows.forEach(row => {
        const rowData = [];
        row.querySelectorAll("td").forEach(cell => {
            rowData.push(cell.innerText);
        });
        data.push(rowData);
    });

    const wb = XLSX.utils.book_new();
    wb.Props = {
        Title: "Lista de Usuários",
        Subject: "Dados",
        Author: "Seu Nome",
        CreatedDate: new Date()
    };
    const ws = XLSX.utils.aoa_to_sheet(data);
    XLSX.utils.book_append_sheet(wb, ws, "Usuários");
    XLSX.writeFile(wb, "usuarios.xlsx");
}

// Função para gerar uma senha aleatória
function generateRandomPassword(length) {
    const charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+";
    let password = "";
    for (let i = 0; i < length; i++) {
        const randomIndex = Math.floor(Math.random() * charset.length);
        password += charset[randomIndex];
    }
    return password;
}

// Limpa o campo de senha ao abrir o modal de edição
$('#insert').on('show.bs.modal', function (e) {
    $('#senha').val(''); // Limpa o valor do campo de senha no modal de edição
});

// Ao clicar no botão que abre o modal de geração de senha, gera uma nova senha aleatória e exibe no campo do modal
$('#senhaModal').on('show.bs.modal', function (e) {
    const novaSenha = generateRandomPassword(10); // Gerar senha de comprimento 10
    document.getElementById("senhaAleatoria").value = novaSenha; // Exibe a senha aleatória no campo do modal
});

// Ao clicar no botão "Gerar Nova Senha" dentro do modal, gera uma nova senha aleatória e exibe no campo do modal
$('#gerarNovaSenha').click(function () {
    const novaSenha = generateRandomPassword(10); // Gerar senha de comprimento 10
    document.getElementById("senhaAleatoria").value = novaSenha; // Exibe a senha aleatória no campo do modal
});

// Ao clicar no botão "Usar Senha" dentro do modal, preenche o campo de senha principal com a senha exibida no modal e fecha o modal
$('#usarSenha').click(function () {
    const selectedPassword = document.getElementById("senhaAleatoria").value; // Obtém a senha exibida no modal
    $('#senha').val(selectedPassword); // Preenche o campo de senha no primeiro modal com a senha selecionada
    $('#senhaModal').modal('hide'); // Fecha o modal de geração de senha
});

// Ao clicar no botão que abre o modal de geração de senha, gera uma nova senha aleatória e exibe no campo do modal
$('#senhaModal').on('show.bs.modal', function (e) {
    const novaSenha = generateRandomPassword(10); // Gerar senha de comprimento 10
    document.getElementById("senhaAleatoria").value = novaSenha; // Exibe a senha aleatória no campo do modal
});

// Limpa o campo de senha ao abrir o modal de edição
$('#editModal').on('show.bs.modal', function (e) {
    $('#edit_senha').val(''); // Limpa o valor do campo de senha no modal de edição
});

// Ao clicar no botão "Usar Senha" dentro do modal de edição, preenche o campo de senha no formulário de edição com a senha exibida no modal de geração de senha e fecha o modal
$('#usarSenha').click(function () {
    const selectedPassword = document.getElementById("senhaAleatoria").value;  // Obtém a senha exibida no modal de geração de senha
    $('#edit_senha').val(selectedPassword); // Preenche o campo de senha no modal de edição com a senha selecionada
    $('#senhaModal').modal('hide'); // Fecha o modal de edição
});

// Evento de apagar o usuario
$(document).on('click', '.botao-delete', function()  {
    var id_user = $(this).data('id_user');
    var name = $(this).data('account');

    // Preencher o texto do span com o nome do documento
    $('#delete_user_name').text(name);
    $('#delete_id_user').val(id_user);

    // Abrir o modal de exclusão
    $('#deleteModal').modal('show');
});

// Evento de delete do pdf
$('#deleteForm').submit(function(event) {
    event.preventDefault(); // Impede o envio padrão do formulário

    var formData = new FormData($(this)[0]); // Obter dados do formulário

    // Enviar solicitação AJAX
    $.ajax({
        url: '/deleteuser',
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
                text: 'O usuário foi excluído com sucesso.',
            }).then((result) => {
                // Redirecionar para a página de PDF após o alerta ser fechado
                window.location.href = '/users';
            });
        },
        error: function(xhr, status, error) {
            // Se ocorrer um erro, exibir um alerta de erro
            Swal.fire({
                icon: 'error',
                title: 'Erro!',
                text: 'Ocorreu um erro ao apagar o usuário. Por favor, atualize a página e tente novamente. Caso o problema persistir contate um administrador',
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
        url: '/edituser',
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
                window.location.href = '/users';
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