/* http GET�޼ҵ� �Ķ���� ���� */
function setHTTPGetParam(id){
	switch(id){
		case "search":
			document.getElementById('search_param_page').value = 1;
			document.getElementById('search_param_maxItem').value = document.getElementById('search_option_maxItem').value;
			document.getElementById('search_param_sort').value = document.getElementById('search_option_sort').value;
			//document.getElementById('search_param_input').value = Base64.encode(document.getElementById('search_param_input').value);
			break;
	}
}
