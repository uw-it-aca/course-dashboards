Handlebars.registerHelper('pluralize', function(number, single, plural) {
    if (number === 1) {
        return single;
    }
    return plural;
});

Handlebars.registerHelper('roundPercentage', function(percentage) {
    if(percentage === 0){
        return "0";
    } else if(percentage < 1){
        return "<1";
    } else if (percentage > 100) {
        return "100";
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

Handlebars.registerHelper('toLowerCase', function(str) {
  return str.toLowerCase();
});

Handlebars.registerHelper('toUpperCase', function(str) {
  return str.toUpperCase();
});

Handlebars.registerHelper('myPlanFormat', function(curriculum, course_number, section_id) {
    return curriculum + ' ' + course_number;
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
    return new Handlebars.SafeString((typeof value === "undefined") ? defValue : value);
});

Handlebars.registerHelper('is_defined', function(val, options) {
    if (typeof val === "undefined") {
        return options.inverse(this);
    }
    return options.fn(this);
});
