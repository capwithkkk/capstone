<!DOCTYPE html>
<html>
	<!-- Latest compiled and minified CSS -->
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">

	<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
	<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
	<meta http-equiv="Content-Type" content="text/html" charset="utf-8" />
	<link rel="stylesheet" href="/capstone/css/main.css" type="text/css"/>
	<script src="/capstone/js/custom.js"></script>
	<head>
		<title>Client Side</title>
	</head>


	<body>
        <?php
			if (!isset($_SERVER["REQUEST_METHOD"]) || $_SERVER["REQUEST_METHOD"] != "GET") {
		    	header("HTTP/1.1 400 Invalid Request");
		    	die("ERROR 400: Invalid request.");
		    }
			$page = $_GET['page'];
			$maxItem = $_GET['maxItem'];
			$sort = $_GET['sort'];
			$quary = $_GET['quary'];
			$category = $_GET['category'];
            include 'header.php';
            include 'section.php';
            include 'nav.php';
            include 'footer.php';
        ?>
    </body>

</html>
