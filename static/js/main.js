$('.form-control').change(function(){
    var field_id=$(this).attr('id');
    
    $.ajax({
        method: 'POST',
        url: '/plans/' + field_id,
        data: {
            field_value: $(this).val()
        }, 
        success: function(response) {
            amount = parseInt(response['amount'])
            type_id = response['type_id']
            original_amount = parseInt($('#' + type_id).val())
            $('#' + type_id).val(original_amount + amount)
        }
    });
})