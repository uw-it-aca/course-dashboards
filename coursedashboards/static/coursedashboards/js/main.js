var source = $("#page-top").html();
var template = Handlebars.compile(source);
//plain_template({"netid": "test"});
$("#top_banner").html(template({
    netid: window.user.netid,
    quarter: firstLetterUppercase(window.term.quarter),
    year: window.term.year
}));

//Capitalize the first letter of a word
function firstLetterUppercase(word) 
{
    return word.charAt(0).toUpperCase() + word.slice(1);
}