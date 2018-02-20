<section>
<?php
    if($page != null && $maxItem != null && $query != null && $sort != null){
        $rows = http_print_prod(($page - 1) * $maxItem,$maxItem,$query,$sort,$category);
        ?><br><?php
        if($rows->rowCount() <= 0){
            ?>
            <div id="no_item">
                <img id="image_magnifier" src="image/magnifier.png" alt="search">
                <p>"<?= $query?>"에 대한 검색결과가 없습니다. 다른 키워드를 넣어 입력해보세요.</p>
            </div>
            <?php
        }
        else{
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
    }else{
        ?>
        <div id="no_item">
            <img id="image_forbidden" src="image/forbidden.png" alt="search">
            <p>잘못된 키워드입니다. 다시 입력해주세요.</p>
        </div>
        <?php
    }
?>
</section>
