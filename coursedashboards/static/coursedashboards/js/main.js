//Display the top bar: netid and course dropdown
var source = $("#page-top").html();
var template = Handlebars.compile(source);
$("#top_banner").html(template({
    netid: window.user.netid,
    quarter: firstLetterUppercase(window.term.quarter),
    year: window.term.year,
    sections: window.section_data
}));

//Display data about the currently selected course
var current = $("#current-course-data").html();
var currentTemplate = Handlebars.compile(current);
$("#current-course-target").html(currentTemplate({
    current_median: 2.9,
    current_num_registered: 182,
    current_capacity:344,
    current_repeat_students:3
}));

//Capitalize the first letter of a word
function firstLetterUppercase(word) 
{
    return word.charAt(0).toUpperCase() + word.slice(1);
}