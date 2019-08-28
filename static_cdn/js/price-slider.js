/*! jQuery UI - v1.12.1 - 2016-09-14 
* http://jqueryui.com
* Includes: widget.js, position.js, data.js, disable-selection.js, effect.js, effects/effect-blind.js, effects/effect-bounce.js, effects/effect-clip.js, effects/effect-drop.js, effects/effect-explode.js, effects/effect-fade.js, effects/effect-fold.js, effects/effect-highlight.js, effects/effect-puff.js, effects/effect-pulsate.js, effects/effect-scale.js, effects/effect-shake.js, effects/effect-size.js, effects/effect-slide.js, effects/effect-transfer.js, focusable.js, form-reset-mixin.js, jquery-1-7.js, keycode.js, labels.js, scroll-parent.js, tabbable.js, unique-id.js, widgets/accordion.js, widgets/autocomplete.js, widgets/button.js, widgets/checkboxradio.js, widgets/controlgroup.js, widgets/datepicker.js, widgets/dialog.js, widgets/draggable.js, widgets/droppable.js, widgets/menu.js, widgets/mouse.js, widgets/progressbar.js, widgets/resizable.js, widgets/selectable.js, widgets/selectmenu.js, widgets/slider.js, widgets/sortable.js, widgets/spinner.js, widgets/tabs.js, widgets/tooltip.js
* Copyright jQuery Foundation and other contributors; Licensed MIT */

(function( factory ) {
    if ( typeof define === "function" && define.amd ) {

        // AMD. Register as an anonymous module.
        define([ "jquery" ], factory );
    } else {

        // Browser globals
        factory( jQuery );
    }
}(function( $ ) {

$.ui = $.ui || {};

var version = $.ui.version = "1.12.1";


/*!
 * jQuery UI Widget 1.12.1
 * http://jqueryui.com
 *
 * Copyright jQuery Foundation and other contributors
 * Released under the MIT license.
 * http://jquery.org/license
 */

//>>label: Widget
//>>group: Core
//>>description: Provides a factory for creating stateful widgets with a common API.
//>>docs: http://api.jqueryui.com/jQuery.widget/
//>>demos: http://jqueryui.com/widget/



var widgetUuid = 0;
var widgetSlice = Array.prototype.slice;

$.cleanData = ( function( orig ) {
    return function( elems ) {
        var events, elem, i;
        for ( i = 0; ( elem = elems[ i ] ) != null; i++ ) {
            try {

                // Only trigger remove when necessary to save time
                events = $._data( elem, "events" );
                if ( events && events.remove ) {
                    $( elem ).triggerHandler( "remove" );
                }

            // Http://bugs.jquery.com/ticket/8235
            } catch ( e ) {}
        }
        orig( elems );
    };
} )( $.cleanData );

$.widget = function( name, base, prototype ) {
    var existingConstructor, constructor, basePrototype;

    // ProxiedPrototype allows the provided prototype to remain unmodified
    // so that it can be used as a mixin for multiple widgets (#8876)
    var proxiedPrototype = {};

    var namespace = name.split( "." )[ 0 ];
    name = name.split( "." )[ 1 ];
    var fullName = namespace + "-" + name;

    if ( !prototype ) {
        prototype = base;
        base = $.Widget;
    }

    if ( $.isArray( prototype ) ) {
        prototype = $.extend.apply( null, [ {} ].concat( prototype ) );
    }

    // Create selector for plugin
    $.expr[ ":" ][ fullName.toLowerCase() ] = function( elem ) {
        return !!$.data( elem, fullName );
    };

    $[ namespace ] = $[ namespace ] || {};
    existingConstructor = $[ namespace ][ name ];
    constructor = $[ namespace ][ name ] = function( options, element ) {

        // Allow instantiation without "new" keyword
        if ( !this._createWidget ) {
            return new constructor( options, element );
        }

        // Allow instantiation without initializing for simple inheritance
        // must use "new" keyword (the code above always passes args)
        if ( arguments.length ) {
            this._createWidget( options, element );
        }
    };

    // Extend with the existing constructor to carry over any static properties
    $.extend( constructor, existingConstructor, {
        version: prototype.version,

        // Copy the object used to create the prototype in case we need to
        // redefine the widget later
        _proto: $.extend( {}, prototype ),

        // Track widgets that inherit from this widget in case this widget is
        // redefined after a widget inherits from it
        _childConstructors: []
    } );

    basePrototype = new base();

    // We need to make the options hash a property directly on the new instance
    // otherwise we'll modify the options hash on the prototype that we're
    // inheriting from
    basePrototype.options = $.widget.extend( {}, basePrototype.options );
    $.each( prototype, function( prop, value ) {
        if ( !$.isFunction( value ) ) {
            proxiedPrototype[ prop ] = value;
            return;
        }
        proxiedPrototype[ prop ] = ( function() {
            function _super() {
                return base.prototype[ prop ].apply( this, arguments );
            }

            function _superApply( args ) {
                return base.prototype[ prop ].apply( this, args );
            }

            return function() {
                var __super = this._super;
                var __superApply = this._superApply;
                var returnValue;

                this._super = _super;
                this._superApply = _superApply;

                returnValue = value.apply( this, arguments );

                this._super = __super;
                this._superApply = __superApply;

                return returnValue;
            };
        } )();
    } );
    constructor.prototype = $.widget.extend( basePrototype, {

        // TODO: remove support for widgetEventPrefix
        // always use the name + a colon as the prefix, e.g., draggable:start
        // don't prefix for widgets that aren't DOM-based
        widgetEventPrefix: existingConstructor ? ( basePrototype.widgetEventPrefix || name ) : name
    }, proxiedPrototype, {
        constructor: constructor,
        namespace: namespace,
        widgetName: name,
        widgetFullName: fullName
    } );

    // If this widget is being redefined then we need to find all widgets that
    // are inheriting from it and redefine all of them so that they inherit from
    // the new version of this widget. We're essentially trying to replace one
    // level in the prototype chain.
    if ( existingConstructor ) {
        $.each( existingConstructor._childConstructors, function( i, child ) {
            var childPrototype = child.prototype;

            // Redefine the child widget using the same prototype that was
            // originally used, but inherit from the new version of the base
            $.widget( childPrototype.namespace + "." + childPrototype.widgetName, constructor,
                child._proto );
        } );

        // Remove the list of existing child constructors from the old constructor
        // so the old child constructors can be garbage collected
        delete existingConstructor._childConstructors;
    } else {
        base._childConstructors.push( constructor );
    }

    $.widget.bridge( name, constructor );

    return constructor;
};

$.widget.extend = function( target ) {
    var input = widgetSlice.call( arguments, 1 );
    var inputIndex = 0;
    var inputLength = input.length;
    var key;
    var value;

    for ( ; inputIndex < inputLength; inputIndex++ ) {
        for ( key in input[ inputIndex ] ) {
            value = input[ inputIndex ][ key ];
            if ( input[ inputIndex ].hasOwnProperty( key ) && value !== undefined ) {

                // Clone objects
                if ( $.isPlainObject( value ) ) {
                    target[ key ] = $.isPlainObject( target[ key ] ) ?
                        $.widget.extend( {}, target[ key ], value ) :

                        // Don't extend strings, arrays, etc. with objects
                        $.widget.extend( {}, value );

                // Copy everything else by reference
                } else {
                    target[ key ] = value;
                }
            }
        }
    }
    return target;
};

$.widget.bridge = function( name, object ) {
    var fullName = object.prototype.widgetFullName || name;
    $.fn[ name ] = function( options ) {
        var isMethodCall = typeof options === "string";
        var args = widgetSlice.call( arguments, 1 );
        var returnValue = this;

        if ( isMethodCall ) {

            // If this is an empty collection, we need to have the instance method
            // return undefined instead of the jQuery instance
            if ( !this.length && options === "instance" ) {
                returnValue = undefined;
            } else {
                this.each( function() {
                    var methodValue;
                    var instance = $.data( this, fullName );

                    if ( options === "instance" ) {
                        returnValue = instance;
                        return false;
                    }

                    if ( !instance ) {
                        return $.error( "cannot call methods on " + name +
                            " prior to initialization; " +
                            "attempted to call method '" + options + "'" );
                    }

                    if ( !$.isFunction( instance[ options ] ) || options.charAt( 0 ) === "_" ) {
                        return $.error( "no such method '" + options + "' for " + name +
                            " widget instance" );
                    }

                    methodValue = instance[ options ].apply( instance, args );

                    if ( methodValue !== instance && methodValue !== undefined ) {
                        returnValue = methodValue && methodValue.jquery ?
                            returnValue.pushStack( methodValue.get() ) :
                            methodValue;
                        return false;
                    }
                } );
            }
        } else {

            // Allow multiple hashes to be passed on init
            if ( args.length ) {
                options = $.widget.extend.apply( null, [ options ].concat( args ) );
            }

            this.each( function() {
                var instance = $.data( this, fullName );
                if ( instance ) {
                    instance.option( options || {} );
                    if ( instance._init ) {
                        instance._init();
                    }
                } else {
                    $.data( this, fullName, new object( options, this ) );
                }
            } );
        }

        return returnValue;
    };
};

$.Widget = function( /* options, element */ ) {};
$.Widget._childConstructors = [];

$.Widget.prototype = {
    widgetName: "widget",
    widgetEventPrefix: "",
    defaultElement: "<div>",

    options: {
        classes: {},
        disabled: false,

        // Callbacks
        create: null
    },

    _createWidget: function( options, element ) {
        element = $( element || this.defaultElement || this )[ 0 ];
        this.element = $( element );
        this.uuid = widgetUuid++;
        this.eventNamespace = "." + this.widgetName + this.uuid;

        this.bindings = $();
        this.hoverable = $();
        this.focusable = $();
        this.classesElementLookup = {};

        if ( element !== this ) {
            $.data( element, this.widgetFullName, this );
            this._on( true, this.element, {
                remove: function( event ) {
                    if ( event.target === element ) {
                        this.destroy();
                    }
                }
            } );
            this.document = $( element.style ?

                // Element within the document
                element.ownerDocument :

                // Element is window or document
                element.document || element );
            this.window = $( this.document[ 0 ].defaultView || this.document[ 0 ].parentWindow );
        }

        this.options = $.widget.extend( {},
            this.options,
            this._getCreateOptions(),
            options );

        this._create();

        if ( this.options.disabled ) {
            this._setOptionDisabled( this.options.disabled );
        }

        this._trigger( "create", null, this._getCreateEventData() );
        this._init();
    },

    _getCreateOptions: function() {
        return {};
    },

    _getCreateEventData: $.noop,

    _create: $.noop,

    _init: $.noop,

    destroy: function() {
        var that = this;

        this._destroy();
        $.each( this.classesElementLookup, function( key, value ) {
            that._removeClass( value, key );
        } );

        // We can probably remove the unbind calls in 2.0
        // all event bindings should go through this._on()
        this.element
            .off( this.eventNamespace )
            .removeData( this.widgetFullName );
        this.widget()
            .off( this.eventNamespace )
            .removeAttr( "aria-disabled" );

        // Clean up events and states
        this.bindings.off( this.eventNamespace );
    },

    _destroy: $.noop,

    widget: function() {
        return this.element;
    },

    option: function( key, value ) {
        var options = key;
        var parts;
        var curOption;
        var i;

        if ( arguments.length === 0 ) {

            // Don't return a reference to the internal hash
            return $.widget.extend( {}, this.options );
        }

        if ( typeof key === "string" ) {

            // Handle nested keys, e.g., "foo.bar" => { foo: { bar: ___ } }
            options = {};
            parts = key.split( "." );
            key = parts.shift();
            if ( parts.length ) {
                curOption = options[ key ] = $.widget.extend( {}, this.options[ key ] );
                for ( i = 0; i < parts.length - 1; i++ ) {
                    curOption[ parts[ i ] ] = curOption[ parts[ i ] ] || {};
                    curOption = curOption[ parts[ i ] ];
                }
                key = parts.pop();
                if ( arguments.length === 1 ) {
                    return curOption[ key ] === undefined ? null : curOption[ key ];
                }
                curOption[ key ] = value;
            } else {
                if ( arguments.length === 1 ) {
                    return this.options[ key ] === undefined ? null : this.options[ key ];
                }
                options[ key ] = value;
            }
        }

        this._setOptions( options );

        return this;
    },

    _setOptions: function( options ) {
        var key;

        for ( key in options ) {
            this._setOption( key, options[ key ] );
        }

        return this;
    },

    _setOption: function( key, value ) {
        if ( key === "classes" ) {
            this._setOptionClasses( value );
        }

        this.options[ key ] = value;

        if ( key === "disabled" ) {
            this._setOptionDisabled( value );
        }

        return this;
    },

    _setOptionClasses: function( value ) {
        var classKey, elements, currentElements;

        for ( classKey in value ) {
            currentElements = this.classesElementLookup[ classKey ];
            if ( value[ classKey ] === this.options.classes[ classKey ] ||
                    !currentElements ||
                    !currentElements.length ) {
                continue;
            }

            // We are doing this to create a new jQuery object because the _removeClass() call
            // on the next line is going to destroy the reference to the current elements being
            // tracked. We need to save a copy of this collection so that we can add the new classes
            // below.
            elements = $( currentElements.get() );
            this._removeClass( currentElements, classKey );

            // We don't use _addClass() here, because that uses this.options.classes
            // for generating the string of classes. We want to use the value passed in from
            // _setOption(), this is the new value of the classes option which was passed to
            // _setOption(). We pass this value directly to _classes().
            elements.addClass( this._classes( {
                element: elements,
                keys: classKey,
                classes: value,
                add: true
            } ) );
        }
    },

    _setOptionDisabled: function( value ) {
        this._toggleClass( this.widget(), this.widgetFullName + "-disabled", null, !!value );

        // If the widget is becoming disabled, then nothing is interactive
        if ( value ) {
            this._removeClass( this.hoverable, null, "ui-state-hover" );
            this._removeClass( this.focusable, null, "ui-state-focus" );
        }
    },

    enable: function() {
        return this._setOptions( { disabled: false } );
    },

    disable: function() {
        return this._setOptions( { disabled: true } );
    },

    _classes: function( options ) {
        var full = [];
        var that = this;

        options = $.extend( {
            element: this.element,
            classes: this.options.classes || {}
        }, options );

        function processClassString( classes, checkOption ) {
            var current, i;
            for ( i = 0; i < classes.length; i++ ) {
                current = that.classesElementLookup[ classes[ i ] ] || $();
                if ( options.add ) {
                    current = $( $.unique( current.get().concat( options.element.get() ) ) );
                } else {
                    current = $( current.not( options.element ).get() );
                }
                that.classesElementLookup[ classes[ i ] ] = current;
                full.push( classes[ i ] );
                if ( checkOption && options.classes[ classes[ i ] ] ) {
                    full.push( options.classes[ classes[ i ] ] );
                }
            }
        }

        this._on( options.element, {
            "remove": "_untrackClassesElement"
        } );

        if ( options.keys ) {
            processClassString( options.keys.match( /\S+/g ) || [], true );
        }
        if ( options.extra ) {
            processClassString( options.extra.match( /\S+/g ) || [] );
        }

        return full.join( " " );
    },

    _untrackClassesElement: function( event ) {
        var that = this;
        $.each( that.classesElementLookup, function( key, value ) {
            if ( $.inArray( event.target, value ) !== -1 ) {
                that.classesElementLookup[ key ] = $( value.not( event.target ).get() );
            }
        } );
    },

    _removeClass: function( element, keys, extra ) {
        return this._toggleClass( element, keys, extra, false );
    },

    _addClass: function( element, keys, extra ) {
        return this._toggleClass( element, keys, extra, true );
    },

    _toggleClass: function( element, keys, extra, add ) {
        add = ( typeof add === "boolean" ) ? add : extra;
        var shift = ( typeof element === "string" || element === null ),
            options = {
                extra: shift ? keys : extra,
                keys: shift ? element : keys,
                element: shift ? this.element : element,
                add: add
            };
        options.element.toggleClass( this._classes( options ), add );
        return this;
    },

    _on: function( suppressDisabledCheck, element, handlers ) {
        var delegateElement;
        var instance = this;

        // No suppressDisabledCheck flag, shuffle arguments
        if ( typeof suppressDisabledCheck !== "boolean" ) {
            handlers = element;
            element = suppressDisabledCheck;
            suppressDisabledCheck = false;
        }

        // No element argument, shuffle and use this.element
        if ( !handlers ) {
            handlers = element;
            element = this.element;
            delegateElement = this.widget();
        } else {
            element = delegateElement = $( element );
            this.bindings = this.bindings.add( element );
        }

        $.each( handlers, function( event, handler ) {
            function handlerProxy() {

                // Allow widgets to customize the disabled handling
                // - disabled as an array instead of boolean
                // - disabled class as method for disabling individual parts
                if ( !suppressDisabledCheck &&
                        ( instance.options.disabled === true ||
                        $( this ).hasClass( "ui-state-disabled" ) ) ) {
                    return;
                }
                return ( typeof handler === "string" ? instance[ handler ] : handler )
                    .apply( instance, arguments );
            }

            // Copy the guid so direct unbinding works
            if ( typeof handler !== "string" ) {
                handlerProxy.guid = handler.guid =
                    handler.guid || handlerProxy.guid || $.guid++;
            }

            var match = event.match( /^([\w:-]*)\s*(.*)$/ );
            var eventName = match[ 1 ] + instance.eventNamespace;
            var selector = match[ 2 ];

            if ( selector ) {
                delegateElement.on( eventName, selector, handlerProxy );
            } else {
                element.on( eventName, handlerProxy );
            }
        } );
    },

    _off: function( element, eventName ) {
        eventName = ( eventName || "" ).split( " " ).join( this.eventNamespace + " " ) +
            this.eventNamespace;
        element.off( eventName ).off( eventName );

        // Clear the stack to avoid memory leaks (#10056)
        this.bindings = $( this.bindings.not( element ).get() );
        this.focusable = $( this.focusable.not( element ).get() );
        this.hoverable = $( this.hoverable.not( element ).get() );
    },

    _delay: function( handler, delay ) {
        function handlerProxy() {
            return ( typeof handler === "string" ? instance[ handler ] : handler )
                .apply( instance, arguments );
        }
        var instance = this;
        return setTimeout( handlerProxy, delay || 0 );
    },

    _hoverable: function( element ) {
        this.hoverable = this.hoverable.add( element );
        this._on( element, {
            mouseenter: function( event ) {
                this._addClass( $( event.currentTarget ), null, "ui-state-hover" );
            },
            mouseleave: function( event ) {
                this._removeClass( $( event.currentTarget ), null, "ui-state-hover" );
            }
        } );
    },

    _focusable: function( element ) {
        this.focusable = this.focusable.add( element );
        this._on( element, {
            focusin: function( event ) {
                this._addClass( $( event.currentTarget ), null, "ui-state-focus" );
            },
            focusout: function( event ) {
                this._removeClass( $( event.currentTarget ), null, "ui-state-focus" );
            }
        } );
    },

    _trigger: function( type, event, data ) {
        var prop, orig;
        var callback = this.options[ type ];

        data = data || {};
        event = $.Event( event );
        event.type = ( type === this.widgetEventPrefix ?
            type :
            this.widgetEventPrefix + type ).toLowerCase();

        // The original event may come from any element
        // so we need to reset the target on the new event
        event.target = this.element[ 0 ];

        // Copy original event properties over to the new event
        orig = event.originalEvent;
        if ( orig ) {
            for ( prop in orig ) {
                if ( !( prop in event ) ) {
                    event[ prop ] = orig[ prop ];
                }
            }
        }

        this.element.trigger( event, data );
        return !( $.isFunction( callback ) &&
            callback.apply( this.element[ 0 ], [ event ].concat( data ) ) === false ||
            event.isDefaultPrevented() );
    }
};

$.each( { show: "fadeIn", hide: "fadeOut" }, function( method, defaultEffect ) {
    $.Widget.prototype[ "_" + method ] = function( element, options, callback ) {
        if ( typeof options === "string" ) {
            options = { effect: options };
        }

        var hasOptions;
        var effectName = !options ?
            method :
            options === true || typeof options === "number" ?
                defaultEffect :
                options.effect || defaultEffect;

        options = options || {};
        if ( typeof options === "number" ) {
            options = { duration: options };
        }

        hasOptions = !$.isEmptyObject( options );
        options.complete = callback;

        if ( options.delay ) {
            element.delay( options.delay );
        }

        if ( hasOptions && $.effects && $.effects.effect[ effectName ] ) {
            element[ method ]( options );
        } else if ( effectName !== method && element[ effectName ] ) {
            element[ effectName ]( options.duration, options.easing, callback );
        } else {
            element.queue( function( next ) {
                $( this )[ method ]();
                if ( callback ) {
                    callback.call( element[ 0 ] );
                }
                next();
            } );
        }
    };
} );

var widget = $.widget;



var mouseHandled = false;
$( document ).on( "mouseup", function() {
    mouseHandled = false;
} );

var widgetsMouse = $.widget( "ui.mouse", {
    version: "1.12.1",
    options: {
        cancel: "input, textarea, button, select, option",
        distance: 1,
        delay: 0
    },
    _mouseInit: function() {
        var that = this;

        this.element
            .on( "mousedown." + this.widgetName, function( event ) {
                return that._mouseDown( event );
            } )
            .on( "click." + this.widgetName, function( event ) {
                if ( true === $.data( event.target, that.widgetName + ".preventClickEvent" ) ) {
                    $.removeData( event.target, that.widgetName + ".preventClickEvent" );
                    event.stopImmediatePropagation();
                    return false;
                }
            } );

        this.started = false;
    },

    // TODO: make sure destroying one instance of mouse doesn't mess with
    // other instances of mouse
    _mouseDestroy: function() {
        this.element.off( "." + this.widgetName );
        if ( this._mouseMoveDelegate ) {
            this.document
                .off( "mousemove." + this.widgetName, this._mouseMoveDelegate )
                .off( "mouseup." + this.widgetName, this._mouseUpDelegate );
        }
    },

    _mouseDown: function( event ) {

        // don't let more than one widget handle mouseStart
        if ( mouseHandled ) {
            return;
        }

        this._mouseMoved = false;

        // We may have missed mouseup (out of window)
        ( this._mouseStarted && this._mouseUp( event ) );

        this._mouseDownEvent = event;

        var that = this,
            btnIsLeft = ( event.which === 1 ),

            // event.target.nodeName works around a bug in IE 8 with
            // disabled inputs (#7620)
            elIsCancel = ( typeof this.options.cancel === "string" && event.target.nodeName ?
                $( event.target ).closest( this.options.cancel ).length : false );
        if ( !btnIsLeft || elIsCancel || !this._mouseCapture( event ) ) {
            return true;
        }

        this.mouseDelayMet = !this.options.delay;
        if ( !this.mouseDelayMet ) {
            this._mouseDelayTimer = setTimeout( function() {
                that.mouseDelayMet = true;
            }, this.options.delay );
        }

        if ( this._mouseDistanceMet( event ) && this._mouseDelayMet( event ) ) {
            this._mouseStarted = ( this._mouseStart( event ) !== false );
            if ( !this._mouseStarted ) {
                event.preventDefault();
                return true;
            }
        }

        // Click event may never have fired (Gecko & Opera)
        if ( true === $.data( event.target, this.widgetName + ".preventClickEvent" ) ) {
            $.removeData( event.target, this.widgetName + ".preventClickEvent" );
        }

        // These delegates are required to keep context
        this._mouseMoveDelegate = function( event ) {
            return that._mouseMove( event );
        };
        this._mouseUpDelegate = function( event ) {
            return that._mouseUp( event );
        };

        this.document
            .on( "mousemove." + this.widgetName, this._mouseMoveDelegate )
            .on( "mouseup." + this.widgetName, this._mouseUpDelegate );

        event.preventDefault();

        mouseHandled = true;
        return true;
    },

    _mouseMove: function( event ) {

        // Only check for mouseups outside the document if you've moved inside the document
        // at least once. This prevents the firing of mouseup in the case of IE<9, which will
        // fire a mousemove event if content is placed under the cursor. See #7778
        // Support: IE <9
        if ( this._mouseMoved ) {

            // IE mouseup check - mouseup happened when mouse was out of window
            if ( $.ui.ie && ( !document.documentMode || document.documentMode < 9 ) &&
                    !event.button ) {
                return this._mouseUp( event );

            // Iframe mouseup check - mouseup occurred in another document
            } else if ( !event.which ) {

                // Support: Safari <=8 - 9
                // Safari sets which to 0 if you press any of the following keys
                // during a drag (#14461)
                if ( event.originalEvent.altKey || event.originalEvent.ctrlKey ||
                        event.originalEvent.metaKey || event.originalEvent.shiftKey ) {
                    this.ignoreMissingWhich = true;
                } else if ( !this.ignoreMissingWhich ) {
                    return this._mouseUp( event );
                }
            }
        }

        if ( event.which || event.button ) {
            this._mouseMoved = true;
        }

        if ( this._mouseStarted ) {
            this._mouseDrag( event );
            return event.preventDefault();
        }

        if ( this._mouseDistanceMet( event ) && this._mouseDelayMet( event ) ) {
            this._mouseStarted =
                ( this._mouseStart( this._mouseDownEvent, event ) !== false );
            ( this._mouseStarted ? this._mouseDrag( event ) : this._mouseUp( event ) );
        }

        return !this._mouseStarted;
    },

    _mouseUp: function( event ) {
        this.document
            .off( "mousemove." + this.widgetName, this._mouseMoveDelegate )
            .off( "mouseup." + this.widgetName, this._mouseUpDelegate );

        if ( this._mouseStarted ) {
            this._mouseStarted = false;

            if ( event.target === this._mouseDownEvent.target ) {
                $.data( event.target, this.widgetName + ".preventClickEvent", true );
            }

            this._mouseStop( event );
        }

        if ( this._mouseDelayTimer ) {
            clearTimeout( this._mouseDelayTimer );
            delete this._mouseDelayTimer;
        }

        this.ignoreMissingWhich = false;
        mouseHandled = false;
        event.preventDefault();
    },

    _mouseDistanceMet: function( event ) {
        return ( Math.max(
                Math.abs( this._mouseDownEvent.pageX - event.pageX ),
                Math.abs( this._mouseDownEvent.pageY - event.pageY )
            ) >= this.options.distance
        );
    },

    _mouseDelayMet: function( /* event */ ) {
        return this.mouseDelayMet;
    },

    // These are placeholder methods, to be overriden by extending plugin
    _mouseStart: function( /* event */ ) {},
    _mouseDrag: function( /* event */ ) {},
    _mouseStop: function( /* event */ ) {},
    _mouseCapture: function( /* event */ ) { return true; }
} );





var widgetsProgressbar = $.widget( "ui.progressbar", {
    version: "1.12.1",
    options: {
        classes: {
            "ui-progressbar": "ui-corner-all",
            "ui-progressbar-value": "ui-corner-left",
            "ui-progressbar-complete": "ui-corner-right"
        },
        max: 100,
        value: 0,

        change: null,
        complete: null
    },

    min: 0,

    _create: function() {

        // Constrain initial value
        this.oldValue = this.options.value = this._constrainedValue();

        this.element.attr( {

            // Only set static values; aria-valuenow and aria-valuemax are
            // set inside _refreshValue()
            role: "progressbar",
            "aria-valuemin": this.min
        } );
        this._addClass( "ui-progressbar", "ui-widget ui-widget-content" );

        this.valueDiv = $( "<div>" ).appendTo( this.element );
        this._addClass( this.valueDiv, "ui-progressbar-value", "ui-widget-header" );
        this._refreshValue();
    },

    _destroy: function() {
        this.element.removeAttr( "role aria-valuemin aria-valuemax aria-valuenow" );

        this.valueDiv.remove();
    },

    value: function( newValue ) {
        if ( newValue === undefined ) {
            return this.options.value;
        }

        this.options.value = this._constrainedValue( newValue );
        this._refreshValue();
    },

    _constrainedValue: function( newValue ) {
        if ( newValue === undefined ) {
            newValue = this.options.value;
        }

        this.indeterminate = newValue === false;

        // Sanitize value
        if ( typeof newValue !== "number" ) {
            newValue = 0;
        }

        return this.indeterminate ? false :
            Math.min( this.options.max, Math.max( this.min, newValue ) );
    },

    _setOptions: function( options ) {

        // Ensure "value" option is set after other values (like max)
        var value = options.value;
        delete options.value;

        this._super( options );

        this.options.value = this._constrainedValue( value );
        this._refreshValue();
    },

    _setOption: function( key, value ) {
        if ( key === "max" ) {

            // Don't allow a max less than min
            value = Math.max( this.min, value );
        }
        this._super( key, value );
    },

    _setOptionDisabled: function( value ) {
        this._super( value );

        this.element.attr( "aria-disabled", value );
        this._toggleClass( null, "ui-state-disabled", !!value );
    },

    _percentage: function() {
        return this.indeterminate ?
            100 :
            100 * ( this.options.value - this.min ) / ( this.options.max - this.min );
    },

    _refreshValue: function() {
        var value = this.options.value,
            percentage = this._percentage();

        this.valueDiv
            .toggle( this.indeterminate || value > this.min )
            .width( percentage.toFixed( 0 ) + "%" );

        this
            ._toggleClass( this.valueDiv, "ui-progressbar-complete", null,
                value === this.options.max )
            ._toggleClass( "ui-progressbar-indeterminate", null, this.indeterminate );

        if ( this.indeterminate ) {
            this.element.removeAttr( "aria-valuenow" );
            if ( !this.overlayDiv ) {
                this.overlayDiv = $( "<div>" ).appendTo( this.valueDiv );
                this._addClass( this.overlayDiv, "ui-progressbar-overlay" );
            }
        } else {
            this.element.attr( {
                "aria-valuemax": this.options.max,
                "aria-valuenow": value
            } );
            if ( this.overlayDiv ) {
                this.overlayDiv.remove();
                this.overlayDiv = null;
            }
        }

        if ( this.oldValue !== value ) {
            this.oldValue = value;
            this._trigger( "change" );
        }
        if ( value === this.options.max ) {
            this._trigger( "complete" );
        }
    }
} );


/*!
 * jQuery UI Selectable 1.12.1
 * http://jqueryui.com
 *
 * Copyright jQuery Foundation and other contributors
 * Released under the MIT license.
 * http://jquery.org/license
 */

//>>label: Selectable
//>>group: Interactions
//>>description: Allows groups of elements to be selected with the mouse.
//>>docs: http://api.jqueryui.com/selectable/
//>>demos: http://jqueryui.com/selectable/
//>>css.structure: ../../themes/base/selectable.css



var widgetsSelectable = $.widget( "ui.selectable", $.ui.mouse, {
    version: "1.12.1",
    options: {
        appendTo: "body",
        autoRefresh: true,
        distance: 0,
        filter: "*",
        tolerance: "touch",

        // Callbacks
        selected: null,
        selecting: null,
        start: null,
        stop: null,
        unselected: null,
        unselecting: null
    },
    _create: function() {
        var that = this;

        this._addClass( "ui-selectable" );

        this.dragged = false;

        // Cache selectee children based on filter
        this.refresh = function() {
            that.elementPos = $( that.element[ 0 ] ).offset();
            that.selectees = $( that.options.filter, that.element[ 0 ] );
            that._addClass( that.selectees, "ui-selectee" );
            that.selectees.each( function() {
                var $this = $( this ),
                    selecteeOffset = $this.offset(),
                    pos = {
                        left: selecteeOffset.left - that.elementPos.left,
                        top: selecteeOffset.top - that.elementPos.top
                    };
                $.data( this, "selectable-item", {
                    element: this,
                    $element: $this,
                    left: pos.left,
                    top: pos.top,
                    right: pos.left + $this.outerWidth(),
                    bottom: pos.top + $this.outerHeight(),
                    startselected: false,
                    selected: $this.hasClass( "ui-selected" ),
                    selecting: $this.hasClass( "ui-selecting" ),
                    unselecting: $this.hasClass( "ui-unselecting" )
                } );
            } );
        };
        this.refresh();

        this._mouseInit();

        this.helper = $( "<div>" );
        this._addClass( this.helper, "ui-selectable-helper" );
    },

    _destroy: function() {
        this.selectees.removeData( "selectable-item" );
        this._mouseDestroy();
    },

    _mouseStart: function( event ) {
        var that = this,
            options = this.options;

        this.opos = [ event.pageX, event.pageY ];
        this.elementPos = $( this.element[ 0 ] ).offset();

        if ( this.options.disabled ) {
            return;
        }

        this.selectees = $( options.filter, this.element[ 0 ] );

        this._trigger( "start", event );

        $( options.appendTo ).append( this.helper );

        // position helper (lasso)
        this.helper.css( {
            "left": event.pageX,
            "top": event.pageY,
            "width": 0,
            "height": 0
        } );

        if ( options.autoRefresh ) {
            this.refresh();
        }

        this.selectees.filter( ".ui-selected" ).each( function() {
            var selectee = $.data( this, "selectable-item" );
            selectee.startselected = true;
            if ( !event.metaKey && !event.ctrlKey ) {
                that._removeClass( selectee.$element, "ui-selected" );
                selectee.selected = false;
                that._addClass( selectee.$element, "ui-unselecting" );
                selectee.unselecting = true;

                // selectable UNSELECTING callback
                that._trigger( "unselecting", event, {
                    unselecting: selectee.element
                } );
            }
        } );

        $( event.target ).parents().addBack().each( function() {
            var doSelect,
                selectee = $.data( this, "selectable-item" );
            if ( selectee ) {
                doSelect = ( !event.metaKey && !event.ctrlKey ) ||
                    !selectee.$element.hasClass( "ui-selected" );
                that._removeClass( selectee.$element, doSelect ? "ui-unselecting" : "ui-selected" )
                    ._addClass( selectee.$element, doSelect ? "ui-selecting" : "ui-unselecting" );
                selectee.unselecting = !doSelect;
                selectee.selecting = doSelect;
                selectee.selected = doSelect;

                // selectable (UN)SELECTING callback
                if ( doSelect ) {
                    that._trigger( "selecting", event, {
                        selecting: selectee.element
                    } );
                } else {
                    that._trigger( "unselecting", event, {
                        unselecting: selectee.element
                    } );
                }
                return false;
            }
        } );

    },

    _mouseDrag: function( event ) {

        this.dragged = true;

        if ( this.options.disabled ) {
            return;
        }

        var tmp,
            that = this,
            options = this.options,
            x1 = this.opos[ 0 ],
            y1 = this.opos[ 1 ],
            x2 = event.pageX,
            y2 = event.pageY;

        if ( x1 > x2 ) { tmp = x2; x2 = x1; x1 = tmp; }
        if ( y1 > y2 ) { tmp = y2; y2 = y1; y1 = tmp; }
        this.helper.css( { left: x1, top: y1, width: x2 - x1, height: y2 - y1 } );

        this.selectees.each( function() {
            var selectee = $.data( this, "selectable-item" ),
                hit = false,
                offset = {};

            //prevent helper from being selected if appendTo: selectable
            if ( !selectee || selectee.element === that.element[ 0 ] ) {
                return;
            }

            offset.left   = selectee.left   + that.elementPos.left;
            offset.right  = selectee.right  + that.elementPos.left;
            offset.top    = selectee.top    + that.elementPos.top;
            offset.bottom = selectee.bottom + that.elementPos.top;

            if ( options.tolerance === "touch" ) {
                hit = ( !( offset.left > x2 || offset.right < x1 || offset.top > y2 ||
                    offset.bottom < y1 ) );
            } else if ( options.tolerance === "fit" ) {
                hit = ( offset.left > x1 && offset.right < x2 && offset.top > y1 &&
                    offset.bottom < y2 );
            }

            if ( hit ) {

                // SELECT
                if ( selectee.selected ) {
                    that._removeClass( selectee.$element, "ui-selected" );
                    selectee.selected = false;
                }
                if ( selectee.unselecting ) {
                    that._removeClass( selectee.$element, "ui-unselecting" );
                    selectee.unselecting = false;
                }
                if ( !selectee.selecting ) {
                    that._addClass( selectee.$element, "ui-selecting" );
                    selectee.selecting = true;

                    // selectable SELECTING callback
                    that._trigger( "selecting", event, {
                        selecting: selectee.element
                    } );
                }
            } else {

                // UNSELECT
                if ( selectee.selecting ) {
                    if ( ( event.metaKey || event.ctrlKey ) && selectee.startselected ) {
                        that._removeClass( selectee.$element, "ui-selecting" );
                        selectee.selecting = false;
                        that._addClass( selectee.$element, "ui-selected" );
                        selectee.selected = true;
                    } else {
                        that._removeClass( selectee.$element, "ui-selecting" );
                        selectee.selecting = false;
                        if ( selectee.startselected ) {
                            that._addClass( selectee.$element, "ui-unselecting" );
                            selectee.unselecting = true;
                        }

                        // selectable UNSELECTING callback
                        that._trigger( "unselecting", event, {
                            unselecting: selectee.element
                        } );
                    }
                }
                if ( selectee.selected ) {
                    if ( !event.metaKey && !event.ctrlKey && !selectee.startselected ) {
                        that._removeClass( selectee.$element, "ui-selected" );
                        selectee.selected = false;

                        that._addClass( selectee.$element, "ui-unselecting" );
                        selectee.unselecting = true;

                        // selectable UNSELECTING callback
                        that._trigger( "unselecting", event, {
                            unselecting: selectee.element
                        } );
                    }
                }
            }
        } );

        return false;
    },

    _mouseStop: function( event ) {
        var that = this;

        this.dragged = false;

        $( ".ui-unselecting", this.element[ 0 ] ).each( function() {
            var selectee = $.data( this, "selectable-item" );
            that._removeClass( selectee.$element, "ui-unselecting" );
            selectee.unselecting = false;
            selectee.startselected = false;
            that._trigger( "unselected", event, {
                unselected: selectee.element
            } );
        } );
        $( ".ui-selecting", this.element[ 0 ] ).each( function() {
            var selectee = $.data( this, "selectable-item" );
            that._removeClass( selectee.$element, "ui-selecting" )
                ._addClass( selectee.$element, "ui-selected" );
            selectee.selecting = false;
            selectee.selected = true;
            selectee.startselected = true;
            that._trigger( "selected", event, {
                selected: selectee.element
            } );
        } );
        this._trigger( "stop", event );

        this.helper.remove();

        return false;
    }

} );


/*!
 * jQuery UI Selectmenu 1.12.1
 * http://jqueryui.com
 *
 * Copyright jQuery Foundation and other contributors
 * Released under the MIT license.
 * http://jquery.org/license
 */

//>>label: Selectmenu
//>>group: Widgets
// jscs:disable maximumLineLength
//>>description: Duplicates and extends the functionality of a native HTML select element, allowing it to be customizable in behavior and appearance far beyond the limitations of a native select.
// jscs:enable maximumLineLength
//>>docs: http://api.jqueryui.com/selectmenu/
//>>demos: http://jqueryui.com/selectmenu/
//>>css.structure: ../../themes/base/core.css
//>>css.structure: ../../themes/base/selectmenu.css, ../../themes/base/button.css
//>>css.theme: ../../themes/base/theme.css



var widgetsSelectmenu = $.widget( "ui.selectmenu", [ $.ui.formResetMixin, {
    version: "1.12.1",
    defaultElement: "<select>",
    options: {
        appendTo: null,
        classes: {
            "ui-selectmenu-button-open": "ui-corner-top",
            "ui-selectmenu-button-closed": "ui-corner-all"
        },
        disabled: null,
        icons: {
            button: "ui-icon-triangle-1-s"
        },
        position: {
            my: "left top",
            at: "left bottom",
            collision: "none"
        },
        width: false,

        // Callbacks
        change: null,
        close: null,
        focus: null,
        open: null,
        select: null
    },

    _create: function() {
        var selectmenuId = this.element.uniqueId().attr( "id" );
        this.ids = {
            element: selectmenuId,
            button: selectmenuId + "-button",
            menu: selectmenuId + "-menu"
        };

        this._drawButton();
        this._drawMenu();
        this._bindFormResetHandler();

        this._rendered = false;
        this.menuItems = $();
    },

    _drawButton: function() {
        var icon,
            that = this,
            item = this._parseOption(
                this.element.find( "option:selected" ),
                this.element[ 0 ].selectedIndex
            );

        // Associate existing label with the new button
        this.labels = this.element.labels().attr( "for", this.ids.button );
        this._on( this.labels, {
            click: function( event ) {
                this.button.focus();
                event.preventDefault();
            }
        } );

        // Hide original select element
        this.element.hide();

        // Create button
        this.button = $( "<span>", {
            tabindex: this.options.disabled ? -1 : 0,
            id: this.ids.button,
            role: "combobox",
            "aria-expanded": "false",
            "aria-autocomplete": "list",
            "aria-owns": this.ids.menu,
            "aria-haspopup": "true",
            title: this.element.attr( "title" )
        } )
            .insertAfter( this.element );

        this._addClass( this.button, "ui-selectmenu-button ui-selectmenu-button-closed",
            "ui-button ui-widget" );

        icon = $( "<span>" ).appendTo( this.button );
        this._addClass( icon, "ui-selectmenu-icon", "ui-icon " + this.options.icons.button );
        this.buttonItem = this._renderButtonItem( item )
            .appendTo( this.button );

        if ( this.options.width !== false ) {
            this._resizeButton();
        }

        this._on( this.button, this._buttonEvents );
        this.button.one( "focusin", function() {

            // Delay rendering the menu items until the button receives focus.
            // The menu may have already been rendered via a programmatic open.
            if ( !that._rendered ) {
                that._refreshMenu();
            }
        } );
    },

    _drawMenu: function() {
        var that = this;

        // Create menu
        this.menu = $( "<ul>", {
            "aria-hidden": "true",
            "aria-labelledby": this.ids.button,
            id: this.ids.menu
        } );

        // Wrap menu
        this.menuWrap = $( "<div>" ).append( this.menu );
        this._addClass( this.menuWrap, "ui-selectmenu-menu", "ui-front" );
        this.menuWrap.appendTo( this._appendTo() );

        // Initialize menu widget
        this.menuInstance = this.menu
            .menu( {
                classes: {
                    "ui-menu": "ui-corner-bottom"
                },
                role: "listbox",
                select: function( event, ui ) {
                    event.preventDefault();

                    // Support: IE8
                    // If the item was selected via a click, the text selection
                    // will be destroyed in IE
                    that._setSelection();

                    that._select( ui.item.data( "ui-selectmenu-item" ), event );
                },
                focus: function( event, ui ) {
                    var item = ui.item.data( "ui-selectmenu-item" );

                    // Prevent inital focus from firing and check if its a newly focused item
                    if ( that.focusIndex != null && item.index !== that.focusIndex ) {
                        that._trigger( "focus", event, { item: item } );
                        if ( !that.isOpen ) {
                            that._select( item, event );
                        }
                    }
                    that.focusIndex = item.index;

                    that.button.attr( "aria-activedescendant",
                        that.menuItems.eq( item.index ).attr( "id" ) );
                }
            } )
            .menu( "instance" );

        // Don't close the menu on mouseleave
        this.menuInstance._off( this.menu, "mouseleave" );

        // Cancel the menu's collapseAll on document click
        this.menuInstance._closeOnDocumentClick = function() {
            return false;
        };

        // Selects often contain empty items, but never contain dividers
        this.menuInstance._isDivider = function() {
            return false;
        };
    },

    refresh: function() {
        this._refreshMenu();
        this.buttonItem.replaceWith(
            this.buttonItem = this._renderButtonItem(

                // Fall back to an empty object in case there are no options
                this._getSelectedItem().data( "ui-selectmenu-item" ) || {}
            )
        );
        if ( this.options.width === null ) {
            this._resizeButton();
        }
    },

    _refreshMenu: function() {
        var item,
            options = this.element.find( "option" );

        this.menu.empty();

        this._parseOptions( options );
        this._renderMenu( this.menu, this.items );

        this.menuInstance.refresh();
        this.menuItems = this.menu.find( "li" )
            .not( ".ui-selectmenu-optgroup" )
                .find( ".ui-menu-item-wrapper" );

        this._rendered = true;

        if ( !options.length ) {
            return;
        }

        item = this._getSelectedItem();

        // Update the menu to have the correct item focused
        this.menuInstance.focus( null, item );
        this._setAria( item.data( "ui-selectmenu-item" ) );

        // Set disabled state
        this._setOption( "disabled", this.element.prop( "disabled" ) );
    },

    open: function( event ) {
        if ( this.options.disabled ) {
            return;
        }

        // If this is the first time the menu is being opened, render the items
        if ( !this._rendered ) {
            this._refreshMenu();
        } else {

            // Menu clears focus on close, reset focus to selected item
            this._removeClass( this.menu.find( ".ui-state-active" ), null, "ui-state-active" );
            this.menuInstance.focus( null, this._getSelectedItem() );
        }

        // If there are no options, don't open the menu
        if ( !this.menuItems.length ) {
            return;
        }

        this.isOpen = true;
        this._toggleAttr();
        this._resizeMenu();
        this._position();

        this._on( this.document, this._documentClick );

        this._trigger( "open", event );
    },

    _position: function() {
        this.menuWrap.position( $.extend( { of: this.button }, this.options.position ) );
    },

    close: function( event ) {
        if ( !this.isOpen ) {
            return;
        }

        this.isOpen = false;
        this._toggleAttr();

        this.range = null;
        this._off( this.document );

        this._trigger( "close", event );
    },

    widget: function() {
        return this.button;
    },

    menuWidget: function() {
        return this.menu;
    },

    _renderButtonItem: function( item ) {
        var buttonItem = $( "<span>" );

        this._setText( buttonItem, item.label );
        this._addClass( buttonItem, "ui-selectmenu-text" );

        return buttonItem;
    },

    _renderMenu: function( ul, items ) {
        var that = this,
            currentOptgroup = "";

        $.each( items, function( index, item ) {
            var li;

            if ( item.optgroup !== currentOptgroup ) {
                li = $( "<li>", {
                    text: item.optgroup
                } );
                that._addClass( li, "ui-selectmenu-optgroup", "ui-menu-divider" +
                    ( item.element.parent( "optgroup" ).prop( "disabled" ) ?
                        " ui-state-disabled" :
                        "" ) );

                li.appendTo( ul );

                currentOptgroup = item.optgroup;
            }

            that._renderItemData( ul, item );
        } );
    },

    _renderItemData: function( ul, item ) {
        return this._renderItem( ul, item ).data( "ui-selectmenu-item", item );
    },

    _renderItem: function( ul, item ) {
        var li = $( "<li>" ),
            wrapper = $( "<div>", {
                title: item.element.attr( "title" )
            } );

        if ( item.disabled ) {
            this._addClass( li, null, "ui-state-disabled" );
        }
        this._setText( wrapper, item.label );

        return li.append( wrapper ).appendTo( ul );
    },

    _setText: function( element, value ) {
        if ( value ) {
            element.text( value );
        } else {
            element.html( "&#160;" );
        }
    },

    _move: function( direction, event ) {
        var item, next,
            filter = ".ui-menu-item";

        if ( this.isOpen ) {
            item = this.menuItems.eq( this.focusIndex ).parent( "li" );
        } else {
            item = this.menuItems.eq( this.element[ 0 ].selectedIndex ).parent( "li" );
            filter += ":not(.ui-state-disabled)";
        }

        if ( direction === "first" || direction === "last" ) {
            next = item[ direction === "first" ? "prevAll" : "nextAll" ]( filter ).eq( -1 );
        } else {
            next = item[ direction + "All" ]( filter ).eq( 0 );
        }

        if ( next.length ) {
            this.menuInstance.focus( event, next );
        }
    },

    _getSelectedItem: function() {
        return this.menuItems.eq( this.element[ 0 ].selectedIndex ).parent( "li" );
    },

    _toggle: function( event ) {
        this[ this.isOpen ? "close" : "open" ]( event );
    },

    _setSelection: function() {
        var selection;

        if ( !this.range ) {
            return;
        }

        if ( window.getSelection ) {
            selection = window.getSelection();
            selection.removeAllRanges();
            selection.addRange( this.range );

        // Support: IE8
        } else {
            this.range.select();
        }

        // Support: IE
        // Setting the text selection kills the button focus in IE, but
        // restoring the focus doesn't kill the selection.
        this.button.focus();
    },

    _documentClick: {
        mousedown: function( event ) {
            if ( !this.isOpen ) {
                return;
            }

            if ( !$( event.target ).closest( ".ui-selectmenu-menu, #" +
                    $.ui.escapeSelector( this.ids.button ) ).length ) {
                this.close( event );
            }
        }
    },

    _buttonEvents: {

        // Prevent text selection from being reset when interacting with the selectmenu (#10144)
        mousedown: function() {
            var selection;

            if ( window.getSelection ) {
                selection = window.getSelection();
                if ( selection.rangeCount ) {
                    this.range = selection.getRangeAt( 0 );
                }

            // Support: IE8
            } else {
                this.range = document.selection.createRange();
            }
        },

        click: function( event ) {
            this._setSelection();
            this._toggle( event );
        },

        keydown: function( event ) {
            var preventDefault = true;
            switch ( event.keyCode ) {
            case $.ui.keyCode.TAB:
            case $.ui.keyCode.ESCAPE:
                this.close( event );
                preventDefault = false;
                break;
            case $.ui.keyCode.ENTER:
                if ( this.isOpen ) {
                    this._selectFocusedItem( event );
                }
                break;
            case $.ui.keyCode.UP:
                if ( event.altKey ) {
                    this._toggle( event );
                } else {
                    this._move( "prev", event );
                }
                break;
            case $.ui.keyCode.DOWN:
                if ( event.altKey ) {
                    this._toggle( event );
                } else {
                    this._move( "next", event );
                }
                break;
            case $.ui.keyCode.SPACE:
                if ( this.isOpen ) {
                    this._selectFocusedItem( event );
                } else {
                    this._toggle( event );
                }
                break;
            case $.ui.keyCode.LEFT:
                this._move( "prev", event );
                break;
            case $.ui.keyCode.RIGHT:
                this._move( "next", event );
                break;
            case $.ui.keyCode.HOME:
            case $.ui.keyCode.PAGE_UP:
                this._move( "first", event );
                break;
            case $.ui.keyCode.END:
            case $.ui.keyCode.PAGE_DOWN:
                this._move( "last", event );
                break;
            default:
                this.menu.trigger( event );
                preventDefault = false;
            }

            if ( preventDefault ) {
                event.preventDefault();
            }
        }
    },

    _selectFocusedItem: function( event ) {
        var item = this.menuItems.eq( this.focusIndex ).parent( "li" );
        if ( !item.hasClass( "ui-state-disabled" ) ) {
            this._select( item.data( "ui-selectmenu-item" ), event );
        }
    },

    _select: function( item, event ) {
        var oldIndex = this.element[ 0 ].selectedIndex;

        // Change native select element
        this.element[ 0 ].selectedIndex = item.index;
        this.buttonItem.replaceWith( this.buttonItem = this._renderButtonItem( item ) );
        this._setAria( item );
        this._trigger( "select", event, { item: item } );

        if ( item.index !== oldIndex ) {
            this._trigger( "change", event, { item: item } );
        }

        this.close( event );
    },

    _setAria: function( item ) {
        var id = this.menuItems.eq( item.index ).attr( "id" );

        this.button.attr( {
            "aria-labelledby": id,
            "aria-activedescendant": id
        } );
        this.menu.attr( "aria-activedescendant", id );
    },

    _setOption: function( key, value ) {
        if ( key === "icons" ) {
            var icon = this.button.find( "span.ui-icon" );
            this._removeClass( icon, null, this.options.icons.button )
                ._addClass( icon, null, value.button );
        }

        this._super( key, value );

        if ( key === "appendTo" ) {
            this.menuWrap.appendTo( this._appendTo() );
        }

        if ( key === "width" ) {
            this._resizeButton();
        }
    },

    _setOptionDisabled: function( value ) {
        this._super( value );

        this.menuInstance.option( "disabled", value );
        this.button.attr( "aria-disabled", value );
        this._toggleClass( this.button, null, "ui-state-disabled", value );

        this.element.prop( "disabled", value );
        if ( value ) {
            this.button.attr( "tabindex", -1 );
            this.close();
        } else {
            this.button.attr( "tabindex", 0 );
        }
    },

    _appendTo: function() {
        var element = this.options.appendTo;

        if ( element ) {
            element = element.jquery || element.nodeType ?
                $( element ) :
                this.document.find( element ).eq( 0 );
        }

        if ( !element || !element[ 0 ] ) {
            element = this.element.closest( ".ui-front, dialog" );
        }

        if ( !element.length ) {
            element = this.document[ 0 ].body;
        }

        return element;
    },

    _toggleAttr: function() {
        this.button.attr( "aria-expanded", this.isOpen );

        // We can't use two _toggleClass() calls here, because we need to make sure
        // we always remove classes first and add them second, otherwise if both classes have the
        // same theme class, it will be removed after we add it.
        this._removeClass( this.button, "ui-selectmenu-button-" +
            ( this.isOpen ? "closed" : "open" ) )
            ._addClass( this.button, "ui-selectmenu-button-" +
                ( this.isOpen ? "open" : "closed" ) )
            ._toggleClass( this.menuWrap, "ui-selectmenu-open", null, this.isOpen );

        this.menu.attr( "aria-hidden", !this.isOpen );
    },

    _resizeButton: function() {
        var width = this.options.width;

        // For `width: false`, just remove inline style and stop
        if ( width === false ) {
            this.button.css( "width", "" );
            return;
        }

        // For `width: null`, match the width of the original element
        if ( width === null ) {
            width = this.element.show().outerWidth();
            this.element.hide();
        }

        this.button.outerWidth( width );
    },

    _resizeMenu: function() {
        this.menu.outerWidth( Math.max(
            this.button.outerWidth(),

            // Support: IE10
            // IE10 wraps long text (possibly a rounding bug)
            // so we add 1px to avoid the wrapping
            this.menu.width( "" ).outerWidth() + 1
        ) );
    },

    _getCreateOptions: function() {
        var options = this._super();

        options.disabled = this.element.prop( "disabled" );

        return options;
    },

    _parseOptions: function( options ) {
        var that = this,
            data = [];
        options.each( function( index, item ) {
            data.push( that._parseOption( $( item ), index ) );
        } );
        this.items = data;
    },

    _parseOption: function( option, index ) {
        var optgroup = option.parent( "optgroup" );

        return {
            element: option,
            index: index,
            value: option.val(),
            label: option.text(),
            optgroup: optgroup.attr( "label" ) || "",
            disabled: optgroup.prop( "disabled" ) || option.prop( "disabled" )
        };
    },

    _destroy: function() {
        this._unbindFormResetHandler();
        this.menuWrap.remove();
        this.button.remove();
        this.element.show();
        this.element.removeUniqueId();
        this.labels.attr( "for", this.ids.element );
    }
} ] );


/*!
 * jQuery UI Slider 1.12.1
 * http://jqueryui.com
 *
 * Copyright jQuery Foundation and other contributors
 * Released under the MIT license.
 * http://jquery.org/license
 */

//>>label: Slider
//>>group: Widgets
//>>description: Displays a flexible slider with ranges and accessibility via keyboard.
//>>docs: http://api.jqueryui.com/slider/
//>>demos: http://jqueryui.com/slider/
//>>css.structure: ../../themes/base/core.css
//>>css.structure: ../../themes/base/slider.css
//>>css.theme: ../../themes/base/theme.css



var widgetsSlider = $.widget( "ui.slider", $.ui.mouse, {
    version: "1.12.1",
    widgetEventPrefix: "slide",

    options: {
        animate: false,
        classes: {
            "ui-slider": "ui-corner-all",
            "ui-slider-handle": "ui-corner-all",

            // Note: ui-widget-header isn't the most fittingly semantic framework class for this
            // element, but worked best visually with a variety of themes
            "ui-slider-range": "ui-corner-all ui-widget-header"
        },
        distance: 0,
        max: 100,
        min: 0,
        orientation: "horizontal",
        range: false,
        step: 10,
        value: 0,
        values: null,

        // Callbacks
        change: null,
        slide: null,
        start: null,
        stop: null
    },

    // Number of pages in a slider
    // (how many times can you page up/down to go through the whole range)
    numPages: 5,

    _create: function() {
        this._keySliding = false;
        this._mouseSliding = false;
        this._animateOff = true;
        this._handleIndex = null;
        this._detectOrientation();
        this._mouseInit();
        this._calculateNewMax();

        this._addClass( "ui-slider ui-slider-" + this.orientation,
            "ui-widget ui-widget-content" );

        this._refresh();

        this._animateOff = false;
    },

    _refresh: function() {
        this._createRange();
        this._createHandles();
        this._setupEvents();
        this._refreshValue();
    },

    _createHandles: function() {
        var i, handleCount,
            options = this.options,
            existingHandles = this.element.find( ".ui-slider-handle" ),
            handle = "<span tabindex='0'></span>",
            handles = [];

        handleCount = ( options.values && options.values.length ) || 1;

        if ( existingHandles.length > handleCount ) {
            existingHandles.slice( handleCount ).remove();
            existingHandles = existingHandles.slice( 0, handleCount );
        }

        for ( i = existingHandles.length; i < handleCount; i++ ) {
            handles.push( handle );
        }

        this.handles = existingHandles.add( $( handles.join( "" ) ).appendTo( this.element ) );

        this._addClass( this.handles, "ui-slider-handle", "ui-state-default" );

        this.handle = this.handles.eq( 0 );

        this.handles.each( function( i ) {
            $( this )
                .data( "ui-slider-handle-index", i )
                .attr( "tabIndex", 0 );
        } );
    },

    _createRange: function() {
        var options = this.options;

        if ( options.range ) {
            if ( options.range === true ) {
                if ( !options.values ) {
                    options.values = [ this._valueMin(), this._valueMin() ];
                } else if ( options.values.length && options.values.length !== 2 ) {
                    options.values = [ options.values[ 0 ], options.values[ 0 ] ];
                } else if ( $.isArray( options.values ) ) {
                    options.values = options.values.slice( 0 );
                }
            }

            if ( !this.range || !this.range.length ) {
                this.range = $( "<div>" )
                    .appendTo( this.element );

                this._addClass( this.range, "ui-slider-range" );
            } else {
                this._removeClass( this.range, "ui-slider-range-min ui-slider-range-max" );

                // Handle range switching from true to min/max
                this.range.css( {
                    "left": "",
                    "bottom": ""
                } );
            }
            if ( options.range === "min" || options.range === "max" ) {
                this._addClass( this.range, "ui-slider-range-" + options.range );
            }
        } else {
            if ( this.range ) {
                this.range.remove();
            }
            this.range = null;
        }
    },

    _setupEvents: function() {
        this._off( this.handles );
        this._on( this.handles, this._handleEvents );
        this._hoverable( this.handles );
        this._focusable( this.handles );
    },

    _destroy: function() {
        this.handles.remove();
        if ( this.range ) {
            this.range.remove();
        }

        this._mouseDestroy();
    },

    _mouseCapture: function( event ) {
        var position, normValue, distance, closestHandle, index, allowed, offset, mouseOverHandle,
            that = this,
            o = this.options;

        if ( o.disabled ) {
            return false;
        }

        this.elementSize = {
            width: this.element.outerWidth(),
            height: this.element.outerHeight()
        };
        this.elementOffset = this.element.offset();

        position = { x: event.pageX, y: event.pageY };
        normValue = this._normValueFromMouse( position );
        distance = this._valueMax() - this._valueMin() + 1;
        this.handles.each( function( i ) {
            var thisDistance = Math.abs( normValue - that.values( i ) );
            if ( ( distance > thisDistance ) ||
                ( distance === thisDistance &&
                    ( i === that._lastChangedValue || that.values( i ) === o.min ) ) ) {
                distance = thisDistance;
                closestHandle = $( this );
                index = i;
            }
        } );

        allowed = this._start( event, index );
        if ( allowed === false ) {
            return false;
        }
        this._mouseSliding = true;

        this._handleIndex = index;

        this._addClass( closestHandle, null, "ui-state-active" );
        closestHandle.trigger( "focus" );

        offset = closestHandle.offset();
        mouseOverHandle = !$( event.target ).parents().addBack().is( ".ui-slider-handle" );
        this._clickOffset = mouseOverHandle ? { left: 0, top: 0 } : {
            left: event.pageX - offset.left - ( closestHandle.width() / 2 ),
            top: event.pageY - offset.top -
                ( closestHandle.height() / 2 ) -
                ( parseInt( closestHandle.css( "borderTopWidth" ), 10 ) || 0 ) -
                ( parseInt( closestHandle.css( "borderBottomWidth" ), 10 ) || 0 ) +
                ( parseInt( closestHandle.css( "marginTop" ), 10 ) || 0 )
        };

        if ( !this.handles.hasClass( "ui-state-hover" ) ) {
            this._slide( event, index, normValue );
        }
        this._animateOff = true;
        return true;
    },

    _mouseStart: function() {
        return true;
    },

    _mouseDrag: function( event ) {
        var position = { x: event.pageX, y: event.pageY },
            normValue = this._normValueFromMouse( position );

        this._slide( event, this._handleIndex, normValue );

        return false;
    },

    _mouseStop: function( event ) {
        this._removeClass( this.handles, null, "ui-state-active" );
        this._mouseSliding = false;

        this._stop( event, this._handleIndex );
        this._change( event, this._handleIndex );

        this._handleIndex = null;
        this._clickOffset = null;
        this._animateOff = false;

        return false;
    },

    _detectOrientation: function() {
        this.orientation = ( this.options.orientation === "vertical" ) ? "vertical" : "horizontal";
    },

    _normValueFromMouse: function( position ) {
        var pixelTotal,
            pixelMouse,
            percentMouse,
            valueTotal,
            valueMouse;

        if ( this.orientation === "horizontal" ) {
            pixelTotal = this.elementSize.width;
            pixelMouse = position.x - this.elementOffset.left -
                ( this._clickOffset ? this._clickOffset.left : 0 );
        } else {
            pixelTotal = this.elementSize.height;
            pixelMouse = position.y - this.elementOffset.top -
                ( this._clickOffset ? this._clickOffset.top : 0 );
        }

        percentMouse = ( pixelMouse / pixelTotal );
        if ( percentMouse > 1 ) {
            percentMouse = 1;
        }
        if ( percentMouse < 0 ) {
            percentMouse = 0;
        }
        if ( this.orientation === "vertical" ) {
            percentMouse = 1 - percentMouse;
        }

        valueTotal = this._valueMax() - this._valueMin();
        valueMouse = this._valueMin() + percentMouse * valueTotal;

        return this._trimAlignValue( valueMouse );
    },

    _uiHash: function( index, value, values ) {
        var uiHash = {
            handle: this.handles[ index ],
            handleIndex: index,
            value: value !== undefined ? value : this.value()
        };

        if ( this._hasMultipleValues() ) {
            uiHash.value = value !== undefined ? value : this.values( index );
            uiHash.values = values || this.values();
        }

        return uiHash;
    },

    _hasMultipleValues: function() {
        return this.options.values && this.options.values.length;
    },

    _start: function( event, index ) {
        return this._trigger( "start", event, this._uiHash( index ) );
    },

    _slide: function( event, index, newVal ) {
        var allowed, otherVal,
            currentValue = this.value(),
            newValues = this.values();

        if ( this._hasMultipleValues() ) {
            otherVal = this.values( index ? 0 : 1 );
            currentValue = this.values( index );

            if ( this.options.values.length === 2 && this.options.range === true ) {
                newVal =  index === 0 ? Math.min( otherVal, newVal ) : Math.max( otherVal, newVal );
            }

            newValues[ index ] = newVal;
        }

        if ( newVal === currentValue ) {
            return;
        }

        allowed = this._trigger( "slide", event, this._uiHash( index, newVal, newValues ) );

        // A slide can be canceled by returning false from the slide callback
        if ( allowed === false ) {
            return;
        }

        if ( this._hasMultipleValues() ) {
            this.values( index, newVal );
        } else {
            this.value( newVal );
        }
    },

    _stop: function( event, index ) {
        this._trigger( "stop", event, this._uiHash( index ) );
    },

    _change: function( event, index ) {
        if ( !this._keySliding && !this._mouseSliding ) {

            //store the last changed value index for reference when handles overlap
            this._lastChangedValue = index;
            this._trigger( "change", event, this._uiHash( index ) );
        }
    },

    value: function( newValue ) {
        if ( arguments.length ) {
            this.options.value = this._trimAlignValue( newValue );
            this._refreshValue();
            this._change( null, 0 );
            return;
        }

        return this._value();
    },

    values: function( index, newValue ) {
        var vals,
            newValues,
            i;

        if ( arguments.length > 1 ) {
            this.options.values[ index ] = this._trimAlignValue( newValue );
            this._refreshValue();
            this._change( null, index );
            return;
        }

        if ( arguments.length ) {
            if ( $.isArray( arguments[ 0 ] ) ) {
                vals = this.options.values;
                newValues = arguments[ 0 ];
                for ( i = 0; i < vals.length; i += 1 ) {
                    vals[ i ] = this._trimAlignValue( newValues[ i ] );
                    this._change( null, i );
                }
                this._refreshValue();
            } else {
                if ( this._hasMultipleValues() ) {
                    return this._values( index );
                } else {
                    return this.value();
                }
            }
        } else {
            return this._values();
        }
    },

    _setOption: function( key, value ) {
        var i,
            valsLength = 0;

        if ( key === "range" && this.options.range === true ) {
            if ( value === "min" ) {
                this.options.value = this._values( 0 );
                this.options.values = null;
            } else if ( value === "max" ) {
                this.options.value = this._values( this.options.values.length - 1 );
                this.options.values = null;
            }
        }

        if ( $.isArray( this.options.values ) ) {
            valsLength = this.options.values.length;
        }

        this._super( key, value );

        switch ( key ) {
            case "orientation":
                this._detectOrientation();
                this._removeClass( "ui-slider-horizontal ui-slider-vertical" )
                    ._addClass( "ui-slider-" + this.orientation );
                this._refreshValue();
                if ( this.options.range ) {
                    this._refreshRange( value );
                }

                // Reset positioning from previous orientation
                this.handles.css( value === "horizontal" ? "bottom" : "left", "" );
                break;
            case "value":
                this._animateOff = true;
                this._refreshValue();
                this._change( null, 0 );
                this._animateOff = false;
                break;
            case "values":
                this._animateOff = true;
                this._refreshValue();

                // Start from the last handle to prevent unreachable handles (#9046)
                for ( i = valsLength - 1; i >= 0; i-- ) {
                    this._change( null, i );
                }
                this._animateOff = false;
                break;
            case "step":
            case "min":
            case "max":
                this._animateOff = true;
                this._calculateNewMax();
                this._refreshValue();
                this._animateOff = false;
                break;
            case "range":
                this._animateOff = true;
                this._refresh();
                this._animateOff = false;
                break;
        }
    },

    _setOptionDisabled: function( value ) {
        this._super( value );

        this._toggleClass( null, "ui-state-disabled", !!value );
    },

    //internal value getter
    // _value() returns value trimmed by min and max, aligned by step
    _value: function() {
        var val = this.options.value;
        val = this._trimAlignValue( val );

        return val;
    },

    //internal values getter
    // _values() returns array of values trimmed by min and max, aligned by step
    // _values( index ) returns single value trimmed by min and max, aligned by step
    _values: function( index ) {
        var val,
            vals,
            i;

        if ( arguments.length ) {
            val = this.options.values[ index ];
            val = this._trimAlignValue( val );

            return val;
        } else if ( this._hasMultipleValues() ) {

            // .slice() creates a copy of the array
            // this copy gets trimmed by min and max and then returned
            vals = this.options.values.slice();
            for ( i = 0; i < vals.length; i += 1 ) {
                vals[ i ] = this._trimAlignValue( vals[ i ] );
            }

            return vals;
        } else {
            return [];
        }
    },

    // Returns the step-aligned value that val is closest to, between (inclusive) min and max
    _trimAlignValue: function( val ) {
        if ( val <= this._valueMin() ) {
            return this._valueMin();
        }
        if ( val >= this._valueMax() ) {
            return this._valueMax();
        }
        var step = ( this.options.step > 0 ) ? this.options.step : 1,
            valModStep = ( val - this._valueMin() ) % step,
            alignValue = val - valModStep;

        if ( Math.abs( valModStep ) * 2 >= step ) {
            alignValue += ( valModStep > 0 ) ? step : ( -step );
        }

        // Since JavaScript has problems with large floats, round
        // the final value to 5 digits after the decimal point (see #4124)
        return parseFloat( alignValue.toFixed( 5 ) );
    },

    _calculateNewMax: function() {
        var max = this.options.max,
            min = this._valueMin(),
            step = this.options.step,
            aboveMin = Math.round( ( max - min ) / step ) * step;
        max = aboveMin + min;
        if ( max > this.options.max ) {

            //If max is not divisible by step, rounding off may increase its value
            max -= step;
        }
        this.max = parseFloat( max.toFixed( this._precision() ) );
    },

    _precision: function() {
        var precision = this._precisionOf( this.options.step );
        if ( this.options.min !== null ) {
            precision = Math.max( precision, this._precisionOf( this.options.min ) );
        }
        return precision;
    },

    _precisionOf: function( num ) {
        var str = num.toString(),
            decimal = str.indexOf( "." );
        return decimal === -1 ? 0 : str.length - decimal - 1;
    },

    _valueMin: function() {
        return this.options.min;
    },

    _valueMax: function() {
        return this.max;
    },

    _refreshRange: function( orientation ) {
        if ( orientation === "vertical" ) {
            this.range.css( { "width": "", "left": "" } );
        }
        if ( orientation === "horizontal" ) {
            this.range.css( { "height": "", "bottom": "" } );
        }
    },

    _refreshValue: function() {
        var lastValPercent, valPercent, value, valueMin, valueMax,
            oRange = this.options.range,
            o = this.options,
            that = this,
            animate = ( !this._animateOff ) ? o.animate : false,
            _set = {};

        if ( this._hasMultipleValues() ) {
            this.handles.each( function( i ) {
                valPercent = ( that.values( i ) - that._valueMin() ) / ( that._valueMax() -
                    that._valueMin() ) * 100;
                _set[ that.orientation === "horizontal" ? "left" : "bottom" ] = valPercent + "%";
                $( this ).stop( 1, 1 )[ animate ? "animate" : "css" ]( _set, o.animate );
                if ( that.options.range === true ) {
                    if ( that.orientation === "horizontal" ) {
                        if ( i === 0 ) {
                            that.range.stop( 1, 1 )[ animate ? "animate" : "css" ]( {
                                left: valPercent + "%"
                            }, o.animate );
                        }
                        if ( i === 1 ) {
                            that.range[ animate ? "animate" : "css" ]( {
                                width: ( valPercent - lastValPercent ) + "%"
                            }, {
                                queue: false,
                                duration: o.animate
                            } );
                        }
                    } else {
                        if ( i === 0 ) {
                            that.range.stop( 1, 1 )[ animate ? "animate" : "css" ]( {
                                bottom: ( valPercent ) + "%"
                            }, o.animate );
                        }
                        if ( i === 1 ) {
                            that.range[ animate ? "animate" : "css" ]( {
                                height: ( valPercent - lastValPercent ) + "%"
                            }, {
                                queue: false,
                                duration: o.animate
                            } );
                        }
                    }
                }
                lastValPercent = valPercent;
            } );
        } else {
            value = this.value();
            valueMin = this._valueMin();
            valueMax = this._valueMax();
            valPercent = ( valueMax !== valueMin ) ?
                    ( value - valueMin ) / ( valueMax - valueMin ) * 100 :
                    0;
            _set[ this.orientation === "horizontal" ? "left" : "bottom" ] = valPercent + "%";
            this.handle.stop( 1, 1 )[ animate ? "animate" : "css" ]( _set, o.animate );

            if ( oRange === "min" && this.orientation === "horizontal" ) {
                this.range.stop( 1, 1 )[ animate ? "animate" : "css" ]( {
                    width: valPercent + "%"
                }, o.animate );
            }
            if ( oRange === "max" && this.orientation === "horizontal" ) {
                this.range.stop( 1, 1 )[ animate ? "animate" : "css" ]( {
                    width: ( 100 - valPercent ) + "%"
                }, o.animate );
            }
            if ( oRange === "min" && this.orientation === "vertical" ) {
                this.range.stop( 1, 1 )[ animate ? "animate" : "css" ]( {
                    height: valPercent + "%"
                }, o.animate );
            }
            if ( oRange === "max" && this.orientation === "vertical" ) {
                this.range.stop( 1, 1 )[ animate ? "animate" : "css" ]( {
                    height: ( 100 - valPercent ) + "%"
                }, o.animate );
            }
        }
    },

    _handleEvents: {
        keydown: function( event ) {
            var allowed, curVal, newVal, step,
                index = $( event.target ).data( "ui-slider-handle-index" );

            switch ( event.keyCode ) {
                case $.ui.keyCode.HOME:
                case $.ui.keyCode.END:
                case $.ui.keyCode.PAGE_UP:
                case $.ui.keyCode.PAGE_DOWN:
                case $.ui.keyCode.UP:
                case $.ui.keyCode.RIGHT:
                case $.ui.keyCode.DOWN:
                case $.ui.keyCode.LEFT:
                    event.preventDefault();
                    if ( !this._keySliding ) {
                        this._keySliding = true;
                        this._addClass( $( event.target ), null, "ui-state-active" );
                        allowed = this._start( event, index );
                        if ( allowed === false ) {
                            return;
                        }
                    }
                    break;
            }

            step = this.options.step;
            if ( this._hasMultipleValues() ) {
                curVal = newVal = this.values( index );
            } else {
                curVal = newVal = this.value();
            }

            switch ( event.keyCode ) {
                case $.ui.keyCode.HOME:
                    newVal = this._valueMin();
                    break;
                case $.ui.keyCode.END:
                    newVal = this._valueMax();
                    break;
                case $.ui.keyCode.PAGE_UP:
                    newVal = this._trimAlignValue(
                        curVal + ( ( this._valueMax() - this._valueMin() ) / this.numPages )
                    );
                    break;
                case $.ui.keyCode.PAGE_DOWN:
                    newVal = this._trimAlignValue(
                        curVal - ( ( this._valueMax() - this._valueMin() ) / this.numPages ) );
                    break;
                case $.ui.keyCode.UP:
                case $.ui.keyCode.RIGHT:
                    if ( curVal === this._valueMax() ) {
                        return;
                    }
                    newVal = this._trimAlignValue( curVal + step );
                    break;
                case $.ui.keyCode.DOWN:
                case $.ui.keyCode.LEFT:
                    if ( curVal === this._valueMin() ) {
                        return;
                    }
                    newVal = this._trimAlignValue( curVal - step );
                    break;
            }

            this._slide( event, index, newVal );
        },
        keyup: function( event ) {
            var index = $( event.target ).data( "ui-slider-handle-index" );

            if ( this._keySliding ) {
                this._keySliding = false;
                this._stop( event, index );
                this._change( event, index );
                this._removeClass( $( event.target ), null, "ui-state-active" );
            }
        }
    }
} );
}));