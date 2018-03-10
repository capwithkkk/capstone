<?php
	include 'exception.php';
?>
<!DOCTYPE html>
<html>
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">

	<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
	<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
	<meta http-equiv="Content-Type" content="text/html" charset="utf-8">
	<link rel="stylesheet" href="css/main.css" type="text/css"/>
	<link rel="icon" type="image/png" sizes="32x32" href="image/favicon-32x32.png">
	<script src="js/custom.js"></script>
	<head>
		<title>MarketExplorer</title>
	</head>


	<body>
        <?php
			try{
				$page = isset($_GET['page'])?$_GET['page']:1;
				$maxItem = isset($_GET['maxItem'])?$_GET['maxItem']:null;
				$sort = isset($_GET['sort'])?$_GET['sort']:null;
				$query = isset($_GET['query'])?$_GET['query']:null;
				$category = isset($_GET['category'])&&!empty($_GET['category'])?$_GET['category']:array("전체");
				$minPrice = isset($_GET['minPrice'])?$_GET['minPrice']:0;
				$maxPrice = isset($_GET['maxPrice'])?$_GET['maxPrice']:2147483647;
				include 'database.php';
	            include 'header.php';
	            include 'section.php';
	            include 'nav.php';
	            include 'footer.php';
			}catch(Exception $e){
				errorFunction(500 ,"Internal Server Error");
			}
        ?>
    </body>

</html>
