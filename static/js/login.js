$('#log_in').click(function() {
    var username = $('#username').val();
    var password = $('#password').val();
    
    $.ajax({
        method: 'POST',
        url: '/verify_user',
        data: {
            username: username,
            password: password
        },
        success: function(response) {
            if (response === "ok") {
                console.log("ok")
            }
        }
    });
});
