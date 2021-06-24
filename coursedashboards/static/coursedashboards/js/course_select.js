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
    return $('div.current-section #current_course_label').val();
}
