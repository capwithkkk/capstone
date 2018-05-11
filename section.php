<section>
    <?php
        if($page != null && $maxItem != null && $query != null && $sort != null && $minPrice !== null && $maxPrice !== null && $minPrice <= $maxPrice ){
            $rows = http_print_prod(($page - 1) * $maxItem,$maxItem,$query,$sort,$category,$minPrice,$maxPrice);
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
                        <div id="advanced_option_selector" class="row">
                            <span class="col-xs-12">
                                <div class="list-group">
                                    <span class="list-group-item active">카테고리 (최대 6개 까지 선택가능):</span>
                                </div>
                                <div id="option_selector_category_list" class="list-group list-group-horizontal">
                                    <?php
                                        $category_rows = http_get_category(array_diff($category,['미분류',"전체"]));
                                        $category_rows = $category_rows->fetchAll();
                                        foreach($category_rows as $category_row){
                                            $temp_category = $category_row['category_name'];
                                            if($temp_category != "전체"){
                                            $temp_id = $category_row['category_id'];
                                                ?><a href="javascript:addAdvancedCategoryLabel('<?=$temp_category?>',<?=$temp_id?>);" class="list-group-item"><?=$temp_category?></a><?php
                                            }
                                        }
                                    ?>
                                </div>
                                <br>
                                <div id="option_selector_price_list" class="list-group list-group-horizontal">
                                    <form id="advanced_option_form">
                                        <input type="hidden" name="maxItem" value="<?=$maxItem?>" id="adv_search_param_maxItem">
                                        <input type="hidden" name="sort" value="<?=$sort?>" id="adv_search_param_sort">
                                        <label class="list-group-item active" for="price_input_min">가격범위:</label>
                                        <div class="list-group-item">
                                            <span><input type="text" name="minPrice" class="form-control input-sm number_only" id="price_input_min"></span>
                                            <span>~</span>
                                            <span><input type="text" name="maxPrice" class="form-control input-sm number_only" id="price_input_max"></span>
                                        </div>
                                        <label class="list-group-item active" for="product_input_name">제품명:</label>
                                        <div class="list-group-item">
                                            <span><input class="form-control" type="text" name="query" id="adv_search_param_input" placeholder="Search..." maxlength="255" autocomplete="off"></span>
                                        </div>
                                        <span>
                                            <legend>SEARCH</legend>
                                            <button id="option_selector_search_button" class="btn btn-default" type="submit"><span class="glyphicon glyphicon-search"></span></button>
                                        </span>
                                        <div id="option_selector_category_labels">
                                        </div>
                                        <span id="option_selector_error">
                                        </span>
                                    </form>
                                </div>
                            </span>
                        </div>
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
                                $category_name = (strpos($row['category_name'],"미분류") === false)?$row['category_name']:"미분류";
                                $category_url = "search.php?page=1&maxItem=$maxItem&sort=$sort&category%5B%5D=$category_name&query=$query"
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
                <p>잘못된 요청입니다. 빠진 키워드나 필수 입력 사항이 있는지 확인하시고, 다시 입력해주세요.</p>
            </div>
            <?php
        }
    ?>

</section>
