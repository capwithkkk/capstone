<?php
    $host = "localhost";
    $user = "admin";
    $password = "admin";
    $database = "capstone";
    $db = new PDO("mysql:dbname=$database;host=$host;charset=utf8", $user,$password);
    $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);


    function http_print_prod($rankMin,$limit,$key,$option,$category){
        global $db;

        if(is_numeric($rankMin)  && is_numeric($limit)){
            $key = $db->quote("%".$key."%");
            $category = $db->quote($category);

            switch($option){
                case "low_price":
                    $sort_query = "ORDER BY price asc";
                    break;
                case "high_price":
                    $sort_query = "ORDER BY price desc";
                    break;
                default:
                    $sort_query = "";
                    break;
            }

            $full_query =  "SELECT product.* from product NATURAL JOIN category WHERE name LIKE $key and (category_name = $category or category_name in (SELECT T1.category_name FROM category AS T1 INNER JOIN (SELECT category_name FROM category WHERE parent_name = $category) AS T2 ON T2.category_name = T1.parent_name OR T1.parent_name = $category GROUP BY T1.category_name)) $sort_query LIMIT $rankMin,$limit";

            $rows = $db->query($full_query);

            return $rows;

        }
        else {
            return $db->query("SELECT * from category");
        }
    }



?>
