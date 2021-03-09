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

    if ($(".course-select").length === 0) {
        return;
    }

    displayCourseSelector(courseHash());

    if (courseHash()) {
        if (!displayCourse(courseHash())) {
            displayErrorPage();
        }
    } else {
        var section = firstCourseRecentQuarter();

        $('#my_courses').val(section.curriculum + '-' + section.course_number + '-' + section.section_id);
        displayCourse(section.section_label);
    }

    // Listen for course dropdown selection change
    $("#my_courses").change(function() {
        $('#course_quarters').html('');
        displaySelectedCourse();
    });

    // Listen for term dropdown selection change
    $("#current-course-target").on('change', 'select[name="course_quarters"]', function(e) {
        displaySelectedCourse();
    });
});


function displayPageHeader() {
    //Display the top bar: netid and course dropdown
    var source = $("#page-top").html();
    var template = Handlebars.compile(source);
    $("#top_banner").html(template({ netid: window.user.netid }));
}

function courseHash() {
    return decodeURIComponent(window.location.hash.slice(1));
}

function displayCourseSelector(label) {
    var section_data = getSectionDataByLabel(label),
        courses = [],
        term_index = -1,
        course_curriculum,
        course_number,
        course_id,
        seen = [];

    $.each(window.section_data, function () {
        var section = this;

        if (course_curriculum != section.curriculum &&
            course_number != section.course_number) {

            course_id = section.curriculum + '-' + section.course_number + '-' + section.section_id;
            if (!seen.includes(course_id)) {
                courses.push({
                    curriculum: section.curriculum,
                    course_number: section.course_number,
                    section_id: section.section_id,
                    title: section.course_title,
                    selected: (section_data &&
                               section_data.curriculum.toLowerCase() == section.curriculum.toLowerCase() &&
                               section_data.course_number == section.course_number)
                });

                seen.push(course_id);
            }
        }
    });

    source = $("#course-select").html();
    template = Handlebars.compile(source);
    $(".course-select").html(template({
        courses: courses
    }));
}

function displaySelectedCourse() {
    displayCourse(getSelectedCourseLabel());
}

function displayCourse(label) {
    var section_data = getSectionDataByLabel(label);

    if (!section_data) {
        return false;
    }

    if (section_data && section_data.loaded) {
        showCourseData(label);
    } else {
        fetchCourseData(label, function () {
            showCourseData(label);
        });
    }

    if (window.section_historic_data[label].loaded){
        showHistoricDataSelectors(section_data, ALL_QUARTERS, ALL_YEARS);
        showHistoricCourseData(section_data, ALL_QUARTERS, ALL_YEARS);
    } else {
        fetchHistoricCourseData(section_data, function () {
            showHistoricDataSelectors(section_data, ALL_QUARTERS, ALL_YEARS);
            showHistoricCourseData(section_data, ALL_QUARTERS, ALL_YEARS);
        });
    }

    return true;
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
        displayCourse(history.state.course);
    }
});

//Display data about the currently selected course - called whenever selection changes
function showCourseData(label) {
    var current = $("#current-course-data").html(),
        currentTemplate = Handlebars.compile(current),
        section = getSectionDataByLabel(label),
        terms = [];

    $.each(window.section_data, function () {
        if (this.curriculum == section.curriculum &&
            this.course_number == section.course_number &&
            this.section_id == section.section_id) {
            terms.push({
                year: this.year,
                quarter: firstLetterUppercase(this.quarter),
                current: (this.year == window.term.year &&
                          this.quarter.toLowerCase() == window.term.quarter.toLowerCase()),
                selected: (this.year == section.year &&
                           this.quarter.toLowerCase() == section.quarter.toLowerCase())
            });
        }
    });

    $("#current-course-target").html(currentTemplate({
        concurrent_courses:section.concurrent_courses,
        current_majors:section.current_student_majors,
        curriculum:section.curriculum,
        course_number:section.course_number,
        section_id:section.section_id,
        terms: terms,
        canvas_course_url:section.canvas_course_url,
        display_course: section.display_course
    }));

    if (compare_terms(section.year, section.quarter.toLowerCase(),
                      window.term.year, window.term.quarter.toLowerCase()) >= 0) {
        var currentPanel = $("#current-course-panel").html(),
            currentPanelTemplate = Handlebars.compile(currentPanel);

        $("#current-data-panel").html(currentPanelTemplate({
            current_median: section.current_median,
            current_num_registered: section.current_enrollment,
            current_capacity:section.limit_estimate_enrollment,
            current_repeat_students:section.current_repeating
        }));
    } else {
        var historicPanel = $("#historic-course-panel").html(),
            historicPanelTemplate = Handlebars.compile(historicPanel);

        $("#current-data-panel").html(historicPanelTemplate({
            median_gpa: section.current_median,
            median_course_grade: section.median_course_grade,
            failed_percent: calculateFailedPercentage([section]),
            total_students: section.course_grades.length,
            section_count: 1
        }));
    }

    $('.course-title span').html(section.course_title);

    updateCourseURL(section.curriculum + '-' + section.course_number + '-' + section.section_id,
              section.year + '-' + section.quarter + '-' + section.curriculum + '-' +
              section.course_number + '-' + section.section_id);

    // update term labels
    $('span.displayed-quarter').html(firstLetterUppercase(section.quarter) + " " + section.year);

    setup_exposures($("#current-course-target"));
    $('.current-section .popover-dismiss').popover({ trigger: 'focus'});

    $('.current-section [data-toggle="popover"]').popover();
    $('.current-section .cumulative-popover')
        .on('inserted.bs.popover', function () {
            renderGPADisribution('current-gpa-distribution', section.gpas);
        });
}

function fetchCourseData(label, on_success) {
    startLoadingCourseData();

    var startTime = Date.now();

    $.ajax({
        url: "/api/v1/course/" + label,
        dataType: "JSON",
        type: "GET",
        accepts: {html: "text/html"},
        success: function(results) {
            results.loaded = true;
            setSectionDataByLabel(label, results);

            if (on_success) {
                on_success.call();
            }

            var totalTime = Date.now() - startTime;

            gtag('event', 'course_data', {
                'eventLabel': label,
                'value': totalTime
            });
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

function fetchHistoricCourseData(section_data, on_success) {
    startLoadingHistoricCourseData();
    var startTime = Date.now();

    $.ajax({
        url: "/api/v1/course/" + section_data.section_label + '/past',
        dataType: "JSON",
        type: "GET",
        accepts: {html: "text/html"},
        success: function(results) {
            window.section_historic_data[section_data.section_label] = results.past_offerings;
            window.section_historic_data[section_data.section_label].loaded = true;
            var totalTime = Date.now() - startTime;

            gtag('event', 'historic_course_data', {
                'eventLabel': section_data.section_label,
                'value': totalTime
            });

            if (on_success) {
                on_success.call();
            }

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
function showHistoricDataSelectors(section_data, quarter, year, taught=ALL_MY_COURSES) {
    //Fix case of past quarters and create arrays without duplicate quarters/years
    var valid_quarters = [];
    var valid_years = [];
    var combined = [];//stores quarter + year so that when a quarter is selected, can only select years where the course was offered in that quarter & vice versa
    var section_label = section_data.section_label;

    $.each(window.section_historic_data[section_label], function () {
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
    var sections = window.section_historic_data[section_label];

    var instructed_sections = getInstructedSections(sections);

    for (var i = 0; i < instructed_sections.length; i++){
        if(offeringMatchesQuarter(instructed_sections[i], taught)){
            instructed_sections[i].selected = "selected";
        } else {
            instructed_sections[i].selected = "";
        }
    }

    $("#historic-selector-target").html(selectorsTemplate({
        past_quarters:prepOptions(quarter, valid_quarters, ALL_QUARTERS),
        past_years:prepOptions(year, valid_years, ALL_YEARS),
        student_total:calculateTotalStudents(sections),
        year_count:calculatePastYearCount(sections),
        section_label: section_data.section_label,
        curriculum: section_data.curriculum,
        course_number: section_data.course_number,
        section_id: section_data.section_id,
        total_students: calculateTotalStudents(sections),
        section_count: calculateSectionCount(sections),
        instructed_sections: instructed_sections,
        only_my_courses: only_my_courses,
        all_my_courses: taught == ALL_MY_COURSES ? "selected" : ""
    }));

    //Historic data selection
    $(".historic-filter").change(function() {
        updateHistoricDisplay();
    });
    setPillListeners();
}

function getSelectedCourseLabel() {
    var $selected_course = $("select[name='my_courses'] option:selected"),
        $selected_term = $("select[name='course_quarters'] option:selected"),
        curriculum = $selected_course.attr('data-curriculum'),
        course_number = $selected_course.attr('data-course-number'),
        section_id = $selected_course.attr('data-section-id'),
        year,
        quarter,
        label = '';

    if ($selected_term.length) {
        year = $selected_term.attr('data-year');
        quarter = $selected_term.attr('data-quarter');
        $.each(window.section_data, function () {
            if (this.curriculum == curriculum &&
                this.course_number == course_number &&
                this.section_id == section_id &&
                this.year.toString() == $selected_term.attr('data-year') &&
                this.quarter.toLowerCase() == quarter.toLowerCase()) {
                label = this.section_label;
                return false;
            }
        });
    } else {
        $.each(window.section_data, function () {
            if (this.curriculum == curriculum &&
                this.course_number == course_number &&
                this.section_id == section_id) {
                label = this.section_label;
            }

            if (this.curriculum == curriculum &&
                this.course_number == course_number &&
                this.section_id == section_id &&
                this.year == window.term.year &&
                this.quarter.toLowerCase() == window.term.quarter.toLowerCase()) {
                label = this.section_label;
                return false;
            }
        });
    }


    return label;
}


function firstCourseRecentQuarter() {
    var first_recent_section_data = null;

    $.each(window.section_data, function () {
        if (!first_recent_section_data) {
            first_recent_section_data = this;
        } else if (compare_terms(this.year, this.quarter,
                                 first_recent_section_data.year,
                                 first_recent_section_data.quarter) > 0 &&
                   compare_terms(first_recent_section_data.year,
                                 first_recent_section_data.quarter,
                                 window.term.year, window.term.quarter) <= 0) {
            first_recent_section_data = this;
        }
    });

    return first_recent_section_data;
}

function getSectionDataByLabel(label) {
    var section_data = null;

    $.each(window.section_data, function () {
        if (this.section_label == label) {
            section_data = this;
            return false;
        }
    });

    return section_data;
}

function setSectionDataByLabel(label, section){
    $.each(window.section_data, function (i) {
        if (this.section_label == label) {
            window.section_data[i] = section;
            return false;
        }
    });
}

function updateHistoricDisplay(){
    var section_data = getSectionDataByLabel(getSelectedCourseLabel());
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
        newYear = parseInt(newYear);
    }

    showHistoricDataSelectors(section_data, newQuarter, newYear, taught);
    showHistoricCourseData(section_data, newQuarter, newYear, taught);
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
function showHistoricCourseData(section_data, quarter, year, taught=ALL_MY_COURSES) {
    var past_offerings = window.section_historic_data[section_data.section_label],
        offerings = filterOfferings(past_offerings, quarter, year, only_my_courses),
        historic,
        historicTemplate;

    $.each(offerings, function () {
        var offering = this;

        offering.quarter = firstLetterUppercase(offering.quarter);
    });

    if(taught !== ALL_MY_COURSES){
        var section;

        $.each(offerings, function () {
            var offering = this;

            if(offeringMatchesQuarter(offering, taught)){
                section = offering;
            }
        });

        if(section !== undefined) {
            offerings = [section];
        }
    }

    var section_count = calculateSectionCount(offerings, quarter, year);
    var latest_majors = calculateCommon(offerings, "latest_majors","major");
    latest_majors = latest_majors.slice(0, 20);

    if (offerings.length) {
        var historicPanel = $("#historic-course-panel").html(),
            historicPanelTemplate = Handlebars.compile(historicPanel);

        historic = $("#historic-course-data").html();
        historicTemplate = Handlebars.compile(historic);

        $("#historic-course-target").html(historicTemplate({
            common_majors:calculateCommon(offerings, "majors","major"),
            latest_majors: latest_majors,
            common_courses:calculateCommon(offerings, "concurrent_courses","course"),
            selected_quarter:quarter,
            selected_year:year,
            instructors: getInstructorsByTerm(offerings),
            display_course: shouldDisplayCourse(offerings)
            //past_terms:window.section_data[index].past_offerings
        }));

        $("#historic-course-panel-target").html(historicPanelTemplate({
            median_gpa: calculateMedianGPA(offerings),
            median_course_grade: calculateCourseMedian(offerings),
            failed_percent: calculateFailedPercentage(offerings),
            total_students: calculateTotalStudents(offerings),
            section_count: section_count
        }));

        setup_exposures($("#historic-course-target"));

        $('#historic-course-target [data-toggle="popover"]').popover();
        $('#historic-course-target .popover-dismiss').popover({ trigger: 'focus'});
        $('#historic-course-target .cumulative-popover')
            .on('inserted.bs.popover', function () {
                renderGPADisribution('historic-gpa-distribution',
                                     gatherMedianGPAs(offerings));
            });

        $('#historic-course-target .course-gpa-popover')
            .on('inserted.bs.popover', function () {
                renderGPADisribution('historic-course-gpa-distribution',
                                     gatherCourseGrades(offerings));
            });
    } else {
        historic = $("#no-historic-course-data").html();
        historicTemplate = Handlebars.compile(historic);

        $("#historic-course-target").html(historicTemplate());
    }
}

function setup_exposures($container) {
    $container.find(".toggle-show").each(function () {
        var $this = $(this),
            $list = $this.closest('.list').find('> ol.list-unstyled > li'),
            show_length = $this.attr('data-toggle-length');

        show_length = show_length ? show_length : 5;

        if ($list.length <= show_length) {
            $this.parent().hide();
        } else {
            $list.slice(show_length).hide();
        }

    });

    $container.find(".toggle-show").on('click', function () {
        var $this = $(this),
            $list = $this.closest('.list').find('> ol.list-unstyled > li'),
            expanded = $this.attr("expanded"),
            $hidden,
            show_length = $this.attr('data-toggle-length');
            show_length_max = $this.attr('data-toggle-length-max');

        show_length = show_length ? show_length : 5;

        if (expanded === "true") {
            $this.html("Show more...");
            $this.attr("expanded", false);
            $list.slice(parseInt(show_length)).hide();
            return false;
        } else{
            $this.html("Show less...");
            $this.attr("expanded", true);
            if (show_length_max) {
                $list.slice(0, parseInt(show_length_max) + 1).show();
            } else {
                $list.slice(0).show();
            }

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

function renderGPADisribution(container, gpas) {
    var gpas_dist = Array((2.5*10) + 1).fill(0),
        categories = [],
        max = 0;

    $.each(gpas, function () {
        gpas_dist[(this <= 1.5) ? 0 : Math.round((this - 1.5) * 10)]++;
    });

    $.each(gpas_dist, function (i) {
        if (this > max) {
            max = this;
        }

        categories.push((1.5 + (i * 0.1)).toFixed(1).toString());
    });

    Highcharts.chart(container, {
        title: {
            text: undefined
        },
        credits: {
            enabled: false
        },
        chart: {
            type: 'column',
            height: 120
        },
        xAxis: {
            categories: categories,
            title: {
                text: "GPA"
            }
        },
        yAxis: {
            tickInterval: 5,
            title: {
                text: 'Frequency'
            },
            xlabels: {
                enabled: false
            }
        },
        tooltip: {
            formatter: function () {
                var tip = this.y + ' with GPA of ' + this.x;

                if (this.x == 1.5) {
                    tip += ' or less';
                }

                return tip;
            }
        },
        series: [{
            name: 'GPA',
            showInLegend: false,
            data: gpas_dist
        }]
    });
}

function getInstructorsByTerm(sections) {
    var terms = {};

    $.each(sections, function () {
        var section = this,
            term = section.year + ' ' + section.quarter;

        $.each(section.instructors, function () {
            var instructor = this;

            if (!terms.hasOwnProperty(term)) {
                terms[term] = {
                    instructors: []
                };
            }

            if (instructor.preferred_surname && instructor.preferred_surname.length !== 0) {
                instructor.first_name = instructor.preferred_first_name;
                instructor.surname = instructor.preferred_surname;
            } else {
                var name = instructor.display_name.split(' ');

                if (name.length > 1) {
                    instructor.first_name = name.slice(0, -1).join(' ');
                    instructor.surname = name.slice(-1)[0];
                } else {
                    instructor.first_name = null;
                    instructor.surname = name[0];
                }
            }

            terms[term].instructors.push(instructor);
        });
    });

    return $.map(terms, function (o, key) {
        var term = key.split(' ');
        o.quarter = term[1];
        o.year = parseInt(term[0]);
        o.instructors.sort(function (a, b) {
            if (a.surname < b.surname) { return -1; }
            if (a.surname > b.surname) { return 1; }
            return 0;
        });
        return o;
    }).sort(function (a, b) {
        return compare_terms(a.year, a.quarter, b.year, b.quarter);
    });
}


function compare_terms(a_year, a_quarter, b_year, b_quarter) {
    var quarters = ['autumn', 'summer', 'spring', 'winter'],
        y = a_year - b_year;

    return (y !== 0) ? y : (quarters.indexOf(a_quarter.toLowerCase()) -
                            quarters.indexOf(b_quarter.toLowerCase()));
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

function gatherMedianGPAs(sections) {
    gpas = [];

    for(var i = 0; i < sections.length; i++){
        gpas.push.apply(gpas, sections[i].gpas);
    }

    return gpas;
}

function gatherCourseGrades(sections) {
    var grades = [];

    for (var o = 0; o < sections.length; o++) {
        grades = grades.concat(sections[o].course_grades);
    }

    return grades;
}

function calculateMedianGPA(sections){
    gpas = gatherMedianGPAs(sections);
    return gpas.length ? (Math.round(math.median(gpas) * 100) / 100).toFixed(2) : 0;
}

function calculateCourseMedian(sections) {
    grades = gatherCourseGrades(sections);
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
    var obj = {},
        total_students = 0,
        original_objects = {};

    for (var o = 0; o < sections.length; o++) {
        var term_obj = sections[o][list_type];
        total_students += sections[o].enrollment;

        for (var m = 0; m < term_obj.length; m++) {

            if (obj.hasOwnProperty(term_obj[m][name_type])) {
                obj[term_obj[m][name_type]] += term_obj[m].number_students;
            } else {
                obj[term_obj[m][name_type]] = term_obj[m].number_students;
                original_objects[term_obj[m][name_type]] = term_obj[m];
            }
        }
    }

    var result = sortObj(obj, total_students, name_type);

    if (name_type === "course"){
        for(var i = 0; i < result.length; i++){
            result[i].title = original_objects[result[i].course].title;
        }
    }

    return result;
}

//check if past offering was in the range selected in the dropdowns
function quarterIsInRange(past_offering, quarter, year) {
    if(year === ALL_YEARS && quarter === ALL_QUARTERS)
        return true;

    if(year === ALL_YEARS)
        return quarter === past_offering.quarter;

    if(quarter === ALL_QUARTERS)
        return year === past_offering.year;

    return (past_offering.year === year && quarter === past_offering.quarter);
}

function getInstructedSections(past_offerings){
    var instructed = [];

    $.each(past_offerings, function () {
        if(isInstructor(this)){
            instructed.push(this);
        }
    });

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
    if(offerings.length > 1) {
        return true;
    } else if(offerings.length === 1){
        return isInstructor(offerings[0]);
    }

    return false;
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
