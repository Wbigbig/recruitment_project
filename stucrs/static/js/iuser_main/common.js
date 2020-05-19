// 固定路由
var main_route = '/iuser';

//查询，恢复页码到1，并提交表单
var search = function(){
	jqu.formItem('page','form_search').val(1);
	$('#form_search').get(0).submit();
};

//导航栏切换
$('.nav li:eq(2)').addClass("active");

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
var presave = function(we_id){
	if (we_id === 0){
		$('#modal1').modal('show').on('shown.bs.modal', function (e) {
            // 关键代码，如没将modal设置为 block，则$modala_dialog.height() 为零
            $(this).css('display', 'block');
            var modalHeight=$(window).height() / 2 - $('#modal1 .modal-dialog').height() / 2;
            $(this).find('.modal-dialog').css({
                'margin-top': modalHeight
            });
        });
		return false;
	}

	var thisUrl = main_route + '/work_experience_info';
	jqu.loadJson(thisUrl,{we_id:we_id},function(result){
		
		// alert(jqu.obj2json(result));
		
		// 将获得的内容填写到修改表单中
		jqu.formLoad('form_am',result.data);
		//打开对话框
		$('#modal1').modal('show').on('shown.bs.modal', function (e) {
            // 关键代码，如没将modal设置为 block，则$modala_dialog.height() 为零
            $(this).css('display', 'block');
            var modalHeight=$(window).height() / 2 - $('#modal1 .modal-dialog').height() / 2;
            $(this).find('.modal-dialog').css({
                'margin-top': modalHeight
            });
        });
	});
};

//提交，保存
var save = function(){
	var data = jqu.formData('form_am');
	// alert(jqu.obj2json(data));
	// 进行必填项的判断
	if(data.company_name===''){
		alert('公司 必须填写');
		return;
	}
	if(data.company_industry===''){
		alert('行业 必须填写');
		return;
	}
	if(data.entry_time===''){
		alert('入职时间 必须填写');
		return;
	}
	if(data.departure_time===''){
		alert('离职时间 必须填写');
		return;
	}
	if(data.job_title===''){
		alert('职位名称 必须填写');
		return;
	}
	if(data.department===''){
		alert('所属部门 必须填写');
		return;
	}
	if(data.job_content===''){
		alert('工作内容 必须填写');
		return;
	}

	
	// 保存前的提示
	if(!confirm('确实要保存吗？'))
		return;
	var thisUrl = main_route + '/work_experience_save';
	//提交数据进行保存
	jqu.loadJson(thisUrl,data,function(result){
		if(result.status === 500){
			alert(result.msg);
			return;
		}
		//保存成功，刷新页面
		alert('保存成功');
		$('#form_search').get(0).submit();
	});
	
};

// 删除
var remove = function(we_id){
	if(!confirm('确实要删除该记录吗？'))
		return;
	thisUrl = main_route + '/work_experience_remove';
	jqu.loadJson(thisUrl,{we_id:we_id},function(result){
		if(result.status === 500){
			alert(result.msg);
			return;
		}
		
		alert('删除成功');
		$('#form_search').get(0).submit();
	});
};

// 删除收藏
var heart_remove = function(job_id){
	thisUrl = main_route + '/position_heart_remove';
	jqu.loadJson(thisUrl,{job_id:job_id},function(result){
		if(result.status === 500){
			alert(result.msg);
			return;
		}

		alert('删除成功');
		$('#form_search').get(0).submit();
	});
};