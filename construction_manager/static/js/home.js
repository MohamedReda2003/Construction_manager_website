$(document).ready(function() {
    $('#add-site').click(function() {
        var name = $('#new-site-name').val();
        if (name) {
            $.ajax({
                url: '/api/add_construction_site/',
                method: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({ name: name }),
                success: function(response) {
                    $('#site-table-body').append(
                        '<tr data-id="' + response.id + '">' +
                        '<td>' + response.name + '</td>' +
                        '<td>' + response.last_modified + '</td>' +
                        '<td><button class="delete-site">Delete</button></td>' +
                        '</tr>'
                    );
                }
            });
        }
    });

    $(document).on('click', '.delete-site', function() {
        var row = $(this).closest('tr');
        var siteId = row.data('id');
        $.ajax({
            url: '/api/delete_construction_site/' + siteId + '/',
            method: 'DELETE',
            success: function() {
                row.remove();
            }
        });
    });
});
