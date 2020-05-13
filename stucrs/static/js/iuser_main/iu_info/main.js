jQuery(document).ready(function($){
	//hide the subtle gradient layer (.cd-pricing-list > li::after) when pricing table has been scrolled to the end (mobile version only)
	checkScrolling($('.cd-pricing-body'));
	$(window).on('resize', function(){
		window.requestAnimationFrame(function(){checkScrolling($('.cd-pricing-body'))});
	});
	$('.cd-pricing-body').on('scroll', function(){ 
		var selected = $(this);
		window.requestAnimationFrame(function(){checkScrolling(selected)});
	});

	function checkScrolling(tables){
		tables.each(function(){
			var table= $(this),
				totalTableWidth = parseInt(table.children('.cd-pricing-features').width()),
		 		tableViewport = parseInt(table.width());
			if( table.scrollLeft() >= totalTableWidth - tableViewport -1 ) {
				table.parent('li').addClass('is-ended');
			} else {
				table.parent('li').removeClass('is-ended');
			}
		});
	}

	//重置简介信息
	function resetMonthly(){
		var real_name = $("[data-type='monthly'] span")[0];
		if (real_name.innerText === "None" || real_name.innerText === ""){
			real_name.innerHTML = "-";
			$("[data-type='yearly'] span input").val("");
		}
		$("[data-type='monthly'] li").each(function (i) {
			var li_val = $(this).context.innerText;
			if(li_val === "None" || li_val === ""){
				$(this).text("请修改信息");
				$("[data-type='yearly'] ul input").eq(i).val("");
			}
		})
	}
	resetMonthly();

	//switch from monthly to annual pricing tables
	bouncy_filter($('.cd-pricing-container'));

	function bouncy_filter(container) {
		container.each(function(){
			var pricing_table = $(this);
			var filter_list_container = pricing_table.children('.cd-pricing-list'),
				filter_radios = filter_list_container.find('input[type="radio"]'),
				pricing_table_wrapper = pricing_table.find('.cd-pricing-wrapper');

			//store pricing table items
			var table_elements = {};
			filter_radios.each(function(){
				var filter_type = $(this).val();
				table_elements[filter_type] = pricing_table_wrapper.find('li[data-type="'+filter_type+'"]');
			});

			//detect input change event
			filter_radios.on('change', function(event){
				event.preventDefault();
				//detect which radio input item was checked
				var selected_filter = $(event.target).val();

				//更新用户信息
				if( selected_filter === 'monthly' ) {
					var iu_inputs = $("[data-type='yearly'] ul input");
					var iu_param = {
						"user_name": iu_inputs.eq(0).val(),
						"phone": iu_inputs.eq(1).val(),
						"email": iu_inputs.eq(2).val(),
						"birthday": iu_inputs.eq(3).val(),
						"city": iu_inputs.eq(4).val(),
						"current_identity": iu_inputs.eq(5).val(),
						"industry": iu_inputs.eq(6).val(),
						"personal_experience": iu_inputs.eq(7).val(),
						"educational_experience": iu_inputs.eq(8).val()
					};
					var jsonKey = JSON.stringify(iu_param);
					console.log("执行更新请求", jsonKey);
					//创建异步对象
					var xhr = new XMLHttpRequest();
					//这种请求的类型及url
					//post请求一定要添加请求头才行，不然会报错
					xhr.open("post","/iuser/iu_update");
					xhr.setRequestHeader("Content-type","application/json");
					//发送请求
					xhr.send(jsonKey);
					xhr.onreadystatechange = function(){
						//这步为判断服务器是否正确响应
						if(xhr.readyState == 4 && xhr.status == 200){
							console.log(xhr.responseText);
							var data = xhr.responseText;   // 获取响应数据
							var json=JSON.parse(data);
							if (json.status === 200){
								// alert(json.data);
								console.log(json);
								window.location.href = json.redirect_url;
							}else {
								alert(json.msg);
							}
							return false;
						}
					};
				}

				//give higher z-index to the pricing table items selected by the radio input
				show_selected_items(table_elements[selected_filter]);

				//rotate each cd-pricing-wrapper 
				//at the end of the animation hide the not-selected pricing tables and rotate back the .cd-pricing-wrapper
				
				if( !Modernizr.cssanimations ) {
					hide_not_selected_items(table_elements, selected_filter);
					pricing_table_wrapper.removeClass('is-switched');
				} else {
					pricing_table_wrapper.addClass('is-switched').eq(0).one('webkitAnimationEnd oanimationend msAnimationEnd animationend', function() {		
						hide_not_selected_items(table_elements, selected_filter);
						pricing_table_wrapper.removeClass('is-switched');
						//change rotation direction if .cd-pricing-list has the .cd-bounce-invert class
						if(pricing_table.find('.cd-pricing-list').hasClass('cd-bounce-invert')) pricing_table_wrapper.toggleClass('reverse-animation');
					});
				}
			});
		});
	}
	function show_selected_items(selected_elements) {
		selected_elements.addClass('is-selected');
	}

	function hide_not_selected_items(table_containers, filter) {
		$.each(table_containers, function(key, value){
	  		if ( key != filter ) {	
				$(this).removeClass('is-visible is-selected').addClass('is-hidden');

			} else {
				$(this).addClass('is-visible').removeClass('is-hidden is-selected');
			}
		});
	}
});