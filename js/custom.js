"use strict";
var categoryLoaded = false;
var category_list = [];

function setHTTPGetParam(){
    $('#search_param_page').val(1);
    $('#search_param_maxItem').val($('#search_option_maxItem').attr("value"));
    $('#search_param_sort').val($('#search_option_sort').attr("value"));
}

function addAdvancedCategoryLabel(category,id){
    if(category_list.length < 6 && category_list.indexOf(category) === -1){
        category_list.push(category);
        var category_label = $("<span></span>");
        category_label.addClass("label label-primary");
        category_label.addClass("category_label_" + id);
        category_label.append(category + " ");
        var close_button = $("<a></a>");
        close_button.attr("href","javascript:removeAdvancedCategoryLabel('" + category + "'," + id + ")");
        close_button.append("&times;");
        category_label.append(close_button);
        var input_form = $("<input></input>");
        input_form.attr("type","hidden");
        input_form.attr("name","category[]");
        input_form.attr("value",category);
        input_form.addClass("category_label_" + id);
        $("#advanced_option_form").append(input_form);
        $("#option_selector_category_labels").append(category_label);
    }
}

function removeAdvancedCategoryLabel(category,id) {
    var index = category_list.indexOf(category);
    if(index >= 0){
        category_list.splice(index,1);
        $(".category_label_" + id).remove();
    }
}

function dropdownSelection(id,value,title) {
    var caret = $("<span></span>").addClass("caret");
    $(id).val(value).text(title + " ").append(caret);
}

function categoryLoad(data,status){
	var category_core = $("#category_core");
	createCategoryItem(category_core,data,0);
}

function setCategory(name) {
    $('#search_param_category').val(name);
    $("#category_label").text("카테고리 : " + name);
    $("#popup_category").modal('hide');
}

function createCategoryItem(parent,item,level){
    var select = $("<a></a>").attr("href","javascript:setCategory(\""+ item.name + "\");").text(">".repeat(level) + item.name);
	var newTag = $("<li></li>").attr("value",item.name).append(select);
    newTag.addClass("list-group-item");

    parent.append(newTag);
    if(item.child.length>0) {
        var panel  = $("<ul></ul>");
        panel.addClass("list-group");
        parent.append(panel);
        newTag.addClass("tagged");
        newTag.click(function () {
            panel.slideToggle("slow");
        });
        for (var i = 0; i < item.child.length; i++) {
            createCategoryItem(panel, item.child[i],level+1);
        }
    }
}

function validationNumber(e){
    if ($.inArray(e.keyCode, [46, 8, 9, 27, 13, 110, 190]) !== -1 ||
        (e.keyCode == 65 && (e.ctrlKey === true || e.metaKey === true)) ||
        (e.keyCode == 67 && (e.ctrlKey === true || e.metaKey === true)) ||
        (e.keyCode == 88 && (e.ctrlKey === true || e.metaKey === true)) ||
        (e.keyCode >= 35 && e.keyCode <= 39)){
        return;
    }
    if ((e.shiftKey || (e.keyCode < 48 || e.keyCode > 57)) && (e.keyCode < 96 || e.keyCode > 105)) {
        e.preventDefault();
    }
}

function categoryShow() {
	if(categoryLoaded === false){
    	$.get("category.php",categoryLoad);
        categoryLoaded = true;
	}
}

function advanced_search(price_low, price_high, keyword, category_list, sort, maxpage){
    var to_json;
    to_json.price_low = price_low;
    to_json.price_high = price_high;
    to_json.keyword = keyword;
    to_json.category_list = category_list;
    to_json.category_list = sort;
    to_json.category_list = maxpage;
    $.get("adv_search.php",JSON.stringify(to_json),refresh_field);

}

function init(){
    $("#setting_ok").click(setHTTPGetParam);
    $("#search_form").submit(setHTTPGetParam);
    $("#advanced_option_form").submit(function(event){
        setHTTPGetParam();
        if(category_list.length == 0){
            $("#option_selector_error").text("#에러 : 카테고리 미 선택.");
            event.preventDefault();
        } else if($("#price_input_min").val() == ""){
            $("#option_selector_error").text("#에러 : 최소 가격 미 지정.");
            event.preventDefault();
        }else if($("#price_input_max").val() == ""){
            $("#option_selector_error").text("#에러 : 최대 가격 미 지정.");
            event.preventDefault();
        }else if($("#adv_search_param_input").val() == ""){
            $("#option_selector_error").text("#에러 : 제품명 미 지정.");
            event.preventDefault();
        }else{
            return;
        }
    });
	$("#search_option_category").click(categoryShow);
	$(".number_only").keydown(validationNumber);
    $(".search_option_sort_item").click(function () {dropdownSelection("#search_option_sort",$(this).attr("title"),$(this).text());});
    $(".search_option_maxItem_item").click(function () {dropdownSelection("#search_option_maxItem",$(this).attr("title"),$(this).text());});
}

$(document).ready(init);