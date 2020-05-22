// 登录页js
// $("button[type='submit']").click(function () {
$("button[id='main-login']").click(function () {
    var acc = $("#inputEmail3").val();
    var password = $("#inputPassword3").val();
    var u_type = $("input[name='check']:checked").val();
    if(u_type == null){
        alert("请勾选身份噢！");
        return false;
    }
    var jsonKey = JSON.stringify({"acc": acc, "password": password, "u_type": u_type});
    console.log("执行登录请求", u_type);
    //创建异步对象
    var xhr = new XMLHttpRequest();
    //这种请求的类型及url
    //post请求一定要添加请求头才行，不然会报错
    xhr.open("post",".");
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
});

$("button[id='main-register']").click(function () {
    var registerParam = {
        "u_type": $("input[name='check']:checked").val(),
        "register_param": {
            "phone": $("#inputPhone").val(),
            "email": $("#inputEmail3").val(),
            "password": $("#inputPassword3").val()
        }
    };
    var jsonKey = JSON.stringify(registerParam);
    console.log("执行注册请求", jsonKey);
    //创建异步对象
    var xhr = new XMLHttpRequest();
    //这种请求的类型及url
    //post请求一定要添加请求头才行，不然会报错
    xhr.open("post",".");
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
});