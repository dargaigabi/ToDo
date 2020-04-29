$('.form-control').change(function(){
    var field_id=$(this).attr('id');
    
    $.ajax({
        method: 'POST',
        url: '/plans/allocation/' + field_id,
        data: {
            field_value: $(this).val()
        }, 
        success: function(response) {
            var amount = parseInt(response['amount'])
            var type_id = response['type_id']
            var original_amount = parseInt($('#' + type_id).val())
            $('#' + type_id).val(original_amount + amount)
        }
    });
})

$('.period_selector').change(function() {
    var field_id=$(this).children(':selected').data('id');
    console.log(field_id)
    $.ajax({
        method: 'POST',
        url: '/plans/period/' + field_id,
        success : function(response) {
            var planned_amounts = response['planned_amounts']

        }
    })
})