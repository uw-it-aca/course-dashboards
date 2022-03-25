//
//  intro.js - manage introductory modal display
//


var INTRODUCTION_VERSION = 1;

var displayWelcomeModal = function () {
    if (window.user.intro_modal === 0) {
        var source = $("#coda-introductory-modal").html(),
            template = Handlebars.compile(source);

        $(template({ netid: window.user.netid })).appendTo('body');
        $("#coda_intro_modal").modal({ backdrop: 'static' });

        registerWelcomeModalEvents();
    }
};


var registerWelcomeModalEvents = function () {
    $('body').on('hidden.bs.modal', '#coda_intro_modal', markIntroductionSeen);
};


var markIntroductionSeen = function () {
    var $body = $('body'),
        csrf_token = $("input[name=csrfmiddlewaretoken]")[0].value;

    $.ajax({
        url: "/api/v1/user/" + window.user.netid + "/introduction",
        type: "POST",
        data: JSON.stringify({ "seen": true, "version": INTRODUCTION_VERSION}),
        contentType: "application/json",
        accepts: {html: "application/json"},
        headers: {
            "X-CSRFToken": csrf_token
        },
        success: function(results) {
            $body.trigger('endorse:IntroductionSeenSuccess', [results]);
        },
        error: function(xhr, status, error) {
            $body.trigger('endorse:IntroductionSeenFailure', [error]);
        }
    });
};
