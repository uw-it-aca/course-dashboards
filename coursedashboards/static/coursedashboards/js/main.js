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
    var index = $("select[name='my_courses'] option:selected").index();
    showCurrentCourseData(index);
    showHistoricDataSelectors(index, "All Quarters", "All Years");
    showHistoricCourseData(index, "All Quarters", "All Years");
});


var index = $("select[name='my_courses'] option:selected").index();
showCurrentCourseData(index);
showHistoricDataSelectors(index, "All Quarters", "All Years");
showHistoricCourseData(index, "All Quarters", "All Years");

//Display data about the currently selected course - called whenever selection changes
function showCurrentCourseData(index) {
    var current = $("#current-course-data").html();
    var currentTemplate = Handlebars.compile(current);
    $("#current-course-target").html(currentTemplate({
        current_median: window.section_data[index].current_median,
        current_num_registered: window.section_data[index].current_enrollment,
        current_capacity:window.section_data[index].limit_estimate_enrollment,
        current_repeat_students:section_data[index].current_repeating,
        concurrent_courses:window.section_data[index].concurrent_courses,
        current_majors:window.section_data[index].current_student_majors
    }));
}

//Populate the historic data selectors for the currently selected course
function showHistoricDataSelectors(index, quarter, year) {
    //Fix case of past quarters and create arrays without duplicate quarters/years
    var valid_quarters = [];
    var valid_years = [];
    var combined = [];//stores quarter + year so that when a quarter is selected, can only select years where the course was offered in that quarter & vice versa
    var past_offerings = window.section_data[index].past_offerings;
    for (var o in past_offerings) {
        past_offerings[o].quarter = firstLetterUppercase(past_offerings[o].quarter);
        if (combined.indexOf(past_offerings[o].quarter + past_offerings[o].year) == -1)
            combined.push(past_offerings[o].quarter + past_offerings[o].year);
        if (valid_quarters.indexOf(past_offerings[o].quarter) == -1)
            valid_quarters.push(past_offerings[o].quarter);
        if (valid_years.indexOf(past_offerings[o].year) == -1)
            valid_years.push(past_offerings[o].year);
    }
    //Remove any invalid combinations of quarter and year based on current selection
    if (quarter != "All Quarters") {
        var remove_years = [];
        for (var y in valid_years)
            if (combined.indexOf(quarter + valid_years[y]) == -1)
                remove_years.push(valid_years[y]);
        while (remove_years.length > 0) {
            valid_years.splice(valid_years.indexOf(remove_years[0]),1);
            remove_years.splice(0,1);
        }
    }
    if (year != "All Years") {
        var remove_quarters = [];
        for (var q in valid_quarters)
            if (combined.indexOf(valid_quarters[q] + year) == -1)
                remove_quarters.push(valid_quarters[q]);
        while (remove_quarters.length > 0) {
            valid_quarters.splice(valid_quarters.indexOf(remove_quarters[0]),1);
            remove_quarters.splice(0,1);
        }
    }
    
    //Load template
    var selectors = $("#historic-data-selectors").html();
    var selectorsTemplate = Handlebars.compile(selectors);
    $("#historic-selector-target").html(selectorsTemplate({
        past_quarters:prepOptions(quarter, valid_quarters, "All Quarters"), past_years:prepOptions(year, valid_years, "All Years")
    }));
    
    //Historic data selection
    $(".historic-filter").change(function() {
        console.log("selection change ");
        index = $("select[name='my_courses'] option:selected").index();
        var newQuarter = $("select[name='historic_filter_quarter'] option:selected").val();
        var newYear = $("select[name='historic_filter_year'] option:selected").val();
        showHistoricDataSelectors(index, newQuarter, newYear);
        showHistoricCourseData(index, newQuarter, newYear);
    });
}

//Prepares the handlebars variable for historic data selectors
function prepOptions(selected, valid, all) {
    options = [];
    //make sure All option gets pushed
    options.push({
        name: all,
        selected: (selected==all)? "selected":""
    });
    for (var v in valid) {
        options.push({
            name: valid[v],
            selected: (valid[v]==selected) ? "selected":""
        });
    }
    return options;
}

//Display data about the past offerings of selected course - called whenever selection changes
function showHistoricCourseData(index, quarter, year) {
    var past_offerings = window.section_data[index].past_offerings;
    for (var i = 0; i < past_offerings.length; i++)
        past_offerings[i].quarter = firstLetterUppercase(past_offerings[i].quarter);
    var historic = $("#historic-course-data").html();
    var historicTemplate = Handlebars.compile(historic);
    console.log("show historic data for " + quarter + " " + year);
    $("#historic-course-target").html(historicTemplate({
        common_majors:calculateCommon(index, quarter, year, "majors","major"),
        latest_majors:calculateCommon(index, quarter, year, "latest_majors","major"),
        common_courses:calculateCommon(index, quarter, year, "concurrent_courses","course"),
        selected_quarter:quarter,
        selected_year:year,
        median_course_grade: calculateCourseGrade(index, quarter, year),
        failed_percent: calculateFailedPercentage(index, quarter, year),
        instructors: getInstructors(index, quarter, year)
        //past_terms:window.section_data[index].past_offerings
    }));
}

function getInstructors(index, quarter, year) {
    var all_quarters = "All Quarters";
    var all_years = "All Years";
    var past_offerings = window.section_data[index].past_offerings;
    var instructors = [];
    for (var o = 0; o < past_offerings.length; o++) {
        if (quarterIsInRange(past_offerings[o], year, all_years, quarter, all_quarters)) {
            for (var i in past_offerings[o].instructors) {
                instructors.push({
                    quarter: past_offerings[o].quarter,
                    year: past_offerings[o].year,
                    display_name: past_offerings[o].instructors[i].display_name,
                    uw_email: past_offerings[o].instructors[i].uwnetid + "@uw.edu"
                });
            }
        }
    }
    return instructors;
}


function calculateCourseGrade(index, quarter, year) {
    var all_quarters = "All Quarters";
    var all_years = "All Years";
    var past_offerings = window.section_data[index].past_offerings;
    var grades = [];
    for (var o = 0; o < past_offerings.length; o++) {
        var offering = past_offerings[o];
        if (quarterIsInRange(offering, year, all_years, quarter, all_quarters)) {
            grades = grades.concat(offering.course_grades);
        }
    }

    return (grades.length) ? math.median(grades) : 'None';
}


function calculateFailedPercentage(index, quarter, year) {
    var all_quarters = "All Quarters";
    var all_years = "All Years";
    var past_offerings = window.section_data[index].past_offerings;
    var n = 0;
    var failed = 0;
    for (var o = 0; o < past_offerings.length; o++) {
        var offering = past_offerings[o];
        if (quarterIsInRange(offering, year, all_years, quarter, all_quarters)) {
            var grades = offering.course_grades;
            for (var g = 0; g < grades.length; g++){
                n += 1;
                if (grades[g] <= 0.0) { failed += 1; }
            }
        }
    }

    return (n > 0) ? Math.round((failed * 100)/ n) : 0;
}


//Calculates all of the common major/course lists based on historic selections
function calculateCommon(index, quarter, year, list_type, name_type) {
    var all_quarters = "All Quarters";
    var all_years = "All Years";
    var past_offerings = window.section_data[index].past_offerings;
    var obj = {};
    var total_students = 0;
    for (var o = 0; o < past_offerings.length; o++) {
        if (quarterIsInRange(past_offerings[o], year, all_years, quarter, all_quarters)) {
            var term_obj = past_offerings[o][list_type];
            for (var m = 0; m < term_obj.length; m++) {
                total_students += term_obj[m].number_students;
                if (obj.hasOwnProperty(term_obj[m][name_type]))
                    obj[term_obj[m][name_type]] += term_obj[m].number_students;
                else obj[term_obj[m][name_type]] = term_obj[m].number_students;
            }
        }
    }
    return sortObj(obj, total_students, name_type);
}

//check if past offering was in the range selected in the dropdowns
function quarterIsInRange(past_offering, year, all_years, quarter, all_quarters) {
    return ((past_offering.year == year && quarter == all_quarters) ||
            (year == all_years && past_offering.quarter == quarter) ||
            (year == all_years && quarter == all_quarters) ||
            (year != all_years && quarter != all_quarters));
}

//order majors/courses by number of students
function sortObj(arr, total_students, name_type) {
    var sorted = [];
    for (var i in arr) {
        if (name_type == "major")
            sorted.push({"major":i, "number_students":arr[i], "percent_students": ((arr[i]/total_students)*100).toFixed(2)});
        else
            sorted.push({"course":i, "number_students":arr[i], "percent_students": ((arr[i]/total_students)*100).toFixed(2)});
    }
    return reverseSortByNumStudents(sorted);
}

//sort array of objects by number_students value
function reverseSortByNumStudents(arr) {
    arr.sort(function(a, b) {
        return a.number_students - b.number_students;
    });
    return arr.reverse();
}


//Capitalize the first letter of a word
function firstLetterUppercase(word) 
{
    return word.charAt(0).toUpperCase() + word.slice(1);
}
