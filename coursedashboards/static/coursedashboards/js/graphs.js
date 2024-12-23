//
//  graphs.js - functions to display graphical info
//


function renderGPADisribution(container, median, gpas) {
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
            height: 120,
            width: 250
        },
        xAxis: {
            categories: categories,
            title: {
                //text: "GPA"
                text: ''
            },
            xplotLines: [{
                label: {
                    useHTML: true,
                    text: '<div style="background-color: white; font-size: small; padding: 2px; border: 1px solid lightgray; border-radius: 6px;">' + median + '</div>',
                    rotation: 0,
                    align: 'center',
                    verticalAlign: 'top',
                    y: 30,
                    x: 20
                },
                color: '#FF0000',
                width: 3,
                zIndex: 4,
                value: (median - 1.5) * 10
            }]
        },
        yAxis: {
            tickInterval: 5,
            title: {
            //    text: 'Frequency'
                text: ''
            },
            labels: {
                enabled: false
            }
        },
        tooltip: {
            formatter: function () {
                var tip = this.y + ' with GPA of ' + categories[this.x];

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
    }).addAnnotation({
        draggable: '',
        crop: false,
        shapes:[{
            type: 'image',
            src: '/static/coursedashboards/img/triangle-12.png',
            height: 12,
            width: 12,
            point: {
                x: ((median - 1.5) * 10) - 1,
                xAxis: 0,
                y: 0,
                yAxis: 0
            }
        }]
    });
}


function renderStudentProfile(category, category_students, total_students) {
    var container = 'enrollment-profile-' + category + '-graph',
        categories = [category],
        chart_height = 24,
        bar_height = 18,
        bar_width = 430,
        profile_series = [category_students],
        remainder_series = [total_students - category_students];

    Highcharts.chart(container, {
        chart: {
            type: 'bar',
            height: chart_height,
            width: bar_width,
            borderWidth: 0,
            margin: [0,0,0,0]
        },
        pane: {
            size: '120%'
        },
        legend: {
            enabled: false
        },
        title: undefined,
        xAxis: {
            categories: categories,
            visible: false
        },
        yAxis: {
            visible: false,
        },
        tooltip: {
            formatter: function () {
                return this.y + ((this.series.name == 'students') ? ' ' : ' non-') + this.category + ' students';
            }
        },
        plotOptions: {
            series: {
                stacking: 'percentage',
                pointWidth: bar_height,
                groupPadding: 1,
                pointPadding: 0,
                dataLabels: {
                    enabled: true,
                    format: '{point.percentage:.0f}%'
                }
            }
        },
        series: [{
            name: 'remainder',
            data: remainder_series
        },{
            name: 'students',
            data: profile_series
        }]
    });
}


function renderCoursePercentage1(container, percentages, name_prop, percent_prop) {
    var data = [],
        other = 100,
        chart_width = 240;

    $.each(percentages.splice(0, 9), function () {
        data.push([this[name_prop], Math.ceil(this[percent_prop])]);
        other -= this[percent_prop];
    });

    Highcharts.chart(container, {
        chart: {
            height: 325,
            width: chart_width,
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false
        },
        title: {
            floating: true,
            text: 'Top 10<br>By Percentage',
            useHTML: true,
            y: 90,
            style: {
                fontSize: '0.75em'
            }
        },
        legend: {
            floating: true,
            labelFormat: '{y}%   {name}'
        },
        credits: {
            enabled: false
        },
        tooltip: {
            pointFormat: '{point.name}: <b>{point.y:.1f}%</b>',
            headerFormat: ''
        },
        accessibility: {
            point: {
                valueSuffix: '%'
            }
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                dataLabels: {
                    enabled: false,
                    distance: -24,
                    style: {
                        fontWeight: 'bold',
                        color: 'white'
                    }
                },
                center: ['50%', '40%'],
                selected: false,
                startAngle: -90,
                endAngle: 90,
                size: chart_width,
                innerSize: 150,
                showInLegend: true
            }
        },
        series: [{
            type: 'pie',
            data: data
        }]
    });
}


function renderCoursePercentage2(container, percentages, name_prop, percent_prop) {
    var series = [],
        categories = [],
        other = 100;

    $.each(percentages.slice(0, 9), function () {
        categories.push(this.major_name);
        series.push({
            name: this[name_prop],
            data: [Math.ceil(this[percent_prop])]
        });
        other -= this[percent_prop];
    });

    categories.push('Other');
    series.push({
        name: 'Other',
        percent: other,
        data: [other]
    });

    Highcharts.chart(container, {
        chart: {
            type: 'bar',
            height:200,
            width: 250,
            plotAreaHeight: 500,
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false
        },
        title: undefined,
        legend: {
            labelFormatter: function () {
                return this.chart.series[this.index].dataTable.columns.y[0] + '%  ' + this.name;
            }
        },
        credits: {
            enabled: false
        },
        xAxis: {
            categories: categories,
            visible: false
        },
        yAxis: {
            visible: false,
            max: 100,
            maxPadding: 0,
            reversedStacks: false,
            title: {
                text: null
            }
        },
        tooltip: {
            pointFormat: '{series.name}: <b>{point.y:.1f}%</b>',
            headerFormat: ''
        },
        accessibility: {
            point: {
                valueSuffix: '%'
            }
        },
        plotOptions: {
            series: {
                stacking: 'normal',
                borderWidth: 0,
                pointPadding: 0,
                groupPadding: 0,
                dataLabels: {
                    enabled: true
                }
            }
        },
        series: series
    });
}
