//
//  course_data.js - functions to fetch historic course data
//



var setSectionDataByLabel = function (label, section) {
    var is_loaded = false;

    $.each(window.section_data, function (i) {
        if (this.section_label == label) {
            window.section_data[i] = section;
            is_loaded = true;
            return false;
        }
    });

    if (!is_loaded) {
        section.section_label = section_label;
        window.section_data.push(section);
    }
};

var fetchCourseData = function (label) {
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

            var totalTime = Date.now() - startTime;

            gtag('event', 'course_data', {
                'eventLabel': label,
                'value': totalTime
            });

            $('div.current-section').trigger(
                'coda:CurrentCourseDataSuccess', [label]);
        },
        error: function(xhr, status, error) {
            console.log('ERROR (' + status + '): ' + error);
        },
        complete: function () {
            stopLoadingCourseData();
        }
    });
};

var startLoadingCourseData = function () {
    $(".section-container.current-section").addClass('loading');
};

var stopLoadingCourseData = function () {
    $(".section-container.current-section").removeClass('loading');
};

var fetchCourseProfileData = function (label) {
    var startTime = Date.now();

    $.ajax({
        url: "/api/v1/course/" + label + '/profile',
        dataType: "JSON",
        type: "GET",
        accepts: {html: "text/html"},
        success: function(results) {
            var totalTime = Date.now() - startTime;

            gtag('event', 'course_profile_data', {
                'eventLabel': label,
                'value': totalTime
            });

            $('div.current-section').trigger(
                'coda:CurrentCourseProfileDataSuccess', [results]);
        },
        error: function(xhr, status, error) {
            console.log('ERROR (' + status + '): ' + error);
        }
    });
};
