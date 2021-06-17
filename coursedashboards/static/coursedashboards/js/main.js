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
        var section = firstCourseRecentQuarter();

        $('#my_courses').val(section.curriculum 
                             + '-' + section.course_number 
                             + '-' + section.section_id);
        displayCourse(section.section_label);
    }

    registerEvents();
});


function registerEvents() {
    $('div.course-info')
        .on(
            'change', '#my_courses',
            function (e) {
                displaySelectedCourse();
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
        .on(
            'coda:HistoricCourseDataSuccess',
            function (e, section_data, data) {
                showHistoricCourseData(section_data, data);
            })
        .on('click', '#myTab .all-courses', function (e) {
            var filter = filterChoices();

            fetchHistoricCourseData(
                getSectionDataByLabel(getSelectedCourseLabel()), filter);
        })
        .on('click', '#myTab .my-courses', function (e) {
            fetchHistoricCourseData(
                getSectionDataByLabel(getSelectedCourseLabel()), {only_instructed: true});
        })
        .on('change', '#allcourses .historic-filter', function (e) {
            var filter = filterChoices(
                (this.name === 'historic_filter_year') ? this.value : null,
                (this.name === 'historic_filter_quarter') ? this.value : null)

            fetchHistoricCourseData(
                getSectionDataByLabel(getSelectedCourseLabel()), filter);
        });
}


function filterChoices(year_override, quarter_override) {
    var year = year_override ? year_override : $('#allcourses #historic_filter_year option:selected').val(),
        quarter = quarter_override ? quarter_override : $('#allcourses #historic_filter_quarter option:selected').val(),
        filter = {
            'year': ((year === ALL_YEARS) ? '' : year),
            'quarter': ((quarter === ALL_QUARTERS) ? '' : quarter),
            'only_instructed': false
        };

    return filter
}

function displayPageHeader() {
    //Display the top bar: netid and course dropdown
    var source = $("#page-top").html();
    var template = Handlebars.compile(source);
    $("#top_banner").html(template({ netid: window.user.netid }));
}

function courseHash() {
    return decodeURIComponent(window.location.hash.slice(1));
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

function compare_terms(a_year, a_quarter, b_year, b_quarter) {
    var quarters = ['autumn', 'summer', 'spring', 'winter'],
        y = a_year - b_year;

    return (y !== 0) ? y : (quarters.indexOf(a_quarter.toLowerCase()) -
                            quarters.indexOf(b_quarter.toLowerCase()));
}
