//Display the top bar: netid and course dropdown
var source = $("#page-top").html();
var template = Handlebars.compile(source);
$("#top_banner").html(template({
    netid: window.user.netid,
    quarter: firstLetterUppercase(window.term.quarter),
    year: window.term.year,
    sections: window.section_data
}));

//Listed for course dropdown selection change
$("#my_courses").change(function() {
    showCurrentCourseData();
})

showCurrentCourseData();

//Display data about the currently selected course - called whenever selection changes
function showCurrentCourseData() {
    var index = $("select[name='my_courses'] option:selected").index()
    var current = $("#current-course-data").html();
    var currentTemplate = Handlebars.compile(current);
    $("#current-course-target").html(currentTemplate({
        current_median: window.section_data[index].current_median,
        current_num_registered: window.section_data[index].current_enrollment,
        current_capacity:window.section_data[index].limit_estimate_enrollment,
        current_repeat_students:3,
        concurrent_courses:window.section_data[index].concurrent_courses
    }));
}

//Capitalize the first letter of a word
function firstLetterUppercase(word) 
{
    return word.charAt(0).toUpperCase() + word.slice(1);
}