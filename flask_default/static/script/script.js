$(document).ready(function() {
	namespace = '/test';
	var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);

	socket.on('state_connected', function(msg) {
		//console.log(msg.data);
		$('#btnState').html(''+msg.data+'');
		$('#btnState').prop('value', ''+msg.data+'');
	});


	socket.on('new_speed', function(msg) {
		//console.log(msg.data);
		gauge.value=msg.data;		
		myLine.data.labels.push(msg.count);
		myLine.data.datasets.forEach((dataset) => {dataset.data.push(msg.data)});
		if (msg.count > 30){
			myLine.data.labels.shift();
			myLine.data.datasets.forEach((dataset) => {dataset.data.shift()})
		}
		myLine.update();
	});

	socket.on('ovladanie_LED', function(msg) {
		$('#btnLED').html(''+msg.data+'');
		$('#btnLED').prop('value', ''+msg.data+'');
	});

	socket.on('auto_LED', function(msg) {
		$('#btnAuto').html(''+msg.data+'');
		$('#btnAuto').prop('value', ''+msg.data+'');
	});
	
	socket.on('control_response', function(msg) {
		$('#control').html(''+msg.data+'');
		$('#control').prop('value', ''+msg.data+'');
	});

	socket.on('lane_response', function(msg) {
		$('#lane_assist').html(''+msg.data+'');
		$('#lane_assist').prop('value', ''+msg.data+'');
	});

	socket.on('cruise_response', function(msg) {
		$('#adapt_cruise').html(''+msg.data+'');
		$('#adapt_cruise').prop('value', ''+msg.data+'');
	});

	$('#btnAuto').click(function(event) {
		//console.log($(this).val());
		socket.emit('svetla_auto', {value: $(this).val()});
		return false;
	});

	$('#btnLED').click(function(event) {
	  //console.log($(this).val());
		socket.emit('svetla', {value: $(this).val()});
		return false;
	});

	$('#lane_assist').click(function(event) {
		//console.log($(this).val());
		socket.emit('lane_request', {value: $(this).val()});
		return false;
	});

	$('#adapt_cruise').click(function(event) {
		//console.log($(this).val());
		socket.emit('cruise_request', {value: $(this).val()});
		return false;
	});

	$('#btnState').click(function(event) {
		//console.log($(this).val());
		socket.emit('e_state', {value: $(this).val()});
		return false;
	});
	
	$('#control').click(function(event) {
		//console.log($(this).val());
		socket.emit('control_state', {value: $(this).val()});
		return false;
	});

	$('#disconnect').click(function(event) {
		//console.log($(this).val());
		socket.emit('disconnect_request');
		return false;
	});

	$('#speed').on('input', function() {
		//console.log($(this).val());
		socket.emit('speed_input', {value: $(this).val()});
		return false;
	});

	$('#steering').on('input', function() {
		//console.log($(this).val());
		socket.emit('steering_input', {value: $(this).val()});
		return false;
	});

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
					labelString: 'Time'
				}
			}],
			yAxes: [{
				display: true,
				scaleLabel: {
					display: true,
					labelString: 'Value'
				}
			}]
		}
	}
};

window.onload = function(global) {
	var ctx = document.getElementById('chart').getContext('2d');
	myLine = new Chart(ctx, chart_config);
};

