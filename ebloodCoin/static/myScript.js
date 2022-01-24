
function loadCharts(labels, values, legend) {
	chartBar(labels,values,legend);
	chartLine(labels,values,legend);
	chartPie(labels,values,legend);
	/*chartRadar(labels,values,legend);*/
	
}


 function transparentize(value, opacity) {
  var alpha = opacity === undefined ? 0.5 : 1 - opacity;
  return colorLib(value).alpha(alpha).rgbString();
}

function chartBar(labels, values, legend) {


		const CHART_COLORS = {
		  red: 'rgb(255, 99, 132)',
		  orange: 'rgb(255, 159, 64)',
		  yellow: 'rgb(255, 205, 86)',
		  green: 'rgb(75, 192, 192)',
		  blue: 'rgb(54, 162, 235)',
		  purple: 'rgb(153, 102, 255)',
		  grey: 'rgb(201, 203, 207)'
		};
   
		var ctx = document.getElementById("myChartBar").getContext('2d');
		
		var myChartBar = new Chart(ctx, {
			type: 'bar',
		responsive:true,
		maintainAspectRatio: false,
			
			data: {labels : labels,
			
				datasets: [{
					label: legend,
					data: values,
					borderColor: CHART_COLORS.blue
     
				}]
			},
			
			options: {
				scales: {
					yAxes: [{
						ticks: {
							beginAtZero:false
						}
					}]
				}
			}

		});
}


function chartLine(labels, values, legend) {
   

		const data = {
		labels: labels,
		datasets: [{
			label: legend,
			data: values,
			fill: false,
			borderColor: 'rgb(75, 192, 192)',
			tension: 0.1
		}]
		};


		  const config = {
			type: 'line',
			data: data,
		};

		var myChartLine = new Chart(document.getElementById('myChartLine'),config);
}


function chartPie(labels, values, legend) {
   

		const CHART_COLORS = {
		  red: 'rgb(255, 99, 132)',
		  orange: 'rgb(255, 159, 64)',
		  yellow: 'rgb(255, 205, 86)',
		  green: 'rgb(75, 192, 192)',
		  blue: 'rgb(54, 162, 235)',
		  purple: 'rgb(153, 102, 255)',
		  grey: 'rgb(201, 203, 207)'
		};

		const DATA_COUNT = values.length;
		
		const data = {
		  labels: ['Red', 'Orange', 'Yellow', 'Green', 'Blue'],
		  datasets: [
		    {
		      label: 'Dataset 1',
		      data: values,
		      backgroundColor: Object.values(CHART_COLORS),
		    }
		  ]
		};
		  
		  
		const config = {
		  type: 'pie',
		  data: data,
		  options: {
		    responsive: true,
		    plugins: {
		      legend: {
		        position: 'top',
		      },
		      title: {
		        display: true,
		        text: 'Chart.js Pie Chart'
		      }
		    }
		  },
		};  
		  

		var myChartPie = new Chart(document.getElementById('myChartPie'),config);
}




function numbers(config) {
  var cfg = config || {};
  var min = valueOrDefault(cfg.min, 0);
  var max = valueOrDefault(cfg.max, 100);
  var from = valueOrDefault(cfg.from, []);
  var count = valueOrDefault(cfg.count, 8);
  var decimals = valueOrDefault(cfg.decimals, 8);
  var continuity = valueOrDefault(cfg.continuity, 1);
  var dfactor = Math.pow(10, decimals) || 0;
  var data = [];
  var i, value;

  for (i = 0; i < count; ++i) {
    value = (from[i] || 0) + this.rand(min, max);
    if (this.rand() <= continuity) {
      data.push(Math.round(dfactor * value) / dfactor);
    } else {
      data.push(null);
    }
  }

  return data;
}


function months(config) {

  const MONTHS = [
		  'January',
		  'February',
		  'March',
		  'April',
		  'May',
		  'June',
		  'July',
		  'August',
		  'September',
		  'October',
		  'November',
		  'December'
		];

  var cfg = config || {};
  var count = cfg.count || 12;
  var section = cfg.section;
  var values = [];
  var i, value;

  for (i = 0; i < count; ++i) {
    value = MONTHS[Math.ceil(i) % 12];
    values.push(value.substring(0, section));
  }

  return values;
}




function chartRadar(labels, values, legend) {
   
   
   const CHART_COLORS = {
  red: 'rgb(255, 99, 132)',
  orange: 'rgb(255, 159, 64)',
  yellow: 'rgb(255, 205, 86)',
  green: 'rgb(75, 192, 192)',
  blue: 'rgb(54, 162, 235)',
  purple: 'rgb(153, 102, 255)',
  grey: 'rgb(201, 203, 207)'
};
   		

		const DATA_COUNT = 7;
		const NUMBER_CFG = {count: DATA_COUNT, min: 0, max: 100};

		const labelsM = months({count: 7});
		const data = {
		labels: labelsM,
		datasets: [
			{
			label: 'Dataset 1',
			data: numbers(NUMBER_CFG),
			borderColor: CHART_COLORS.red,
			backgroundColor: transparentize(CHART_COLORS.red, 0.5),
			},
			{
			label: 'Dataset 2',
			data: numbers(NUMBER_CFG),
			borderColor: CHART_COLORS.blue,
			backgroundColor: transparentize(CHART_COLORS.blue, 0.5),
			}
		]
		};


		  const config = {
			type: 'radar',
			data: data,
			options: {
				responsive: true,
				plugins: {
				title: {
					display: true,
					text: 'Chart.js Radar Chart'
				}
				}
			},
			};

		var myChartRadar = new Chart(document.getElementById('myChartRadar'),config);
}

