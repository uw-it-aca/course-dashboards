//
//  graphs.js - functions to display graphical info
//


function renderGPADisribution(container, gpas) {
    var gpas_dist = Array((2.5*10) + 1).fill(0),
        categories = [],
        max = 0;

    $.each(gpas, function () {
        gpas_dist[(this <= 1.5) ? 0 : Math.round((this - 1.5) * 10)]++;
    });

    $.each(gpas_dist, function (i) {
        if (this > max) {
            max = this;
        }

        categories.push((1.5 + (i * 0.1)).toFixed(1).toString());
    });

    Highcharts.chart(container, {
        title: {
            text: undefined
        },
        credits: {
            enabled: false
        },
        chart: {
            type: 'column',
            height: 120
        },
        xAxis: {
            categories: categories,
            title: {
                text: "GPA"
            }
        },
        yAxis: {
            tickInterval: 5,
            title: {
                text: 'Frequency'
            },
            xlabels: {
                enabled: false
            }
        },
        tooltip: {
            formatter: function () {
                var tip = this.y + ' with GPA of ' + this.x;

                if (this.x == 1.5) {
                    tip += ' or less';
                }

                return tip;
            }
        },
        series: [{
            name: 'GPA',
            showInLegend: false,
            data: gpas_dist
        }]
    });
}
