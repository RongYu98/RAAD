$(document).ready(function () {
	// LOGIN
    $('#sign-in').click(function(){
        var username = $('#username input').val();
        var password = $('#password input').val();
        username.replace("<", "&lt");
        username.replace(">", "&gt");
        $('#alert').hide();
        
        // ajax call
        var api_url = '/signin/'
        $.ajax({
            url: api_url,
            headers: {'Access-Control-Allow-Origin':'*'},
            contentType: "application/json",
            dataType: 'json',
            type: 'POST',
            data: {username: username, password: password},
            success: function(result){
                if(result.status == 200){
                    window.location.href = "/admin/blacklist";
                }
                else{
                    window.location.href = "/admin";
                }
            },
            error: function(xhr, textStatus, errorThrown){
                window.location.href = "/admin";
            }
        });
    });
});