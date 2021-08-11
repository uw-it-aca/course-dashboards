Handlebars.registerHelper('pluralize', function(number, single, plural) {
    if (number === 1) {
        return single;
    }
    return plural;
});

Handlebars.registerHelper('roundPercentage', function(percentage) {
    if(percentage < 1){
        return "<1";
    }
    return Math.round(percentage);
});

Handlebars.registerHelper('toFixed', function(percentage, decimals) {
    return parseFloat(percentage).toFixed(decimals);
});

Handlebars.registerHelper('formatName', function(name) {
    if(name && name === name.toUpperCase()){
        return name.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
    } else {
        return name;
    }
});

Handlebars.registerHelper('myPlanFormat', function(curriculum, course_number, section_id) {
    return curriculum + course_number + section_id;
});

Handlebars.registerHelper('gt', function(lval, rval, options) {
    if (rval > lval) {
        return options.inverse(this);
    }
    return options.fn(this);
});

Handlebars.registerHelper('static', function(path) {
    return window.static_url + path;
});

Handlebars.registerHelper('defaultValue', function (value, defValue) {
    var safe = value || defValue;

    return new Handlebars.SafeString(safe);
});
