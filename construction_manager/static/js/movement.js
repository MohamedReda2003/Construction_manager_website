$(document).ready(function() {
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    const csrftoken = getCookie('csrftoken');

    $('#departure_site').change(function() {
        var siteId = $(this).val();
        if (siteId) {
            $.ajax({
                url: '/api/get_materials_for_site/' + siteId + '/',
                method: 'GET',
                success: function(response) {
                    var materialSelect = $('#material_description');
                    materialSelect.empty();
                    materialSelect.append('<option value="">Select Material</option>');
                    response.forEach(function(material) {
                        materialSelect.append('<option value="' + material.id + '" data-quantity="' + material.quantity + '">' + material.description + '</option>');
                    });
                }
            });
        } else {
            $('#material_description').empty();
            $('#material_description').append('<option value="">Select Material</option>');
        }
    });

    $('#material_description').change(function() {
        var selectedOption = $(this).find('option:selected');
        var maxQuantity = selectedOption.data('quantity');
        $('#quantity').attr({
            'max': maxQuantity,
            'min': 0
        });
    });

    $('#move-material').click(function() {
        var quantityInput = $('#quantity');
        var maxQuantity = parseInt(quantityInput.attr('max'), 10);
        var quantity = parseInt(quantityInput.val(), 10);

        if (quantity > maxQuantity) {
            alert('Quantity exceeds available amount at departure site');
            return;
        }

        var data = {
            departure_site: $('#departure_site').val(),
            material_description: $('#material_description').val(),
            quantity: quantity,
            destination_site: $('#destination_site').val()
        };

        $.ajax({
            url: '/api/move_material/',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(data),
            headers: {
                'X-CSRFToken': csrftoken
            },
            success: function(response) {
                alert('Material moved successfully');
                // Optionally, update the UI to reflect the changes
            },
            error: function(xhr) {
                alert(xhr.responseText);
            }
        });
    });
});
