// search-script.js
$(document).ready(function () {
    $("#searchInput").on("input", function () {
        var searchTerm = $(this).val().toLowerCase();

        $(".product-row").each(function () {
            var name = $(this).find(".name").text().toLowerCase();
            var category = $(this).find(".category").text().toLowerCase();
            var hidden = $(this).hasClass("hidden-row") || $(this).find('.hidden-checkbox').prop('checked');
            var isChecked = $(this).find('.hidden-checkbox').prop('checked');

            if ((name.includes(searchTerm) || category.includes(searchTerm)) && (!hidden || (hidden && searchTerm === "false")) && (!hidden || (hidden && isChecked))) {
                $(this).show();
            } else {
                $(this).hide();
            }
        });
    });
});

// main-script.js
$(document).ready(function () {
    // Получение CSRF-токена из cookie
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Установка CSRF-токена для AJAX-запросов
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        }
    });

    // Обработка события изменения чекбокса
    $('.hidden-checkbox').change(function () {
        // Запомнить изменение чекбокса, обновление статуса будет после нажатия на кнопку "Скрыть"
        $(this).data('changed', true);
    });

    // Функция для рекурсивного обновления страницы
    function refreshPage() {
        location.reload();
    }

    // Обработка события клика по кнопке "Скрыть"
    $('.Hidden-button').click(function () {
        // Обновление статуса только для измененных чекбоксов
        $('.hidden-checkbox').each(function () {
            if ($(this).data('changed')) {
                var productId = $(this).data('product-id');
                var isChecked = $(this).prop('checked');

                // AJAX-запрос для обновления поля 'hidden' в базе данных
                $.ajax({
                    method: 'POST',
                    url: '/update_hidden_status_products/',
                    data: {
                        product_id: productId,
                        is_hidden: isChecked
                    },
                    success: function (data) {
                        console.log('Статус скрытия успешно обновлен.');
                        // После успешного обновления вызываем функцию для рекурсивного обновления страницы
                        refreshPage();
                    },
                    error: function (error) {
                        console.error('Ошибка при обновлении статуса скрытия:', error);
                    }
                });
            }
        });
    });

    // Обработка события клика по кнопке "Показать/Скрыть"
    $('.Show-hidden-button').click(function () {
        // Переключение видимости строк с классом 'hidden-row'
        $('.product-row.hidden-row').toggleClass('newly-shown-row');

        // Обновление текста кнопки
        var buttonText = $('.product-row.hidden-row').length > 0 ? 'Hide hidden' : 'Show hidden';
        $(this).text(buttonText);
    });
});
