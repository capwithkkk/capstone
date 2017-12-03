<?php
    include "database.php"
?>
<section>

<?php
    if($page != null && $maxItem != null && $quary != null && $sort != null){
        $rows = http_print_prod(($page - 1) * $maxItem,$maxItem,$quary,$sort,"전체");
        ?><br><?php
        foreach ($rows as $row) {
            $price_num = (is_numeric($row['price']))?number_format($row['price']):0;
            ?>
            <div id="content">
                <span><img class="img-rounded" src=<?=$row['pic_url']?> alt = <?=$row["name"]?>></span>
                <span>
                    <div><a href=<?=$row['url']?> tartet = "_blank"><span id="content_name"><?=$row["name"]?></span></a></div>
                    <div>판매처 :<span id="content_store"> <?=$row['store']?></span></div>
                    <div>가격 : <span id="content_price"> <?=$price_num?> 원</span></div>
                </span>
            </div>
            <br>
            <?php

        }

    }
?>
</section>
