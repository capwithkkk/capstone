<?php
    $host = "localhost";
    $user = "admin";
    $password = "admin";
    $database = "capstone";
    $db = new PDO("mysql:dbname=$database;host=$host;charset=utf8", $user,$password);
    $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    function make_core_condition($db, $key, $category){
        $core_cond = "";
        if(!empty($category)){
            $first = "";
            $second = "";
            $third = "";
            foreach($category as $unit){
                $unit = $db->quote($unit);
                $first .= "category_name = $unit or ";
                $second .= "parent_name = $unit or ";
                $third .= "T1.parent_name = $unit or ";
            }
            $first = substr($first,0,-3);
            $second = substr($second,0,-3);
            $third = substr($third,0,-3);

            $core_cond .= "category_id in (SELECT category_id FROM category WHERE ($first or category_name in (SELECT T1.category_name FROM category AS T1 INNER JOIN (SELECT category_name FROM category WHERE $second) AS T2 ON T2.category_name = T1.parent_name OR $third GROUP BY T1.category_name))) ";
        }
        if($key != null){
            if($core_cond != ""){
                $core_cond .= "and ";
            }
            $key = $db->quote("*$key*");
            $core_cond .= "MATCH(name,brand) against($key in boolean mode)";
        }
        return $core_cond;
    }

    function http_print_prod($rankMin,$limit,$key,$option,$category,$minPrice,$maxPrice){
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
                case "new_date":
                    $sort_query = "ORDER BY category_id desc";
                    break;
                default:
                    $sort_query = "";
                    break;
            }
            $minPrice = $db->quote($minPrice);
            $maxPrice = $db->quote($maxPrice);
            $full_query =  "SELECT product.*, category_name FROM product RIGHT JOIN category using(category_id) WHERE $core_cond and price >= $minPrice and price <= $maxPrice $sort_query LIMIT $rankMin,$limit";
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

    function http_get_category($category){
        global $db;
        if(!empty($category)){
            $first = "";
            foreach($category as $unit){
                $unit = $db->quote($unit);
                $first .= "category_name = $unit or ";
            }
            $first = substr($first,0,-3);
            $full_query =  "SELECT * FROM category WHERE parent_name IN (SELECT parent_name FROM category WHERE $first)";
        }else{
            $full_query =  "SELECT * FROM category WHERE parent_name != '미분류'";
        }
        $rows = $db->query($full_query);
        return $rows;
    }




?>
