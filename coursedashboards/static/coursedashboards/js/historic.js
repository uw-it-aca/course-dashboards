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
            $('#historic_filter_quarter option').slice(1).attr('disabled', 'disabled');
            $.each(window.historic_terms.raw, function () {
                var $option = $('#historic_filter_quarter option[value="' + this.quarter + '"]');

                if (this.year === data.filter.year) {
                    $option.removeAttr('disabled', 'disabled');
                }
            });
        } else {
            $('#historic_filter_year').val(ALL_YEARS);
            $('#historic_filter_quarter option').removeAttr('disabled');
        }

        if (data.filter.quarter) {
            $('#historic_filter_quarter').val(data.filter.quarter);
            $('#historic_filter_year option').slice(1).attr('disabled', 'disabled');
            $.each(window.historic_terms.raw, function () {
                var $option = $('#historic_filter_year option[value="' + this.year + '"]');

                if (this.quarter === data.filter.quarter) {
                    $option.removeAttr('disabled', 'disabled');
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

        /* tabled for now
        historic = $("#historic-course-data-span").html();
        historicTemplate = Handlebars.compile(historic);

        var first = data.past_offerings.terms[data.past_offerings.terms.length - 1].split('-'),
            last = data.past_offerings.terms[0].split('-'),
            first_term = first[1].charAt(0).toUpperCase() + first[1].slice(1),
            last_term = last[1].charAt(0).toUpperCase() + last[1].slice(1);

        context = {
            first_year: first[0],
            first_term: first_term,
            first_term_short: first_term.slice(0, 3)
        };

        if (data.past_offerings.terms.length > 1) {
            context.last_year = last[0];
            context.last_term = last_term;
            context.last_term_short = last_term.slice(0, 3);
        }

        $('span.historic-span').html(historicTemplate(context));
        */

        showHistoricPreviousInstructors(section_label, data);
    } else {
        if (filter && filter.only_instructed) {
            historic = $("#no-display-historic-course-panel").html();
            historicTemplate = Handlebars.compile(historic);

            $("#historic-performance-panel").html(historicTemplate());
        } else {
            historic = $("#no-historic-course-data").html();
            historicTemplate = Handlebars.compile(historic);

            $("#historic-course-target").html(historicTemplate());
            $('span.historic-span').html('');

        }

        return false;
    }

    return true;
};

var setupHistoricInstructedSelector = function (data) {
    if (!window.historic_instructed_terms) {
        window.historic_instructed_terms = [];
        $.each(data.past_offerings.terms, function () {
            var parts = this.split('-');

            if (!currentOrLaterTerm(parts[0], parts[1])) {
                window.historic_instructed_terms.push(this);
            }
        });
    }
};

var currentOrLaterTerm = function (year, quarter) {
    return (compare_terms(year, quarter, window.term.year, window.term.quarter) >= 0);
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
                if (currentOrLaterTerm(year, quarter)) {
                    return true;
                }

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
    var cached_data = _preloadHistoricPanel(
        'historic-performance-panel', section_label, filter,
        'historic-performance-template');

    if (cached_data) {
        showHistoricPerformanceData(section_label, cached_data);
    } else {
        getHistoricPerformanceData(section_label, filter);
    }
};

var showHistoricPerformanceData = function (section_label, data) {
    var $panel = _postloadHistoricPanel(
        'historic-performance-panel',
        section_label, data.filter, data,
        'historic-performance-template',
        {
            median_gpa: calculateMedianGPA(data.performance.gpas),
            median_course_grade: calculateCourseMedian(data.performance.course_grades),
            failed_percent: calculateFailedPercentage(data.performance.course_grades),
            total_students: data.performance.enrollment,
            section_count: data.performance.offering_count,
            gpa_distribution_time: 'historic'
        });

    bind_events($panel, data.performance.gpas, data.performance.course_grades);
};

var loadHistoricConcurrentCourses = function (section_label, filter) {
    var cached_data = _preloadHistoricPanel(
        'historic-concurrent-courses-panel', section_label, filter,
        'historic-concurrent-courses-template');

    if (cached_data) {
        showHistoricConcurrentCourses(section_label, cached_data);
    } else {
        getHistoricConcurrentCourses(section_label, filter);
    }
};

var showHistoricConcurrentCourses = function (section_label, data) {
    var $panel = _postloadHistoricPanel(
        'historic-concurrent-courses-panel',
        section_label, data.filter, data,
        'historic-concurrent-courses-template',
        {
            common_courses: data.concurrent_courses
        });

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
    var cached_data = _preloadHistoricPanel(
        'historic-course-major-panel', section_label, filter,
        'historic-course-major-template');

    if (cached_data) {
        showHistoricStudentMajors(section_label, cached_data);
    } else {
        getHistoricStudentMajors(section_label, filter);
    }
};

var showHistoricStudentMajors = function (section_label, data) {
    var $panel = _postloadHistoricPanel(
        'historic-course-major-panel',
        section_label, data.filter, data,
        'historic-course-major-template',
        {
            common_majors: data.student_majors
        });

    bind_events($panel);
};

var loadHistoricGraduatedMajors = function (section_label, filter) {
    var cached_data = _preloadHistoricPanel(
        'historic-grad-major-panel', section_label, filter,
        'historic-grad-major-template');

    if (cached_data) {
        showHistoricGraduatedMajors(section_label, cached_data);
    } else {
        getHistoricGraduatedMajors(section_label, filter);
    }
};

var showHistoricGraduatedMajors = function (section_label, data) {
    var $panel = _postloadHistoricPanel(
        'historic-grad-major-panel',
        section_label, data.filter, data,
        'historic-grad-major-template',
        {
            latest_majors: data.graduated_majors
        });

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
        return compare_terms(a.year, a.quarter, b.year, b.quarter) * -1;
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

var _preloadHistoricPanel = function (panel_id, section_label, filter, template_id) {
    var template = Handlebars.compile($('#' + template_id).html()),
        panel_class_name = _getHistoricPanelClassName(panel_id, section_label, filter),
        cached_data = null;

    $('#' + panel_id).html(template()).addClass(panel_class_name);

    return window.historic_data_cache.hasOwnProperty(panel_class_name) ? window.historic_data_cache[panel_class_name] : null;
};

var _postloadHistoricPanel = function (panel_id, section_label, filter, data, template_id, context) {
    var template = Handlebars.compile($('#' + template_id).html()),
        panel_class_name = _getHistoricPanelClassName(panel_id, section_label, filter),
        $panel = $('.' + panel_class_name);

    $panel.html(template(context));

    window.historic_data_cache[panel_class_name] = data;

    return $panel;
};

var _getHistoricPanelClassName = function (panel_id, section_label, filter) {
    var mashup = panel_id + section_label + '/' +
        (((typeof filter !== 'undefined') && filter.year) ? filter.year : '') + '/' +
        (((typeof filter !== 'undefined') && filter.quarter) ? filter.quarter : '') + '/' +
        (((typeof filter !== 'undefined') && filter.only_instructed) ? filter.only_instructed : '');

    return "historic_" + Math.abs(
        mashup.split("").reduce(
            function (a, b) {
                a = ((a << 5) - a) + b.charCodeAt(0);
                return a & a;
            }, 0)
    );
};
