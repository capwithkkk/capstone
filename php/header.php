<header>
    <div class="container">
    <div id="search" class="row">
        <div class="col-xs-4">
            <form id="search_form" action="search.php" onsubmit="setHTTPGetParam('search')" metohd="get">
                <fieldset>
                    <legend>SEARCH</legend>
                    <input type="hidden" name="page" value="1" id="search_param_page">
                    <input type="hidden" name="maxItem" value="10" id="search_param_maxItem">
                    <input type="hidden" name="sort" value="0" id="search_param_sort">
                    <input type="hidden" name="category" value="<?= $category ?>" id="search_param_category">
                    <div class="input-group input-group-sm">
                        <input class="form-control" type="text" name="quary" value="<?= $quary ?>" id="search_param_input" placeholder="Search..." maxlength="255" autocomplete="off">
                        <span class="input-group-btn">
                            <button id="search_button" class="btn btn-default" type="submit"><span class="glyphicon glyphicon-search"></span></button>
                        </span>
                    </div>
                </fieldset>
            </form>
        </div>
        <div id="search_option" class="col-xs-8">
            <div class="row">
                <span>
					<input id="search_option_category" class="btn-primary" data-toggle="modal" data-target="#popup" type="button" value="카테고리변경(<?= $category ?>)">
				</span>
                <span>
                    <p>정렬옵션</p>
                    <select id="search_option_sort">
                        <option value="new_date" <?php if($sort == "new_date")print "selected"; ?>>최신 등록순</option>
                        <option value="low_price"<?php if($sort == "low_price")print "selected"; ?>>낮은 가격순</option>
                        <option value="high_price"<?php if($sort == "high_price")print "selected"; ?>>높은 가격순</option>
                    </select>
                </span>
                <span>
                    <p>페이지 당 표시</p>
                    <select id="search_option_maxItem">
                        <option value="5" <?php if($maxItem == "5")print "selected"; ?>>5</option>
                        <option value="10"<?php if($maxItem == "10")print "selected"; ?>>10</option>
                        <option value="25"<?php if($maxItem == "25")print "selected"; ?>>25</option>
                    </select>
                </span>
            </div>
        </div>
    </div>
    <div id="popup" class="modal fade" role="dialog" >
        <div class="modal-dialog">

            <div class="modal-content">
                <div class="modal-header">
                    <button type="button" class="close" data-dismiss="modal">&times;</button>
                    <h4 class="modal-title">카테고리</h4>
                </div>
                <div class="modal-body" id="category_core">
                </div>
            </div>
        </div>
    </div>
    </div>
</header>
