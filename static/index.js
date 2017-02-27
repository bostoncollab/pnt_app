var map = Array.prototype.map;
baseMarkerGroup = new L.LayerGroup();
var mymap = L.map('mapid').setView([39.464559, -76.117401], 12);
L.tileLayer('http://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}').addTo(mymap);
mymap.on('click', addReceiver);

var iconType1 = L.icon({
    iconUrl: 'static/starIcon.png',
    iconSize: [32, 32],
});

var popup = L.popup();

var ipTarget = location.host
// for laptop, uncomment below
//ipTarget = "localhost"

var newReceiver = null;
var dummt       = null;
var receiverLon =  39.464559; //default
var receiverLat = -76.117401; //default
var inputDateSring = new Date().format('Y-m-d H:i');
var env      = "o"
var surround = "u"
var jam      = "n"
var spoof    = "n"

function addMarker(e){
    var clickLat = e.latlng.lat;
    var clickLOn = e.latlng.lng;
    if(addMarker != null){
	newMarker.remove();
	console.log("Removing old marker");
    }
    mymap.panTo(new L.LatLng(clickLat, clickLng));
}


function addReceiver(e){
    receiverLat = e.latlng.lat;
    receiverLon = e.latlng.lng;
    if(newReceiver != null){
	newReceiver.remove();
	console.log("Removing old receiver");
    }
    onMapClick(e);
    newReceiver = L.marker(e.latlng, {icon:iconType1}).addTo(mymap)
    mymap.panTo(new L.LatLng(receiverLat, receiverLon));
}


function get_date(){
    inputDateString = document.getElementById('calendar').value;
    console.log(inputDateString);
}


function get_param(){
    var foo = document.getElementById('env-buttons');
    var env = foo.value;
    var foo = document.getElementById('surround-list');
    var sur = foo.options[foo.selectedIndex].value;
    var foo = document.getElementById('jam-list');
    var jam = foo.options[foo.selectedIndex].value;
    var foo = document.getElementById('spoof-list');
    var spf = foo.options[foo.selectedIndex].value;
    
    console.log(env + ":" + sur + ":" + jam + ":" + spf)
    return env + ":" + sur + ":" + jam + ":" + spf
}


function goto(){
    var longitude = document.getElementById('longitude').value;
    var latitude  = document.getElementById('latitude').value;
    mymap.panTo(new L.LatLng(latitude, longitude));
    mymap.setZoom(10);
}


function clearReceiver(){
    if(newReceiver != null){
	newReceiver.remove();
	console.log("Removing old receiver");
	newReceiver = null;
    }
}


function run(){
    if(newReceiver == null){
	$( "#dialog" ).dialog("open");
	return;
    }
    get_date();
    foo = inputDateString.split(" ")
    date = foo[0]
    time = foo[1]
    paramCode = get_param();
    newReceiver.bindPopup("Processing ... results forthcoming.").openPopup();
    $.get('http://' + ipTarget + ':5000/data?longitude=' + receiverLon + '&latitude=' + receiverLat + '&date=' + date + "&time=" + time + "&param=" + 
	  paramCode, (data) => {
	      newReceiver.bindPopup("<b>Signal Summary</b><br>" + "Latitude: " + String(receiverLat.toFixed(6)) + " deg<br>" + "Longitude: " + String(receiverLon.toFixed(6)) + " deg<br>" +
				    "Elevation: " + String(data.elevation.toFixed(2)) + " m<br>" + "Datetime: " + inputDateString + "<br>" +
				    "No. Visible Satellites: " + String(data.numberVisibleSatellites) +
				    "<br>" + "Constellation Quality: " + String(data.constellationQuality.toFixed(3)) + "<br>Accuracy Metric:" + String(data.accuracy.toFixed(2))).openPopup();
              console.log(data);
              result = data.satelliteDetails;
              var satAlt = map.call(result, (v) => (v.satAlt));
              console.log(satAlt);
	  });
}


function onMapClick(e) {
  var clickLat = e.latlng.lat;
  var clickLng = e.latlng.lng;
  console.log(clickLat);
  console.log(clickLng);
}
