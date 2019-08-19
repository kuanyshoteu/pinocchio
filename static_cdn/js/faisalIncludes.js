$(document).ready(function () {
  // Filter-list start

  let filterElement = $('.filter-element');
  let filterList = $('.filter-list');
  let filterTitle = $('.filter-title');
  let filterItem = $('.filter-item');

  $(document.body).on('click', function (e) {
    $('.search_hint').hide();
    if ($(e.target).closest(filterElement).length === 0) {
      filterList.addClass('filter-list-hide');
    }
  });

  filterTitle.on('click', function () {
    filterTitle.children('i').toggleClass('up');
    filterList.toggleClass('filter-list-hide');
  });

  filterItem.on('click', function () {
    $(this).children('i').toggleClass('show-icon');
    if ($(this).attr('status') == '0') {
      $(this).attr('status', '1')
    }
    else {
      $(this).attr('status', '0')
    }
    filtercrm()
  });

  // Filter-list end
  // Landing gallery start

  $('#landing__gallery-close').on('click', function() {
    $('.schoolLanding__header-gallery').css('display', 'none');
    // console.log('work');
  });

  // $('#landing__gallery-download').on('click', function(event) {
  //   var bg_url = $('.owl-item.active').children(0).css('background-image');
  //   bg_url = /^url\((['"]?)(.*)\1\)$/.exec(bg_url);
  //   bg_url = bg_url ? bg_url[2] : "";
  //   console.log(bg_url);

  //   var a = document.createElement('a');
  //   a.href = bg_url;
  //   a.download = bg_url;
  //   console.log(a);
  //   document.body.appendChild(a);
  //   a.click();
  //   document.body.removeChild(a);
  // });

  $('.schoolLanding__header-wrapper').on('click', function () {
    $('.schoolLanding__header-gallery').css('display', 'block');

    var sync1 = $("#schoolLanding__header-gallery__sliderone");
    var sync2 = $("#schoolLanding__header-gallery__slidertwo");
    var slidesPerPage = 10; //globaly define number of elements per page
    var syncedSecondary = true;

    sync1.owlCarousel({
      items: 1,
      // slideSpeed: 2000,
      nav: true,
      // autoplay: true,
      dots: true,
      loop: true,
      responsiveRefreshRate: 200,
      navText: ['<svg width="100%" height="100%" viewBox="0 0 11 20"><path style="fill:none;stroke-width: 1px;stroke: #fff;" d="M9.554,1.001l-8.607,8.607l8.607,8.606"/></svg>', '<svg width="100%" height="100%" viewBox="0 0 11 20" version="1.1"><path style="fill:none;stroke-width: 1px;stroke: #fff;" d="M1.054,18.214l8.606,-8.606l-8.606,-8.607"/></svg>'],
    }).on('changed.owl.carousel', syncPosition);

    sync2
      .on('initialized.owl.carousel', function () {
        sync2.find(".owl-item").eq(0).addClass("current");
      })
      .owlCarousel({
        items: slidesPerPage,
        dots: true,
        nav: true,
        smartSpeed: 200,
        slideSpeed: 500,
        slideBy: slidesPerPage, //alternatively you can slide by 1, this way the active slide will stick to the first item in the second carousel
        responsiveRefreshRate: 100,
        responsive: {
          1180:{
            items: slidesPerPage
          },
          860:{
            items: 8
          },
          768:{
            items: 6
          },
          480: {
            items: 4
          },
          320:{
            items: 3
          }

        }
      }).on('changed.owl.carousel', syncPosition2);

    function syncPosition(el) {
      //if you set loop to false, you have to restore this next line
      //var current = el.item.index;

      //if you disable loop you have to comment this block
      var count = el.item.count - 1;
      var current = Math.round(el.item.index - (el.item.count / 2) - .5);

      if (current < 0) {
        current = count;
      }
      if (current > count) {
        current = 0;
      }

      //end block

      sync2
        .find(".owl-item")
        .removeClass("current")
        .eq(current)
        .addClass("current");
      var onscreen = sync2.find('.owl-item.active').length - 1;
      var start = sync2.find('.owl-item.active').first().index();
      var end = sync2.find('.owl-item.active').last().index();

      if (current > end) {
        sync2.data('owl.carousel').to(current, 100, true);
      }
      if (current < start) {
        sync2.data('owl.carousel').to(current - onscreen, 100, true);
      }
    }

    function syncPosition2(el) {
      if (syncedSecondary) {
        var number = el.item.index;
        sync1.data('owl.carousel').to(number, 100, true);
      }
    }

    sync2.on("click", ".owl-item", function (e) {
      e.preventDefault();
      var number = $(this).index();
      sync1.data('owl.carousel').to(number, 300, true);
    });
  });

  // Landing gallery end
  // Landing category selector start
  $('.schoolLanding__content-category__item').on('click', function () {
    $('.schoolLanding__content-services__item').hide()
    $('.schoolLanding__content-category__item').removeClass('active');
    $(this).toggleClass('active');
    id = $(this).attr('id')
    $('.category'+id).show()
  });
  // Landing slider
  var item_count = parseInt($('.schoolLanding__content-teacher').length);
  $('.schoolLanding__content-teachers').owlCarousel({
    loop: true,
    autoplay: true,
    autoplayTimeout: 3000,
    margin: 10,
    dots: false,
    nav: false,
    items: 5,
    onInitialize: function(event) {
      // Check if only one slide in carousel
      if (item_count < 4) {
        $('.schoolLanding__content-teachers').css({
          'display': 'flex',
          'justifyContent': 'center'
        })
        this.options.loop = false;
        console.log('less one')
      }
      // I have more than one slide?! Great what are my options?!
      else {
        this.options.loop = true;
        console.log('more one')
      }
    },
  })
  // Landing end
  // map_phone-close script start

  $('.map_phone-main').on('click', function () {
    $('.map_phone-main').hide();
    $('.map_phone-other').show();
    $(this).hide()
  });
  $('.map_phone-main2').on('click', function () {
    $('.map_phone-other2').show();
  });
  // map_phone-close script end
  // map_someorg start
  var summWeight = 0;
  var summSlides = $('.map_sameorg-item').length;
  $('.select__prev').on('click', function () {
    if (summWeight !== 0) {
      var itemWeight = $('.map_sameorg-item:first-child').outerWidth();
      summWeight -= itemWeight;
      $('.map_sameorg-item').css('left', '-' + summWeight + 'px');
    }
    if (summWeight === 0) {
      $('.select__next').css('color', '#285c8a')
      $('.select__prev').css('color', '#99b1c6')
    }
  });

  $('.select__next').on('click', function () {
    var itemWeight = $('.map_sameorg-item').outerWidth();
    if (summWeight !== summSlides * itemWeight - itemWeight) {
      summWeight += itemWeight;
      $('.map_sameorg-item').css('left', '-' + summWeight + 'px')
    }
    if (summWeight === summSlides * itemWeight - itemWeight) {
      $('.select__next').css('color', '#99b1c6')
      $('.select__prev').css('color', '#285c8a')
    }
  });

  // map_someorg end
  // Number counter start

  let number = document.getElementById('number-counter');
  let start = 0;
  if (number && parseInt(number.textContent > 0)) {
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
  $('.search_by_tags').click(function (e) {
    filtercrm()
  })
  function filtercrm() {
    $('.crm_card').hide()
    search_text = $('#search_text').val()
    filterstring = ''
    if (search_text != '') {
      filterstring = filterstring + '.' + search_text.replace(' ', '.')
    }
    set = document.getElementsByClassName('filter-item')
    for (var i = set.length - 1; i >= 0; i--) {
      if (set[i].getAttribute('status') != '0') {
        title = set[i].getAttribute('id').replace(' ', '').replace(' ', '').replace(' ', '').replace(' ', '')
        filterstring = filterstring + '.' + title
      }
    }
    $(filterstring).show()
    if (filterstring == '') {
      $('.crm_card').show()
    }
  }
  $('.card_form-select-contact-btn').on('click', function () {
    url = '/schools/api/card_called/'
    id = $(this).attr('id')
    this_ = $(this)
    selector = document.getElementsByClassName('card_form-select-contact'+id)[0];
    action = selector.options[selector.selectedIndex].value;
    console.log(action)
    $.ajax({
      url: url,
      data: {
        'id': id,
        'action':action,
      },
      dataType: 'json',
      success: function (data) {
        this_.hide();
        $('.card_form-select-contact' + this_.attr('id')).show();
      }
    })
  });
  $('#search_text').on('input', function (e) {
    text = $(this).val()
    if (text.length == 0) {
      filtercrm()
      $('.search_hint').hide();
    }
    else {
      url = '/schools/api/call_helper/'
      $.ajax({
        url: url,
        data: {
          'text': text,
          'reverse': 'no',
        },
        dataType: 'json',
        success: function (data) {
          if (data.res.length == 0) {
            $('.search_hint').hide();
          }
          else {
            $('.search_hint').empty();
            url = $('.show_url').attr('url')
            for (var i = 0; i < data.res.length; i++) {
              var element = $('<div class="hint_item" onclick="hint_item(' + "'" + data.res[i] + "'" + ')">' + data.res[i] + '</div>').appendTo('.search_hint');
            }
            $('.search_hint').show();
          }
        }
      })
    }
  })
  $('.search_by_tags').on('click', function (e) {
    filtercrm()
  })

  // Number counter end
});