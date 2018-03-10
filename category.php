<?php
    include 'exception.php';
    include "database.php";
    class Tree{

        public $name;
        public $child;

        function __construct($name){
            $this->name = $name;
            $this->child = array();
        }

        function push($node){
            array_push($this->child,$node);
        }

        function toJson(){
            return json_encode($this);
        }

    }


    function getChild($rows,$parent){
        $arr = array();
        foreach($rows as $row){
            if($row['parent_name'] === $parent && $parent !== $row['category_name']){
                array_push($arr,$row);
            }
        }
        return $arr;
    }

    function make_recursivly($rows,$target){
        $name = $target['category_name'];
        $node = new Tree($target['category_name']);

        $child = getChild($rows,$name);
        if(count($child) > 0){
            reset($child);
            foreach($child as $row){
                $node->push(make_recursivly($rows,$row));
            }
        }

        return $node;
    }



    $rows = http_get_category(null);
    $rows = $rows->fetchAll();
    foreach($rows as $row){
        if($row['parent_name'] === $row['category_name']){
            $root = $row;
            break;
        }
    }



    header("Content-Type:application/json");
    $result = make_recursivly($rows,$root);
    print mb_convert_encoding($result->toJson(),"UTF-8");
?>
