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
    console.log("Botão clicado");
    var id_user = $(this).data('id_user');
    var name = $(this).data('name');
    var office = $(this).data('office');
    var role = $(this).data('role');
    var password = $(this).data('password');

    // Preencher os campos do modal de edição com os dados
    $('#edit_nome').val(name);
    $('#edit_cargo').val(office);
    $('#edit_role').val(role);
    $('#edit_senha').val(password);
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