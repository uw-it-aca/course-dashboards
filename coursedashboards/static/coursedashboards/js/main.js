//Display the top bar: netid and course dropdown
var source = $("#page-top").html();
var template = Handlebars.compile(source);
$("#top_banner").html(template({
    netid: window.user.netid,
    quarter: firstLetterUppercase(window.term.quarter),
    year: window.term.year,
    sections: window.section_data
}));

//Listed for course dropdown selection change
$("#my_courses").change(function() {
    console.log("change");
    var index = $("select[name='my_courses'] option:selected").index();
    showCurrentCourseData(index);
    showHistoricCourseData(index, "All Quarters", "All Years");
});


var index = $("select[name='my_courses'] option:selected").index();
showCurrentCourseData(index);
showHistoricCourseData(index);

//Display data about the currently selected course - called whenever selection changes
function showCurrentCourseData(index) {
    var current = $("#current-course-data").html();
    var currentTemplate = Handlebars.compile(current);
    $("#current-course-target").html(currentTemplate({
        current_median: window.section_data[index].current_median,
        current_num_registered: window.section_data[index].current_enrollment,
        current_capacity:window.section_data[index].limit_estimate_enrollment,
        current_repeat_students:3,
        concurrent_courses:window.section_data[index].concurrent_courses,
        current_majors:window.section_data[index].current_student_majors
    }));
}

//Display data about the past offerings of selected course - called whenever selection changes
function showHistoricCourseData(index, quarter, year) {
    var past_offerings = window.section_data[index].past_offerings;
    for (var i = 0; i < past_offerings.length; i++)
        past_offerings[i].quarter = firstLetterUppercase(past_offerings[i].quarter);
    var historic = $("#historic-course-data").html();
    var historicTemplate = Handlebars.compile(historic);
    var quarter = $("select[name='historic_filter_quarter'] option:selected").val();
    if (quarter == undefined)
        quarter = "All Quarters";
    var year = $("select[name='historic_filter_year'] option:selected").val();
    if (year == undefined)
        year = "All Years";
    $("#historic-course-target").html(historicTemplate({
        past_terms:window.section_data[index].past_offerings,
        common_majors:calculateCommonMajorsForOffering(index, quarter, year),
        latest_majors:calculateRecentMajorsForOffering(index, quarter, year),
        common_courses:commonConcurrentCoursesForOffering(index, quarter, year),
        selected_quarter:quarter,
        selected_year:year
    }));
}

//Historic quarter selection
$("#historic_filter_quarter").change(function() {
    console.log("quarter change");
    var index = $("select[name='my_courses'] option:selected").index();
    showCurrentCourseData(index);
    showHistoricCourseData(index, $("select[name='historic_filter_quarter'] option:selected").val(), $("select[name='historic_filter_year'] option:selected").val());
});

$("#historic_filter_year").change(function() {
    console.log("year change");
    var index = $("select[name='my_courses'] option:selected").index();
    showCurrentCourseData(index);
    showHistoricCourseData(index, $("select[name='historic_filter_quarter'] option:selected").val(), $("select[name='historic_filter_year'] option:selected").val());
})

//On page load, quarter and year are undefined
//When dropdown changed, page redraw shows default selection
function calculateCommonMajorsForOffering(index, quarter, year) {
    var all_quarters = "All Quarters";
    var all_years = "All Years";
    var past_offerings = window.section_data[index].past_offerings;
    var majors = {};
    var total_students = 0;
    if (quarter != all_quarters && year != all_years) {
        for (var o = 0; o < past_offerings.length; o++) {
            if (past_offerings[o].quarter == quarter && past_offerings[o].year == year)
                majors = past_offerings[o].majors;
        }
    }
    else {
        for (var o = 0; o < past_offerings.length; o++) {
            if (quarterIsInRange(past_offerings[o], year, all_years, quarter, all_quarters)) {
                var term_majors = past_offerings[o].majors;
                for (var m = 0; m < term_majors.length; m++) {
                    total_students += term_majors[m].number_students;
                    if (majors.hasOwnProperty(term_majors[m].major))
                        majors[term_majors[m].major] += term_majors[m].number_students;
                    else majors[term_majors[m].major] = term_majors[m].number_students;
                }
            }
        }
        
    }
    return sortMajors(majors, total_students);
}

function calculateRecentMajorsForOffering(index, quarter, year) {
    var all_quarters = "All Quarters";
    var all_years = "All Years";
    var past_offerings = window.section_data[index].past_offerings;
    var majors = {};
    var total_students = 0;
    if (quarter != all_quarters && year != all_years) {
        for (var o = 0; o < past_offerings.length; o++) {
            if (past_offerings[o].quarter == quarter && past_offerings[o].year == year)
                majors = past_offerings[o].latest_majors;
        }
    }
    else {
        for (var o = 0; o < past_offerings.length; o++) {
            if (quarterIsInRange(past_offerings[o], year, all_years, quarter, all_quarters)) {
                var term_majors = past_offerings[o].latest_majors;
                for (var m = 0; m < term_majors.length; m++) {
                    total_students += term_majors[m].number_students;
                    if (majors.hasOwnProperty(term_majors[m].major))
                        majors[term_majors[m].major] += term_majors[m].number_students;
                    else majors[term_majors[m].major] = term_majors[m].number_students;
                }
            }
        }
        
    }
    return sortMajors(majors, total_students);
}

function quarterIsInRange(past_offering, year, all_years, quarter, all_quarters) {
    if ((past_offering.year == year && quarter == all_quarters) ||
        (year == all_years && past_offering.quarter == quarter) ||
        (year == all_years && quarter == all_quarters))
        return true;
    else return false;
}

function sortMajors(majors, total_students) {
    var sorted = [];
    for (var m in majors) {
        sorted.push({"major":m, "number_students":majors[m], "percent_students": ((majors[m]/total_students)*100).toFixed(2)});
    }
    return reverseSortByNumStudents(sorted);
}

function reverseSortByNumStudents(arr) {
    arr.sort(function(a, b) {
        return a.number_students - b.number_students;
    });
    return arr.reverse();
}

function commonConcurrentCoursesForOffering(index, quarter, year) {
    var all_quarters = "All Quarters";
    var all_years = "All Years";
    var past_offerings = window.section_data[index].past_offerings;
    var courses = {};
    var total_students = 0;
    if (quarter != all_quarters && year != all_years) {
        for (var o = 0; o < past_offerings.length; o++) {
            if (past_offerings[o].quarter == quarter && past_offerings[o].year == year)
                courses = past_offerings[o].concurrent_courses;
        }
    }
    else {
        for (var o = 0; o < past_offerings.length; o++) {
            if (quarterIsInRange(past_offerings[o], year, all_years, quarter, all_quarters)) {
                var term_courses = past_offerings[o].concurrent_courses;
                for (var m = 0; m < term_courses.length; m++) {
                    total_students += term_courses[m].number_students;
                    if (courses.hasOwnProperty(term_courses[m].major))
                        courses[term_courses[m].course] += term_courses[m].number_students;
                    else courses[term_courses[m].course] = term_courses[m].number_students;
                }
            }
        }
        
    }
    var sorted = [];
    for (var m in courses) {
        sorted.push({"course":m, "number_students":courses[m], "percent_students": ((courses[m]/total_students)*100).toFixed(2)});
    }
    return reverseSortByNumStudents(sorted);
}

//Capitalize the first letter of a word
function firstLetterUppercase(word) 
{
    return word.charAt(0).toUpperCase() + word.slice(1);
}