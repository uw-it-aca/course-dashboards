//
//  course_select.js - functions supporting course selector display
//


function displayCourseSelector(label) {
    var section_data = getSectionDataByLabel(label),
        courses = [],
        term_index = -1,
        course_curriculum,
        course_number,
        course_id,
        seen = [];

    $.each(window.section_data, function () {
        var section = this;

        if (course_curriculum != section.curriculum &&
            course_number != section.course_number) {

            course_id = section.curriculum + '-' + section.course_number + '-' + section.section_id;
            if (!seen.includes(course_id)) {
                courses.push({
                    curriculum: section.curriculum,
                    course_number: section.course_number,
                    section_id: section.section_id,
                    title: section.course_title,
                    selected: (section_data &&
                               section_data.curriculum.toLowerCase() == section.curriculum.toLowerCase() &&
                               section_data.course_number == section.course_number)
                });

                seen.push(course_id);
            }
        }
    });

    source = $("#course-select").html();
    template = Handlebars.compile(source);
    $(".course-select").html(template({
        courses: courses
    }));
}

function getSelectedCourseLabel() {
    var $selected_course = $("select[name='my_courses'] option:selected"),
        $selected_term = $("select[name='course_quarters'] option:selected"),
        curriculum = $selected_course.attr('data-curriculum'),
        course_number = $selected_course.attr('data-course-number'),
        section_id = $selected_course.attr('data-section-id'),
        year,
        quarter,
        label = '';

    if ($selected_term.length) {
        year = $selected_term.attr('data-year');
        quarter = $selected_term.attr('data-quarter');
        $.each(window.section_data, function () {
            if (this.curriculum == curriculum &&
                this.course_number == course_number &&
                this.section_id == section_id &&
                this.year.toString() == $selected_term.attr('data-year') &&
                this.quarter.toLowerCase() == quarter.toLowerCase()) {
                label = this.section_label;
                return false;
            }
        });
    } else {
        $.each(window.section_data, function () {
            if (this.curriculum == curriculum &&
                this.course_number == course_number &&
                this.section_id == section_id) {
                label = this.section_label;
            }

            if (this.curriculum == curriculum &&
                this.course_number == course_number &&
                this.section_id == section_id &&
                this.year == window.term.year &&
                this.quarter.toLowerCase() == window.term.quarter.toLowerCase()) {
                label = this.section_label;
                return false;
            }
        });
    }


    return label;
}
