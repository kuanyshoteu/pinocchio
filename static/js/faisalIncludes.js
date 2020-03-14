$(document).ready(function () { 
  // Landing gallery start

  $('#landing__gallery-close').on('click', function() {
    $('.schoolLanding__header-gallery').css('display', 'none');
    // console.log('work');
  });

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

  // Number counter end

   // Kanban script start

  $(document).on('click', '.kanban-column-add__open', function(){
    $(this).parent().removeClass('kanban-column-add__hidden')
    .addClass('kanban-column-add__showed');
    $('.kanban-column-add input').focus();
  });

  $(document).on('click', '.kanban-column-add i', function(){
    $(this).parent().removeClass('kanban-column-add__showed')
    .addClass('kanban-column-add__hidden');
  });

  $(document).on('click', '.kanban-column-add button', function(){
    let inputVal = $('.kanban-column-add input').val();
    let elem = $(`<div class="kanban-column"><div class="kanban-column-item"><h5>${inputVal}</h5></div><div class="kanban-column-item__add kanban-column-add-item__hidden"><a class="kanban-column-item-add__open">+ Добавьте еще одну карточку</a><input placeholder="Ввести заголовок для этой карточки" type="text"><button>Добавить карточку</button><i class="icon close icon"></i></div></div>`);
    if(inputVal !== '') {
      $(this).parent().parent().before(elem);
      $(this).siblings('input').val('').focus();
    }
  });

  $(document).on('click', '.kanban-column-item-add__open', function(){
    $(this).parent().removeClass('kanban-column-add-item__hidden')
    .addClass('kanban-column-add-item__showed');
    $('.kanban-column-item__add input').focus();
  });

  $(this).on('click', '.kanban-column-item__add i', function(){
    $(this).parent().removeClass('kanban-column-add-item__showed')
    .addClass('kanban-column-add-item__hidden');
  });

  $(document).on('click', '.kanban-column-item__add button', function(){
    let input = $(this).siblings('input');
    let inputVal = input.val();
    let elem = $(`<div class="kanban-column-task" draggable="true">${inputVal}</div>`)
    if(inputVal !== '') $(this).parent().siblings().append(elem);
    input.val('');
    input.focus();
  });

  $(document).on('click', '.kanban-column-task', function(){
    $('#kanban-modal').modal('show');
  });

  $(document).on('click', '.kanban-modal-icon-close', function(){
    $('#kanban-modal').modal('hide');
  });

  $(document).on('click', '.kanban-modal-desc', function(){
    $('.kanban-modal-desc').addClass('kanban-modal-desc-hidden');
    $('.kanban-modal-desc__text-block').removeClass('kanban-modal-desc-hidden');
    $('.kanban-modal-desc__text').focus();
  });


  $('.kanban-modal-desc__text-block-btn').on('click', function(){
    let kanbanTextBlock = $('.kanban-modal-desc');

    kanbanTextBlock.text($('.kanban-modal-desc__text').val())
    kanbanTextBlock.removeClass('kanban-modal-desc-hidden');
    $('.kanban-modal-desc__text-block').addClass('kanban-modal-desc-hidden');

    if (kanbanTextBlock.text() !== 'Добавить более подробное описание...') {
      kanbanTextBlock.addClass('kanban-modal-desc-edited');
    }
    if (kanbanTextBlock.text() === '') {
      kanbanTextBlock.text('Добавить более подробное описание...');
      kanbanTextBlock.removeClass('kanban-modal-desc-edited')
    }
  });

  $('.kanban-modal-desc__text-block-btn__close').on('click', function(){
    let kanbanTextBlock = $('.kanban-modal-desc');

    kanbanTextBlock.removeClass('kanban-modal-desc-hidden');
    $('.kanban-modal-desc__text-block').addClass('kanban-modal-desc-hidden');
    $('.kanban-modal-desc__text').val(kanbanTextBlock.text());
  });

  $('.kanban-modal-features__modal-input').datepicker({ timepicker: true });
  $('.kanban-modal-features__modal-input').data(['datepicker'])

  $('#kanban-modal-features__item-clock').on('click', function(){
    console.log('Clicked')
    $('.kanban-modal-features__modal').css('display', 'block');
    $('.kanban-modal-features__modal-input').focus();
  });

  $('.kanban-modal-features__modal-btn').on('click', function(){
    $('.kanban-modal-features__modal').css('display', 'none');
  });

  //Kanban Drag n Drop

  var firstDragEl = document.querySelectorAll('.kanban-column-item');

  for (item of firstDragEl) {
    new Sortable(item, {
      group: "colums",
      handle: ".kanban-column-task",
      draggable: ".kanban-column-task",
      ghostClass: "sortable-ghost",
      onAdd: function (evt) {
        var itemEl = evt.item;
      },
      onUpdate: function (evt) {
        var itemEl = evt.item; // the current dragged HTMLElement
      },
      onRemove: function (evt) {
        var itemEl = evt.item;
      }
    });
  }
});



