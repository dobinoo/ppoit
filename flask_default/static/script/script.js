//Funkcnost ak uz je stranka bezpecne nacitana
$(document).ready(function() {
	namespace = '/test';
	var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);
	var graph_sample=0


////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////

//Start/Stop
	socket.on('state_connected', function(msg) {
		//console.log(msg.data);
		$('#state').html(''+msg.data+'');
		$('#state').prop('value', ''+msg.data+'');
	});


	//Svetla on/off
	socket.on('ovladanie_LED', function(msg) {
		$('#led_on_off').html(''+msg.data+'');
		$('#led_on_off').prop('value', ''+msg.data+'');
	});

	//Automaticke svetla on/off
	socket.on('auto_LED', function(msg) {
		$('#led_manual_auto').html(''+msg.data+'');
		$('#led_manual_auto').prop('value', ''+msg.data+'');
	});

	//Ovladanie remote/web
	socket.on('control_response', function(msg) {
		$('#control').html(''+msg.data+'');
		$('#control').prop('value', ''+msg.data+'');
	});

	//Lane assist on/off
	socket.on('lane_response', function(msg) {
		$('#lane_assist').html(''+msg.data+'');
		$('#lane_assist').prop('value', ''+msg.data+'');
	});

	//Adaptivny tempomat
	socket.on('cruise_response', function(msg) {
		$('#adapt_cruise').html(''+msg.data+'');
		$('#adapt_cruise').prop('value', ''+msg.data+'');
	});
////////////////////////////////////////////////////


////////////////////////////////////////////////////
///////////////////////////////////////////////////

	//Automaticke svetla on/off
	$('#led_manual_auto').click(function(event) {
		console.log($(this).val());
		socket.emit('svetla_auto', {value: $(this).val()});
		return false;
	});

	//Svetla on/off
	$('#led_on_off').click(function(event) {
	  console.log($(this).val());
		socket.emit('svetla', {value: $(this).val()});
		return false;
	});

	//Lane assist on/off
	$('#lane_assist').click(function(event) {
		console.log($(this).val());
		socket.emit('lane_request', {value: $(this).val()});
		return false;
	});

	//Adaptivny tempomat
	$('#adapt_cruise').click(function(event) {
		console.log($(this).val());
		socket.emit('cruise_request', {value: $(this).val()});
		return false;
	});

	//Start/Stop
	$('#state').click(function(event) {
		console.log($(this).val());
		socket.emit('e_state', {value: $(this).val()});
		return false;
	});

	//Adaptivny tempomat
	$('#control').click(function(event) {
		console.log($(this).val());
		socket.emit('control_state', {value: $(this).val()});
		return false;
	});

	//Odpojenie
	$('#disconnect').click(function(event) {
		console.log($(this).val());
		socket.emit('disconnect_request');
		alert("Boli ste odpojený !");
		return false;
	});

	//Rychlost
	$('#speed').on('input', function() {
		console.log($(this).val());
		socket.emit('speed_input', {value: $(this).val()});
		return false;
	});

	//Riadenie
	$('#steering').on('input', function() {
		console.log($(this).val());
		socket.emit('steering_input', {value: $(this).val()});
		return false;
	});
	////////////////////////////////////////////////////


	//Spravanie grafu
	socket.on('new_speed', function(msg) {
		//console.log(msg.data);
		gauge.value=msg.data;
		myLine.data.labels.push(msg.count);
		myLine.data.datasets.forEach((dataset) => {dataset.data.push(msg.data)});
		graph_sample = graph_sample +1
		if (graph_sample>16){//(msg.count > 30){
			graph_sample = graph_sample -1
			myLine.data.labels.shift();
			myLine.data.datasets.forEach((dataset) => {dataset.data.shift()})
		}
		myLine.update();
	});


	//Tachometer
	var gauge = new RadialGauge({
		renderTo: 'canvas-tachometer',
		width: 300,
		height: 300,
		units: "%",
		minValue: 0,
		maxValue: 100,
		majorTicks: [
			"0",
			"10",
			"20",
			"30",
			"40",
			"50",
			"60",
			"70",
			"80",
			"90",
			"100",
		],
		minorTicks: 2,
		strokeTicks: true,
		highlights: [
			{
			"from": 70,
			"to": 100,
			"color": "rgba(200, 50, 50, .75)"
			}
		],
		colorPlate: "#fff",
		borderShadowWidth: 0,
		borders: false,
		needleType: "arrow",
		needleWidth: 2,
		needleCircleSize: 7,
		needleCircleOuter: true,
		needleCircleInner: false,
		animationDuration: 100,
		animationRule: "linear"
	}).draw();

	(function(){
		document.getElementById('vid_webcam').href = window.location.protocol + '//' + window.location.hostname + ':8081';
	})();
});

//Nastavenie grafu
var chart_config = {
	type: 'line',
	data: {
		labels: [ 0 ], //y
		datasets: [{
			label: "Speed",
			backgroundColor: "#db7749",
			borderColor: "#db7749",
			data: [ 0 ], //x
			fill: false,
		}]
	},
	options: {
		responsive: true,
		title:{
			display: true,
			text: 'Data from car'
		},
		scales:{
			xAxes: [{
				display: true,
				scaleLabel: {
					display: true,
					labelString: 'Time(s)'
				}
			}],
			yAxes: [{
				display: true,
				scaleLabel: {
					display: true,
					labelString: 'Value(%)'
				}
			}]
		}
	}
};

window.onload = function(global) {
	var ctx = document.getElementById('chart').getContext('2d');
	myLine = new Chart(ctx, chart_config);
};
