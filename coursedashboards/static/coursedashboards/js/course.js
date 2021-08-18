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
        current_course_panel = (compare_terms(section.year,
                                              section.quarter.toLowerCase(),
                                              window.term.year,
                                              window.term.quarter.toLowerCase()) >= 0),
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
                current: (this.year == window.term.year &&
                          this.quarter.toLowerCase() == window.term.quarter.toLowerCase()),
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
            failed_percent: calculateFailedPercentage(section.course_grades),
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

    if (section_data && section_data.loaded) {
        showCourseData(label);
    } else {
        fetchCourseData(label);
    }

    fetchHistoricCourseData(section_data.section_label);

    return true;
};

//Capitalize the first letter of a word
var firstLetterUppercase = function (word) {
    return word.charAt(0).toUpperCase() + word.slice(1);
};
