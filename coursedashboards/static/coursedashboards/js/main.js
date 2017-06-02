var source = $("#page-top").html();
var template = Handlebars.compile(source);
//plain_template({"netid": "test"});
$("#username-container").html(template({
    netid: window.user.netid
}));