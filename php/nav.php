<nav>
    <?php
        $search_page = "search.php";
        $start_page = ($page < 6)? 1:$page - 5;
        if($page > 1){
            ?><a href="<?=$search_page?>?page=<?=$page-1?>&maxItem=<?=$maxItem?>&sort=<?=$sort?>&quary=<?=$quary?>"><이전</a><?php
        }

        for($i = $start_page; $i < $start_page+10; $i++){
            if($i == $page){
                ?><strong><?=$i?></strong><?php
            }
            else{
                ?><a href="<?=$search_page?>?page=<?=$i?>&maxItem=<?=$maxItem?>&sort=<?=$sort?>&quary=<?=$quary?>"><?=$i?></a><?php
            }
        }
        ?><a href="<?=$search_page?>?page=<?=$page+1?>&maxItem=<?=$maxItem?>&sort=<?=$sort?>&quary=<?=$quary?>">다음></a>
</nav>
