var fortune_you_got;

function getFortune() {
	$.get("/fortunes", function(data) {
        fortune_you_got = data;
        return "WHO CARES";
	});
	alert("HEY");
}

// var companyData;
// getChartData() {
// 	... get jsonblob sav as companyData
// 	call drawGraph(blob);
// }

// drawGraph(data) {
// 	... second half of that
// }

onClick Google {
var newData = [];
var number_companies = jsonblob['data'].length;
for (i ... comanies)
   if i.name == 'Google'
   	   newData.append(i)
}

jsonblob['data'][0].length	