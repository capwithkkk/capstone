<nav>
    <ul class="pagination">
    <?php
        if($page != null && $maxItem != null && $query != null && $sort != null){
            $maxItemCount = http_get_count($query,$category);
            $maxpage = ceil($maxItemCount / $maxItem);
            $search_page = "search.php";
            $start_page = ($page < 6)? 1:$page - 5;
            if($maxpage > 0){
                if($page > 1){
                    ?><li><a href="<?=$search_page?>?page=<?=$page-1?>&maxItem=<?=$maxItem?>&sort=<?=$sort?>&category=<?=$category?>&query=<?=$query?>"><이전</a></li><?php
                }
                $last_page = $maxpage<$start_page+10?$maxpage:$start_page+10;
                if($maxpage < $page){
                    ?><li class="active"><a href="#"><?=$page?></a></li><?php
                }
                else{
                    for($i = $start_page; $i <= $last_page; $i++){
                        if($i == $page){
                            ?><li class="active"><a href="#"><?=$i?></a></li><?php
                        }
                        else{
                            ?><li><a href="<?=$search_page?>?page=<?=$i?>&maxItem=<?=$maxItem?>&sort=<?=$sort?>&category=<?=$category?>&query=<?=$query?>"><?=$i?></a></li><?php
                        }
                    }
                }
                if($page < $maxpage){
            ?><li><a href="<?=$search_page?>?page=<?=$page+1?>&maxItem=<?=$maxItem?>&sort=<?=$sort?>&category=<?=$category?>&query=<?=$query?>">다음></a></li>
            <?php
                }
            }
        }
        ?>
    </ul>
</nav>
