// 固定路由
var main_route = '/jobs';

//查询，恢复页码到1，并提交表单
var search = function(){
	jqu.formItem('page','form_search').val(1);
	$('#form_search').get(0).submit();
};

//导航栏切换
$('.nav li:eq(0)').addClass("active");

//重置每页数量
$('#pagesize').change(function () {
	var pagesize = $(this).val();
	$("input[name='pagesize']").eq(0).val(pagesize);
});

//翻页栏切换
var changePage = function(page){
	//找到当前页
	var curpage = jqu.formInt('page','form_search');
	if(curpage==page){
		//如果将要跳转的页码和当前页码一致，就不需要处理了
		return;
	}
	
	//将表单中隐藏域的页码切换为page，并提交表单
	jqu.formItem('page','form_search').val(page);
	$('#form_search').get(0).submit();
};

//打开新增对话框
var presave = function(id, type){
	$('#modal1').modal('show');
	return false;
	var thisUrl = '/' + type + '/presave';
	jqu.loadJson(thisUrl,{id:id},function(result){
		
		// alert(jqu.obj2json(result));
		
		// 将获得的内容填写到修改表单中
		jqu.formLoad('form_am',result.record);
		//打开对话框
		$('#modal1').modal('show');
	});
};

//发起投递
var delivery = function(job_id){
	// 提示
	if(!confirm('将投递个人信息至企业，确实要投递个人信息吗？'))
		return;
	var thisUrl = main_route + '/delivery';
	//提交数据进行投递
	var jsonData = {"job_id": job_id};
	// $.post(thisUrl, jsonData, function (result) {
	// 	console.log(result);
	// });
	jqu.loadJson(thisUrl,jsonData,function(result){
		console.log(result);
		if(result.status === 200){
			alert(result.data);
			return;
		}
		if(result.status === 302){
			window.location.href = result.redirect_url;
			return;
		}
		//投递失败
		alert(result.msg);
	});
};

//收藏
var heart = function (job_id) {
	var thisUrl = main_route + '/heart';
	//提交数据进行收藏
	var jsonData = {"job_id": job_id};
	// $.post(thisUrl, jsonData, function (result) {
	// 	console.log(result);
	// });
	jqu.loadJson(thisUrl,jsonData,function(result){
		console.log(result);
		if(result.status === 200){
			alert(result.data);
			return;
		}
		//收藏失败
		alert(result.msg);
	});
};

var init = function(){
	//日期控件的初始化
	jqu.formItem('start_time','form_search').datetimepicker({
		format: 'yyyy-mm-dd',
		autoclose: 1,
		todayHighlight: 1,
		todayBtn: true,
		language: 'zh-CN',
		minView:2
	});
	
	jqu.formItem('end_time','form_search').datetimepicker({
		format: 'yyyy-mm-dd',
		autoclose: 1,
		todayHighlight: 1,
		todayBtn: true,
		language: 'zh-CN',
		minView:2
	});
	
	//根据上一次查询的日期端，设置到文本框中
	jqu.formItem('start_time','form_search').val(start_time);
	jqu.formItem('end_time','form_search').val(end_time);

	//新增/修改表单中的日期
	jqu.formItem('fdate','form_am').datetimepicker({
		format: 'yyyy-mm-dd',
		autoclose: 1,
		todayHighlight: 1,
		todayBtn: true,
		language: 'zh-CN',
		minView:2
	});
};

$(init);