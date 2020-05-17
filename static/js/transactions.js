$(document).ready(function() {
    var periodId = $('.transaction_period_selector').children(':selected').data('id');
    fillTableWithTransactionData(periodId);
})

$('.transaction_period_selector').change(function() {
    var periodId = $(this).children(':selected').data('id');
    fillTableWithTransactionData(periodId);
})

function fillTableWithTransactionData(periodId) {
    $.ajax({
        url: "/" + periodId,
        method: 'POST',
        success: function(response) {
            var table = $('#transaction_table')
            table.empty()
            var transaction_list = response['list_of_transactions']
            for (var i = 0; i < transaction_list.length; i++) {
                var id = transaction_list[i][3]
                var date = transaction_list[i][1]
                var category = transaction_list[i][0]
                var detail = transaction_list[i][2]
                var amount = transaction_list[i][4]

                table.append('<tr><td>' + id + 
                            '</td><td>' + date + 
                            '</td><td>' + category + 
                            '</td><td>' + detail +
                            '</td><td>' + amount + '</td></tr>')
            }

            var dictionary_of_sums = response['dictionary_of_sums']
            $('#1').val(dictionary_of_sums['recurring_expenses'])
            $('#2').val(dictionary_of_sums['one_time_expenses'])
            $('#3').val(dictionary_of_sums['recurring_incomes'])
            $('#4').val(dictionary_of_sums['one_time_incomes'])
            $('#5').val(dictionary_of_sums['sum'])
        }
    });
}