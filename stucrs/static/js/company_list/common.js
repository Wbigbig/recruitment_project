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

//提交，保存
var save = function(type){
	var data = jqu.formData('form_am');
	alert(jqu.obj2json(data));
	switch (type) {
		case 'news':
			// 进行必填项的判断
			if(data.fclass==''){
				alert('栏目 必须填写');
				return;
			}
			if(data.title==''){
				alert('标题 必须填写');
				return;
			}
			if(data.fdate==''){
				alert('日期 必须填写');
				return;
			}
			if(data.content==''){
				alert('内容 必须填写');
				return;
			} break;
		case 'stu':
			// 进行必填项的判断
			if(data.code==''){
				alert('学号 必须填写');
				return;
			}
			if(data.name==''){
				alert('姓名 必须填写');
				return;
			}
			if(data.birthday==''){
				alert('生日 必须填写');
				return;
			}
			if(data.age==''){
				alert('年龄 必须填写');
				return;
			}
			if(data.institute==''){
				alert('学院 必须填写');
				return;
			}
			if(data.fclass==''){
				alert('班级 必须填写');
				return;
			}break;
		case 'course':
			// 进行必填项的判断
			if(data.code==''){
				alert('课程编号 必须填写');
				return;
			}
			if(data.name==''){
				alert('课程名称 必须填写');
				return;
			}
			if(data.score==''){
				alert('课程学分 必须填写');
				return;
			}
			if(data.institute==''){
				alert('开课学院 必须填写');
				return;
			}break;
		default:
			alert('')
	}
	
	// 保存前的提示
	if(!confirm('确实要保存吗？'))
		return;
	var thisUrl = '/' + type + '/save';
	//提交数据进行保存
	jqu.loadJson(thisUrl,data,function(result){
		if(!result.succ){
			alert(result.stmt);
			return;
		}
		
		//保存成功，刷新页面
		alert('保存成功');
		$('#form_search').get(0).submit();
	});
	
};

// 删除
var remove = function(id, type){
	if(!confirm('确实要删除该记录吗？'))
		return;
	thisUrl = '/' + type + '/remove';
	jqu.loadJson(thisUrl,{id:id},function(result){
		if(!result.succ){
			alert(result.stmt);
			return;
		}
		
		alert('删除成功');
		$('#form_search').get(0).submit();
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
	jqu.formItem('company_name','form_search').val(company_name);
	jqu.formItem('company_industry','form_search').val(company_industry);
	jqu.formItem('address','form_search').val(address);
	
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