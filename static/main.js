//$(document).ready(function () {

//loads dataTable JQuery

$(function () {
	var startDateParam = getUrlParameter('startDate') || '2015-07-19'
	var endDateParam = getUrlParameter('endDate') || '2015-08-17'

	var url = '/json?startDate=' + startDateParam + '&endDate=' + endDateParam;

	// console.log(url)

	loadChartData(url);

	$('#analysis-table').dataTable({
		ajax: url,
		columns: [
			{ data: 'name' },
			{ data: 'overall_sentiment'},
			{ data: 'overall_prob'},
			{ data: 'current_stock_price'}
		]
	});

	//make ajax call to call the json object in /json route. It will return the json object into the function as the data argument
	$.get(url, function (data) {
		// console.log('data: ', data);
	});
});

//loads SentimentChartData

function loadChartData(url) {
	$.get(url, function (jsondata){
		var dates = jsondata['data'][0]['dates'],
			 datesArray = Object.keys(dates);

		// for (var i = 0, len = jsondata['data'].length; i < len; i++) {
		// 	var cachedDates = jsondata['data'][i]['dates'];
		// 	var probArray = [];

		// 	for (var dateKey in cachedDates) {
		// 		var probs = cachedDates[dateKey]['probability_avg']
		// 		probArray.push(probs);		
		// 	}
		// 	// console.log(probArray);	
		// }
		var scatterData = [];
		var strokeColor = ['#F16220','#F99E15', '#DA6E12', '#DA4321', '#F91A15', '#F9244F', '#DA20A3', '#DB2FF1', '#9220DA', '#6D24F9'];
		
		jsondata.data = Array(jsondata['data'][0]);
		debugger;
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
    	
//     	var data = {
//     		labels: datesArray,
//     		datasets: [
// 	    		{
// 	    			label: "Alibaba",
// 	            	fillColor: "rgba(220,220,220,0.2)",
// 	            	strokeColor: "rgba(220,220,220,1)",
// 	            	pointColor: "rgba(220,220,220,1)",
// 	            	pointStrokeColor: "#fff",
// 	            	pointHighlightFill: "#fff",
// 	            	pointHighlightStroke: "rgba(220,220,220,1)",
// 	            	data: [65, "", "", 59, "", 80, 1, 72, "", 100, "", 95]
//             	},
//             	{
// 		            label: "Apple",
// 		            fillColor: "rgba(151,187,205,0.2)",
// 		            strokeColor: "rgba(151,187,205,1)",
// 		            pointColor: "rgba(151,187,205,1)",
// 		            pointStrokeColor: "#fff",
// 		            pointHighlightFill: "#fff",
// 		            pointHighlightStroke: "rgba(151,187,205,1)",
// 		            data: [28, 48, 40, 19, 86, 27, 90]
//             	},
//             	{
// 		            label: "Chipotle",
// 		            fillColor: "rgba(151,187,205,0.2)",
// 		            strokeColor: "rgba(151,187,205,1)",
// 		            pointColor: "rgba(151,187,205,1)",
// 		            pointStrokeColor: "#fff",
// 		            pointHighlightFill: "#fff",
// 		            pointHighlightStroke: "rgba(151,187,205,1)",
// 		            data: [28, 48, 40, 19, 86, 27, 90]
//             	},
//             	{
// 		            label: "Disney",
// 		            fillColor: "rgba(151,187,205,0.2)",
// 		            strokeColor: "rgba(151,187,205,1)",
// 		            pointColor: "rgba(151,187,205,1)",
// 		            pointStrokeColor: "#fff",
// 		            pointHighlightFill: "#fff",
// 		            pointHighlightStroke: "rgba(151,187,205,1)",
// 		            data: [28, 48, 40, 19, 86, 27, 90]
//             	},
//             	{
// 		            label: "Facebook",
// 		            fillColor: "rgba(151,187,205,0.2)",
// 		            strokeColor: "rgba(151,187,205,1)",
// 		            pointColor: "rgba(151,187,205,1)",
// 		            pointStrokeColor: "#fff",
// 		            pointHighlightFill: "#fff",
// 		            pointHighlightStroke: "rgba(151,187,205,1)",
// 		            data: [28, 48, 40, 19, 86, 27, 90]
//             	},
//             	{
// 		            label: "Google",
// 		            fillColor: "rgba(151,187,205,0.2)",
// 		            strokeColor: "rgba(151,187,205,1)",
// 		            pointColor: "rgba(151,187,205,1)",
// 		            pointStrokeColor: "#fff",
// 		            pointHighlightFill: "#fff",
// 		            pointHighlightStroke: "rgba(151,187,205,1)",
// 		            data: [28, 48, 40, 19, 86, 27, 90]
//             	},
//             	{
// 		            label: "Microsoft",
// 		            fillColor: "rgba(151,187,205,0.2)",
// 		            strokeColor: "rgba(151,187,205,1)",
// 		            pointColor: "rgba(151,187,205,1)",
// 		            pointStrokeColor: "#fff",
// 		            pointHighlightFill: "#fff",
// 		            pointHighlightStroke: "rgba(151,187,205,1)",
// 		            data: [28, 48, 40, 19, 86, 27, 90]
//             	},
//             	{
// 		            label: "Nike",
// 		            fillColor: "rgba(151,187,205,0.2)",
// 		            strokeColor: "rgba(151,187,205,1)",
// 		            pointColor: "rgba(151,187,205,1)",
// 		            pointStrokeColor: "#fff",
// 		            pointHighlightFill: "#fff",
// 		            pointHighlightStroke: "rgba(151,187,205,1)",
// 		            data: [28, 48, 40, 19, 86, 27, 90]
//             	},
//             	{
// 		            label: "Tesla",
// 		            fillColor: "rgba(151,187,205,0.2)",
// 		            strokeColor: "rgba(151,187,205,1)",
// 		            pointColor: "rgba(151,187,205,1)",
// 		            pointStrokeColor: "#fff",
// 		            pointHighlightFill: "#fff",
// 		            pointHighlightStroke: "rgba(151,187,205,1)",
// 		            data: [28, 48, 40, 19, 86, 27, 90]
//             	},
//             	{
// 		            label: "Twitter",
// 		            fillColor: "rgba(151,187,205,0.2)",
// 		            strokeColor: "rgba(151,187,205,1)",
// 		            pointColor: "rgba(151,187,205,1)",
// 		            pointStrokeColor: "#fff",
// 		            pointHighlightFill: "#fff",
// 		            pointHighlightStroke: "rgba(151,187,205,1)",
// 		            data: [28, 48, 40, 19, 86, 27, 90]
//             	},             	             	             	
//     		]
    	// }
    	var myChart = new Chart(sentiments).Scatter(scatterData);
	});   
};


//loads StockPriceChartData

function loadStockPriceChartData(url) {
	$.get(url, function (jsondata){ 
		var dates = jsondata['data'][0]['dates'],
			 datesArray = Object.keys(dates);

		for (var i = 0, len = jsondata['data'].length; i < len; i++) {
			var cachedDates = jsondata['data'][i]['dates'];
			var historicalStocksArray = [];

			for (var dateKey in cachedDates) {
				var historicalStockPrice = cachedDates[dateKey]['historical_stock_price']
				historicalStocksArray.push(historicalStockPrice);		
			}
			console.log(historicalStocksArray);	
		}

		
    	var sentiments = document.getElementById('stockchart').getContext('2d');
    	var data = {
    		labels: datesArray,
    		datasets: [
	    		{
	    			label: "Alibaba",
	            	fillColor: "rgba(220,220,220,0.2)",
	            	strokeColor: "rgba(220,220,220,1)",
	            	pointColor: "rgba(220,220,220,1)",
	            	pointStrokeColor: "#fff",
	            	pointHighlightFill: "#fff",
	            	pointHighlightStroke: "rgba(220,220,220,1)",
	            	data: [65, 59, 80, 81, 56, 55, 40]
            	},
            	{
		            label: "Apple",
		            fillColor: "rgba(151,187,205,0.2)",
		            strokeColor: "rgba(151,187,205,1)",
		            pointColor: "rgba(151,187,205,1)",
		            pointStrokeColor: "#fff",
		            pointHighlightFill: "#fff",
		            pointHighlightStroke: "rgba(151,187,205,1)",
		            data: [28, 48, 40, 19, 86, 27, 90]
            	},
            	{
		            label: "Chipotle",
		            fillColor: "rgba(151,187,205,0.2)",
		            strokeColor: "rgba(151,187,205,1)",
		            pointColor: "rgba(151,187,205,1)",
		            pointStrokeColor: "#fff",
		            pointHighlightFill: "#fff",
		            pointHighlightStroke: "rgba(151,187,205,1)",
		            data: [28, 48, 40, 19, 86, 27, 90]
            	},
            	{
		            label: "Disney",
		            fillColor: "rgba(151,187,205,0.2)",
		            strokeColor: "rgba(151,187,205,1)",
		            pointColor: "rgba(151,187,205,1)",
		            pointStrokeColor: "#fff",
		            pointHighlightFill: "#fff",
		            pointHighlightStroke: "rgba(151,187,205,1)",
		            data: [28, 48, 40, 19, 86, 27, 90]
            	},
            	{
		            label: "Facebook",
		            fillColor: "rgba(151,187,205,0.2)",
		            strokeColor: "rgba(151,187,205,1)",
		            pointColor: "rgba(151,187,205,1)",
		            pointStrokeColor: "#fff",
		            pointHighlightFill: "#fff",
		            pointHighlightStroke: "rgba(151,187,205,1)",
		            data: [28, 48, 40, 19, 86, 27, 90]
            	},
            	{
		            label: "Google",
		            fillColor: "rgba(151,187,205,0.2)",
		            strokeColor: "rgba(151,187,205,1)",
		            pointColor: "rgba(151,187,205,1)",
		            pointStrokeColor: "#fff",
		            pointHighlightFill: "#fff",
		            pointHighlightStroke: "rgba(151,187,205,1)",
		            data: [28, 48, 40, 19, 86, 27, 90]
            	},
            	{
		            label: "Microsoft",
		            fillColor: "rgba(151,187,205,0.2)",
		            strokeColor: "rgba(151,187,205,1)",
		            pointColor: "rgba(151,187,205,1)",
		            pointStrokeColor: "#fff",
		            pointHighlightFill: "#fff",
		            pointHighlightStroke: "rgba(151,187,205,1)",
		            data: [28, 48, 40, 19, 86, 27, 90]
            	},
            	{
		            label: "Nike",
		            fillColor: "rgba(151,187,205,0.2)",
		            strokeColor: "rgba(151,187,205,1)",
		            pointColor: "rgba(151,187,205,1)",
		            pointStrokeColor: "#fff",
		            pointHighlightFill: "#fff",
		            pointHighlightStroke: "rgba(151,187,205,1)",
		            data: [28, 48, 40, 19, 86, 27, 90]
            	},
            	{
		            label: "Tesla",
		            fillColor: "rgba(151,187,205,0.2)",
		            strokeColor: "rgba(151,187,205,1)",
		            pointColor: "rgba(151,187,205,1)",
		            pointStrokeColor: "#fff",
		            pointHighlightFill: "#fff",
		            pointHighlightStroke: "rgba(151,187,205,1)",
		            data: [28, 48, 40, 19, 86, 27, 90]
            	},
            	{
		            label: "Twitter",
		            fillColor: "rgba(151,187,205,0.2)",
		            strokeColor: "rgba(151,187,205,1)",
		            pointColor: "rgba(151,187,205,1)",
		            pointStrokeColor: "#fff",
		            pointHighlightFill: "#fff",
		            pointHighlightStroke: "rgba(151,187,205,1)",
		            data: [28, 48, 40, 19, 86, 27, 90]
            	},             	             	             	
    		]
    	}
    	var myChart = new Chart(sentiments).Line(data);
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
