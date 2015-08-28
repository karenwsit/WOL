//$(document).ready(function () {

//loads dataTable JQuery

$(function () {
	var startDateParam = getUrlParameter('startDate') || '2015-07-19'
	var endDateParam = getUrlParameter('endDate') || '2015-08-17'

	var url = '/json?startDate=' + startDateParam + '&endDate=' + endDateParam;

	// console.log(url)

	loadChartData(url);
	loadStockPriceChartData(url);

	$('#analysis-table').dataTable({
		ajax: url,
		columns: [
			{ data: 'name' },
			{ data: 'overall_sentiment'},
			{ data: 'overall_prob'},
			{ data: 'current_stock_price'}
		],
		createdRow: function (row) {
			$(row).addClass('stock-row');
		}
	});

	var apiTable = new $.fn.dataTable.Api( '#analysis-table' );
	//make ajax call to call the json object in /json route. It will return the json object into the function as the data argument
	$.get(url, function (data) {
		// console.log('data: ', data);
	});

	$('tbody').on('click', '.stock-row', function(){
		var tr = $(this);
        var row = apiTable.row(tr);
 
        if ( row.child.isShown() ) {
            // This row is already open - close it
            row.child.hide();
            tr.removeClass('shown');
        }
        else {
            // Open this row
            row.child( createChildTable(row.data()) ).show();
            tr.addClass('shown');
        }
	});

	function createChildTable (data) {
		var dateTable = $('<table class="child-table">' +
			'<thead><tr>'+
				'<th>Date</th>' +
				'<th>Tweet</th>' +
			'</tr></thead>' +
			'<tbody></tbody></table>');

		var $tbody = dateTable.find('tbody');
		for (var dateKey in data.dates) {
			var dateObj = data.dates[dateKey];
			var $dateRow = $('<tr>');
			var $tweetCell = $('<td>');

			$tbody.append($dateRow);
			
			$dateRow.append($('<td>').text(dateKey));
			$dateRow.append($tweetCell);

			for (var i = 0; i < dateObj['tweets'].length; i++){
				var tweetObj = dateObj['tweets'][i]
				var $tweetLink = $('<a>');
				$tweetLink.text(tweetObj.text);
				$tweetLink.attr({
					class: 'tweet-link',
					href: tweetObj.url,
					target: '_blank'
				});

				$tweetCell.append($tweetLink);
			}
		}

		return dateTable;
	}
});

//loads SentimentChartData

function loadChartData(url) {
	$.get(url, function (jsondata){
		var dates = jsondata['data'][0]['dates'],
			 datesArray = Object.keys(dates);

		var scatterData = [];
		var strokeColor = ['#F16220','#F99E15', '#DA6E12', '#DA4321', '#F91A15', '#F9244F', '#DA20A3', '#DB2FF1', '#9220DA', '#6D24F9'];
		
		// jsondata.data = Array(jsondata['data'][0]);

		for (var i=0; i < jsondata['data'].length; i++){
			// for each stock, make a data obj
			var stockObj = jsondata['data'][i];
			var dataObj = {
				label : stockObj.name,
				strokeColor: strokeColor[i],
		      	pointColor: strokeColor[i],
		      	pointStrokeColor: '#fff',		

			};
			var xyData = [];
			var keysList = Object.keys(stockObj.dates);
			for (var j = 0; j < keysList.length; j++) {
				var dateObj = stockObj.dates[keysList[j]];
				var xyObj = {
					x : dateObj.unix_time,
					y : dateObj.probability_avg
				};
				xyData.push(xyObj);
			};

			dataObj.data = xyData;
			scatterData.push(dataObj);
		}

		var sentiments = document.getElementById('sentimentchart').getContext('2d');
    	var myChart = new Chart(sentiments).Scatter(scatterData);
	});   
};
//loads StockPriceChartData

function loadStockPriceChartData(url) {
	// console.log('load stock price chart')
	$.get(url, function (jsondata){ 
		// console.log(jsondata)
		var dates = jsondata['data'][0]['dates'],
			 datesArray = Object.keys(dates);

		var stockData = []
		var color = ['#F16220','#F99E15', '#DA6E12', '#DA4321', '#F91A15', '#F9244F', '#DA20A3', '#DB2FF1', '#9220DA', '#6D24F9'];

		for (var i = 0, len = jsondata['data'].length; i < len; i++) {
			var cachedDates = jsondata['data'][i]['dates'];
			var historicalStocksArray = [];

			for (var dateKey in cachedDates) {
				var historicalStockPrice = cachedDates[dateKey]['historical_stock_price']
				historicalStocksArray.push(historicalStockPrice);		
			}
			console.log(historicalStocksArray);

			var stockObj = jsondata['data'][i];
			var dataObj = {
				label : stockObj.name,
				fillColor: 'transparent', //dcolor[i],
            	strokeColor: color[i],
            	pointColor: color[i],
            	pointStrokeColor: "#fff",
            	pointHighlightFill: "#fff",
            	pointHighlightStroke: color[i],
            	data: historicalStocksArray
            };

            stockData.push(dataObj)
		}

        console.log(stockData);

        var chartData = {
        	labels: datesArray,
        	datasets: stockData
        }

    	var stockprices = document.getElementById('stockchart').getContext('2d');
    	var myChart = new Chart(stockprices).Line(chartData);
	});   
};


var getUrlParameter = function getUrlParameter(sParam) {
    var sPageURL = decodeURIComponent(window.location.search.substring(1)),
        sURLVariables = sPageURL.split('&'),
        sParameterName,
        i;

    for (i = 0; i < sURLVariables.length; i++) {
        sParameterName = sURLVariables[i].split('=');

        if (sParameterName[0] === sParam) {
            return sParameterName[1] === undefined ? true : sParameterName[1];
        }
    }
};
