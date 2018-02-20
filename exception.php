<?php
    function errorFunction($errno, $errstr){
        die("ERROR $errno: $errstr.");
    }
    function invalid_request($errno, $errstr){
        errorFunction(400,"Invalid Request");
    }
    if (!isset($_SERVER["REQUEST_METHOD"])) {
        header("HTTP/1.1 $errno $errstr");
        errorFunction(400,"Invalid Request");
    }
    if($_SERVER["REQUEST_METHOD"] != "GET"){
        header("HTTP/1.1 $errno $errstr");
        errorFunction(405,"Method Not Allowed");
    }
    set_error_handler("invalid_request");
?>
