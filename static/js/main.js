
var jsonChartData;

// when all of the html in index.html in the page has loaded, you run the function below
$( document ).ready(function() {
    
    var url = '/json';

    getChartData(url);

    $('#analysis-table').dataTable({
        ajax: url,
        columns: [
            { data: 'name' },
            {
                data: 'overall_sentiment',
                render: function(data) {
                    if (data == 'POSITIVE') {
                        return '<div class="sentiment positive">'+ 'Woo hoo' +'</div>';
                    }
                    else if (data == 'NEGATIVE') {
                        return '<div class="sentiment negative">'+ 'Boo hoo' +'</div>';
                    }
                }
            },
            {
                data: 'overall_prob',
                render: function(data) {
                    return (data*100).toFixed(2) + '%';
                }
            },
            {
                data: 'current_stock_price',
                render: function(data) {
                    return '$' + (data*1).toFixed(2);
                }
            }
        ],
        createdRow: function (row) {
            $(row).addClass('stock-row');
        }
    });

    var apiTable = new $.fn.dataTable.Api( '#analysis-table' );


    $('tbody').on('click', '.stock-row', function(){
        var tr = $(this);
        var row = apiTable.row(tr);
        var stockName = $(this).children('.sorting_1').text();
 
        if ( row.child.isShown() ) {
            // This row is already open - close it
            row.child.hide();
            tr.removeClass('shown');
            drawSentimentChart(jsonChartData);
            drawStockChart(jsonChartData);
        }
        else {
            // Open this row
            row.child( createChildTable(row.data()) ).show();
            tr.addClass('shown');
            var number_companies = jsonChartData['data'].length;
            for (var i = 0; i < number_companies; i++){
                if (jsonChartData.data[i].name == stockName) {
                    var stockObj = {
                        'data' : [jsonChartData.data[i]]
                    };
                    drawSentimentChart(stockObj);
                    drawStockChart(stockObj);
                }
            }
        }
    });

    // Creates the jQuery DataTable child tables; takes in json object data & outputs specific tweets & dates
     
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
            var $tweetCell = $('<td class="tweet-cell">');

            $tbody.append($dateRow);
            
            $dateRow.append($('<td class="date-cell">').text(dateKey));
            $dateRow.append($tweetCell);

            for (var i = 0; i < dateObj['tweets'].length; i++){
                var tweetObj = dateObj['tweets'][i];
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

//loads jsonObject for both Charts
//gets called after the page loads/after the DOM is created which is why it sits outside of document.ready
var getChartData = function(url) {
    $.get(url, function (jsondata){
        jsonChartData = jsondata;
        drawSentimentChart(jsondata);
        drawStockChart(jsondata);
    });
};

function drawSentimentChart(jsonblob){
    var scatterData = [];
    var strokeColor = ['#4FB7C0','#F99E15', '#DA6E12', '#DA4321', '#F91A15', '#F9244F', '#DA20A3', '#DB2FF1', '#9220DA', '#6D24F9'];

    for (var i=0; i < jsonblob['data'].length; i++){
        // for each stock, make a data obj
        var stockObj = jsonblob['data'][i];
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
            var unixTime = dateObj.unix_time;
            var xyObj = {
                x : new Date(dateObj.unix_time * 1000),
                y : dateObj.probability_avg
            };
            xyData.push(xyObj);
        }

        dataObj.data = xyData;
        scatterData.push(dataObj);
    }

    var sentiments = document.getElementById('sentimentchart').getContext('2d');
    var canvas = document.getElementById('sentimentchart');
    var myChart = new Chart(sentiments).Scatter(scatterData, {scaleType: 'date'}, {legendTemplate: "<ul class=\"<%=name.toLowerCase()%>-legend\"><%for(var i=0;i<datasets.length;i++){%><li><span class=\"<%=name.toLowerCase()%>-legend-marker\" style=\"background-color:<%=datasets[i].strokeColor%>\"></span><%=datasets[i].label%></li><%}%></ul>"});
    var gradient = sentiments.createLinearGradient(0, canvas.height, 0, 0);
    gradient.addColorStop(0, "rgba(0, 164, 228,0.2)");
    gradient.addColorStop(0, "rgba(0, 164, 228,0.2)");

    myChart.datasets[0].backgroundColor = gradient;
    myChart.update();
}


function drawStockChart(jsonblob2) {
    var scatterData = [];
    var strokeColor = ['#4FB7C0','#F99E15', '#DA6E12', '#DA4321', '#F91A15', '#F9244F', '#DA20A3', '#DB2FF1', '#9220DA', '#6D24F9'];

    for (var i=0; i < jsonblob2['data'].length; i++){
        // for each stock, make a data obj
        var stockObj = jsonblob2['data'][i];
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
                x : new Date(dateObj.unix_time * 1000),
                y : dateObj.historical_stock_price
            };
            xyData.push(xyObj);
        }

        dataObj.data = xyData;
        scatterData.push(dataObj);
    }

    var stockprices = document.getElementById('stockchart').getContext('2d');
    var myChart = new Chart(stockprices).Scatter(scatterData, {scaleType: 'date'});
}