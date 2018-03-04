"use strict";
var categoryLoaded = false;

function setHTTPGetParam(){
    $('#search_param_page').val(1);
    $('#search_param_maxItem').val($('#search_option_maxItem').attr("value"));
    $('#search_param_sort').val($('#search_option_sort').attr("value"));
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
    $("#category_label").text("카테고리 : " + name)
    $("#popup_category").modal('hide');
}

function createCategoryItem(parent,item,level){
    var select = $("<a></a>").attr("href","javascript:setCategory(\""+ item.name + "\");").text(">".repeat(level) + item.name);
	var newTag = $("<li></li>").attr("value",item.name).append(select);
    newTag.addClass("list-group-item")

    parent.append(newTag);
    if(item.child.length>0) {
        var panel  = $("<ul></ul>");
        panel.addClass("list-group")
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

function categoryShow() {
	if(categoryLoaded === false){
    	$.get("category.php",categoryLoad);
        categoryLoaded = true;
	}
}

function init(){
    $("#setting_ok").click(setHTTPGetParam)
    $("#search_form").submit(setHTTPGetParam)
	$("#search_option_category").click(categoryShow);

    $(".search_option_sort_item").click(function () {dropdownSelection("#search_option_sort",$(this).attr("title"),$(this).text());})
    $(".search_option_maxItem_item").click(function () {dropdownSelection("#search_option_maxItem",$(this).attr("title"),$(this).text());})
}

$(document).ready(init);