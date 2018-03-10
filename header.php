<header>
    <div class="container">
        <div id="logo" class="row">
            <a id="logo_link" href="/capstone">
                <img id="logo_image" src="image/logo.png" alt="Logo">
            </a>
        </div>
        <div id="search" class="row">
            <div class="col-xs-1">
                <span></span>
    			<a id="search_option_category" href="#" data-toggle="modal" data-target="#popup_category" >
    				<img id="category_image_small" src="image/category.png">
    			</a>
    		</div>
    		<div class="col-xs-1">
                <span></span>
    			<a id="search_option_setting" href="#" data-toggle="modal" data-target="#popup_setting">
    				<img id="setting_image_small" src="image/page_option.png">
    			</a>
    		</div>
            <div class="col-xs-4">
                <span class="label label-default" id="category_label">카테고리 : <?=$category[0]?></span>
                <form id="search_form" action="search.php" onsubmit="setHTTPGetParam('search')" metohd="get">
                    <fieldset>
                        <legend>SEARCH</legend>
                        <input type="hidden" name="maxItem" value="<?=$maxItem?>" id="search_param_maxItem">
                        <input type="hidden" name="sort" value="<?=$sort?>" id="search_param_sort">
                        <input type="hidden" name="category[]" value="<?=$category[0]?>" id="search_param_category">
                        <div class="input-group input-group-sm">
                            <input class="form-control" type="text" name="query" value="<?=$query?>" id="search_param_input" placeholder="Search..." maxlength="255" autocomplete="off">
                            <span class="input-group-btn">
                                <button id="search_button" class="btn btn-default" type="submit"><span class="glyphicon glyphicon-search"></span></button>
                            </span>
                        </div>
                    </fieldset>
                </form>
            </div>
        </div>

    </div>
</header>
<div id="popup_category" class="modal fade" role="dialog" >
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal">&times;</button>
                <h4 class="modal-title">카테고리(클릭으로 펼치기)</h4>
            </div>
            <div class="modal-body">
				<ul class="list-group" id="category_core">
				</ul>
			</div>
        </div>
    </div>
</div>
<div id="popup_setting" class="modal fade" role="dialog" >
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal">&times;</button>
                <h4 class="modal-title">페이지옵션</h4>
            </div>
            <div class="modal-body" id="option_core">
                <div class="row">
                    <div class="dropdown">
                        <label for="search_option_sort" class="col-xs-4">정렬옵션 :</label>
                        <div class="col-xs-4">
                            <?php
                                $dropdown_text = "N/A";
                                switch($sort){
                                    case "new_date":
                                        $dropdown_text = "최신 등록순";
                                        break;
                                    case "low_price":
                                        $dropdown_text = "낮은 가격순";
                                        break;
                                    case "high_price":
                                        $dropdown_text = "높은 가격순";
                                        break;

                                }
                            ?>
                            <button class="btn dropdown-toggle" id="search_option_sort" type="button" data-toggle="dropdown" value="<?=$sort?>"><?=$dropdown_text?> <span class="caret"></span></button>
                            <ul class="dropdown-menu">
                                <li><a href="javascript:void(0)" class="search_option_sort_item" title="new_date">최신 등록순</a></li>
                                <li><a href="javascript:void(0)" class="search_option_sort_item" title="low_price">낮은 가격순</a></li>
                                <li><a href="javascript:void(0)" class="search_option_sort_item" title="high_price">높은 가격순</a></li>
                            </ul>
                        </div>
                    </div>
                </div>
                <div class="row">
                    <div class="dropdown">
                        <label for="search_option_maxItem" class="col-xs-4">페이지 당 표시 :</label>
                        <div class="col-xs-4">
                            <button class="btn dropdown-toggle" id="search_option_maxItem" type="button" data-toggle="dropdown" value="<?=$maxItem?>"><?=$maxItem?>개 <span class="caret"></span></button>
                            <ul class="dropdown-menu">
                                <li><a href="javascript:void(0)" class="search_option_maxItem_item" title="8">8개</a></li>
                                <li><a href="javascript:void(0)" class="search_option_maxItem_item" title="16">16개</a></li>
                                <li><a href="javascript:void(0)" class="search_option_maxItem_item" title="30">30개</a></li>
                            </ul>
                        </div>
                    </div>
                </div>
                <div class="row">
                    <button id="setting_ok" type="button" class="btn" data-dismiss="modal">확인</button>
                </div>

            </div>
        </div>
    </div>
</div>
