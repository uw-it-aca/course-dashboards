//
//  historic.js - functions to display historic course data
//

// Constant variables
var ALL_QUARTERS = "All Quarters";
var ALL_YEARS = "All Years";
var ALL_MY_COURSES = "All My Courses";


//Display data about the past offerings of selected course - called whenever selection changes
var showHistoricCourseData = function (section_label, data, filter) {

    // paint historic course selector
    var historic = $("#historic-course-data").html(),
        historicTemplate = Handlebars.compile(historic),
        context,
        parts;

    if (filter && filter.only_instructed) {
        // builds window.historic_instructed_terms since initial load is all instructed courses
        setupHistoricInstructedSelector(data);
    } else {
        // builds window.historic_terms since initial load is all terms
        setupHistoricTermSelector(data);
    }

    parts = section_label.split('-');
    context = {
        past_quarters: window.historic_terms.quarters,
        past_years: window.historic_terms.years,
        curriculum: parts[2],
        course_number: parts[3],
        section_id: parts[4],
        instructed_sections: window.historic_instructed_terms,
        only_my_courses: data.filter.only_instructed
    };

    $("#historic-course-target").html(historicTemplate(context));

    if (filter && filter.only_instructed) {
        var value = (data.filter.year) ? data.filter.year + '-' + data.filter.quarter : ALL_MY_COURSES;

        $('#historic-course-target #historic_filter_instructed').val(value);
    } else {
        // select filter terms and set appropriate options
        if (data.filter.year) {
            $('#historic_filter_year').val(data.filter.year);
            $.each(window.historic_terms.raw, function () {
                var $option = $('#historic_filter_quarter option[value="' + this.quarter + '"]');

                if (this.year === data.filter.year) {
                    $option.removeAttr('disabled', 'disabled');
                } else {
                    $option.attr('disabled', 'disabled');
                }
            });
        } else {
            $('#historic_filter_year').val(ALL_YEARS);
            $('#historic_filter_quarter option').removeAttr('disabled');
        }

        if (data.filter.quarter) {
            $('#historic_filter_quarter').val(data.filter.quarter);
            $.each(window.historic_terms.raw, function () {
                var $option = $('#historic_filter_year option[value="' + this.year + '"]');

                if (this.quarter === data.filter.quarter) {
                    $option.removeAttr('disabled', 'disabled');
                } else {
                    $option.attr('disabled', 'disabled');
                }
            });
        } else {
            $('#historic_filter_quarter').val(ALL_QUARTERS);
            $('#historic_filter_year').removeAttr('disabled');
        }
    }

    // paint past offerings info
    if (data.past_offerings.terms.length > 0) {
        if (!shouldDisplayCourse(data)) {
            var historicPanel = $("#no-display-historic-course-panel").html(),
                historicPanelTemplate = Handlebars.compile(historicPanel);

            $("#historic-performance-panel").html(historicPanelTemplate());
            return false;
        }

        showHistoricPreviousInstructors(section_label, data);
    } else {
        historic = $("#no-historic-course-data").html();
        historicTemplate = Handlebars.compile(historic);

        $("#historic-course-target").html(historicTemplate());
        return false;
    }

    return true;
};

var setupHistoricInstructedSelector = function (data) {
    if (!window.historic_instructed_terms) {
        window.historic_instructed_terms = [];
        $.each(data.past_offerings.terms, function () {
            window.historic_instructed_terms.push(this);
        });
    }
};

var setupHistoricTermSelector = function (data) {
    if (!window.historic_terms) {
        window.historic_terms = {
            years: [],
            quarters: [],
            raw: []
        };

        $.each(data.sections, function (year, quarters) {
            $.each(quarters, function (quarter, instructors) {
                window.historic_terms.raw.push({
                    year: year,
                    quarter: quarter
                });

                if (window.historic_terms.years.indexOf(year) < 0) {
                    window.historic_terms.years.push(year);
                }

                if (window.historic_terms.quarters.indexOf(quarter) < 0) {
                    window.historic_terms.quarters.push(quarter);
                }

                if (instructors.indexOf(window.user.netid) >= 0) {
                    instructed_sections.push({
                        'year': s.year,
                        'quarter': s.quarter
                    });
                }
            });
        });

        window.historic_terms.years.sort().reverse();
    }
};

var loadHistoricPerformanceData = function (section_label, filter) {
    var template = Handlebars.compile($('#historic-performance-template').html());

    $('#historic-performance-panel').html(template());
    getHistoricPerformanceData(section_label, filter);
};

var showHistoricPerformanceData = function (section_label, data) {
    var template = Handlebars.compile($('#historic-performance-template').html()),
        $panel = $('#historic-performance-panel');

    if ($('.historic-enrollment', $panel).length == 1) {
        $panel.html(template({
            median_gpa: calculateMedianGPA(data.performance.gpas),
            median_course_grade: calculateCourseMedian(data.performance.course_grades),
            failed_percent: calculateFailedPercentage(data.performance.course_grades),
            total_students: data.performance.enrollment,
            section_count: data.performance.offering_count,
            gpa_distribution_time: 'historic'}));

        bind_events($panel, data.performance.gpas, data.performance.course_grades);
    }
};

var loadHistoricConcurrentCourses = function (section_label, filter) {
    var template = Handlebars.compile($("#historic-concurrent-courses-template").html());

    $('#historic-concurrent-courses-panel').html(template());
    getHistoricConcurrentCourses(section_label, filter);
};

var showHistoricConcurrentCourses = function (section_label, data) {
    var template = Handlebars.compile($("#historic-concurrent-courses-template").html()),
        $panel = $('#historic-concurrent-courses-panel');

    $panel.html(template({
        common_courses: data.concurrent_courses
    }));

    bind_events($panel);

    getHistoricCourseGPAs(section_label, data.concurrent_courses);
};

var showHistoricCourseGPAs = function (section_label, data) {
    $.each(data.gpas, function () {
        var $span = $('[id="' + this.curriculum +'-' + this.course_number + '-gpa"]'),
            html = '(' + this.grade + ')';

        $span.html(html);
    });
};

var loadHistoricStudentMajors = function (section_label, filter) {
    var template = Handlebars.compile($("#historic-course-major-template").html());

    $('#historic-course-major-panel').html(template());
    getHistoricStudentMajors(section_label, filter);
};

var showHistoricStudentMajors = function (section_label, data) {
    var template = Handlebars.compile($("#historic-course-major-template").html()),
        $panel = $('#historic-course-major-panel');

    $panel.html(template({
        common_majors: data.student_majors
    }));

    bind_events($panel);
};

var loadHistoricGraduatedMajors = function (section_label, filter) {
    var template = Handlebars.compile($("#historic-grad-major-template").html());

    $('#historic-grad-major-panel').html(template());
    getHistoricGraduatedMajors(section_label, filter);
};

var showHistoricGraduatedMajors = function (section_label, data) {
    var template = Handlebars.compile($("#historic-grad-major-template").html()),
        $panel = $('#historic-grad-major-panel');

    $panel.html(template({
        latest_majors: data.graduated_majors
    }));

    bind_events($panel);
};

var showHistoricPreviousInstructors = function (section_label, data) {
    var $panel = $('#historic-previous-instructors-panel');

    $panel.html(
        Handlebars.compile($('#historic-previous-instructors-template').html())({
            instructors: getInstructorsByTerm(data.past_offerings.terms, data.sections)
        }));

    bind_events($panel);
};


var bind_events = function ($container, gpas, course_grades) {
    setup_exposures($container);

    $('[data-toggle="popover"]', $container).popover();
    $('.popover-dismiss', $container).popover({ trigger: 'focus'});
    if (gpas) {
        $('.cumulative-popover', $container)
            .on('inserted.bs.popover', function () {
                renderGPADisribution('historic-gpa-distribution', gpas);
            });
    }

    if (course_grades) {
        $('.course-gpa-popover', $container)
            .on('inserted.bs.popover', function () {
                renderGPADisribution('historic-course-gpa-distribution',
                                     course_grades);
            });
    }
};

var setup_exposures = function ($container) {
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
};

//Calculates all of the common major/course lists based on historic selections
var calculateCommon = function (past_offerings, list_type, name_type) {
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
};

//order majors/courses by number of students
var sortObj = function (arr, total_students, name_type) {
    var sorted = [];

    for (var i in arr) {
        if (name_type == "major")
            sorted.push({"major":i, "number_students":arr[i], "percent_students": ((arr[i]/total_students)*100).toFixed(2)});
        else
            sorted.push({"course":i, "number_students":arr[i], "percent_students": ((arr[i]/total_students)*100).toFixed(2)});
    }
    return reverseSortByNumStudents(sorted);
};

var getInstructorsByTerm = function (term_list, sections) {
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
};

var shouldDisplayCourse = function (data) {
    var term_count = data.past_offerings.terms.length;

    if(term_count > 1) {
        return true;
    } else if(term_count === 1){
        return isInstructor(data);
    }

    return false;
};

//sort array of objects by number_students value
var reverseSortByNumStudents = function (arr) {
    arr.sort(function(a, b) {
        return a.number_students - b.number_students;
    });
    return arr.reverse();
};

var isInstructor = function (data) {
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
};
