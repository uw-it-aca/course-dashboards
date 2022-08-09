<template>
  <!-- Button trigger modal -->
  <button type="button" class="btn btn-dark" data-bs-toggle="modal" data-bs-target="#exampleModal">
    <i class="bi bi-bar-chart-fill"></i>
  </button>

  <!-- Modal -->
  <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="exampleModalLabel">Histogram</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body" style="position: relative;">
          <div class="d-flex">
            <!-- <div class="y-axis"># of Students</div> -->
            <div :id="'hist-' + id"></div>
          </div>
          <!-- <div class="text-center">GPA</div> -->
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import * as d3 from "d3";
// import { Modal } from "bootstrap";
export default {
  name: "Histogram",
  props: {
    data: Array,
    id: String,
  },
  methods: {
    // resetHistElement() {
    //   let histogram = document.getElementById("hist-" + this.id);
    //   histogram.innerHTML = "";
    // }
  },
  mounted: function () {

    // let hist = new Modal()
    let margin = {top: 10, right: 30, bottom: 30, left: 40},
    width = 460 - margin.left - margin.right,
    height = 400 - margin.top - margin.bottom;

    // append the svg object to the body of the page
    let svg = d3.select("#hist-" + this.id)
      .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
      .append("g")
        .attr("transform",
              "translate(" + margin.left + "," + margin.top + ")");

    // X axis: scale and draw:
    let x = d3.scaleLinear()
        .domain([0, 4])     // can use this instead of 1000 to have the max of data: d3.max(data, function(d) { return +d.price })
        .range([0, width]);
    svg.append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x));

    svg.append("text")             
      .attr("transform",
            "translate(" + (width/2) + "," + 
                           (height + margin.top + 20) + ")")
      .style("text-anchor", "middle")
      .attr("class", "text-danger small fw-bold fs-10")
      .text("GPA");

    // set the parameters for the histogram
    let histogram = d3.histogram()
        .value(function(d) { return d; })   // I need to give the vector of value
        .domain(x.domain())  // then the domain of the graphic
        .thresholds(x.ticks(25)); // then the numbers of bins

    // And apply this function to data to get the bins
    let bins = histogram(this.data);

    // Y axis: scale and draw:
    let y = d3.scaleLinear()
        .range([height, 0]);
        y.domain([0, d3.max(bins, function(d) { return d.length; })]);   // d3.hist has to be called before the Y axis obviously
    svg.append("g")
        .call(d3.axisLeft(y));
    
    const tooltip = d3.select("#hist-" + this.id)
    .append("div")
    .style("opacity", 0)
    .attr("class", "tooltip")
    .style("background-color", "black")
    .style("color", "white")
    .style("border-radius", "5px")
    .style("padding", "10px")
    .style("position", "absolute")

  // A function that change this tooltip when the user hover a point.
  // Its opacity is set to 1: we can now see it. Plus it set the text and position of tooltip depending on the datapoint (d)
  const showTooltip = function(event,d) {
    let transform = event.explicitOriginalTarget.attributes.transform.value;
    let translate = transform.replace("translate(", "").replace(")", "").split(",");
    tooltip
      .transition()
      .duration(100)
      .style("opacity", 1)
    tooltip
      .html(d.length + " students (" + d.x0 + " - " + d.x1 + ")")
      .style("left", translate[0] + "px")
      .style("top", (translate[1]) + "px")
  }
  // const moveTooltip = function(event,d) {
  //   let transform = event.explicitOriginalTarget.attributes.transform.value;
  //   let translate = transform.replace("translate(", "").replace(")", "").split(",");
  //   tooltip
  //     .style("left", translate[0] + "px")
  //     .style("top", (translate[1]) + "px")
  // }
  // A function that change this tooltip when the leaves a point: just need to set opacity to 0 again
  const hideTooltip = function(event,d) {
    tooltip
      .transition()
      .duration(100)
      .style("opacity", 0)
  }

    // append the bar rectangles to the svg element
    svg.selectAll("rect")
        .data(bins)
        .enter()
        .append("rect")
          .attr("x", 1)
          .attr("transform", function(d) { return "translate(" + x(d.x0) + "," + y(d.length) + ")"; })
          .attr("width", function(d) { return x(d.x1) - x(d.x0) -1 ; })
          .attr("height", function(d) { return height - y(d.length); })
          .style("fill", "#69b3a2")
          .on("mouseover", showTooltip)
          // .on("mousemove", moveTooltip)
          .on("mouseleave", hideTooltip);
  },
};
</script>

<style scoped>

/* .histogram::before {
  content: "# of Students";
  transform: rotate(-90deg);
} */
</style>
