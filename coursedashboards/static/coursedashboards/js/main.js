//
//  main.js - data/functions to support course dashboards
//


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
        displayMyCourseAndHistory();
    }

    registerEvents();
});


var displayMyCourseAndHistory = function (course) {
    var section = firstCourseRecentQuarter(course);

    $('div.course-quarter-year #my_courses').val(section.curriculum +
                                                 '-' + section.course_number +
                                                 '-' + section.section_id);
    displayCourse(section.section_label);
};


var registerEvents = function () {
    $('div.course-quarter-year')
        .on(
            'change', '#my_courses',
            function (e) {
                displayMyCourseAndHistory(this.value);
            });

    $('div.current-section')
        .on(
            'coda:CurrentCourseDataSuccess',
            function (e, label) {
                showCourseData(label);
            })
        .on(
            'change', '#current-course-target select[name="course_quarters"]',
            function (e) {
                $('#course_quarters').html('');
                displaySelectedCourse();
            });

    $('div.historic-section')
        .on('coda:HistoricCourseDataSuccess',
            function (e, section_label, data) {
                if (showHistoricCourseData(section_label, data)) {
                    var filter = filterChoices();

                    loadHistoricPerformanceData(section_label, filter);
                    loadHistoricConcurrentCourses(section_label, filter);
                    loadHistoricConcurrentCourseGPAs(section_label, filter);
                    loadHistoricStudentMajors(section_label, filter);
                    loadHistoricGraduatedMajors(section_label, filter);
                }
            })
        .on('coda:HistoricPerformanceSuccess',
            function (e, section_label, data) {
                showHistoricPerformanceData(section_label, data);
            })
        .on('coda:HistoricConcurrentCoursesSuccess',
            function (e, section_label, data) {
                showHistoricConcurrentCourses(section_label, data);
            })
        .on('coda:HistoricConcurrentCourseGPAsSuccess',
            function (e, section_label, data) {
                showHistoricConcurrentCourseGPAs(section_label, data);
            })
        .on('coda:HistoricStudentMajorsSuccess',
            function (e, section_label, data) {
                showHistoricStudentMajors(section_label, data);
            })
        .on('coda:HistoricGraduatedMajorsSuccess',
            function (e, section_label, data) {
                showHistoricGraduatedMajors(section_label, data);
            })
        .on('click', '#myTab .all-courses', function (e) {
            var filter = filterChoices();

            fetchHistoricCourseData(getSelectedCourseLabel(), filter);
        })
        .on('click', '#myTab .my-courses', function (e) {
            fetchHistoricCourseData(getSelectedCourseLabel(), {only_instructed: true});
        })
        .on('change', '#allcourses .historic-filter', function (e) {
            var filter = filterChoices(
                (this.name === 'historic_filter_year') ? this.value : null,
                (this.name === 'historic_filter_quarter') ? this.value : null);

            fetchHistoricCourseData(getSelectedCourseLabel(), filter);
        });
};


var filterChoices = function (year_override, quarter_override) {
    var year = year_override ? year_override : $('#allcourses #historic_filter_year option:selected').val(),
        quarter = quarter_override ? quarter_override : $('#allcourses #historic_filter_quarter option:selected').val(),
        filter = {
            'year': ((year === ALL_YEARS) ? '' : year),
            'quarter': ((quarter === ALL_QUARTERS) ? '' : quarter),
            'only_instructed': false
        };

    return filter;
};

var displayPageHeader = function () {
    //Display the top bar: netid and course dropdown
    var source = $("#page-top").html();
    var template = Handlebars.compile(source);
    $("#top_banner").html(template({ netid: window.user.netid }));
};

var courseHash = function () {
    return decodeURIComponent(window.location.hash.slice(1));
};

var displayErrorPage = function () {
    var current = $("#cannot-display-course").html();
    var currentTemplate = Handlebars.compile(current);
    $('.main-content').html(currentTemplate({
        course: courseHash()
    }));
};

var updateCourseURL = function (page, course) {
    if (courseHash() !== course) {
        history.pushState({ page: page, course: course }, page, '#' + course);
    }
};

$(window).bind('popstate', function (e, o) {
    if (history.state && history.state.course) {
        displayCourse(history.state.course);
    }
});


var firstCourseRecentQuarter = function (course) {
    var first_recent_section_data = null,
        course_parts = (course) ? course.split('-') : null,
        curriculum = (course) ? course_parts[0] : null,
        course_number = (course) ? parseInt(course_parts[1]) : null,
        section_id = (course) ? course_parts[2] : null;

    $.each(window.section_data, function () {
        if (course && !(curriculum == this.curriculum &&
                        course_number == this.course_number &&
                        section_id == this.section_id)) {
            return true;
        }

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
};

var compare_terms = function (a_year, a_quarter, b_year, b_quarter) {
    var quarters = ['autumn', 'summer', 'spring', 'winter'],
        y = a_year - b_year;

    return (y !== 0) ? y : (quarters.indexOf(a_quarter.toLowerCase()) -
                            quarters.indexOf(b_quarter.toLowerCase()));
};
