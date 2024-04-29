$(document).ready(function() {
    // Quando o link "Ver mais" for clicado
    $('#ver-mais').click(function(e) {
        e.preventDefault(); // Impedir o comportamento padrão do link
        e.stopPropagation(); // Impedir a propagação do evento para outros elementos

        // Mostrar as próximas notificações ocultas
        $('.list-group-item.extra:hidden').slice(0, 5).show();

        // Se não houver mais notificações ocultas, ocultar o link "Ver mais"
        if ($('.list-group-item.extra:hidden').length === 0) {
            $('#ver-mais').hide();
        }
    });
});

$(document).ready(function() {
    $('#marcar-todas-como-lidas').on('click', function(event) {
        // Impedir a propagação do evento de clique
        event.stopPropagation();
        
        // Requisição AJAX para marcar todas as notificações como lidas
        $.get('/marcar_todas_como_lidas', function() {
            // Remover as notificações marcadas como lidas da página
            $('.list-group .list-group-item').each(function() {
                $(this).remove();
            });
        });
    });
});

document.addEventListener('DOMContentLoaded', function() {
    var notificationTimes = document.querySelectorAll('.notification-time');
    notificationTimes.forEach(function(notificationTime) {
        var timeString = notificationTime.getAttribute('data-time');
        var notificationTimeValue = new Date(timeString.replace('T', ' ')); // Remova o 'T' para garantir compatibilidade com navegadores mais antigos
        var currentTime = new Date();

        var timeDifference = currentTime.getTime() - notificationTimeValue.getTime();
        var hoursDifference = Math.floor(timeDifference / (1000 * 60 * 60));

        if (hoursDifference === 0) {
            notificationTime.textContent = 'Agora mesmo';
        } else {
            notificationTime.textContent = hoursDifference + ' hora(s) atrás';
        }
    });
});