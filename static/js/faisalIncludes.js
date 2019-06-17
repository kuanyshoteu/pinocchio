$(document).ready(function(){
// Filter-list start

  let filterElement = $('.filter-element');
  let filterList = $('.filter-list');
  let filterTitle = $('.filter-title');
  let filterItem = $('.filter-item');

  $(document.body).on('click', function(e){
    $('.search_hint').hide();
    if($(e.target).closest(filterElement).length === 0) {
      filterList.addClass('filter-list-hide');
    }
  });

  filterTitle.on('click', function(){
    filterTitle.children('i').toggleClass('up');
    filterList.toggleClass('filter-list-hide');
  });

  filterItem.on('click', function(){
    $(this).children('i').toggleClass('show-icon');
    if ($(this).attr('status') == '0') {
      $(this).attr('status', '1')
    }
    else{
      $(this).attr('status', '0')      
    }
    filtercrm()
  });

// Filter-list end
// Number counter start

  let number = document.getElementById('number-counter');
  let start = 0;
  if (number){
    let end = +number.textContent;
    let ticks = 20;
    let speed = 70;

    let randomNumbers = [end]

    for (let i = 0; i < ticks - 1; i++) {
      randomNumbers.unshift(
        Math.floor(Math.random() * (end - start + 1) + start)
      );
    }

    randomNumbers.sort((a, b) => { return a - b });

    let x = 0;
    let interval = setInterval(function () {

      number.innerHTML = randomNumbers.shift();

      if (++x === ticks) {
        window.clearInterval(interval);
      }

    }, speed);
}
    $('.search_by_tags').click(function(e) {
        filtercrm()
    })
    function filtercrm(){
        $('.crm_card').hide()
        search_text = $('#search_text').val()
        filterstring = ''
        if (search_text != '') {
            filterstring = filterstring + '.'+search_text.replace(' ', '.')
        }
        set = document.getElementsByClassName('filter-item')
        for (var i = set.length - 1; i >= 0; i--) {
          if (set[i].getAttribute('status') != '0'){
            title = set[i].getAttribute('id')
            filterstring = filterstring + '.'+title.replace(' ', '.')
          }
        }
        $(filterstring).show()
        if (filterstring == '') {
            $('.crm_card').show()
        }
    }
    $('.card_form-select-contact-btn').on('click', function(){
        url = '/schools/api/card_called/'
        id = $(this).attr('id')
        this_ = $(this)
        $.ajax({
            url: url,
            data: {
                'id':id,
            },
            dataType: 'json',
            success: function (data) {
                this_.hide();
                $('.card_form-select-contact'+this_.attr('id')).show();
            }
        })
    });
    $('#search_text').on('input', function(e) {
        text = $(this).val()
        if (text.length == 0) {
            filtercrm()
            $('.search_hint').hide();
        }
        else{
            url = '/schools/api/call_helper/'
            $.ajax({
                url: url,
                data: {
                    'text':text,
                    'reverse':'no',
                },
                dataType: 'json',
                success: function (data) {
                    if(data.res.length == 0){
                        $('.search_hint').hide();
                    }
                    else{
                        $('.search_hint').empty();
                        url = $('.show_url').attr('url')
                        for(var i = 0; i < data.res.length; i++){
                            var element = $('<div class="hint_item" onclick="hint_item('+"'"+data.res[i]+"'"+')">'+data.res[i]+'</div>').appendTo('.search_hint');
                        }
                        $('.search_hint').show();
                    }                
                }
            })
        }
    })
    $('.search_by_tags').on('click',function(e) {
        filtercrm()
    })


// Number counter end
});