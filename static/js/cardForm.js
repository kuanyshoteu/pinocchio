$(document).ready(function () {
    var text = $('#card_comment-textarea');
    var helper = $('#card_comment-helper');
    function closeBlock() {
        return helper.css('display', 'none');
    }

    text.on('keyup', function (e) {
        if (e.keyCode === 51) {
            console.log('#')
            helper.css('display', 'block');
        }
    });

    $('.card_comment-item').on('click', function (e) {
        var str = $(e.target).text();
        if (str.charAt(0) === '#') {
            str = str.slice(1);
        }
        text.val(text.val() + `${str}`);
        closeBlock();
    });

    text.on('input', function () {
        closeBlock();
    });

    let cardFormSelect = $('#card_form-select-contact');
    let cardFormSelectBtn = $('#card_form-select-contact-btn');

    cardFormSelect.on('change', function(){
        cardFormSelect.css('display', 'none');
        cardFormSelectBtn.css('display', 'block');
    });

    $('#card_form-select').on('click', '#card_form-select-contact-btn', function(){
        cardFormSelect.css('display', 'block');
        cardFormSelectBtn.css('display', 'none');
    });
});