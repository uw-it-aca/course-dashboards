//
//  course.js - functions to display course data
//


var getSectionDataByLabel = function (label) {
    var section_data = null;

    $.each(window.section_data, function () {
        if (this.section_label == label) {
            section_data = this;
            return false;
        }
    });

    return section_data;
};


//Display data about the currently selected course - called whenever selection changes
var showCourseData = function (label) {
    var current = $("#current-course-data").html(),
        currentTemplate = Handlebars.compile(current),
        section = getSectionDataByLabel(label),
        terms = [],
        current_course_panel = (compare_terms(section.year, section.quarter,
                                              window.term.year, window.term.quarter) >= 0),
        performanceTemplate;

    if (!current_course_panel && !section.loaded) {
        fetchCourseData(label);
        return;
    }

    $.each(window.section_data, function () {
        if (this.curriculum == section.curriculum &&
            this.course_number == section.course_number &&
            this.section_id == section.section_id) {
            terms.push({
                year: this.year,
                quarter: firstLetterUppercase(this.quarter),
                current: _isCurrentTerm(this),
                selected: (this.year == section.year &&
                           this.quarter.toLowerCase() == section.quarter.toLowerCase())
            });
        }
    });

    $("#current-course-target").html(currentTemplate({
        section_label: section.section_label,
        concurrent_courses: section.concurrent_courses,
        current_majors: section.current_student_majors,
        curriculum: section.curriculum,
        course_number: section.course_number,
        section_id: section.section_id,
        year: section.year,
        quarter: section.quarter,
        terms: terms,
        canvas_course_url: section.canvas_course_url,
        display_course: section.display_course
    }));

    if (current_course_panel) {
        performanceTemplate = Handlebars.compile($("#current-performance-template").html());
        $("#current-performance-panel").html(performanceTemplate({
            current_median: section.current_median ? section.current_median : 'N/A',
            current_num_registered: section.current_enrollment,
            current_capacity:section.limit_estimate_enrollment,
            current_repeat_students:section.current_repeating
        }));
    } else {
        performanceTemplate = Handlebars.compile($("#historic-performance-template").html());
        $("#current-performance-panel").html(performanceTemplate({
            median_gpa: section.current_median ? (section.current_median) : 'N/A',
            median_course_grade: section.median_course_grade ? (section.median_course_grade) : 'N/A',
            failed_percent: section.course_grades ? calculateFailedPercentage(section.course_grades) : 'N/A',
            total_students: section.current_enrollment,
            section_count: 1,
            gpa_distribution_time: 'past'
        }));
    }

    $('.course-title span').html(section.course_title);

    updateCourseURL(section.curriculum + '-' + section.course_number + '-' + section.section_id,
              section.year + '-' + section.quarter + '-' + section.curriculum + '-' +
              section.course_number + '-' + section.section_id);

    // update term labels
    $('span.displayed-quarter').html(firstLetterUppercase(section.quarter) + " " + section.year);

    setup_exposures($("#current-course-target"));
    $('#current-course-target [data-toggle="popover"]').popover();
    $('#current-course-target .popover-dismiss').popover({ trigger: 'focus'});

    $('#current-course-target .cumulative-popover')
        .on('inserted.bs.popover', function () {
            if (current_course_panel) {
                renderGPADisribution('current-gpa-distribution', section.gpas);
            } else {
                renderGPADisribution('past-gpa-distribution', section.gpas);
            }
        });

    $('#current-course-target .course-gpa-popover')
        .on('inserted.bs.popover', function () {
            renderGPADisribution('past-course-gpa-distribution', section.course_grades);
        });

};

var displaySelectedCourse = function () {
    displayCourse(getSelectedCourseLabel());
};

var displayCourse = function (label) {
    var section_data = getSectionDataByLabel(label);

    if (!section_data) {
        return false;
    }

    fetchCourseData(label);
    clearHistoricTermCache();
    fetchHistoricCourseData(section_data.section_label);
    return true;
};

//Capitalize the first letter of a word
var firstLetterUppercase = function (word) {
    return word.charAt(0).toUpperCase() + word.slice(1);
};


var showCourseProfileData = function (data) {
    var valueTemplate = Handlebars.compile($("#enrollment_profile_value").html()),
        attributes = {
            'eop': {
                element_class: 'enrollment-eop-percent',
                meaning: 'in the Early Opportunity Program'
            },
            'transfer': {
                element_class: 'enrollment-transfer-percent',
                meaning: 'are transfer students'
            },
            'disability': {
                element_class: 'enrollment-disability-percent',
                meaning: 'have disabilities'
            },
            'probation': {
                element_class: 'enrollment-probation-percent',
                meaning: 'are on academic probation'
            }
        };

    $.each(attributes, function (k, v) {
        var $id = $('.' + v.element_class);

        if ($id.length) {
            $id.html(valueTemplate({
                percentage: (data && data.hasOwnProperty(k)) ? data[k].percent : -1,
                meaning: v.meaning
            }));
        }
    });

    if (data.hasOwnProperty('disability')) {
        $('div.current-section').trigger(
            'coda:CurrentCourseProfileDisability', [data.disability]);
    }
};


var updateDRSPanel = function (label) {
    var section_data = getSectionDataByLabel(label);

    $('.drs_banner_missing').addClass('visually-hidden');
    if (!_isPastTerm(section_data)) {
        fetchCourseTextbookData(label);
    }
};


var updateGenEdNoticePanel = function (label) {
    var section_data = getSectionDataByLabel(label);

    $('.general-education-notices').addClass('visually-hidden');
    if (!_isPastTerm(section_data)) {
        fetchCourseGenEdData(label);
    }
};


var showCourseTextbookData = function (label, data) {
    var section_data = getSectionDataByLabel(label),
        $drs_missing_textbooks = $('.drs_missing_textbooks'),
        template = Handlebars.compile($("#drs-banner-missing-textbooks").html());

    if (data && data.hasOwnProperty('textbooks') && data.textbooks.length > 0) {
        $drs_missing_textbooks.empty();
    } else {
        $drs_missing_textbooks.html(template({
            sln: data ? data.sln : null,
            campus: _bookstore_campus(data.campus),
            year: section_data.year,
            qtr: _timeschedule_quarter(section_data.quarter),
            curriculum: section_data.curriculum,
            course_number: section_data.course_number,
            section_id: section_data.section_id
        }));
    }
};


var showCourseGenEdData = function (label, data) {
    var section_data = getSectionDataByLabel(label),
        $gen_ed_notices = $('.general-education-notices'),
        template = Handlebars.compile($("#general-education-notices-template").html()),
        html = "";

    $gen_ed_notices.addClass('visually-hidden');
    if (data) {
        html = template(data);
        if (html.length > 10) {
            $gen_ed_notices.html(html);
            $gen_ed_notices.removeClass('visually-hidden');
        }
    }
};


var showCourseProfileDisability = function (disability) {
};


var _isCurrentTerm = function (section_data) {
    return (section_data.year == window.term.year &&
            section_data.quarter.toLowerCase() == window.term.quarter.toLowerCase());
};


var _isPastTerm = function (section_data) {
    return compare_terms(section_data.year, section_data.quarter,
                         window.term.year, window.term.quarter) < 0;
};


var _timeschedule_quarter = function (quarter) {
    return (quarter.toLowerCase() == 'autumn') ? 'AUT' :
        (quarter.toLowerCase() == 'winter') ? 'WIN' :
        (quarter.toLowerCase() == 'spring') ? 'SPR' : 'SUM';
};

var _bookstore_campus = function (campus) {
    return (campus.toLowerCase() == 'bothell') ? 'bothell' :
        (campus.toLowerCase() == 'tacoma') ? 'tacoma' : 'main';
};
