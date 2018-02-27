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
                ?>
                    <div id="section_options" class="container">
                        <!-- <div id="advanced_option_selector" class="row">
                            <span class="col-xs-12">
                                <div class="list-group list-group-horizontal">
                                    <span class="list-group-item active">카테고리:</span>
                                </div>
                                <div id="option_selector_category_list" class="list-group list-group-horizontal">
                                    <a href="javascript:;" class="list-group-item">카테고리1</a>
                                    <a href="javascript:;" class="list-group-item">카테고리2</a>
                                    <a href="javascript:;" class="list-group-item">카테고리3</a>
                                </div>
                                <br>
                                <div id="option_selector_price_list" class="list-group list-group-horizontal">
                                    <label class="list-group-item active" for="price_input_min">가격범위:</label>
                                    <div class="list-group-item">
                                        <span><input type="text" class="form-control input-sm" id="price_input_min"></span>
                                        <span>~</span>
                                        <span><input type="text" class="form-control input-sm" id="price_input_max"></span>
                                    </div>
                                    <label class="list-group-item active" for="product_input_name">브랜드/제품명:</label>
                                    <div class="list-group-item">
                                        <span><input type="text" class="form-control" id="price_input_min"></span>
                                    </div>
                                    <span>
                                        <button id="option_selector_prodict_button" class="btn btn-default" type="submit"><span class="glyphicon glyphicon-search"></span></button>
                                    </span>
                                </div>
                            </span>
                        </div> -->
                    </div>
                    <div id="item_contents" class="container">
                <?php
                foreach ($rows as $row) {
                    $price_num = (is_numeric($row['price']))?number_format($row['price']):0;
                    ?>
                    <div class="content row">
                        <span class="col-xs-2"><img class="img-rounded" src=<?=$row['pic_url']?> alt = <?=$row["name"]?>></span>
                        <span class="col-xs-4">
                            <div><a href=<?=$row['url']?> tartet = "_blank"><span class="content_name"><?=$row["name"]?></span></a></div>
                            <div>판매처 : <span class="content_store"><?=$row['store']?></span></div>
                            <?php
                                $category_name = $row['category_name'];
                                $category_url = "search.php?page=1&maxItem=$maxItem&sort=$sort&category=$category_name&query=$query"
                            ?>
                            <div>카테고리 : <a href="<?=$category_url?>" class="content_category"><?=$category_name?></a></div>
                        </span>
                        <span class="col-xs-3">
                            <div><span class="content_price"> <?=$price_num?> </span>원</div>
                        </span>
                        <span class="col-xs-3">
                            <div>브랜드 : <span class="content_brand"><?=$row['brand']?></span></div>
                        </span>
                    </div>
                    <br>
                    <?php
                }
                ?>
                </div>
                <?php
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
