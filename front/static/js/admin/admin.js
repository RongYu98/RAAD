$(document).ready(function () {
    // ADD IP
    $("#blacklist-ip-content button").click(function(){
        var ip_addr = $('#blacklist-ip-content input').val().trim();
	
        // check if the value is ip address format
        if(ip_addr.match(/^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$/)){
            // ajax call
            var api_url = '/add_ip/'
            $.ajax({
                url: api_url,
                headers: {
                    'Access-Control-Allow-Origin':'*',
                },
                contentType: "application/json",
                dataType: 'json',
                type: 'POST',
                data: {ip: ip_addr},

                success: function(result){
                    if(result.status == 200){
                        $('#blacklist-ip-content input').val("");
                        $('#alert').hide();
			window.location.href = "/admin/blacklist";
                    }
                    else{
                        $('#alert > strong').text('Server Error!');
                        $('#alert').show();
                    }
                },
                error: function(xhr, textStatus, errorThrown){
                    $('#alert > strong').text('Internal Error!');
                    $('#alert').show();
                }
            });
            // hide warning
            $('#blacklist-ip-content input').css('border-color', '');
            $('#blacklist-ip-content input').css('border-width', '');
            $('#blacklist-ip-content').css('margin-top', '2rem');
            $('#warning-msg').hide();
        }
        else{
            // show warning
            $('#blacklist-ip-content input').css('border-color', 'red');
            $('#blacklist-ip-content input').css('border-width', '2px');
            $('#blacklist-ip-content').css('margin-top', '0');
            $('#warning-msg').show();
        }
    }); 

    // MOD threshold
    $('#threshold-inner-content button').click(function(){
        var maxretry = $('#maxretry').val();
        var findtime = $('#findtime').val();
        var bantime = $('#bantime').val();
        // check if the values are integer
        if(maxretry.match(/[0-9 -()+]+$/) && findtime.match(/[0-9 -()+]+$/) && bantime.match(/[0-9 -()+]+$/)){
            // ajax call
            var api_url = 'http://127.0.0.1:9000/set_threshold'
            $.ajax({
                url: api_url,
                headers: {
                    'Access-Control-Allow-Origin':'*',
                },
                contentType: "application/json",
                dataType: 'json',
                type: 'PUT',
                data: {maxretry: maxretry, findtime: findtime, bantime: bantime},
                success: function(result){
                    if(result.status == 200){
                        $('#maxretry').val(maxretry);
                        $('#findtime').val(findtime);
                        $('#bantime').val(bantime);
                        $('#alert').hide();
                    }
                    else{
                        $('#alert > strong').text('Server Error!');
                        $('#alert').show();
                    }
                },
                error: function(xhr, textStatus, errorThrown){
                    $('#alert > strong').text('Internal Error!');
                    $('#alert').show();
                }
            });
        }
        else{
            if(!maxretry.match(/[0-9 -()+]+$/)){
                // warning
                $('#maxretry').css('border-color', 'red');
                $('#maxretry').css('border-width', '2px');
            } 
            if(!findtime.match(/[0-9 -()+]+$/)){
                // warning
                $('#findtime').css('border-color', 'red');
                $('#findtime').css('border-width', '2px');
            } 
            if(!bantime.match(/[0-9 -()+]+$/)){
                // warning
                $('#bantime').css('border-color', 'red');
                $('#bantime').css('border-width', '2px');
            }
        }
    })
    // MOD password
    $('#password-inner-content button').click(function(){
        var password = $('#password').val();
        var confirmed_password = $('#confirmed_password').val();
        // check if the values are identical
        if(password == confirmed_password){
            var shaObj = new jsSHA("SHA-256", "TEXT");
            shaObj.update(password);
            var hash = shaObj.getHash("HEX");
            // ajax call
        }
        else{
            $('#confirmed_password').css('border-color', 'red');
            $('#confirmed_password').css('border-width', '2px');
        }
    })
});
