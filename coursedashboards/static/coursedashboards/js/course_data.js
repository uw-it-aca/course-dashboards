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
    var startTime = Date.now(),
        section_data = getSectionDataByLabel(label);

    if (section_data && section_data.loaded) {
        $('div.current-section').trigger(
            'coda:CurrentCourseDataSuccess', [label]);
        return;
    }

    startLoadingCourseData();

    $.ajax({
        url: "/api/v1/course/" + label,
        dataType: "JSON",
        type: "GET",
        accepts: {text: "application/json"},
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

    if (getCourseProfileData(label)) {
        $('div.current-section').trigger(
            'coda:CurrentCourseProfileDataSuccess', [getCourseProfileData(label)]);
        return;
    }

    $.ajax({
        url: "/api/v1/course/" + label + '/profile',
        dataType: "JSON",
        type: "GET",
        accepts: {text: "application/json"},
        success: function(results) {
            var totalTime = Date.now() - startTime;

            gtag('event', 'course_profile_data', {
                'eventLabel': label,
                'value': totalTime
            });

            setCourseProfileData(label, results);

            $('div.current-section').trigger(
                'coda:CurrentCourseProfileDataSuccess', [results]);
        },
        error: function(xhr, status, error) {
            $('div.current-section').trigger(
                'coda:CurrentCourseProfileDataFailure', [error]);
        }
    });
};

var setCourseProfileData = function (label, profile_data) {
    window.profile_data[label] = profile_data;
};

var getCourseProfileData = function (label) {
    if (window.profile_data.hasOwnProperty(label)) {
        return window.profile_data[label];
    }

    return false;
};

var fetchCourseTextbookData = function (label) {
    var startTime = Date.now();

    if (getCourseTextbookData(label)) {
        $('div.current-section').trigger(
            'coda:CurrentCourseTextbookDataSuccess', [label, getCourseTextbookData(label)]);
        return;
    }

    $.ajax({
        url: "/api/v1/course/" + label + '/textbooks',
        dataType: "JSON",
        type: "GET",
        accepts: {text: "application/json"},
        success: function(results) {
            var totalTime = Date.now() - startTime;

            gtag('event', 'course_textbook_data', {
                'eventLabel': label,
                'value': totalTime
            });

            setCourseTextbookData(label, results);

            $('div.current-section').trigger(
                'coda:CurrentCourseTextbookDataSuccess', [label, results]);
        },
        error: function(xhr, status, error) {
            $('div.current-section').trigger(
                'coda:CurrentCourseTextbookDataFailure', [label, error]);
        }
    });
};

var setCourseTextbookData = function (label, textbook_data) {
    window.textbook_data[label] = textbook_data;
};

var getCourseTextbookData = function (label) {
    if (window.textbook_data.hasOwnProperty(label)) {
        return window.textbook_data[label];
    }

    return false;
};

var fetchCourseGenEdData = function (label) {
    var startTime = Date.now();

    if (getCourseGenEdData(label)) {
        $('div.current-section').trigger(
            'coda:CurrentCourseGenEdDataSuccess', [label, getCourseGenEdData(label)]);
        return;
    }

    $.ajax({
        url: "/api/v1/course/" + label + '/general-education-requirements',
        dataType: "JSON",
        type: "GET",
        accepts: {text: "application/json"},
        success: function(results) {
            var totalTime = Date.now() - startTime;

            gtag('event', 'course_gen_ed_data', {
                'eventLabel': label,
                'value': totalTime
            });

            setCourseGenEdData(label, results);

            $('div.current-section').trigger(
                'coda:CurrentCourseGenEdDataSuccess', [label, results]);
        },
        error: function(xhr, status, error) {
            $('div.current-section').trigger(
                'coda:CurrentCourseGenEdDataFailure', [label, error]);
        }
    });
};

var setCourseGenEdData = function (label, gen_ed_data) {
    window.gen_ed_data[label] = gen_ed_data;
};

var getCourseGenEdData = function (label) {
    if (window.gen_ed_data.hasOwnProperty(label)) {
        return window.gen_ed_data[label];
    }

    return false;
};
