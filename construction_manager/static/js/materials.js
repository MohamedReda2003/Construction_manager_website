$(document).ready(function() {
    $('#add-material').click(function() {
        var data = {
            description: $('#description').val(),
            quantity: $('#quantity').val(),
            unit: $('#unit').val(),
            unit_price: $('#unit_price').val(),
            total_price: $('#total_price').val(),
            n_bc: $('#n_bc').val(),
            n_bl: $('#n_bl').val(),
            supplier: $('#supplier').val(),
            site_id: $('#site_id').val(),
            notes: $('#notes').val()
        };
        $.ajax({
            url: '/api/add_material/',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(data),
            success: function(response) {
                $('#material-table-body').append(
                    '<tr data-id="' + response.id + '">' +
                    '<td>' + response.description + '</td>' +
                    '<td>' + response.quantity + '</td>' +
                    '<td>' + response.unit + '</td>' +
                    '<td>' + response.unit_price + '</td>' +
                    '<td>' + response.total_price + '</td>' +
                    '<td>' + response.n_bc + '</td>' +
                    '<td>' + response.n_bl + '</td>' +
                    '<td>' + response.entry_date + '</td>' +
                    '<td>' + response.supplier + '</td>' +
                    '<td>' + response.site + '</td>' +
                    '<td>' + response.notes + '</td>' +
                    '<td><button class="delete-material">Delete</button></td>' +
                    '</tr>'
                );
            }
        });
    });

    $(document).on('click', '.delete-material', function() {
        var row = $(this).closest('tr');
        var materialId = row.data('id');
        $.ajax({
            url: '/api/delete_material/' + materialId + '/',
            method: 'DELETE',
            success: function() {
                row.remove();
            }
        });
    });
});
