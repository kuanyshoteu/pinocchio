$('.form_query_send').click(function(e) {
    url = '/api/form_query_send/'+$(this).attr('id')
    name = $('.form_name').val()
    phone = $('.form_phone').val()
    city = $('.form_city').val()
    $('.form_loading').show()
    $(this).addClass('disabled')
    if (name.length > 0 && phone.length > 0) {
        $.ajax({
            url: url,
            data: {
                'name':name,
                'phone':phone,
                'city':city,
            },
            dataType: 'json',
            success: function (data) {
                if (data.ok) {
                    $('.wrong_form_query').hide()
                    $('.ok_form_query').show()
                }
                $('.form_query_send').removeClass('disabled')
                $('.form_loading').hide()
            }
        })                
    }
    else{
        $('.wrong_form_query').show()
        $('.ok_form_query').hide()
    }
});