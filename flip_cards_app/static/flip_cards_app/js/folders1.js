$(document).ready(function() {
    // Обработчик для создания новой папки
    $('#createFolderForm').on('submit', function(e) {
        e.preventDefault();
        var folderName = $('#folderName').val();
        var csrftoken = getCookie('csrftoken');
        
        $.ajax({
            url: '/words/catalog/folders/create/',
            type: 'POST',
            headers: {'X-CSRFToken': csrftoken},
            data: {
                'folder_name': folderName
            },
            success: function(response) {
                var newOption = `<li><a class="dropdown-item folder-item" 
                    data-folder-id="${response.folder_id}" href="#">${folderName}</a></li>`;
                $('.folder-list').append(newOption);
                $('#createFolderModal').modal('hide');
                $('#folderName').val('');
                toastr.success('Папка успешно создана');
            },
            error: function(xhr) {
                toastr.error('Ошибка при создании папки');
            }
        });
    });

    // Обработчик для добавления слова в папку
    $('.dropdown-item.folder-item').on('click', function(e) {
        e.preventDefault();
        var folderId = $(this).data('folder-id');
        var wordId = $(this).closest('.dropdown').find('.icon').data('word-id');
        var $dropdownButton = $(this).closest('.dropdown').find('.icon');
        var folderNameText = $(this).text().trim();
        var csrftoken = getCookie('csrftoken');

        $.ajax({
            url: '/words/catalog/folders/add/',
            type: 'POST',
            headers: {'X-CSRFToken': csrftoken},
            data: {
                'folder_id': folderId,
                'word_id': wordId
            },
            success: function(response) {
                // Обновляем содержимое кнопки
                $dropdownButton.html(`
                    <i class="bi bi-folder-fill h5" style="color:#68539E"></i>
                    <span class="badge badge-primary h5">${folderNameText}</span>
                `);
                toastr.success('Слово добавлено в папку');
            },
            error: function(xhr) {
                toastr.error('Ошибка при добавлении в папку');
            }
        });
    });

    // Обработчик для удаления слова из папки
    $('.remove-from-folder').on('click', function(e) {
        e.preventDefault();
        var wordId = $(this).closest('.dropdown').find('.icon').data('word-id');
        var $dropdownButton = $(this).closest('.dropdown').find('.icon');
        var csrftoken = getCookie('csrftoken');

        $.ajax({
            url: '/words/catalog/folders/remove/',
            type: 'POST',
            headers: {'X-CSRFToken': csrftoken},
            data: {
                'word_id': wordId
            },
            success: function(response) {
                $dropdownButton.html(`
                    <i class="bi bi-folder h5" style="color:#68539E"></i>
                `);
                toastr.success('Слово удалено из папки');
            },
            error: function(xhr) {
                toastr.error('Ошибка при удалении из папки');
            }
        });
    });
});