//查询，恢复页码到1，并提交表单
var search = function(){
	jqu.formItem('page','form_search').val(1);
	$('#form_search').get(0).submit();
};

//导航栏切换
$('.nav li:eq(1)').addClass("active");

//重置每页数量
$('#pagesize').change(function () {
	var pagesize = $(this).val();
	$("input[name='pagesize']").eq(0).val(pagesize);
});

//翻页栏切换
var changePage = function(page){
	//找到当前页
	var curpage = jqu.formInt('page','form_search');
	if(curpage===page){
		//如果将要跳转的页码和当前页码一致，就不需要处理了
		return;
	}
	
	//将表单中隐藏域的页码切换为page，并提交表单
	jqu.formItem('page','form_search').val(page);
	$('#form_search').get(0).submit();
};

var init = function(){
	//根据上一次查询的参数，设置到文本框中
};

$(init);