//
//  historic.js - functions to display historic course data
//

// Constant variables
var ALL_QUARTERS = "All Quarters";
var ALL_YEARS = "All Years";
var ALL_MY_COURSES = "All My Courses";


//Display data about the past offerings of selected course - called whenever selection changes
function showHistoricCourseData(section_data, data) {

    // paint historic course selector
    var selectors = $("#historic-data-selectors").html();
    var selectorsTemplate = Handlebars.compile(selectors);

    historic_years = [{year: ALL_YEARS, selected: (data.filter.year) ? 'selected' : '' }];
    historic_quarters = [{quarter: ALL_QUARTERS, selected: (data.filter.quarter === '') ? 'selected' : ''}];
    instructed_sections = [ALL_MY_COURSES];
    $.each(data.sections, function (year, quarters) {
        if (historic_years.indexOf(year) < 0) {
            historic_years.push({
                year: year,
                selected: (data.filter.year === year) ? 'selected' : ''
            });
        }

        $.each(quarters, function (quarter, instructors) {
            if (historic_quarters.indexOf(quarter) < 0) {
                historic_quarters.push({
                    quarter: quarter,
                    selected: (data.filter.quarter === quarter) ? 'selected' : ''
                });
            }

            if (instructors.indexOf(window.user.netid) >= 0) {
                instructed_sections.push({
                    'year': s.year,
                    'quarter': s.quarter,
                    'selected': (data.filter.only_instructed) ? 'selected' : ''
                });
            }
        });
    });

    $("#historic-selector-target").html(selectorsTemplate({
        past_quarters: historic_quarters,
        past_years: historic_years,
        curriculum: section_data.curriculum,
        course_number: section_data.course_number,
        section_id: section_data.section_id,
        instructed_sections: instructed_sections,
        only_my_courses: data.filter.only_instructed
    }));

    // paint past offerings info
    if (data.past_offerings.terms.length > 0) {
        var historicPanel = $("#historic-course-panel").html(),
            historicPanelTemplate = Handlebars.compile(historicPanel);

        historic = $("#historic-course-data").html();
        historicTemplate = Handlebars.compile(historic);

        $("#historic-course-target").html(historicTemplate({
            common_majors: calculateCommon(data.past_offerings, "majors", "major"),
            latest_majors: data.past_offerings.latest_majors.slice(0, 20),
            common_courses: calculateCommon(data.past_offerings, "concurrent_courses", "course"),
            selected_quarter: data.filter.quarter,
            selected_year: data.filter.year,
            instructors: getInstructorsByTerm(data.past_offerings.terms, data.sections),
            display_course: shouldDisplayCourse(data)
            //past_terms:window.section_data[index].past_offerings
        }));

        $("#historic-course-panel-target").html(historicPanelTemplate({
            median_gpa: calculateMedianGPA(data.past_offerings.gpas),
            median_course_grade: calculateCourseMedian(data.past_offerings.course_grades),
            failed_percent: calculateFailedPercentage(data.past_offerings.course_grades),
            total_students: data.past_offerings.enrollment,
            section_count: data.past_offerings.terms.length,
            gpa_distribution_time: 'historic'
        }));

        setup_exposures($("#historic-course-target"));

        $('#historic-course-target [data-toggle="popover"]').popover();
        $('#historic-course-target .popover-dismiss').popover({ trigger: 'focus'});
        $('#historic-course-target .cumulative-popover')
            .on('inserted.bs.popover', function () {
                renderGPADisribution('historic-gpa-distribution',
                                     data.past_offerings.gpas)
            });

        $('#historic-course-target .course-gpa-popover')
            .on('inserted.bs.popover', function () {
                renderGPADisribution('historic-course-gpa-distribution',
                                     data.past_offerings.course_grades);
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

//Calculates all of the common major/course lists based on historic selections
function calculateCommon(past_offerings, list_type, name_type) {
    var obj = {},
        original_objects = {};

    var term_obj = past_offerings[list_type];

    for (var m = 0; m < term_obj.length; m++) {
        if (obj.hasOwnProperty(term_obj[m][name_type])) {
            obj[term_obj[m][name_type]] += term_obj[m].number_students;
        } else {
            obj[term_obj[m][name_type]] = term_obj[m].number_students;
            original_objects[term_obj[m][name_type]] = term_obj[m];
        }
    }

    var result = sortObj(obj, past_offerings.enrollment, name_type);

    if (name_type === "course"){
        for(var i = 0; i < result.length; i++){
            result[i].title = original_objects[result[i].course].title;
        }
    }

    return result;
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

function getInstructorsByTerm(term_list, sections) {
    var terms = {};

    $.each(term_list, function () {
        var term_name = this,
            parts = this.split('-'),
            year = parts[0],
            quarter = parts[1],
            term_key = year + ' ' + quarter;
           //term = section.year + ' ' + section.quarter;

        if (sections.hasOwnProperty(year) && sections[year].hasOwnProperty(quarter)) {
            terms[term_key] = {
                instructors: []
            };

            $.each(sections[year][quarter], function (i, instructor) {
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

                terms[term_key].instructors.push(instructor);
            });
        }
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

function shouldDisplayCourse(data){
    var term_count = data.past_offerings.terms.length

    if(term_count > 1) {
        return true;
    } else if(term_count === 1){
        return isInstructor(data);
    }

    return false;
}

//sort array of objects by number_students value
function reverseSortByNumStudents(arr) {
    arr.sort(function(a, b) {
        return a.number_students - b.number_students;
    });
    return arr.reverse();
}

function isInstructor(data){
    for (var i = 0; i < data.past_offerings.terms.length; i++) {
        t = data.past_offerings.terms[i].split('-');

        if (data.sections.hasOwnProperty(t[0])) {
            if (data.sections[t[0]].hasOwnProperty(t[1])) {
                for (var j = 0; j < data.sections[t[0]][t[1]].length; j++) {
                    if (data.sections[t[0]][t[1]][j].uwnetid === window.user.netid) {
                        return true;
                    }
                }
            }
        }
    }

    return false;
}
