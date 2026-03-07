document.addEventListener("DOMContentLoaded", function(){

let inputs = document.querySelectorAll(".pin")
let statusBox = document.getElementById("status")

/* PIN INPUT BEHAVIOUR */

inputs.forEach((input,index)=>{

input.addEventListener("input", function(){

this.value = this.value.replace(/[^0-9]/g,'')

if(this.value !== "" && index < inputs.length-1){
inputs[index+1].focus()
}

checkPincode()

})

input.addEventListener("keydown", function(e){

if(e.key === "Backspace" && this.value === "" && index > 0){
inputs[index-1].focus()
}

})

})


/* GET PINCODE */

function getPincode(){

let pin=""

inputs.forEach(input=>{
pin += input.value
})

return pin

}


/* MANUAL PINCODE CHECK */

function checkPincode(){

let pincode = getPincode()

if(pincode.length !== 6){
return
}

statusBox.innerHTML =
'<span class="loader"></span> Checking delivery...'

fetch("/check-pincode",{
method:"POST",
headers:{
"Content-Type":"application/json"
},
body: JSON.stringify({pincode:pincode})
})
.then(res=>res.json())
.then(data=>{

let infoLine = `<div class="location-line">${data.city}, ${data.state}</div>`

/* AVAILABLE */

if(data.status==="available"){

statusBox.className="success show"

statusBox.innerHTML =
`${infoLine}<br>
<span class="delivery-msg"></span>`

typeWriter(
"Congrats! You're eligible for 3hrs Xpress Delivery",
document.querySelector(".delivery-msg")
)

/* confetti */

const duration = 3 * 1000;
const end = Date.now() + duration;

(function frame(){

confetti({
particleCount:6,
angle:90,
spread:120,
startVelocity:45,
origin:{x:0.5,y:0.65}
});

if(Date.now() < end){
requestAnimationFrame(frame);
}

})();

/* NOT AVAILABLE */

}else{

statusBox.className="error show"

statusBox.innerHTML =
`${infoLine}<br>
Standard Delivery (6-7 days)`

inputs.forEach(input=>{
input.classList.add("shake")
})

setTimeout(()=>{
inputs.forEach(input=>{
input.classList.remove("shake")
})
},400)

}

})

}


/* TYPEWRITER */

function typeWriter(text, element, speed=35){

let i = 0
element.innerHTML = ""

function typing(){

if(i < text.length){

element.innerHTML =
text.substring(0,i+1) + '<span class="cursor"></span>'

i++

setTimeout(typing,speed)

}else{

element.innerHTML = text

}

}

typing()

}


/* AUTO DETECT LOCATION */

function detectLocation(){

if(navigator.geolocation){

navigator.geolocation.getCurrentPosition(function(position){

fetch("/auto-check",{
method:"POST",
headers:{
"Content-Type":"application/json"
},
body:JSON.stringify({
lat:position.coords.latitude,
lon:position.coords.longitude
})
})
.then(res=>res.json())
.then(data=>{
console.log(data)
})

})

}

}

detectLocation()

})