"use strict";
var categoryLoaded = false;

function setHTTPGetParam(id){
	switch(id){
		case "search":
			$('#search_param_page').val(1);
			$('#search_param_maxItem').val($('#search_option_maxItem').val);
			$('#search_param_sort').val($('#search_option_sort').val);
			//document.getElementById('search_param_input').value = Base64.encode(document.getElementById('search_param_input').value);
			break;
	}
}



function categoryLoad(data,status){

	var category_core = $("#category_core");
	createCategoryItem(category_core,data,0);
}

function setCategory(name) {
    $('#search_param_category').val(name);
    $('#search_option_category').val("카테고리변경(" + name + ")");
    $("#popup").modal('hide');
}

function createCategoryItem(parent,item,level){
    var select = $("<a></a>").attr("href","javascript:setCategory(\""+ item.name + "\");").text(">".repeat(level) + item.name);
	var newTag = $("<div></div>").attr("value",item.name).append(select);

    parent.append(newTag);
    if(item.child.length>0) {
        var panel  = $("<div></div>");
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
    	$.get("/capstone/php/category.php",categoryLoad);
        categoryLoaded = true;
	}
}

function init(){
	alert("hello");
	$("#search_option_category").click(categoryShow);
}

$(document).ready(init);