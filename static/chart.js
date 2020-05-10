console.log(historico);
var escapedString = historico.replace(/'/g,'"');
console.log(escapedString);

historia=JSON.parse(escapedString);
console.log(historia.date4)

window.onload = function() {

    var chart = new CanvasJS.Chart("chartContainer", {
        animationEnabled: true,
        title: {
            text: "Ultimas temperaturas"
        },
        axisX: {
            title: "Time"
        },
        axisY: {
            title: "Temperatura",
            suffix: "° C"
        },
        data: [{
            type: "line",
            name: "Temperatura",
            connectNullData: true,
            //nullDataLineDashType: "solid",
            xValueType: "dateTime",
            xValueFormatString: "DD MMM hh:mm:ss TT",
            yValueFormatString: "#,##0.##\"%\"",
            dataPoints: [
                { x: historia.date0, y: historia.temp0 },
                { x: historia.date1, y: historia.temp1 },
                { x: historia.date2, y: historia.temp2 },
                { x: historia.date3, y: historia.temp3 },
                { x: historia.date4, y: historia.temp4 },
                { x: historia.date5, y: historia.temp5 },
                { x: historia.date6, y: historia.temp6 },
                { x: historia.date7, y: historia.temp7 },
                { x: historia.date8, y: historia.temp8 },
                { x: historia.date9, y: historia.temp9 }
            ]
        }]
    });
    chart.render();
    
    }