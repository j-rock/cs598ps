/**
 * pad - pad a floating point input to be the same length of characters
 *       given a number > -9999 & number < 9999.
 *
 **/
function pad(val) {
  if(val) {
    var leftLimit = 4;
    var rightLimit = 5;
    var prefix = "+";
    if(val < 0) {
        prefix = "-";
    }
    var regex = /([0-9]+)[.]([0-9]+)/g;
    var matches = regex.exec(val);
    var left = (matches[1]+"");
    if(left.length > leftLimit) {
      console.warn("main.pad: invalid value found - greater than 9999");
      left="OVER";
    }else if(left.length < leftLimit) {
      // pad left side to be the same size each time
      while(left.length < leftLimit) left = "0"+left;
    }
    var right = (matches[2]+"").substring(0,rightLimit);

    return prefix+left+"."+right;
  }
  return val;
}
var recordingStatus = false;

function toggleRecording(val) {
  var status = "paused";
  if(val) status = "recording";
  recordingStatus = val;
  document.getElementById("recordingStatus").innerHTML = status;
}

var data={x:[],y:[],z:[]};

/**
 * uploadData - upload the data to the server
 **/
function uploadData(data,id) {
  if(typeof id !== "string") {
    id = new Date().getTime()+"";
  }

  // convert x,y,z array values to matlab compatible arrays for easy plotting
  var matlab = {x:"x=[",y:"y=[",z:"z=["};
  data.x.forEach(function(val,i,arr){
    if(i<(arr.length-1))
      matlab.x+=val+", ";
    else
      matlab.x+=val+"]";
    });
  data.y.forEach(function(val,i,arr){
    if(i<(arr.length-1))
      matlab.y+=val+", ";
    else
      matlab.y+=val+"]";
    });
  data.z.forEach(function(val,i,arr){
    if(i<(arr.length-1))
      matlab.z+=val+", ";
    else
      matlab.z+=val+"]";
    });

  // stringify data
  var _data = JSON.stringify({samplerate:"0.05",data:data,matlab:matlab});
  $.ajax({
    type: "POST",
    url: "/api/motion/"+id,
    data: _data,
    complete: function(){alert("ajax success");}
  });
}

function upload() {
  if(!recordingStatus) {
    uploadData(data);
    data = {x:[],y:[],z:[]};
  }
}

function deviceMotionHandler(eventData) {
  console.log(eventData.acceleration);

  // Grab the acceleration from the results
  var acceleration = eventData.acceleration;

  // record data
  if(recordingStatus) {
    data.x.push((acceleration.x).toFixed(5));
    data.y.push((acceleration.y).toFixed(5));
    data.z.push((acceleration.z).toFixed(5));
  }

  // update the dom
  document.getElementById("devmoAccelX").innerHTML = pad(acceleration.x);
  document.getElementById("devmoAccelY").innerHTML = pad(acceleration.y);
  document.getElementById("devmoAccelZ").innerHTML = pad(acceleration.z);
  document.getElementById("numDataPoints").innerHTML = data.x.length+"";


  // Grab the acceleration including gravity from the results
/*  acceleration = eventData.accelerationIncludingGravity;
  info = xyz.replace("X", pad(acceleration.x));
  info = info.replace("Y", pad(acceleration.y));
  info = info.replace("Z", pad(acceleration.z));
  document.getElementById("moAccelGrav").innerHTML = info;

  // Grab the rotation rate from the results
  var rotation = eventData.rotationRate;
  info = xyz.replace("X", rotation.alpha);
  info = info.replace("Y", rotation.beta);
  info = info.replace("Z", rotation.gamma);
  document.getElementById("moRotation").innerHTML = info;

  // // Grab the refresh interval from the results
  info = eventData.interval;
  document.getElementById("moInterval").innerHTML = info;*/
}


function init() {
  if (window.DeviceMotionEvent) {
    window.addEventListener('devicemotion', deviceMotionHandler, false);
  } else {
    document.getElementById("dmEvent").innerHTML = "Not supported."
  }
}
