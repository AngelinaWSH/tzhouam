function f() {
    var a=document.getElementById("aaa");
    var val=document.getElementById("ss").value;

    a.innerHTML+="<option value='"+val+"'>"+val+"</option>";
}
function g(){
    alert(document.getElementById("aaa").value)
}