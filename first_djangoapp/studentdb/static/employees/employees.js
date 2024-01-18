// search-script.js
$(document).ready(function () {
  $("#searchInput").on("input", function () {
    var searchTerm = $(this).val().toLowerCase();

    $(".warehouse-row").each(function () {
      var id = $(this).find(".employee-id").text().toLowerCase();
      var name = $(this).find(".employee-name").text().toLowerCase();
      var lastName = $(this).find(".employee-lastName").text().toLowerCase();
      var hidden = $(this).find(".hidden-checkbox").prop("checked");

      if ((id.includes(searchTerm) || name.includes(searchTerm) || lastName.includes(searchTerm)) && (!hidden || (hidden && searchTerm === "false"))) {
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
        var employeeId = $(this).data('employee-id');
        var isChecked = $(this).prop('checked');

        // AJAX-запрос для обновления поля 'hidden' в базе данных
        $.ajax({
          method: 'POST',
          url: '/update_hidden_status_employees/',  // Замените на реальный URL
          data: {
            employee_id: employeeId,
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
    // Проверка наличия скрытых строк
    var hasHiddenRows = $('.hidden-row[data-hidden-state="hidden"]').length > 0;

    // Изменение текста кнопки в зависимости от текущего состояния
    var buttonText = hasHiddenRows ? 'Hide hidden' : 'Show hidden';

    // Обновить текст кнопки
    $(this).text(buttonText);

    if (hasHiddenRows) {
      // Показать все строки с классом 'hidden-row' и пометкой 'hidden'
      $('.hidden-row[data-hidden-state="hidden"]').each(function () {
        $(this).removeClass('hidden-row').addClass('newly-shown-row');
      });
    } else {
      // Скрыть все строки с классом 'newly-shown-row'
      $('.newly-shown-row').hide();
      location.reload();
    }
  });
});

