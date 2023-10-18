var graphdata = [];
var graphName = "";

async function getStorageData() {
    let response = await fetch('./storage');
    let graphdata = await response.json()
    return graphdata;
}

async function getSqlData() {
    let response = await fetch('./sql');
    let graphdata = await response.json()
    return graphdata;
}

async function getRedisData() {
    let response = await fetch('./redis');
    let graphdata = await response.json()
    return graphdata;
}

async function GraphHandler(testDataType) {
    // Main Handler
    switch(testDataType) {
        case 'storage':
            graphdata = await getStorageData()
            graphName = "Storage Benchmark";
            break;
        case 'sql':
            graphdata = await getSqlData()
            graphName = "SQL Benchmark";
            break;
        case 'redis':
            graphdata = await getRedisData()
            graphName = "Redis Benchmark";
            break
        default:
            // code block
      }

    //console.log(graphdata)
    //Pass Graph data to graph generator

    cleanData = flattenJson(graphdata)

    google.charts.load("current", {packages:['corechart']});    

    var data = google.visualization.arrayToDataTable([
        ['Genre', 'Fantasy & Sci Fi', 'Romance', 'Mystery/Crime', 'General',
         'Western', 'Literature', { role: 'annotation' } ],
        ['2010', 10, 24, 20, 32, 18, 5, ''],
        ['2020', 16, 22, 23, 30, 16, 9, ''],
        ['2030', 28, 19, 29, 30, 12, 13, '']
      ]);

    var options = {
        width: 600,
        height: 400,
        legend: { position: 'top', maxLines: 3 },
        bar: { groupWidth: '75%' },
        isStacked: true,
        };
    
    var chart = new google.visualization.ColumnChart(document.getElementById("myChart"));
    chart.draw(view, options);
}

function flattenJson(inputJson){
    /// This function flatterns the JSON and returns chart friendly array
    // Return Array of Arrays
    //Convert from 'key:array[test1,test2,test3]' to 'y: test1, label: key'
    var ReturnSet = []
    //Get Number of Tests
    var NoTests = Object.values(inputJson)[0].length;

    // Itterate through each test case
    for (let i = 0; i < NoTests; i++) {
        //Get the Values Test
        var thisResult = []
        for (let key in inputJson) {
            var thisValue = Number(inputJson[key][i]).toFixed(4)
            thisResult.push({x: key, y: thisValue});
        }
        ReturnSet.push(thisResult)
    }

    //Return result
    console.log(ReturnSet)
    return ReturnSet


}