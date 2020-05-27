// 固定路由
// var main_route = '/iuser';
var companyhr_route = '/companyhr';

// 重置个人中心链接
$('#main_href').attr('href', main_route + "/main");

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
var presave = function(_id){
	if (_id === 0){
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
	var thisUrl = null;
	var data = {};
	if(main_route == "/iuser"){
		thisUrl = main_route + '/work_experience_info';
		data = {
			"we_id": _id
		};
	}
	if(main_route == "/companyhr"){
		thisUrl = main_route + '/position_info';
		data = {
			"job_id": _id
		};
	}

	jqu.loadJson(thisUrl,data,function(result){
		
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
	for (var key in data){
		if (data[key] === ''){
			alert('请检查表单信息不为空');
			return;
		}
	}
	
	// 保存前的提示
	if(!confirm('确实要保存吗？'))
		return;

	var thisUrl = null;

	if(main_route == "/iuser"){
		thisUrl = main_route + '/work_experience_save';
	}
	if(main_route == "/companyhr") {
		thisUrl = main_route + '/position_info_save';
	}

	//提交数据进行保存
	jqu.loadJson(thisUrl,data,function(result){
		if(result.status === 500){
			alert(result.msg);
			return;
		}
		//保存成功，刷新页面
		// alert('保存成功');
		alert(result.data);
		$('#form_search').get(0).submit();
	});
	
};

// 删除用户经历或 公司职位
var remove = function(_id){
	if(!confirm('确实要删除该记录吗？'))
		return;

	var thisUrl = null;
	var data = {};
	if(main_route == "/iuser"){
		thisUrl = main_route + '/work_experience_remove';
		data = {
			"we_id": _id
		};
	}
	if(main_route == "/companyhr"){
		thisUrl = main_route + '/position_info_remove';
		data = {
			"job_id": _id
		};
	}

	jqu.loadJson(thisUrl, data,function(result){
		if(result.status === 500){
			alert(result.msg);
			return;
		}
		alert(result.data);
		// alert('删除成功');
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

// 接收简历
var receive = {
    leave_msg: function (dev_id) {
        $('#modal2').modal('show').on('shown.bs.modal', function (e) {
            // 关键代码，如没将modal设置为 block，则$modala_dialog.height() 为零
            $(this).css('display', 'block');
            var modalHeight=$(window).height() / 2 - $('#modal2 .modal-dialog').height() / 2;
            $(this).find('.modal-dialog').css({
                'margin-top': modalHeight
            });
            // 设置delivery_id
            $(this).find('input[name="delivery_id"]').val(dev_id);
            // 设置提交
            $(this).find('button[class="btn btn-primary"]').attr("onclick", "receive.receive_do()");
        });
    },
    receive_do: function () {
        var data = jqu.formData('form_am2');
        var thisUrl = companyhr_route + '/receive';

        // alert(jqu.obj2json(data));
        //提交数据进行接收留言
        jqu.loadJson(thisUrl,data,function(result){
            if(result.status === 500){
                alert(result.msg);
                return;
            }
            //保存成功，刷新页面
            // alert('保存成功');
            alert(result.data);
            $('#form_search').get(0).submit();
        });
    }
};

// 打回简历
var repulse = {
    leave_msg: function (dev_id) {
        $('#modal2').modal('show').on('shown.bs.modal', function (e) {
            // 关键代码，如没将modal设置为 block，则$modala_dialog.height() 为零
            $(this).css('display', 'block');
            var modalHeight=$(window).height() / 2 - $('#modal2 .modal-dialog').height() / 2;
            $(this).find('.modal-dialog').css({
                'margin-top': modalHeight
            });
            // 设置delivery_id
            $(this).find('input[name="delivery_id"]').val(dev_id);
            // 设置提交
            $(this).find('button[class="btn btn-primary"]').attr("onclick", "repulse.repulse_do()");
        });
    },
    repulse_do: function () {
        var data = jqu.formData('form_am2');
        var thisUrl = companyhr_route + '/repulse';

        // alert(jqu.obj2json(data));
        //提交数据进行接收留言
        jqu.loadJson(thisUrl,data,function(result){
            if(result.status === 500){
                alert(result.msg);
                return;
            }
            //保存成功，刷新页面
            // alert('保存成功');
            alert(result.data);
            $('#form_search').get(0).submit();
        });
    }
};