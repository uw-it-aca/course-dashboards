//
//  course_data.js - functions to fetch historic course data
//



function setSectionDataByLabel(label, section){
    $.each(window.section_data, function (i) {
        if (this.section_label == label) {
            window.section_data[i] = section;
            return false;
        }
    });
}

function fetchCourseData(label) {
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
}

function startLoadingCourseData() {
    $(".section-container.current-section").addClass('loading');
}

function stopLoadingCourseData() {
    $(".section-container.current-section").removeClass('loading');
}
