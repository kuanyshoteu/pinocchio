$(document).ready(function(){
// Filter-list start

  let filterElement = $('.filter-element');
  let filterList = $('.filter-list');
  let filterTitle = $('.filter-title');
  let filterItem = $('.filter-item');

  $(document.body).on('click', function(e){
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
  });

// Filter-list end
// Number counter start

  let number = document.getElementById('number-counter');

  console.log();

  let start = 20;
  let end = +number.textContent;
  let ticks = 20;
  let speed = 50;

  let randomNumbers = [end]

  for (let i = 0; i < ticks - 1; i++) {
    randomNumbers.unshift(
      Math.floor(Math.random() * (end - start + 1) + start)
    );
  }

  randomNumbers.sort((a, b) => { return a - b });

  console.log(randomNumbers.length)

  let x = 0;
  let interval = setInterval(function () {

    number.innerHTML = randomNumbers.shift();

    if (++x === ticks) {
      window.clearInterval(interval);
    }

  }, speed);

// Number counter end

});