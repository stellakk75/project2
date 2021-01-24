
// set the dimensions and margins of the graph
let width = 1750
    height = 550
    margin = 40

// The radius of the pieplot is half the width or half the height (smallest one). I subtract a bit of margin.
var radius = Math.min(width, height) / 2 - margin

// append the svg object to the div called 'my_dataviz'
var svg = d3.select("#my_dataviz")
  .append("svg")
    .attr("width", width)
    .attr("height", height)
  .append("g")
    .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

// create 2 data_set
var data1 = {a: 9, b: 20, c:30, d:8, e:12}
var data2 = {a: 6, b: 16, c:20, d:14, e:19, f:12}

// set the color scale
var color = d3.scaleOrdinal()
  .domain(["a", "b", "c", "d", "e", "f"])
  .range(d3.schemeDark2);

// A function that create / update the plot for a given variable:
function update(data) {

  // Compute the position of each group on the pie:
  var pie = d3.pie()
    .value(function(d) {return d.value; })
    .sort(function(a, b) { console.log(a) ; return d3.ascending(a.key, b.key);} ) // This make sure that group order remains the same in the pie chart
  var data_ready = pie(d3.entries(data))

  // map to data
  var u = svg.selectAll("path")
    .data(data_ready)

  // Build the pie chart: Basically, each part of the pie is a path that we build using the arc function.
  u
    .enter()
    .append('path')
    .merge(u)
    .transition()
    .duration(1000)
    .attr('d', d3.arc()
      .innerRadius(0)
      .outerRadius(radius)
    )
    .attr('fill', function(d){ return(color(d.data.key)) })
    .attr("stroke", "white")
    .style("stroke-width", "2px")
    .style("opacity", 1)


  // remove the group that is not present anymore
  u
    .exit()
    .remove()

}

// Initialize the plot with the first dataset
update(data1)


  
  // d3.json('/RawData/new_books.json').then(data => {

  //     console.log(data)
      
  //     let level = data.books;
   
  //     let genre = []

  //     level.forEach(index => {
  //         // console.log(index.Price)
  //         if (index.Genre == 2009) {
  //             genre.push(index.Genre)
  //         }

      
  //    });
  //   });
  //     console.log(genre)
    

//     // Create a pie chart
//     let pieData = [{
//     type: "pie",
//     values: [nonfinction, fiction],
//     lables: ["Non Fiction", "Fiction"],
//     textinfo: "lable+percent",
//     insidetextorientation: "radial"}]

//     // Create a layout for the pie chart
//     let pielayout = [{
//     height: 700,
//     width: 700,
//     title: "Fiction vs Non Fiction"}];


// Plotly.newPlot("pie", pieData, pielayout);

// });

// };






