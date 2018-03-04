<?php
    $host = "localhost";
    $user = "admin";
    $password = "admin";
    $database = "capstone";
    $db = new PDO("mysql:dbname=$database;host=$host;charset=utf8", $user,$password);
    $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    function make_core_condition($db, $key, $category){
        $core_cond = "";
        if($category != null){
            $category = $db->quote($category);
            $core_cond .= "category_id in (SELECT category_id FROM category WHERE (category_name = $category or category_name in (SELECT T1.category_name FROM category AS T1 INNER JOIN (SELECT category_name FROM category WHERE parent_name = $category) AS T2 ON T2.category_name = T1.parent_name OR T1.parent_name = $category GROUP BY T1.category_name))) ";
        }
        if($key != null){
            if($core_cond != ""){
                $core_cond .= "and ";
            }
            $key = $db->quote("%".$key."%");
            $core_cond .= "name LIKE $key";
        }
        return $core_cond;
    }

    function http_print_prod($rankMin,$limit,$key,$option,$category){
        global $db;

        if(is_numeric($rankMin)  && is_numeric($limit)){
            $core_cond = make_core_condition($db, $key, $category);
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
            $full_query =  "SELECT product.*, category_name FROM product RIGHT JOIN category using(category_id) WHERE $core_cond $sort_query LIMIT $rankMin,$limit";
            $rows = $db->query($full_query);

            return $rows;

        }
        else {
            return $db->query("SELECT * from category");
        }
    }

    function http_get_count($key,$category){
        global $db;
        $core_cond = make_core_condition($db, $key, $category);
        $full_query = "SELECT count(*) FROM product WHERE $core_cond";
        $rows = $db->query($full_query);
        $count = 0;
        foreach($rows as $row){
            $count = $row['count(*)'];
        }
        return $count;
    }

    function http_get_category(){
        global $db;
        $full_query =  "SELECT * from category";
        $rows = $db->query($full_query);
        return $rows;
    }



?>
