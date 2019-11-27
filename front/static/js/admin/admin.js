$(document).ready(function () {
    function mark_red(tag){
        $(tag).css('border-color', 'red');
        $(tag).css('border-width', '2px');
    }

    function unmark_red(tag){
        $(tag).css('border-color', '');
        $(tag).css('border-width', '');
    }
    // ADD IP
    $("#blacklist-ip-content button").click(function(){
        var ip_addr = $('#blacklist-ip-content input').val().trim();
        unmark_red('#blacklist-ip-content input');
        $('#alert').hide();
        // check if the value is ip address format
        if(ip_addr.match(/^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$/)){
            // ajax call
            var api_url = '/blacklist_ip/'
            $.ajax({
                url: api_url,
                headers: {'Access-Control-Allow-Origin':'*'},
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
			            if(result.details == "IP Address already banned."){
			                mark_red('#blacklist-ip-content input');
                            $('#blacklist-ip-content').css('margin-top', '0');
                            $('#warning-msg').text("duplicated IP address").show();   
			            }
			            else{
                            $('#alert > strong').text('Server Error!');
                            $('#alert').show();
			            }
                    }
                },
                error: function(xhr, textStatus, errorThrown){
                    $('#alert > strong').text('Internal Error!');
                    $('#alert').show();
                }
            });
            // hide warning
            unmark_red('#blacklist-ip-content input');
            $('#blacklist-ip-content').css('margin-top', '2rem');
            $('#warning-msg').hide();
        }
        else{
            // show warning
	        mark_red('#blacklist-ip-content input');
            $('#blacklist-ip-content').css('margin-top', '0');
            $('#warning-msg').text("wrong input format").show();
        }
    }); 

    // MOD threshold
    $('#threshold-inner-content button').click(function(){
        var maxretry = $('#maxretry').val();
        var findtime = $('#findtime').val();
        var bantime = $('#bantime').val();
        var no_error = true;
        unmark_red('#maxretry');
        unmark_red('#findtime');
        unmark_red('#bantime');
        $('#alert').hide();
        // check if maxretry value is non-zero positive integer or not
        if(!(parseInt(maxretry).toString() === maxretry && parseInt(maxretry) > 0)){
            mark_red('#maxretry');
            no_error &= false;
	    }
	    // check if findtime value is non-zero positive integer or not
        if(!(parseInt(findtime).toString() === findtime && parseInt(findtime) > 0)){
            mark_red('#findtime');
            no_error &= false;
        }
        // check if maxretry value is non-zero positive integer or not
        if(!(parseInt(bantime).toString() === bantime && parseInt(bantime) > 0)){
            mark_red('#bantime');
            no_error &= false;
        }
	    if(no_error){		    
            // ajax call
            var api_url = '/set_threshold/'
            $.ajax({
                url: api_url,
                headers: {'Access-Control-Allow-Origin':'*'},
                contentType: "application/json",
                dataType: 'json',
                type: 'PUT',
                data: {maxretry: maxretry, findtime: findtime, bantime: bantime},
                success: function(result){
                    if(result.status == 200){
                        $('#maxretry').val(maxretry);
                        $('#findtime').val(findtime);
                        $('#bantime').val(bantime);
                        $('#alert').attr('class', 'alert alert-info fade in');
                        $('#alert > strong').text('Succesfully Changed');
                        $('#alert').show();
                    }
                    else{
            			$('#alert').attr('class', 'alert alert-danger fade in');
                        $('#alert > strong').text('Server Error!');
			            $('#alert').show();
                    }
                },
                error: function(xhr, textStatus, errorThrown){
   		            $('#alert').attr('class', 'alert alert-danger fade in');
                    $('#alert > strong').text('Internal Error!');
		            $('#alert').show();
                }
            });
        }
    });
    // MOD password
    $('#password-inner-content button').click(function(){
        var password = $('#new_password').val();
        var confirmed_password = $('#confirmed_password').val();
        unmark_red("#confirmed_password");
        $('#alert').hide();
        // check if the values are identical
        if(password == confirmed_password){
            // ajax call
            var api_url = '/password/'
            $.ajax({
                url: api_url,
                headers: {'Access-Control-Allow-Origin':'*'},
                contentType: "application/json",
                dataType: 'json',
                type: 'PUT',
                data: {password: password, confirmed_password: confirmed_password},
                success: function(result){
                    if(result.status == 200){
                        $('#new_password').val('');
                        $('#confirmed_password').val('');
                        $('#alert').attr('class', 'alert alert-info fade in');
                        $('#alert > strong').text('Succesfully Changed');
                        $('#alert').show();
                    }
                    else{
            			$('#alert').attr('class', 'alert alert-danger fade in');
                        $('#alert > strong').text('Server Error!');
			            $('#alert').show();
                    }
                },
                error: function(xhr, textStatus, errorThrown){
   		            $('#alert').attr('class', 'alert alert-danger fade in');
                    $('#alert > strong').text('Internal Error!');
		            $('#alert').show();
                }
            });
        }
        else{
	        mark_red('#confirmed_password');
        }
    });
});
