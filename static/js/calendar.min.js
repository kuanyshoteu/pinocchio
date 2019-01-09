!function() {
  var day_counter = 0;
  var today = moment();
  var x = 0
  var currentDay = 0
  function Calendar(selector, events) {
    this.el = document.querySelector(selector);
    this.events = events;
    this.current = moment().date(1);
    this.draw();
    var current = document.querySelector('.today');
    if(current) {
      var self = this;
      window.setTimeout(function() {
      }, 500);
    }
  }

  Calendar.prototype.draw = function() {
    //Create Header
    this.drawHeader();

    //Draw Month
    this.drawMonth();

  }

  Calendar.prototype.drawHeader = function() {
    var self = this;
    if(!this.headerr) {
      //Create the headerr elements
      this.headerr = createElement('div', 'headerr');
      this.headerr.className = 'headerr';

      this.title = createElement('h1');

      var right = createElement('div', 'rightt');
      right.addEventListener('click', function() { self.nextMonth(); });

      var left = createElement('div', 'leftt');
      left.addEventListener('click', function() { self.prevMonth(); });

      //Append the Elements
      this.headerr.appendChild(this.title); 
      this.headerr.appendChild(right);
      this.headerr.appendChild(left);
      this.el.appendChild(this.headerr);
    }

    this.title.innerHTML = this.current.format('MMMM YYYY');
    this.title.setAttribute('class', 'header_ym');
    this.title.setAttribute('year', this.current.format('YYYY'));
    this.title.setAttribute('month', this.current.format('MM'));
  }

  Calendar.prototype.drawMonth = function() {
    var self = this;     
    
    if(this.month) {
      this.oldMonth = this.month;
      this.oldMonth.className = 'month out ' + (self.next ? 'next' : 'prev');
      this.oldMonth.addEventListener('webkitAnimationEnd', function() {
        self.oldMonth.parentNode.removeChild(self.oldMonth);
        self.month = createElement('div', 'month');
        self.backFill();
        self.currentMonth();
        self.fowardFill();
        self.el.appendChild(self.month);
        self.currentMonthSun();
        self.fowardFillSun();

        window.setTimeout(function() {
          self.month.className = 'month in ' + (self.next ? 'next' : 'prev');
        }, 16);
      });
    } else {
        this.month = createElement('div', 'month');
        this.el.appendChild(this.month);
        this.backFill();
        this.currentMonth();
        this.fowardFill();
        this.currentMonthSun();
        this.fowardFillSun();
        this.month.className = 'month new';
    }
  }

  Calendar.prototype.backFill = function() {
    var clone = this.current.clone();
    var dayOfWeek = clone.day();
    if(!dayOfWeek) { return; }

    clone.subtract('days', dayOfWeek+1);
    for(var i = dayOfWeek; i > 0 ; i--) {
      this.drawDay(clone.add('days', 1));
    }
  }
  Calendar.prototype.currentMonth = function() {
    var clone = this.current.clone();  
    while(clone.month() === this.current.month()) {
      this.drawDay(clone);
      clone.add('days', 1);
    }
  }
  Calendar.prototype.currentMonthSun = function() {
    var clone = this.current.clone();  
    while(clone.month() === this.current.month()) {
      this.drawDaySun(clone);
      clone.add('days', 1);
    }
  }

  Calendar.prototype.fowardFill = function() {
    var clone = this.current.clone().add('months', 1).subtract('days', 1);
    this.drawDay(clone)
    var dayOfWeek = clone.day();
    if(dayOfWeek === 6) { return; }

    for(var i = dayOfWeek; i < 7 ; i++) {
      this.drawDay(clone.add('days', 1));
    }
  }
  Calendar.prototype.fowardFillSun = function() {
    var clone = this.current.clone().add('months', 1).subtract('days', 1);
    this.drawDay(clone)
    var dayOfWeek = clone.day();
    if(dayOfWeek === 6) { return; }

    for(var i = dayOfWeek; i < 7 ; i++) {
      this.drawDaySun(clone.add('days', 1));
    }
  }

  var week_counter = 0;
  Calendar.prototype.getWeek = function(day) {
    if(!this.week || day.day() === 0) {
      this.week = createElement('div', 'week');
      //this.week.setAttribute('week_num', week_counter);
      this.week.setAttribute('id', week_counter);
      week_counter += 1;
      this.month.appendChild(this.week);
      
    }
  }

  Calendar.prototype.drawDay = function(day) {
    var self = this;
    if(day.format('DD') != currentDay){
        currentDay = day.format('DD')

        this.getWeek(day);
        //Outer Day
        var outer = createElement('div', this.getDayClass(day));
        
        //Day Name
        var name = createElement('div', 'day-name', day.format('ddd'));
        //Day Number
        var number = createElement('div', 'day-number', day.format('DD'));
        //Events
        
        if(day_counter <= 7){
          outer.appendChild(name);
        }
        day_counter += 1;
        len = this.week.id
        outer.appendChild(number);
        outer.setAttribute('number', day_counter)
        outer.setAttribute('id', 'day' + day_counter)
        outer.setAttribute('day', day.format('DD'))
        if(day.format('ddd') != 'Sun'){
            this.week.appendChild(outer);      
        }
    }
  }


  Calendar.prototype.drawDaySun = function(day) {
    if(day.format('DD') != currentDay){
        currentDay = day.format('DD')

        var self = this;
        this.getWeek(day);

        //Outer Day
        var outer = createElement('div', this.getDayClass(day));
        outer.addEventListener('click', function() {
        });

        //Day Name
        var name = createElement('div', 'day-name', day.format('ddd'));
        //Day Number
        var number = createElement('div', 'day-number', day.format('DD'));
        //Events

        if(day.format('ddd') == 'Sun'){
            if(this.week.id != '0'){
                x = parseInt(this.week.id)
                prevWeek = document.getElementsByClassName('week');
                if(x-1-len == 0){
                  outer.appendChild(name);
                }
                outer.appendChild(number);
                outer.setAttribute('number', day_counter)
                outer.setAttribute('id', 'day' + day_counter)
                outer.setAttribute('day', day.format('DD'))
                day_counter += 7;
                prevWeek[x-1-len].appendChild(outer)
            }
        }
    }
  }



  Calendar.prototype.drawEvents = function(day, element) {
    if(day.month() === this.current.month()) {
      var todaysEvents = this.events.reduce(function(memo, ev) {
        if(ev.date.isSame(day, 'day')) {
          memo.push(ev);
        }
        return memo;
      }, []);

      todaysEvents.forEach(function(ev) {
        var evSpan = createElement('span', ev.color);
        element.appendChild(evSpan);
      });
    }
  }

  Calendar.prototype.getDayClass = function(day) {
    classes = ['day'];
    if(day.month() !== this.current.month()) {
      classes.push('other');
    } else if (today.isSame(day, 'day')) {
      classes.push('today');
    }
    return classes.join(' ');
  }


  Calendar.prototype.nextMonth = function() {
    week_counter = 0;
    this.current.add('months', 1);
    this.next = true;
    this.draw();
    day_counter = 0;
  }

  Calendar.prototype.prevMonth = function() {
    week_counter = 0;
    this.current.subtract('months', 1);
    this.next = false;
    this.draw();
    day_counter = 0;
  }

  window.Calendar = Calendar;

  function createElement(tagName, className, innerText) {
    var ele = document.createElement(tagName);
    if(className) {
      ele.className = className;
    }
    if(innerText) {
      ele.innderText = ele.textContent = innerText;
    }
    return ele;
  }
}();

!function() {
  var data = [
  ];

  

  function addDate(ev) {
    
  }

  var calendar = new Calendar('#calendar', data);

}();
