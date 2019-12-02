<?php

$wgHooks['AuthManagerLoginAuthenticateAudit'][] = 'loginAttempt';                                                       
function loginAttempt($response, $user, $username) {
	global $RAADMWfile;
	#$time = date("Y n j H i s");
	$time = date("U");
	$ip = $_SERVER['REMOTE_ADDR'];
	if ($response->status == "PASS") {
		error_log("$time Successful login from $ip".PHP_EOL, 3, $RAADMWfile);
	} else {
		error_log("$time Failed login from $ip".PHP_EOL, 3, $RAADMWfile);
	}
        return true;                                                                                                    }
