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
		//$('#log').append('Received #'+msg.count+': '+msg.data+'<br>').html();
	});

	socket.on('ovladanie_LED', function(msg) {
		$('#btnLED').html(''+msg.data+'');
		$('#btnLED').prop('value', ''+msg.data+'');
	});

	socket.on('auto_LED', function(msg) {
		$('#btnAuto').html(''+msg.data+'');
		$('#btnAuto').prop('value', ''+msg.data+'');
	});

	socket.on('lane_response', function(msg) {
		$('#lane_assist').html(''+msg.data+'');
		$('#lane_assist').prop('value', ''+msg.data+'');
	});

	socket.on('cruise_response', function(msg) {
		$('#adapt_cruise').html(''+msg.data+'');
		$('#adapt_cruise').prop('value', ''+msg.data+'');
	});

	//$('form#emit').submit(function(event) {
	//	socket.emit('my_event', {value: $('#emit_value').val()});
	//	return false;
	//});
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

	$('form#disconnect').submit(function(event) {
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
		units: "Km/h",
		minValue: 0,
		maxValue: 60,
		majorTicks: [
			"0",
			"10",
			"20",
			"30",
			"40",
			"50",
			"60"
		],
		minorTicks: 2,
		strokeTicks: true,
		highlights: [
			{
			"from": 50,
			"to": 60,
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
		animationDuration: 1500,
		animationRule: "linear"
	}).draw();
	// setting value ... gauge.value=500

});
