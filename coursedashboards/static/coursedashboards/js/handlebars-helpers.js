Handlebars.registerHelper('pluralize', function(number, single, plural) {
    if (number === 1) {
        return single;
    }
    return plural;
});

Handlebars.registerHelper('roundPercentage', function(percentage) {
    return Math.round(percentage);
});
