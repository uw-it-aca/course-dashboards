//
//  historic_data.js - functions to fetch historic course data
//


function historicCacheData(section_data, filter, results) {
    var hash = section_data.curriculum + '-' + section_data.section_id +
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
}

function fetchHistoricCourseData(section_data, filter) {
    if (historicCacheData(section_data, filter)) {
        $('div.historic-section').trigger(
            'coda:HistoricCourseDataSuccess',
            [section_data, historicCacheData(section_data, filter)]);
    } else {
        getHistoricCourseData(section_data, filter);
    }
}

function getHistoricCourseData(section_data, filter) {
    startLoadingHistoricCourseData();
    var startTime = Date.now();

    $.ajax({
        url: "/api/v1/course/" + section_data.section_label + '/past' +
            '?past_year=' + ((filter && filter.year !== undefined) ? filter.year : '') +
            '&past_quarter=' + ((filter && filter.quarter !== undefined) ? filter.quarter : '') +
            '&instructed=' + (filter && filter.only_instructed ? 'true' : ''),
        dataType: "JSON",
        type: "GET",
        accepts: {html: "text/html"},
        success: function(results) {
            var totalTime = Date.now() - startTime;

            gtag('event', 'historic_course_data', {
                'eventLabel': section_data.section_label,
                'value': totalTime
            });

            historicCacheData(section_data, filter, results);

            $('div.historic-section').trigger(
                'coda:HistoricCourseDataSuccess', [section_data, results]);
        },
        error: function(xhr, status, error) {
            console.log('ERROR (' + status + '): ' + error);
        },
        complete: function () {
            stopLoadingHistoricCourseData();
        }
    });
}

function startLoadingHistoricCourseData() {
    $(".section-container.historic-section").addClass('loading');
}

function stopLoadingHistoricCourseData() {
    $(".section-container.historic-section").removeClass('loading');
}
