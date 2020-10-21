var ctx = document.getElementById('myChart').getContext('2d');
var data = {
    type: 'scatter',
    data: {
        datasets: [
            {% if data_list_ea > 0 %}
                {% if data_list_ea > 11 %}
                    {% for i in range(12) %}
                    {
                        label: '{{ data_list[i*-1-1].measuringdate|datetime }}',
                        backgroundColor: 'rgb(255, 99, 132)',
                        borderWidth : 1,
                        fill:false,                                                                                                 // line의 아래쪽을 색칠할 것인가?
                        {% if i==11 %} borderColor: 'rgba(255, 205, 86, 0.7)',{% endif %}
                        {% if i==10 %} borderColor: 'rgba(255, 205, 86, 1.0)',{% endif %}
                        {% if i==9 %} borderColor: 'rgba(255, 159, 64, 0.7)',{% endif %}
                        {% if i==8 %} borderColor: 'rgba(255, 159, 64, 1.0)',{% endif %}
                        {% if i==7 %} borderColor: 'rgb(75, 192, 192)',{% endif %}
                        {% if i==6 %} borderColor: 'rgb(203, 152, 255)',{% endif %}
                        {% if i==5 %} borderColor: 'rgb(54, 162, 235)',{% endif %}
                        {% if i==4 %} borderColor: 'rgb(255, 99, 132)',{% endif %}
                        {% if i==3 %} borderColor: 'rgb(35, 132, 132)',{% endif %}
                        {% if i==2 %} borderColor: 'rgb(133, 82, 235)',{% endif %}
                        {% if i==1 %} borderColor: 'rgb(0, 0, 200)',{% endif %}
                        {% if i==0 %} borderColor: 'rgb(150, 0, 0)',{% endif %}
                        showLine: true,
                        pointRadius: 0,
                        lineTension:0.4,                                                                                            // 값을 높이면, line의 장력이 커짐.
                        data: [
                            {% if data_list[i*-1].data09 %}
                                {% for depth in range(point.cst10|int) %}
                                    { x: {{ data_list[i*-1-1].data09.split(',')[point.cst10|int-1-depth] }}-0, y: {{ depth/-2-0.5 }} },
                                {% endfor %}
                            {% endif %}
                        ]
                    },
                    {% endfor %}
                {% else %}
                    {% for i in range(data_list_ea) %}
                    {
                        label: '{{ data_list[i*-1-1].measuringdate|datetime }}',
                        backgroundColor: 'rgb(255, 99, 132)',
                        borderWidth : 1,
                        fill:false,                                                                                                 // line의 아래쪽을 색칠할 것인가?
                        {% if i==11 %} borderColor: 'rgba(255, 205, 86, 0.7)',{% endif %}
                        {% if i==10 %} borderColor: 'rgba(255, 205, 86, 1.0)',{% endif %}
                        {% if i==9 %} borderColor: 'rgba(255, 159, 64, 0.7)',{% endif %}
                        {% if i==8 %} borderColor: 'rgba(255, 159, 64, 1.0)',{% endif %}
                        {% if i==7 %} borderColor: 'rgb(75, 192, 192)',{% endif %}
                        {% if i==6 %} borderColor: 'rgb(203, 152, 255)',{% endif %}
                        {% if i==5 %} borderColor: 'rgb(54, 162, 235)',{% endif %}
                        {% if i==4 %} borderColor: 'rgb(255, 99, 132)',{% endif %}
                        {% if i==3 %} borderColor: 'rgb(35, 132, 132)',{% endif %}
                        {% if i==2 %} borderColor: 'rgb(133, 82, 235)',{% endif %}
                        {% if i==1 %} borderColor: 'rgb(0, 0, 200)',{% endif %}
                        {% if i==0 %} borderColor: 'rgb(150, 0, 0)',{% endif %}
                        showLine: true,
                        pointRadius: 0,
                        lineTension:0.4,                                                                                            // 값을 높이면, line의 장력이 커짐.
                        data: [
                            {% if data_list[i*-1-1].data09 %}
                                {% for depth in range(point.cst10|int) %}
                                    { x: {{ data_list[i*-1-1].data09.split(',')[point.cst10|int-1-depth] }}-0, y: {{ depth/-2-0.5 }} },
                                {% endfor %}
                            {% endif %}
                        ]
                    },
                    {% endfor %}
                {% endif %}
            {% endif %}
        ],
    },
    options: {
        responsive: true,   //auto size : true
        maintainAspectRatio: false, // false하면 그래프 사이즈 조절 가능
        legend: { display: true, position: "bottom", align: "center"}, // 범례 위치 // top, left, bottom, right // start, center, end
        scales: {
            xAxes: [ {
                scaleLabel: { display: true, labelString: '수평변위(mm)' },
                {% if point.data_set|length > 0 %}
                    {% if (point.cst16/point.cst03*100)|float|abs > 100 %}
                        ticks: { min: {{ '%0.2f'|format(-1.5*point.cst03|float) }}, max: {{ '%0.2f'|format(1.5*point.cst03|float) }} }
                    {% elif (point.cst16/point.cst02*100)|float|abs > 100 %}
                        ticks: { min: {{ '%0.2f'|format(-1*point.cst03|float) }}, max: {{ '%0.2f'|format(point.cst03|float) }} }
                    {% elif (point.cst16/point.cst01*100)|float|abs > 100 %}
                        ticks: { min: {{ '%0.2f'|format(-1*point.cst02|float) }}, max: {{ '%0.2f'|format(point.cst02|float) }} }
                    {% else %}
                        ticks: { min: {{ '%0.2f'|format(-1*point.cst01|float) }}, max: {{ '%0.2f'|format(point.cst01|float) }} }
                    {% endif %}
                {% endif %}
            } ],
            yAxes: [{
                scaleLabel: { display: true, labelString: '심도(M)' },
                ticks: { min: {{point.cst10|int/-2}}, max: -1.0, stepSize: 0.5 }
            }]
        },
    }
};
var chart = new Chart(ctx, data);

function getRandomColor() {
    var letters = '0123456789ABCDEF'.split('');
    var color = '#';
    for (var i = 0; i < 6; i++ ) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}
