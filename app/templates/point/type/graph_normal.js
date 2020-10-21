window.chartColors = {
  red: 'rgb(255, 99, 132)',
  orange: 'rgb(255, 159, 64)',
  yellow: 'rgb(255, 205, 86)',
  green: 'rgb(75, 192, 192)',
  blue: 'rgb(54, 162, 235)',
  purple: 'rgb(153, 102, 255)',
  grey: 'rgb(231,233,237)'
};

var ctx = document.getElementById('myChart').getContext('2d');
var data = {
    type: 'line',
    data: {
        labels: [
            {% for data in data_list %}
                "{{ data.measuringdate|gdatetime }}",
            {% endfor %}
        ],
        datasets: [
            {
                label: "{{ point.number }}",
                backgroundColor: 'rgb(255, 99, 132)',
                borderWidth : 1,
                pointRadius: 1.3,
                fill:false,                                                                                                 // line의 아래쪽을 색칠할 것인가?
                {% if point.type == "지하수위계" %} borderColor: window.chartColors.blue,
                {% else %} borderColor: window.chartColors.purple, {% endif %}
                lineTension:0.2,                                                                                            // 값을 높이면, line의 장력이 커짐.
                data: [
                    {% for data in data_list %}
                        {
                            t: new Date("{{ data.measuringdate|gdatetime }}"),
                            {% if point.type == "지하수위계" %} y: {{ '%0.3f'|format(data.data14|float) }}
                            {% else %} y: {{ '%0.2f'|format(data.data13|float) }} {% endif %}
                        },
                    {% endfor %}
                ]
            }
        ]
    },
    options: {
        responsive: true,   //auto size : true
        maintainAspectRatio: false, // false하면 그래프 사이즈 조절 가능
        legend: { display: true, position: "bottom", align: "center"}, // 범례 위치 // top, left, bottom, right // start, center, end
        scales: {
            xAxes: [ {
                type: 'time',
                {% if data_list_ea > 0 %}
                    {% if data_list[-1].data11 > 150 %}
                        time: {
                            unit: 'month',
                            tooltipFormat: "YY/MM/DD",
                            displayFormats: {
                                month: 'YY/MM/DD'
                            }
                        },
                    {% else %}
                        time: {
                            unit: 'day',
                            tooltipFormat: "MM/DD",
                            displayFormats: {
                                day: 'MM/DD'
                            }
                        },
                    {% endif %}
                {% endif %}
                scaleLabel: { display: true, labelString: '날짜' },
                ticks: {
                    major: { fontStyle: 'bold', fontColor: '#FF0000' }
                }
            } ],
            yAxes: [{
                {% if point.type == "지하수위계" %} scaleLabel: { display: true, labelString: '일변위(m)' }, {% endif %}
                {% if point.type == "지표침하계" %} scaleLabel: { display: true, labelString: '변위(mm)' }, {% endif %}
                {% if point.type == "구조물경사계" %} scaleLabel: { display: true, labelString: '변위(Degree)' }, {% endif %}

                {% if point.type == "지하수위계" %}
                    ticks: { min: -0.8, max: 0.8 }
                {% else %}
                    {% if point.data_set|length > 0 %}
                        {% if (point.cst16/point.cst03*100)|float|abs > 100 %}
                            ticks: { min: {{ '%0.1f'|format(-1.5*point.cst03|float) }}, max: {{ '%0.1f'|format(1.5*point.cst03|float) }} }
                        {% elif (point.cst16/point.cst02*100)|float|abs > 100 %}
                            ticks: { min: {{ '%0.1f'|format(-1*point.cst03|float) }}, max: {{ '%0.1f'|format(point.cst03|float) }} }
                        {% else %}
                            ticks: { min: {{ '%0.1f'|format(-1*point.cst02|float) }}, max: {{ '%0.1f'|format(point.cst02|float) }} }
                        {% endif %}
                    {% endif %}
                {% endif %}
            }],
        },
        {% if point.data_set|length > 0 %}
        annotation: {
            annotations: [
                {
                    id: "hline-1",
                    type: "line",
                    mode: "horizontal",
                    drawTime: "afterDatasetsDraw",
                    scaleID: "y-axis-0",
                    value: {{point.cst01}},
                    borderColor: 'rgba(255, 0, 0, 0.5)',
                    borderWidth : 1,
                    borderDash: [2,2],
                    borderDashOffset: 5,
                    label: {
                        backgroundColor: 'rgba(255,0,0,0.0)',
                        fontFamily: "sans-serif",
                        fontSize: 9,
                        //fontStyle: "bold",
                        fontColor: 'rgba(255, 0, 0, 0.5)',
                        //xPadding: 6,
                        //yPadding: 6,
                        cornerRadius: 4,
                        position: "center",
                        content: "1차 관리기준치",
                        //rotation: 90,
                        enabled: true
                    },
                },
                {
                    id: "hline-2",
                    type: "line",
                    mode: "horizontal",
                    drawTime: "afterDatasetsDraw",
                    scaleID: "y-axis-0",
                    value: {{point.cst01}}*-1,
                    borderColor: 'rgba(255, 0, 0, 0.5)',
                    borderWidth : 1,
                    borderDash: [2,2],
                    borderDashOffset: 5,
                    label: {
                        backgroundColor: 'rgba(255,0,0,0.0)',
                        fontColor: 'rgba(255, 0, 0, 0.5)',
                        fontFamily: "sans-serif",
                        fontSize: 9,
                        cornerRadius: 4,
                        position: "center",
                        content: "1차 관리기준치",
                        enabled: true
                    },
                },
                {% if point.type != "지하수위계" %}
                    {% if (point.cst16/point.cst02*100)|float|abs > 100 %}
                        {
                            id: "hline-3",
                            type: "line",
                            mode: "horizontal",
                            drawTime: "afterDatasetsDraw",
                            scaleID: "y-axis-0",
                            value: {{point.cst02}},
                            borderColor: 'rgba(255, 0, 0, 0.5)',
                            borderWidth : 1,
                            borderDash: [2,2],
                            borderDashOffset: 5,
                            label: {
                                backgroundColor: 'rgba(255,0,0,0.0)',
                                fontFamily: "sans-serif",
                                fontSize: 9,
                                //fontStyle: "bold",
                                fontColor: 'rgba(255, 0, 0, 0.5)',
                                //xPadding: 6,
                                //yPadding: 6,
                                cornerRadius: 4,
                                position: "center",
                                content: "2차 관리기준치",
                                //rotation: 90,
                                enabled: true
                            },
                        },
                        {
                            id: "hline-4",
                            type: "line",
                            mode: "horizontal",
                            drawTime: "afterDatasetsDraw",
                            scaleID: "y-axis-0",
                            value: {{point.cst02}}*-1,
                            borderColor: 'rgba(255, 0, 0, 0.5)',
                            borderWidth : 1,
                            borderDash: [2,2],
                            borderDashOffset: 5,
                            label: {
                                backgroundColor: 'rgba(255,0,0,0.0)',
                                fontColor: 'rgba(255, 0, 0, 0.5)',
                                fontFamily: "sans-serif",
                                fontSize: 9,
                                cornerRadius: 4,
                                position: "center",
                                content: "2차 관리기준치",
                                enabled: true
                            },
                        },
                    {% endif %}
                {% endif %}

                {% if point.type != "지하수위계" %}
                    {% if (point.cst16/point.cst03*100)|float|abs > 100 %}
                        {
                            id: "hline-5",
                            type: "line",
                            mode: "horizontal",
                            drawTime: "afterDatasetsDraw",
                            scaleID: "y-axis-0",
                            value: {{point.cst03}},
                            borderColor: 'rgba(255, 0, 0, 0.5)',
                            borderWidth : 1,
                            borderDash: [2,2],
                            borderDashOffset: 5,
                            label: {
                                backgroundColor: 'rgba(255,0,0,0.0)',
                                fontFamily: "sans-serif",
                                fontSize: 9,
                                //fontStyle: "bold",
                                fontColor: 'rgba(255, 0, 0, 0.5)',
                                //xPadding: 6,
                                //yPadding: 6,
                                cornerRadius: 4,
                                position: "center",
                                content: "3차 관리기준치",
                                //rotation: 90,
                                enabled: true
                            },
                        },
                        {
                            id: "hline-6",
                            type: "line",
                            mode: "horizontal",
                            drawTime: "afterDatasetsDraw",
                            scaleID: "y-axis-0",
                            value: {{point.cst03}}*-1,
                            borderColor: 'rgba(255, 0, 0, 0.5)',
                            borderWidth : 1,
                            borderDash: [2,2],
                            borderDashOffset: 5,
                            label: {
                                backgroundColor: 'rgba(255,0,0,0.0)',
                                fontColor: 'rgba(255, 0, 0, 0.5)',
                                fontFamily: "sans-serif",
                                fontSize: 9,
                                cornerRadius: 4,
                                position: "center",
                                content: "3차 관리기준치",
                                enabled: true
                            },
                        },
                    {% endif %}
                {% endif %}
            ]
        }
        {% endif %}
    }
};
var chart = new Chart(ctx, data);
