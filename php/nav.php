<nav>
    <ul class="pagination">
    <?php
        $search_page = "search.php";
        $start_page = ($page < 6)? 1:$page - 5;
        if($page > 1){
            ?><li><a href="<?=$search_page?>?page=<?=$page-1?>&maxItem=<?=$maxItem?>&sort=<?=$sort?>&category=<?=$category?>&quary=<?=$quary?>"><이전</a></li><?php
        }

        for($i = $start_page; $i < $start_page+10; $i++){
            if($i == $page){
                ?><li class="active"><a href="#"><?=$i?></a></li><?php
            }
            else{
                ?><li><a href="<?=$search_page?>?page=<?=$i?>&maxItem=<?=$maxItem?>&sort=<?=$sort?>&category=<?=$category?>&quary=<?=$quary?>"><?=$i?></a></li><?php
            }
        }
        ?><li><a href="<?=$search_page?>?page=<?=$page+1?>&maxItem=<?=$maxItem?>&sort=<?=$sort?>&category=<?=$category?>&quary=<?=$quary?>">다음></a></li>
    </ul>
</nav>
