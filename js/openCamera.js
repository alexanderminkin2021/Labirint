import DeviceDetector from "https://cdn.skypack.dev/device-detector-js@2.2.10";
//const videoElement = document.getElementsByClassName('input_video')[0];
const canvasElement = document.getElementsByClassName('output_canvas')[0];
const canvasCtx = canvasElement.getContext('2d');
//const cursor = document.querySelector(".cursor");

const video = document.getElementById('vid');
const button = document.getElementById('button');
const buttonStop = document.getElementById('buttonStop');
const select = document.getElementById('select');
let choose;
let currentStream;

const handParts = {
  wrist: 0,
  thumb: { base: 1, middle: 2, topKnuckle: 3, tip: 4 },
  indexFinger: { base: 5, middle: 6, topKnuckle: 7, tip: 8 },
  middleFinger: { base: 9, middle: 10, topKnuckle: 11, tip: 12 },
  ringFinger: { base: 13, middle: 14, topKnuckle: 15, tip: 16 },
  pinky: { base: 17, middle: 18, topKnuckle: 19, tip: 20 },
};
//-------------------------------------

let idleUp=document.getElementById("capguyIdleUp");
let idleDown=document.getElementById("capguyIdleDown");
let idleLeft=document.getElementById("capguyIdleLeft");
let idleRight=document.getElementById("capguyIdleRight");

let right=document.getElementById("capguyRight");
let left=document.getElementById("capguyLeft");
let back=document.getElementById("capguyFront");
let front=document.getElementById("capguyBack");

//paths
var direction = "DOWN";
var prevX = 0;
var prevY = 0;

function petCursor_getDirection(numX, numY){
	//
	//set diagonals first (based on previous direction)
    console.log("pet_anim2");
	if(numX > prevX && str_petCursor_direction == "UP"){
		//UP DIAGONAL RIGHT
		arr_petCursorCurrentState = arr_petCursor_up_right;
	}else if(numX < prevX && str_petCursor_direction == "UP"){
		//UP DIAGONAL LEFT
		arr_petCursorCurrentState = arr_petCursor_up_left;
	}else if(numX > prevX && str_petCursor_direction == "DOWN"){
		//DOWN DIAGONAL RIGHT
		arr_petCursorCurrentState = arr_petCursor_down_right;
	}else if(numX < prevX && str_petCursor_direction == "DOWN"){
		//DOWN DIAGONAL LEFT
		arr_petCursorCurrentState = arr_petCursor_down_left;
	}
	//set movement values
	if(numX > prevX && numY == prevY){
		str_petCursor_direction = "RIGHT";
		arr_petCursorCurrentState = arr_petCursor_right;
		arr_petCursorInteract = arr_petCursor_scratch_right;
	}else if(numX < prevX && numY == prevY){
		str_petCursor_direction = "LEFT";
		arr_petCursorCurrentState = arr_petCursor_left;
		arr_petCursorInteract = arr_petCursor_scratch_left;
	}else if(numY > prevY && numX == prevX){
		str_petCursor_direction = "DOWN";
		arr_petCursorCurrentState = arr_petCursor_down;
		arr_petCursorInteract = arr_petCursor_scratch_down;
	}else if(numY < prevY && numX == prevX){
		str_petCursor_direction = "UP";
		arr_petCursorCurrentState = arr_petCursor_up;
		arr_petCursorInteract = arr_petCursor_scratch_up;
	}
	// calculate distance moved
	var dx = numX - prevX;
	var dy = numY - prevY;
	num_petCursor_distance = Math.sqrt(dx * dx + dy * dy);
	//set previous values
	prevX = numX;
	prevY = numY;
}

//special element (a, button, input...)
function petCursor_setForElement(str_tagName, arr){
	var _element = document.getElementsByTagName(str_tagName);
	for (var i=0; i<_element.length; ++i){
		_element[i].style.cursor = 'url(' + str_petCursor_directory + arr[num_petCursor_currFrame] + '), auto';
	}
}

//called with an interval
function petCursor_animateCursor(x,y){
console.log("pet_anim");
	//set and countdown animation states
	//if idle, play idle animation & fall asleep
	//if scratching
	//if running
	//when changing a state, reset num_petCursor_currFrame
	//...

	//special animation states that happen when over certain elements
	//see https://www.w3schools.com/tags/ for more tags
	/*petCursor_setForElement('a', arr_petCursorInteract);
	petCursor_setForElement('button', arr_petCursorInteract);
	petCursor_setForElement('input', arr_petCursorInteract);
	petCursor_setForElement('h1', arr_petCursorInteract);
	petCursor_setForElement('h2', arr_petCursorInteract);
	petCursor_setForElement('h3', arr_petCursorInteract);
	petCursor_setForElement('h4', arr_petCursorInteract);
	petCursor_setForElement('h5', arr_petCursorInteract);
	petCursor_setForElement('h6', arr_petCursorInteract);
*/
	//clicked (surprise animation)
	if(num_petCursor_stateCnt == -5){
		//suprised (mouse has been clicked!)
		arr_petCursorCurrentState = arr_petCursor_surprised;
	}

	//when mouse moves this is set to 0
	//when suprise (click) set to -5
	//increments when not moving, above a certain point indicates a state (sleeping, idle, shocked...)
	num_petCursor_stateCnt += 1;

	//set cursor for main body
	if(num_petCursor_stateCnt == 5){
		//idle (start)
		arr_petCursorCurrentState = arr_petCursor_idle;
		//
	}else if(num_petCursor_stateCnt == 30){
		//started grooming
		arr_petCursorCurrentState = arr_petCursor_idling;
	}else if(num_petCursor_stateCnt == 70){
		//falling asleep
		arr_petCursorCurrentState = arr_petCursor_sleep_start;
	}else if(num_petCursor_stateCnt == 90){
		//sleeping
		arr_petCursorCurrentState = arr_petCursor_sleeping;
	}

	//set to current animation for overall document...
	cursor["background-image"]='url('+str_petCursor_directory + arr_petCursorCurrentState[num_petCursor_currFrame]+')' ;
    cursor["transform"]='translate('+`${x}`+','+ `${y}`+')';
	//control "playhead", step through current array
	// default to one frame per loop
	var inc = 1;

	// when moving, base animation speed on mouse speed instead
	num_petCursor_frameAcc += num_petCursor_distance;
	if (num_petCursor_stateCnt >= 0 && num_petCursor_stateCnt < 5) {
		if (num_petCursor_frameAcc > num_petCursor_frameDivisor) {
			num_petCursor_frameAcc = 0;
		} else {
			inc = 0;
		}
	}
	//increment
	num_petCursor_currFrame += inc;
	//reached end of movement array, loop
	if(num_petCursor_currFrame > arr_petCursorCurrentState.length-1){
		num_petCursor_currFrame = 0;
	}
}

//gets the direction, and manages state
function petCursor_mouseMove(event){
	num_petCursor_stateCnt = 0; //reset state (cursor is moving - send to shocked and then move)
	petCursor_getDirection(event.translate.x, event.translate.y);
}

//clicked -- when cursor is still and you click, pet gets surpised
function petCursor_mouseDown(event){
	num_petCursor_stateCnt = -5; //set to negative value to count up then reset...
}

function startPetCursor(x,y){
	//console.log("starting cursor...");
	//control movement and clicks
	//cursor.addEventListener('transform', petCursor_mouseMove);
	//num_petCursor_stateCnt = 0; //reset state (cursor is moving - send to shocked and then move)
	//petCursor_getDirection(parseInt(x), parseInt(y));
     console.log(x,y);
	//document.addEventListener('mousedown', petCursor_mouseDown);
	//interval controlling the "playhead"
	//int_petCursorAnimation =petCursor_animateCursor(x,y)// setInterval(petCursor_animateCursor, 200);
	//change milliseconds to control animation speed (lower = faster, higher = slower)
	//

    //cursor["transform"]='translate('+parseInt(x)+'px,'+ parseInt(y)+'px)';
}

//---------------------------------------

function stopMediaTracks(stream) {
 console.log("stop");
   stream=video.srcObject;
    var tracks=stream.getTracks();
    for(var i=0;i<tracks.length;i++) {
    var track=tracks[i];
    track.stop();
  }
  hideMen();

            idleUp.style.display = 'block';
       try { var position = idleUp.getBoundingClientRect();
            var x = position.left;
            var y = position.top; }
        catch(e)
        {}
    console.log("new");

  // video.srcObject =null;
}

function gotDevices(mediaDevices) {
  select.innerHTML = '';
  select.appendChild(document.createElement('option'));
  let count = 1;
  mediaDevices.forEach(mediaDevice => {
    if (mediaDevice.kind === 'videoinput') {
      const option = document.createElement('option');
      option.value = mediaDevice.deviceId;
      const label = mediaDevice.label || `Camera ${count++}`;
      const textNode = document.createTextNode(label);
      option.appendChild(textNode);
      select.appendChild(option);
    }
  });
}

buttonStop.addEventListener('click',stopMediaTracks);

button.addEventListener('click', event => {

    console.log(choose);
    if (typeof currentStream !== 'undefined') {
        stopMediaTracks(currentStream);
        console.log("new camera")
    }

     const videoConstraints = {};
      if (select.value === '') {
        //videoConstraints.facingMode = 'environment';
        stopMediaTracks(currentStream);
      } else {
        videoConstraints.deviceId = { exact: select.value };
        console.log(videoConstraints.deviceId);
      }
      const constraints = {
        video: videoConstraints,
        audio: false
      };
      navigator.mediaDevices
        .getUserMedia(constraints)
        .then(stream => {
          currentStream = stream;
          video.srcObject = stream;
          return navigator.mediaDevices.enumerateDevices();
        })
        .then(gotDevices)
        .catch(error => {
          console.error(error);
        });
});

navigator.mediaDevices.enumerateDevices().then(gotDevices);

/*function onResults(handData) {
  drawHandPositions(canvasElement, canvasCtx, handData);

 }

function drawHandPositions(canvasElement, canvasCtx, handData) {
  canvasCtx.save();
  canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);
  canvasCtx.drawImage(
      handData.image, 0, 0, canvasElement.width, canvasElement.height);
  if (handData.multiHandLandmarks) {
    for (const landmarks of handData.multiHandLandmarks) {
      drawConnectors(canvasCtx, landmarks, HAND_CONNECTIONS,
                     {color: '#00FF00', lineWidth: 5});
      drawLandmarks(canvasCtx, landmarks, {color: '#FF0000', lineWidth: 2});
      console.log(handData.multiHandLandmarks[0][8])
    }
  }
  canvasCtx.restore();
}
*/



const hands = new Hands({locateFile: (file) => {
  return `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}`;
}});
hands.setOptions({
  maxNumHands:2,
  modelComplexity: 0,
  minDetectionConfidence: 0.5,
  minTrackingConfidence: 0.5
});


 hands.onResults(onResults);
    const camera = new Camera(video, {
      onFrame: async () => {
        await hands.send({image: video});
      },
      width: 640,
      height: 480
    });

camera.start();


function getCursorCords(handData) {
  if(handData.multiHandLandmarks){
      for (const landmarks of handData.multiHandLandmarks) {
      //console.log(landmarks);
    }

  const { x, y, z } = handData.multiHandLandmarks[0][handParts.indexFinger.tip];
  const mirroredXCoord = -x + 1; /* due to camera mirroring */
  const mirroredYCoord = -y + 1; /* due to camera mirroring */

  return { x: mirroredXCoord, y:mirroredYCoord, z };
  }
  else{
  return;}
}

function convertCordsToDomPosition({ x, y }) {
  return {
    x: `${x * 1000}px`,
    y: `${y * 600}px`
  };
}

let sled=false;
let prevX2=40;
let prevY2=40;
function updateCursor(handData) {
  if(handData.multiHandLandmarks){
        const cursorCords = getCursorCords(handData);
  if (!cursorCords) { return; }
  else{
      let { x, y } = convertCordsToDomPosition(cursorCords);
      //idle.style.transform = `translate(${x}, ${y})`;

      let numX=parseInt(x);
      let numY=parseInt(y);
     var dx2 = numX-prevX2;
	 var dy2 = numY-prevY2;
	 let distance2 = Math.sqrt(dx2 * dx2 + dy2 * dy2);
	 if (distance2>30)
      {
        sled=true;
        prevY2=numY;
        prevX2=numX;
      }
      else{
        sled=false;
      }
      var dx = numX - prevX;
	  var dy = numY - prevY;
	 let distance = Math.sqrt(dx * dx + dy * dy);
    //console.log(distance);
    let err=2;
     if (distance>1.5*err){

        hideMen();
	  //set movement values
	  if(numX > prevX && Math.abs(numY - prevY)<err){// && Math.abs(numX - prevX)>2 ){

           //right.style.display = 'block';
          // right.style.transform = `translate(${x}, ${y})`;
           direction="RIGHT";
	}else if(numX < prevX && Math.abs(numY - prevY)<err){// && Math.abs(numX - prevX)>2 ){
		 //hideMen();

        // left.style.display = 'block';
         //left.style.transform = `translate(${x}, ${y})`;
         direction="LEFT";
	}else if(numY > prevY && Math.abs(numX - prevX)<err){//  && Math.abs(numY - prevY)>2){
		// hideMen();

        //  back.style.display = 'block';
         // back.style.transform = `translate(${x}, ${y})`;
          direction="DOWN";
	}else if(numY < prevY && Math.abs(numX - prevX)<err){ //  && Math.abs(numY - prevY)>2){
		// hideMen();

         //  front.style.display = 'block';
        //   front.style.transform = `translate(${x}, ${y})`;
           direction="UP";
	}
	else {
	   //hideMen();

         // idleUp.style.display = 'block';
         //idleUp.style.transform = `translate(${x}, ${y})`;

	}

	if (direction==="UP"){
	    front.style.display = 'block';
        front.style.transform = `translate(${x}, ${y})`;
	}
	else if (direction==="DOWN"){
	     back.style.display = 'block';
         back.style.transform = `translate(${x}, ${y})`;
	}else if (direction==="RIGHT"){
	     right.style.display = 'block';
         right.style.transform = `translate(${x}, ${y})`;
	}else if (direction==="LEFT"){
	     left.style.display = 'block';
         left.style.transform = `translate(${x}, ${y})`;
	}

	// calculate distance moved

	//set previous values

        prevX = numX;
        prevY = numY;
	}
	else {
	    hideMen();
	    if (direction==="UP"){
	        idleUp.style.display = 'block';
            idleUp.style.transform = `translate(${prevX}px, ${prevY}px)`;
        }
        else if (direction==="DOWN"){
             idleDown.style.display = 'block';
             idleDown.style.transform = `translate(${prevX}px, ${prevY}px)`;
        }else if (direction==="RIGHT"){
             idleRight.style.display = 'block';
             idleRight.style.transform = `translate(${prevX}px, ${prevY}px)`;
        }else if (direction==="LEFT"){
             idleLeft.style.display = 'block';
             idleLeft.style.transform = `translate(${prevX}px, ${prevY}px)`;
        }
	}


/*
  canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);
  canvasCtx.drawImage(idle, 100, 100,75,75);
*/

        canvasCtx.beginPath();
        canvasCtx.fillStyle = "rgba(0,0,0,.5)";
        console.log(numX,numY);
        if (sled===true){
        if (direction==="UP")
        {
             canvasCtx.ellipse(numX+60, numY+100, 4, 6, 0, 0, 2 * Math.PI);
             canvasCtx.ellipse(numX+74, numY+85, 4, 6, 0, 0, 2 * Math.PI);
          }
        else if (direction==="DOWN"){
             canvasCtx.ellipse(numX+60, numY+100, 4, 6, 0, 0, 2 * Math.PI);
             canvasCtx.ellipse(numX+74, numY+85, 4, 6, 0, 0, 2 * Math.PI);

        }else if((direction==="RIGHT" || direction==="LEFT")){
             canvasCtx.ellipse(numX+60, numY+100, 4, 6, Math.PI/2, 0, 2 * Math.PI);

        }
        canvasCtx.fill();
        sled=false;
        }


      }
  }else{return;}
}

function onResults(handData) {
   if (handData.multiHandLandmarks.length!=0) {
   // console.log(handData.multiHandLandmarks);
    updateCursor(handData); }
    else{
    if(choose){
          let stream;
          stopMediaTracks(stream);
         choose=false;
    }

    return;
    }

}

function hideMen(){
right.style.display = 'none';
left.style.display = 'none';
front.style.display = 'none';
back.style.display = 'none';
idleUp.style.display = 'none';
idleDown.style.display = 'none';
idleRight.style.display = 'none';
idleLeft.style.display = 'none';

console.log("hide");
}


 document.addEventListener("DOMContentLoaded", () => {
   console.log("all");
   var delayInMilliseconds = 10; //1 second
    setTimeout(function() {
      //your code to be executed after 1 second
    }, delayInMilliseconds);
   let stream;
   choose=true;
   stopMediaTracks(stream);

  });
