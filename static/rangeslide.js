
var lunes = $("#0").val();
var lunes_split = lunes.split(/:|-/);
var lunes_1 = lunes_split[0] * 60;
var lunes_2 = lunes_split[2] * 60;

var martes = $("#1").val();
var martes_split = martes.split(/:|-/);
var martes_1 = martes_split[0] * 60;
var martes_2 = martes_split[2] * 60;

var miercoles = $("#2").val();
var miercoles_split = miercoles.split(/:|-/);
var miercoles_1 = miercoles_split[0] * 60;
var miercoles_2 = miercoles_split[2] * 60;

var jueves = $("#3").val();
var jueves_split = jueves.split(/:|-/);
var jueves_1 = jueves_split[0] * 60;
var jueves_2 = jueves_split[2] * 60;

var viernes = $("#4").val();
var viernes_split = viernes.split(/:|-/);
var viernes_1 = viernes_split[0] * 60;
var viernes_2 = viernes_split[2] * 60;

var sabado = $("#5").val();
var sabado_split = sabado.split(/:|-/);
var sabado_1 = sabado_split[0] * 60;
var sabado_2 = sabado_split[2] * 60;

var domingo = $("#6").val();
var domingo_split = domingo.split(/:|-/);
var domingo_1 = domingo_split[0] * 60;
var domingo_2 = domingo_split[2] * 60;


jQuery(function() {
    jQuery('#slider-lunes').slider({
        range: true,
        min: 0,
        max: 1440,
        step: 15,
        values: [ lunes_1,lunes_2 ],
        slide: function( event, ui ) {
            var hours1 = Math.floor(ui.values[0] / 60);
            var minutes1 = ui.values[0] - (hours1 * 60);

            if(hours1.length < 10) hours1= '0' + hours;
            if(minutes1.length < 10) minutes1 = '0' + minutes;

            if(minutes1 == 0) minutes1 = '00';

            var hours2 = Math.floor(ui.values[1] / 60);
            var minutes2 = ui.values[1] - (hours2 * 60);

            if(hours2.length < 10) hours2= '0' + hours;
            if(minutes2.length < 10) minutes2 = '0' + minutes;

            if(minutes2 == 0) minutes2 = '00';

            jQuery('#0').val(hours1+':'+minutes1+'-'+hours2+':'+minutes2 );
        }
    });
});

jQuery(function() {
    jQuery('#slider-martes').slider({
        range: true,
        min: 0,
        max: 1440,
        step: 15,
        values: [ martes_1, martes_2 ],
        slide: function( event, ui ) {
            var hours1 = Math.floor(ui.values[0] / 60);
            var minutes1 = ui.values[0] - (hours1 * 60);

            if(hours1.length < 10) hours1= '0' + hours;
            if(minutes1.length < 10) minutes1 = '0' + minutes;

            if(minutes1 == 0) minutes1 = '00';

            var hours2 = Math.floor(ui.values[1] / 60);
            var minutes2 = ui.values[1] - (hours2 * 60);

            if(hours2.length < 10) hours2= '0' + hours;
            if(minutes2.length < 10) minutes2 = '0' + minutes;

            if(minutes2 == 0) minutes2 = '00';

            jQuery('#1').val(hours1+':'+minutes1+'-'+hours2+':'+minutes2 );
        }
    });
});

jQuery(function() {
    jQuery('#slider-miercoles').slider({
        range: true,
        min: 0,
        max: 1440,
        step: 15,
        values: [ miercoles_1, miercoles_2 ],
        slide: function( event, ui ) {
            var hours1 = Math.floor(ui.values[0] / 60);
            var minutes1 = ui.values[0] - (hours1 * 60);

            if(hours1.length < 10) hours1= '0' + hours;
            if(minutes1.length < 10) minutes1 = '0' + minutes;

            if(minutes1 == 0) minutes1 = '00';

            var hours2 = Math.floor(ui.values[1] / 60);
            var minutes2 = ui.values[1] - (hours2 * 60);

            if(hours2.length < 10) hours2= '0' + hours;
            if(minutes2.length < 10) minutes2 = '0' + minutes;

            if(minutes2 == 0) minutes2 = '00';

            jQuery('#2').val(hours1+':'+minutes1+'-'+hours2+':'+minutes2 );
        }
    });
});

jQuery(function() {
    jQuery('#slider-jueves').slider({
        range: true,
        min: 0,
        max: 1440,
        step: 15,
        values: [ jueves_1, jueves_2 ],
        slide: function( event, ui ) {
            var hours1 = Math.floor(ui.values[0] / 60);
            var minutes1 = ui.values[0] - (hours1 * 60);

            if(hours1.length < 10) hours1= '0' + hours;
            if(minutes1.length < 10) minutes1 = '0' + minutes;

            if(minutes1 == 0) minutes1 = '00';

            var hours2 = Math.floor(ui.values[1] / 60);
            var minutes2 = ui.values[1] - (hours2 * 60);

            if(hours2.length < 10) hours2= '0' + hours;
            if(minutes2.length < 10) minutes2 = '0' + minutes;

            if(minutes2 == 0) minutes2 = '00';

            jQuery('#3').val(hours1+':'+minutes1+'-'+hours2+':'+minutes2 );
        }
    });
});

jQuery(function() {
    jQuery('#slider-viernes').slider({
        range: true,
        min: 0,
        max: 1440,
        step: 15,
        values: [ viernes_1, viernes_2 ],
        slide: function( event, ui ) {
            var hours1 = Math.floor(ui.values[0] / 60);
            var minutes1 = ui.values[0] - (hours1 * 60);

            if(hours1.length < 10) hours1= '0' + hours;
            if(minutes1.length < 10) minutes1 = '0' + minutes;

            if(minutes1 == 0) minutes1 = '00';

            var hours2 = Math.floor(ui.values[1] / 60);
            var minutes2 = ui.values[1] - (hours2 * 60);

            if(hours2.length < 10) hours2= '0' + hours;
            if(minutes2.length < 10) minutes2 = '0' + minutes;

            if(minutes2 == 0) minutes2 = '00';

            jQuery('#4').val(hours1+':'+minutes1+'-'+hours2+':'+minutes2 );
        }
    });
});

jQuery(function() {
    jQuery('#slider-sabado').slider({
        range: true,
        min: 0,
        max: 1440,
        step: 15,
        values: [ sabado_1, sabado_2 ],
        slide: function( event, ui ) {
            var hours1 = Math.floor(ui.values[0] / 60);
            var minutes1 = ui.values[0] - (hours1 * 60);

            if(hours1.length < 10) hours1= '0' + hours;
            if(minutes1.length < 10) minutes1 = '0' + minutes;

            if(minutes1 == 0) minutes1 = '00';

            var hours2 = Math.floor(ui.values[1] / 60);
            var minutes2 = ui.values[1] - (hours2 * 60);

            if(hours2.length < 10) hours2= '0' + hours;
            if(minutes2.length < 10) minutes2 = '0' + minutes;

            if(minutes2 == 0) minutes2 = '00';

            jQuery('#5').val(hours1+':'+minutes1+'-'+hours2+':'+minutes2 );
        }
    });
});

jQuery(function() {
    jQuery('#slider-domingo').slider({
        range: true,
        min: 0,
        max: 1440,
        step: 15,
        values: [ domingo_1, domingo_2 ],
        slide: function( event, ui ) {
            var hours1 = Math.floor(ui.values[0] / 60);
            var minutes1 = ui.values[0] - (hours1 * 60);

            if(hours1.length < 10) hours1= '0' + hours;
            if(minutes1.length < 10) minutes1 = '0' + minutes;

            if(minutes1 == 0) minutes1 = '00';

            var hours2 = Math.floor(ui.values[1] / 60);
            var minutes2 = ui.values[1] - (hours2 * 60);

            if(hours2.length < 10) hours2= '0' + hours;
            if(minutes2.length < 10) minutes2 = '0' + minutes;

            if(minutes2 == 0) minutes2 = '00';

            jQuery('#6').val(hours1+':'+minutes1+'-'+hours2+':'+minutes2 );
        }
    });
});