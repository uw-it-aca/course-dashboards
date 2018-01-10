//
//  main.js - data/functions to support course dashboards
//


// Constant variables

var ALL_QUARTERS = "All Quarters";
var ALL_YEARS = "All Years";
var ALL_MY_COURSES = "All My Courses";
var only_my_courses = false;

$(document).ready(function () {
    displayPageHeader();
    displayCourseSelector();

    if (courseHash()) {
        if (!loadCourse(courseHash())) {
            displayErrorPage();
        }
    } else {
        displaySelectedCourse();
    }

    //Listed for course dropdown selection change
    $("#my_courses").change(function() {
        displaySelectedCourse();
    });
});


function displayPageHeader() {
    //Display the top bar: netid and course dropdown
    var source = $("#page-top").html();
    var template = Handlebars.compile(source);
    $("#top_banner").html(template({
        netid: window.user.netid,
        quarter: firstLetterUppercase(window.term.quarter),
        year: window.term.year
    }));
}

function courseHash() {
    return decodeURIComponent(window.location.hash.slice(1));
}

function displayCourseSelector() {
    source = $("#course-select").html();
    template = Handlebars.compile(source);
    $(".course-select").html(template({
        quarter: firstLetterUppercase(window.term.quarter),
        year: window.term.year,
        sections: window.section_data
    }));
}

function displaySelectedCourse() {
    var $option = $("select[name='my_courses'] option:selected");
    var index = $option.index();

    if (window.section_data[index].loaded) {
        showCurrentCourseData(index);
    } else {
        fetchCurrentCourseData(index);
    }

    if (window.section_historic_data[index].loaded){
        showHistoricDataSelectors(index, ALL_QUARTERS, ALL_YEARS);
        showHistoricCourseData(index, ALL_QUARTERS, ALL_YEARS);
    } else {
        fetchHistoricCourseData(index);
    }
}

function displayErrorPage() {
    var current = $("#cannot-display-course").html();
    var currentTemplate = Handlebars.compile(current);
    $('.main-content').html(currentTemplate({
        course: courseHash()
    }));

}

function updateCourseURL(page, course) {
    if (courseHash() !== course) {
        history.pushState({ page: page, course: course }, page, '#' + course);
    }
}

$(window).bind('popstate', function (e, o) {
    if (history.state && history.state.course) {
        loadCourse(history.state.course);
    }
});

function loadCourse(course) {
    var found = false;
    var m = course.match(/^([0-9]{4})-(winter|spring|summer|autumn)-([^-]+)-([0-9]{3})-([a-z]+)$/i);
    if (m && window.term.year === m[1] && window.term.quarter === m[2]) {
        var label = m[3] + ' ' + m[4] + ' ' + m[5];
        var return_val = false;
        $('select#my_courses option').each(function () {
            var $option = $(this);
            if (label === $option.text()) {
                $option.prop('selected', true);
                displaySelectedCourse();
                found = true;
                return false;
            }
        });
    }

    return found;
}

//Display data about the currently selected course - called whenever selection changes
function showCurrentCourseData(index) {
    var current = $("#current-course-data").html();
    var currentTemplate = Handlebars.compile(current);

    section = window.section_data[index];

    $("#current-course-target").html(currentTemplate({
        current_median: section.current_median,
        current_num_registered: section.current_enrollment,
        current_capacity:section.limit_estimate_enrollment,
        current_repeat_students:section.current_repeating,
        concurrent_courses:section.concurrent_courses,
        current_majors:section.current_student_majors,
        curriculum:section.curriculum,
        course_number:section.course_number,
        section_id:section.section_id,
        quarter: window.term.quarter,
        year: window.term.year,
        canvas_course_url:section.canvas_course_url,
        display_course: section.display_course
    }));

    $('.course-title span').html(window.section_data[index].course_title);

    updateCourseURL(section.curriculum + '-' + section.course_number + '-' + section.section_id,
              window.term.year + '-' + window.term.quarter + '-' + section.curriculum + '-' +
              section.course_number + '-' + section.section_id);

    setup_exposures($("#current-course-target"));
}

function fetchCurrentCourseData(index) {
    startLoadingCourseData();
    $.ajax({
        url: "/api/v1/course/" + window.section_data[index].section_label,
        dataType: "JSON",
        type: "GET",
        accepts: {html: "text/html"},
        success: function(results) {
            window.section_data[index] = results;
            window.section_data[index].loaded = true;
            showCurrentCourseData(index);
        },
        error: function(xhr, status, error) {
            console.log('ERROR (' + status + '): ' + error);
        },
        complete: function () {
            stopLoadingCourseData();
        }
    });
}

function startLoadingCourseData() {
    $(".section-container.current-section").addClass('loading');
}

function stopLoadingCourseData() {
    $(".section-container.current-section").removeClass('loading');
}

function fetchHistoricCourseData(index) {
    startLoadingHistoricCourseData();
    $.ajax({
        url: "/api/v1/course/past/" + window.section_data[index].section_label,
        dataType: "JSON",
        type: "GET",
        accepts: {html: "text/html"},
        success: function(results) {
            window.section_historic_data[index] = results.past_offerings;
            window.section_historic_data[index].loaded = true;
            showHistoricDataSelectors(index, ALL_QUARTERS, ALL_YEARS);
            showHistoricCourseData(index, ALL_QUARTERS, ALL_YEARS);

            setPillListeners();

        },
        error: function(xhr, status, error) {
            console.log('ERROR (' + status + '): ' + error);
        },
        complete: function () {
            stopLoadingHistoricCourseData();
        }
    });
}

function setPillListeners(){
    $("#myTab").on("click", ".all-courses", myCoursesToggle);
    $("#myTab").on("click", ".my-courses", myCoursesToggle);
}

function myCoursesToggle(e){
    var is_my_courses = $(e.currentTarget).hasClass("my-courses");

    if(only_my_courses !== is_my_courses){
        only_my_courses = is_my_courses;
        updateHistoricDisplay();
    }
}

function startLoadingHistoricCourseData() {
    $(".section-container.historic-section").addClass('loading');
}

function stopLoadingHistoricCourseData() {
    $(".section-container.historic-section").removeClass('loading');
}

//Populate the historic data selectors for the currently selected course
function showHistoricDataSelectors(index, quarter, year, taught=ALL_MY_COURSES) {
    //Fix case of past quarters and create arrays without duplicate quarters/years
    var valid_quarters = [];
    var valid_years = [];
    var combined = [];//stores quarter + year so that when a quarter is selected, can only select years where the course was offered in that quarter & vice versa
    $.each(window.section_historic_data[index], function () {
        past_offering = this;
        past_offering.quarter = firstLetterUppercase(past_offering.quarter);
        if (combined.indexOf(past_offering.quarter + past_offering.year) == -1)
            combined.push(past_offering.quarter + past_offering.year);
        if (valid_quarters.indexOf(past_offering.quarter) == -1)
            valid_quarters.push(past_offering.quarter);
        if (valid_years.indexOf(past_offering.year) == -1)
            valid_years.push(past_offering.year);
    });

    //Remove any invalid combinations of quarter and year based on current selection
    if (quarter !== ALL_QUARTERS) {
        var remove_years = [];
        for (var y in valid_years)
            if (combined.indexOf(quarter + valid_years[y]) == -1)
                remove_years.push(valid_years[y]);
        while (remove_years.length > 0) {
            valid_years.splice(valid_years.indexOf(remove_years[0]),1);
            remove_years.splice(0,1);
        }
    }
    if (year !== ALL_YEARS) {
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
    var sections = window.section_historic_data[index];

    var instructed_sections = getInstructedSections(sections);

    for (var i = 0; i < instructed_sections.length; i++){
        if(offeringMatchesQuarter(instructed_sections[i], taught)){
            instructed_sections[i]['selected'] = "selected";
        } else {
            instructed_sections[i]['selected'] = "";
        }
    }

    $("#historic-selector-target").html(selectorsTemplate({
        past_quarters:prepOptions(quarter, valid_quarters, ALL_QUARTERS),
        past_years:prepOptions(year, valid_years, ALL_YEARS),
        student_total:calculateTotalStudents(sections),
        year_count:calculatePastYearCount(sections),
        index: index,
        curriculum:window.section_data[index].curriculum,
        course_number:window.section_data[index].course_number,
        section_id:window.section_data[index].section_id,
        total_students: calculateTotalStudents(sections),
        section_count: calculateSectionCount(sections),
        instructed_sections: instructed_sections,
        only_my_courses: only_my_courses,
        all_my_courses: taught == ALL_MY_COURSES ? "selected" : ""
    }));

    //Historic data selection
    $(".historic-filter").change(function() {
        updateHistoricDisplay()
    });
    setPillListeners();
}

function updateHistoricDisplay(){
    var index = $("select[name='my_courses'] option:selected").index();

    var taught = ALL_MY_COURSES;
    var newQuarter = ALL_QUARTERS;
    var newYear = ALL_YEARS;

    if(only_my_courses){
        taught = $("select[name='historic_filter_taught'] option:selected").val();
        taught = taught.replace(' ', '-');
    } else {
        newQuarter = $("select[name='historic_filter_quarter'] option:selected").val();
        newYear = $("select[name='historic_filter_year'] option:selected").val();
    }


    if(newYear === undefined){
        newYear = ALL_YEARS;
    }

    if(newYear !== ALL_YEARS) {
        newYear = parseInt(newYear)
    }

    showHistoricDataSelectors(index, newQuarter, newYear, taught);
    showHistoricCourseData(index, newQuarter, newYear, taught);
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
function showHistoricCourseData(index, quarter, year, taught=ALL_MY_COURSES) {
    var past_offerings = window.section_historic_data[index];
    var offerings = filterOfferings(past_offerings, quarter, year, only_my_courses);

    for (var i = 0; i < offerings.length; i++) {
        offerings[i].quarter = firstLetterUppercase(offerings[i].quarter);
    }

    var historic = $("#historic-course-data").html();
    var historicTemplate = Handlebars.compile(historic);

    if(taught !== ALL_MY_COURSES){
        var section = undefined;

        for(var i = 0; i < offerings.length; i++){
            if(offeringMatchesQuarter(offerings[i], taught)){
                section = offerings[i];
            }
        }

        if(section !== undefined) {
            offerings = [section];
        }
    }

    var section_count = calculateSectionCount(offerings, quarter, year);

    $("#historic-course-target").html(historicTemplate({
        common_majors:calculateCommon(offerings, "majors","major"),
        latest_majors:calculateCommon(offerings, "latest_majors","major"),
        common_courses:calculateCommon(offerings, "concurrent_courses","course"),
        selected_quarter:quarter,
        selected_year:year,
        median_course_grade: calculateCourseMedian(offerings),
        failed_percent: calculateFailedPercentage(offerings),
        total_students: calculateTotalStudents(offerings),
        section_count: section_count,
        instructors: getInstructors(offerings),
        display_course: shouldDisplayCourse(offerings)
        //past_terms:window.section_data[index].past_offerings
    }));

    setup_exposures($("#historic-course-target"));
}

function setup_exposures($container) {
    $container.find(".toggle-show").each(function () {
        var $hidden = $(this).closest('.list').find('ol.list-unstyled li');

        if ($hidden.length <= 10) {
            $(this).parent().hide();
        } else {
            $hidden.slice(10, $hidden.length).hide();
        }

    });

    $container.find(".toggle-show").on('click', function () {
        var expanded = $(this).attr("expanded");

        if (expanded === "true") {
            $(this).html("Show more...");
            $(this).attr("expanded", false);

            var $hidden = $(this).closest('.list').find('ol.list-unstyled li:visible');
            $hidden.slice(10, 20).hide();

            return false;
        } else{
            var $hidden = $(this).closest('.list').find('ol.list-unstyled li:hidden');
            // show next ten
            $hidden.slice(0, 10).show();

            $(this).html("Show less...");
            $(this).attr("expanded", true);

            return false;
        }
    });
}

function filterOfferings(sections, quarter, year, only_my_courses){
    var filtered_sections = [];

    for(var i = 0; i < sections.length; i++){
        if (quarterIsInRange(sections[i], quarter, year)){
            if(!only_my_courses || only_my_courses && isInstructor(sections[i])){
                filtered_sections.push(sections[i]);
            }
        }
    }

    return filtered_sections;
}

function getInstructors(sections) {
    var instructors = [];
    for (var o = 0; o < sections.length; o++) {
        for (var i in sections[o].instructors) {
            instructors.push({
                quarter: sections[o].quarter,
                year: sections[o].year,
                display_name: sections[o].instructors[i].display_name,
                uw_email: sections[o].instructors[i].uwnetid + "@uw.edu"
            });
        }
    }
    return instructors;
}


function calculateTotalStudents(sections) {
    var total_students = 0;
    for (var o = 0; o < sections.length; o++) {
        total_students += sections[o].enrollment;
    }

    return total_students;
}

function calculateSectionCount(sections) {
    return sections.length;
}

function calculatePastYearCount(sections) {
    var start_year = window.term.year;
    for (var o = 0; o < sections.length; o++) {
        if (sections[o].year < start_year) { start_year = sections[o].year; }
    }

    return window.term.year - start_year;
}


function calculateCourseMedian(sections) {
    var grades = [];
    for (var o = 0; o < sections.length; o++) {
        grades = grades.concat(sections[o].course_grades);
    }

    return (grades.length) ? (Math.round(math.median(grades) * 100) / 100).toFixed(2) : 'None';
}


function calculateFailedPercentage(sections) {
    var n = 0;
    var failed = 0;
    for (var o = 0; o < sections.length; o++) {
        var grades = sections[o].course_grades;
        for (var g = 0; g < grades.length; g++) {
            n += 1;
            if (grades[g] <= 0.7) {
                failed += 1;
            }
        }
    }

    return (n > 0) ? Math.round((failed * 100)/ n) : 0;
}


//Calculates all of the common major/course lists based on historic selections
function calculateCommon(sections, list_type, name_type) {
    var obj = {};
    var total_students = 0;

    for (var o = 0; o < sections.length; o++) {
        var term_obj = sections[o][list_type];
        total_students += sections[o].enrollment;

        for (var m = 0; m < term_obj.length; m++) {

            if (obj.hasOwnProperty(term_obj[m][name_type])) {
                obj[term_obj[m][name_type]] += term_obj[m].number_students;
            } else {
                obj[term_obj[m][name_type]] = term_obj[m].number_students;
            }
        }
    }
    
    return sortObj(obj, total_students, name_type);
}

//check if past offering was in the range selected in the dropdowns
function quarterIsInRange(past_offering, quarter, year) {
    if(year === ALL_YEARS && quarter === ALL_QUARTERS)
        return true;

    if(year === ALL_YEARS)
        return quarter === past_offering.quarter;

    if(quarter === ALL_QUARTERS)
        return year === past_offering.year;

    return (past_offering.year === year && quarter === past_offering.quarter)
}

function getInstructedSections(past_offerings){
    var instructed = [];

    for(var i = 0; i < past_offerings.length; i++){
        if(isInstructor(past_offerings[i])){
            instructed.push(past_offerings[i]);
        }
    }

    return instructed;
}

function isInstructor(past_offering){
    for(var i = 0; i < past_offering.instructors.length; i++){
        if (past_offering.instructors[i].uwnetid === window.user.netid){
            return true;
        }
    }
    return false;
}

function offeringMatchesQuarter(offering, taught){
    return taught === offering.quarter + "-" + offering.year;
}

function shouldDisplayCourse(offerings){
    if(offerings.length > 1 || offerings.length === 0) {
        return true;
    } else{
        return isInstructor(offerings[0]);
    }
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
