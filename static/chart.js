console.log(historico);
var escapedString = historico.replace(/'/g,'"');
historia=JSON.parse(escapedString);

function charts() {

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
            type: "area",
            name: "Temperatura",
            connectNullData: true,
            //nullDataLineDashType: "solid",
            xValueType: "dateTime",
            xValueFormatString: "DD MMM hh:mm:ss TT",
            yValueFormatString: "#,##0.##\"°\"",
            dataPoints: [
                { x: new Date(historia.date0), y: parseInt(historia.temp0) },
                { x: new Date(historia.date1), y: parseInt(historia.temp1) },
                { x: new Date(historia.date2), y: parseInt(historia.temp2) },
                { x: new Date(historia.date3), y: parseInt(historia.temp3) },
                { x: new Date(historia.date4), y: parseInt(historia.temp4) },
                { x: new Date(historia.date5), y: parseInt(historia.temp5) },
                { x: new Date(historia.date6), y: parseInt(historia.temp6) },
                { x: new Date(historia.date7), y: parseInt(historia.temp7) },
                { x: new Date(historia.date8), y: parseInt(historia.temp8) },
                { x: new Date(historia.date9), y: parseInt(historia.temp9) }
            ]
        }]
    });
    chart.render();
    
    }