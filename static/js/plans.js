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
            countAllocation();
        }
    });
})

function countAllocation() {
    var recurring_expenses = parseInt($('#1').val());
    var one_time_expenses = parseInt($('#2').val());
    var recurring_incomes = parseInt($('#3').val());
    var one_time_incomes = parseInt($('#4').val());
    var recurring_savings = parseInt($('#5').val());
    var one_time_savings = parseInt($('#6').val());
    var amount_to_allocate = recurring_incomes + one_time_incomes - recurring_expenses - one_time_expenses - recurring_savings - one_time_savings;
    $('#amount_to_allocate').val(amount_to_allocate);
}


$('.period_selector').change(function() {
    var field_id=$(this).children(':selected').data('id');
    $.ajax({
        method: 'POST',
        url: '/plans',
        data: {
            period_id: field_id
        },
        success : function(response) {
            var planned_amounts = response['list_of_plans']
            for (var i = 0; i < planned_amounts.length; i++) {
                var amount = planned_amounts[i][2]
                $('#category-' + (i + 1)).val(amount)
            }
            updateSummary()
        }
    })
})

$(document).ready(function() {
    updateSummary()
})

function updateSummary() {
    resetSummary();
    $('.planned-amount').each(function() {
        var type_id = $(this).data('type-id');
        var original_amount = parseInt($('#' + type_id).val());
        var amount = parseInt($(this).val());
        $('#' + type_id).val(original_amount + amount);
        countAllocation()
    })
}

function resetSummary() {
    var recurring_expenses = parseInt($('#1').val(0));
    var one_time_expenses = parseInt($('#2').val(0));
    var recurring_incomes = parseInt($('#3').val(0));
    var one_time_incomes = parseInt($('#4').val(0));
    var recurring_savings = parseInt($('#5').val(0));
    var one_time_savings = parseInt($('#6').val(0));
}