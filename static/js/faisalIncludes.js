$(document).ready(function(){
// Filter-list start

  let filterElement = $('.filter-element');
  let filterList = $('.filter-list');
  let filterTitle = $('.filter-title');
  let filterItem = $('.filter-item');

  $(document.body).on('click', function(e){
    if($(e.target).closest('.filter-element').length === 0) {
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
});