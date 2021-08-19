//
//  historic_data.js - functions to fetch historic course data
//


var historicCacheData = function (section_label, filter, results) {
    var hash = section_label +
        '-' + ((filter && filter.year !== undefined) ? filter.year : '') +
        '-' + ((filter && filter.quarter !== undefined) ? filter.quarter : '') +
        '-' + ((filter && filter.only_instructed) ? 'instructed' : '');

    if (results) {
        window.historic_data[hash] = results;
        return results;
    } else if (window.historic_data.hasOwnProperty(hash)) {
        return window.historic_data[hash];
    }

    return null;
};

var fetchHistoricCourseData = function (section_label, filter) {
    var cached = historicCacheData(section_label, filter);

    if (cached) {
        $('div.historic-section').trigger(
            'coda:HistoricCourseDataSuccess', [section_label, cached]);
    } else {
        getHistoricCourseData(section_label, filter);
    }
};

var getHistoricCourseData = function (section_label, filter) {
    startLoadingHistoricCourseData();
    var startTime = Date.now();

    $.ajax({
        url: "/api/v1/course/" + section_label + '/past?' + _url_search_terms_from_filter(filter),
        dataType: "JSON",
        type: "GET",
        accepts: {html: "text/html"},
        success: function(results) {
            var totalTime = Date.now() - startTime;

            gtag('event', 'historic_course_data', {
                'eventLabel': section_label,
                'value': totalTime
            });

            historicCacheData(section_label, filter, results, filter);

            $('div.historic-section').trigger(
                'coda:HistoricCourseDataSuccess', [section_label, results, filter]);
        },
        error: function(xhr, status, error) {
            console.log('ERROR (' + status + '): ' + error);
        },
        complete: function () {
            stopLoadingHistoricCourseData();
        }
    });
};

var getHistoricPerformanceData = function (section_label, filter) {
    var url = "/api/v1/course/" + section_label + '/past/performance?' +
        _url_search_terms_from_filter(filter);

    _getHistoricData(url, section_label, 'Performance');
};

var getHistoricConcurrentCourses = function (section_label, filter) {
    var url = "/api/v1/course/" + section_label + '/past/concurrent?' +
        _url_search_terms_from_filter(filter);

    _getHistoricData(url, section_label, 'ConcurrentCourses');
};

var getHistoricCourseGPAs = function (section_label, courses) {
    var url = "/api/v1/course/" + section_label + '/past/gpas?courses=';

    $.each(courses, function (i) {
        if (i) {
            url += ',';
        }

        url += this.curriculum + '-' + this.course_number;
    });

    _getHistoricData(url, section_label, 'CourseGPAs');
};

var getHistoricStudentMajors = function (section_label, filter) {
    var url = "/api/v1/course/" + section_label + '/past/studentmajor?' +
        _url_search_terms_from_filter(filter);

    _getHistoricData(url, section_label, 'StudentMajors');
};

var getHistoricGraduatedMajors = function (section_label, filter) {
    var url = "/api/v1/course/" + section_label + '/past/graduatedmajor?' +
        _url_search_terms_from_filter(filter);

    _getHistoricData(url, section_label, 'GraduatedMajors');
};

var _getHistoricData = function (url, section_label, metric) {
    var startTime = Date.now();

    $.ajax({
        url: url,
        dataType: "JSON",
        type: "GET",
        accepts: {html: "text/html"},
        success: function(results) {
            var totalTime = Date.now() - startTime;

            gtag('event', 'historic_studentmajor_data', {
                'eventLabel': section_label,
                'value': totalTime
            });

            $('div.historic-section').trigger(
                'coda:Historic' + metric + 'Success', [section_label, results]);
        },
        error: function(xhr, status, error) {
            console.log('ERROR (' + status + '): ' + error);
        }
    });
};

var _url_search_terms_from_filter = function (filter) {
    return ['past_year=' + ((filter && filter.year !== undefined) ? filter.year : ''),
            'past_quarter=' + ((filter && filter.quarter !== undefined) ? filter.quarter : ''),
            'instructor=' + (filter && filter.only_instructed ? window.window.user.netid : '')].join('&');
};

var startLoadingHistoricCourseData = function () {
    $(".section-container.historic-section").addClass('loading');
};

var stopLoadingHistoricCourseData = function () {
    $(".section-container.historic-section").removeClass('loading');
};

var startLoadingHistoricPerformanceData = function () {
    $(".section-container.historic-section").addClass('loading');
};

var stopLoadingHistoricPerformanceData = function () {
    $(".section-container.historic-section").removeClass('loading');
};
