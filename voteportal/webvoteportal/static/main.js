navibtn = document.getElementById("navibtn");
navi = document.getElementById("navi");
thebody = document.getElementById("body");
loader = document.getElementById("loadercont");



navibtn.addEventListener('click' , function(){
 console.log("Clicked");
 if(navi.style.display === "none"){
    navi.style.display = "block";
 }
 else{
    navi.style.display = "none";
 }

});
window.addEventListener("load", function(){
loader.style.display = "block";
loader.style.display = "none";
});