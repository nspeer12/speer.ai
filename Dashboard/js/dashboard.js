var os = require('os');
// var diskfree = require("diskfree");

function openSettingsMenu() {
    const win = window.open("Home.html", "_blank", "fullscreen= false");
    win.center();
}

const keyDownCallback = keyPressed.bind(this);
const keyUpCallback = keyReleased.bind(this);

function keyReleased(event)
{
    window.removeEventListener("keydown", keyDownCallback);
    window.removeEventListener("keyup", keyUpCallback);
}

function keyPressed(event){
    var keyText = document.getElementById("note_input");

    if(keyText.textContent === "")
    {
        keyText.append(event.key); 
    }
    else
    {
        keyText.append(' + ' + event.key); 
    }
}

function startRecording()
{
    var keyText = document.getElementById("note_input");
    keyText.textContent = "";
    window.addEventListener("keydown", keyDownCallback);
    window.addEventListener("keyup", keyUpCallback);
}

setInterval(function() {
    diagnostics();
  }, 2000);

setInterval(function() {
    clock();
  }, 1000);
  
var days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
const months = ["January", "February", "March", "April", "May", "June",
  "July", "August", "September", "October", "November", "December"];


var lastAverage = cpuAverage()

function cpuAverage() {

    //Initialise sum of idle and time of cores and fetch CPU info
    var totalIdle = 0, totalTick = 0;
    var cpus = os.cpus();

    //Loop through CPU cores
    for(var i = 0, len = cpus.length; i < len; i++) {

        //Select CPU core
        var cpu = cpus[i];

        //Total up the time in the cores tick
        for(type in cpu.times) {
        totalTick += cpu.times[type];
        }     

        //Total up the idle time of the core
        totalIdle += cpu.times.idle;
    }

    //Return the average Idle and Tick times
    return {idle: totalIdle / cpus.length,  total: totalTick / cpus.length};
}

function clock() {
    var d = new Date();
    document.getElementById("time_local").innerHTML = d.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
    document.getElementById("time_day").innerHTML = days[d.getDay()]
    document.getElementById("time_date").innerHTML = d.getDate()
    document.getElementById("time_month").innerHTML = months[d.getMonth()]
}

function diagnostics() {
    var tempPoll = cpuAverage();

    var idleDifference = tempPoll.idle - lastAverage.idle;
    var totalDifference = tempPoll.total - lastAverage.total;

    lastAverage = tempPoll;
  
    //Calculate the average percentage CPU usage
    var percentageCPU = 100 - ~~(100 * idleDifference / totalDifference);

    document.getElementById("cpu").innerText = "CPU Usage: " + percentageCPU + "%";
    document.getElementById("ram").innerText = "Free Memory: " + Math.round(os.freemem() / (1000000)) + " MB";

    // diskfree.check('C:', function onDiskInfo(error, info) {
    //     if (error) {
    //         // You can see if its a known error
    //         if (diskfree.isErrBadPath(err)) {
    //             throw new Error('Path is Wrong');
    //         } else if (diskfree.isErrDenied(error)) {
    //             throw new Error('Permission Denied');
    //         } else if (diskfree.isErrIO(error)) {
    //             throw new Error('IO Error');
    //         }
     
    //         throw new Error('Unknown error: ' + error);
    //     }
     
    // document.getElementById("storage").innerText = "Free Memory: " + Math.round(info.free / (1000000)) + " MB";
    // });
}