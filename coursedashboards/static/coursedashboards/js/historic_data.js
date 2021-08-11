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
    if (historicCacheData(section_label, filter)) {
        $('div.historic-section').trigger(
            'coda:HistoricCourseDataSuccess',
            [section_label, historicCacheData(section_label, filter)]);
    } else {
        getHistoricCourseData(section_label, filter);
    }
};

var getHistoricCourseData = function (section_label, filter) {
    startLoadingHistoricCourseData();
    var startTime = Date.now();

    $.ajax({
        url: "/api/v1/course/" + section_label + '/past' +
            '?past_year=' + ((filter && filter.year !== undefined) ? filter.year : '') +
            '&past_quarter=' + ((filter && filter.quarter !== undefined) ? filter.quarter : '') +
            '&instructed=' + (filter && filter.only_instructed ? 'true' : ''),
        dataType: "JSON",
        type: "GET",
        accepts: {html: "text/html"},
        success: function(results) {
            var totalTime = Date.now() - startTime;

            gtag('event', 'historic_course_data', {
                'eventLabel': section_label,
                'value': totalTime
            });

            historicCacheData(section_label, filter, results);

            $('div.historic-section').trigger(
                'coda:HistoricCourseDataSuccess', [section_label, results]);
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
    var url = "/api/v1/course/" + section_label + '/past/performance' +
        '?past_year=' + ((filter && filter.year !== undefined) ? filter.year : '') +
        '&past_quarter=' + ((filter && filter.quarter !== undefined) ? filter.quarter : '') +
        '&instructed=' + (filter && filter.only_instructed ? 'true' : '');

    _getHistoricData(url, section_label, 'Performance');
};

var getHistoricConcurrentCourses = function (section_label, filter) {
    var url = "/api/v1/course/" + section_label + '/past/concurrent' +
        '?past_year=' + ((filter && filter.year !== undefined) ? filter.year : '') +
        '&past_quarter=' + ((filter && filter.quarter !== undefined) ? filter.quarter : '') +
        '&instructed=' + (filter && filter.only_instructed ? 'true' : '');

    _getHistoricData(url, section_label, 'ConcurrentCourses');
};

var getHistoricConcurrentCourseGPAs = function (section_label, filter) {
    var url = "/api/v1/course/" + section_label + '/past/gpas' +
        '?past_year=' + ((filter && filter.year !== undefined) ? filter.year : '') +
        '&past_quarter=' + ((filter && filter.quarter !== undefined) ? filter.quarter : '') +
        '&instructed=' + (filter && filter.only_instructed ? 'true' : '');

    _getHistoricData(url, section_label, 'ConcurrentCourseGPAs');
};

var getHistoricStudentMajors = function (section_label, filter) {
    var url = "/api/v1/course/" + section_label + '/past/studentmajor' +
        '?past_year=' + ((filter && filter.year !== undefined) ? filter.year : '') +
        '&past_quarter=' + ((filter && filter.quarter !== undefined) ? filter.quarter : '') +
        '&instructed=' + (filter && filter.only_instructed ? 'true' : '');

    _getHistoricData(url, section_label, 'StudentMajors');
};

var getHistoricGraduatedMajors = function (section_label, filter) {
    var url = "/api/v1/course/" + section_label + '/past/graduatedmajor' +
        '?past_year=' + ((filter && filter.year !== undefined) ? filter.year : '') +
        '&past_quarter=' + ((filter && filter.quarter !== undefined) ? filter.quarter : '') +
        '&instructed=' + (filter && filter.only_instructed ? 'true' : '');

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
