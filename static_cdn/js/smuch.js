setTimeout(function() { 
    if (!UI.USER.id) return;
    var ver = '1',
        key = 'user#' + UI.USER.id;
    key = ver + '.modal-suggest-social.' + key;
    var dtlast = parseFloat($.storage(key)) || 0,
        dtnow = +new Date(),
        interval = 1000 * 86400 * 14; // не чаще, чем раз в две недели
    if (dtnow - dtlast < interval) return;

    var chainctl = $.Chain.unwanted.ctl('socad.popup');
    $('#modal-suggest-social').on({
        'show.bs.modal': chainctl.lock,
        'hide.bs.modal': chainctl.unlock,
    });

    chainctl.enqueue(function() {
        $('#modal-suggest-social').promisedModal({ clone: false }).then(function() {
            $.storage(key, Number.MAX_VALUE);
        }, function() {
            $.storage(key, dtnow);
        });
    });
}, 60000);

$('#modal-logreg').on('mousedown', '.save-location', function() {
    UI.request({
        u: 'https://smotriuchis.ru/form/ret',
        d: { 'ret': window.location.href },
        c: function() { return false; }
    });
});
(function() {
    var socid2name = {"fb":"Facebook","vk":"\u0412\u041a\u043e\u043d\u0442\u0430\u043a\u0442\u0435","ok":"\u041e\u0434\u043d\u043e\u043a\u043b\u0430\u0441\u0441\u043d\u0438\u043a\u0438","mr":"Mail.Ru","ya":"Yandex","tw":"Twitter","gl":"Google","ig":"Instagram"};
    $('#wdgsocauth-login').on('mousedown', '[socid]', function() {
        var socid = $(this).attr('socid');
        xstatAction.userLogin(socid2name[socid]);
    });
    $('#wdgsocauth-register').on('mousedown', '[socid]', function() {
        var socid = $(this).attr('socid');
        xstatAction.userRegister(socid2name[socid]);
    });
})();


(function() {
    var mkFlowDeferred = function(preventDefault, cb) {
        var deferred = $.Deferred();
        cb = cb || function() {};
        deferred.always(cb);
        if (!preventDefault) deferred.done(function(type, result) {
            if (result && (result.type == 'success')) UI.reload(true);
        });
        return deferred;
    };

    var flowDeferred = mkFlowDeferred(),
        returnToMain = true,         returnToOrg = false,         hideReject = true; 
var UI_logreg = {
    $elts: {
        //socLogin: $('#wdgsocauth-login'),
        iLogin: $('#modal-logreg-login').find('iframe'),
        //socRegister: $('#wdgsocauth-register'),
        iRegister: $('#modal-logreg-register').find('iframe')
    },
    xstat: {
        login: 'login',
        register: 'register',
        current: {},
        passed: {},
        defaults: {
            login: 'button#entermyaccount',
            register: false
        }
    },
    loaded: false,
    open: function(goRegister, preventDefault, xstatOpts) {
        flowDeferred = mkFlowDeferred(preventDefault, function (type) {
            UI_logreg.xstat.current = {};
            // Аналитика
            if (type == 'login') xstatAction.userLogin('email');
            else if (type == 'register') xstatAction.userRegister('email');
        });
        UI_logreg.needRefresh = true;
        UI_logreg.xstat.passed = xstatOpts || {};
        $('#modal-logreg').modal('show');


        if (goRegister || (UI.USER && !UI.USER.hid)) $('#modal-logreg [marker=go-register]').click();
        else $('#modal-logreg [marker=go-login]').click();
        UI_logreg.mkXstat();
        return flowDeferred.promise();
    },
    openOrg: function(goRegister, preventDefault) {
        flowDeferred = mkFlowDeferred(preventDefault);
        $('#modal-orglogreg').modal('show');
        if (goRegister) $('#modal-orglogreg [marker=go-register]').click();
        else $('#modal-orglogreg [marker=go-login]').click();
        return flowDeferred.promise();
    },
    _whenIFrame: function($iframe) {
        var src = $iframe.attr('data-src'),
            deferred = $iframe.data('deferred');
        if (!deferred) {
            deferred = $.Deferred();
            $iframe.data('deferred', deferred);
            $iframe.on('load', function() { deferred.resolve(); });
        }
        if (src) $iframe.attr('src', src); // загрузить содержимое нужно сразу
        return deferred.promise();
    },
    _whenReady: function() {
        if (!UI_logreg.needRefresh) return $.Deferred().reject().promise();
        if (UI_logreg.loaded) return $.when();
        return $.when(
            UI_logreg._whenIFrame(UI_logreg.$elts.iLogin),
            UI_logreg._whenIFrame(UI_logreg.$elts.iRegister)
        ).done(function() {
            UI_logreg.loaded = true;
        });
    },
    xstatValues: function() {
        var xstat = UI_logreg.xstat;
        xstat.current = $.extend({}, xstat.defaults, xstat.current, xstat.passed);
        return xstat.current;
    },
    mkXstat: function() {
        UI_logreg._whenReady().then(function() {
            var xstat = UI_logreg.xstatValues(),
                $elts = UI_logreg.$elts;
            if (xstat.login) {
                //$elts.socLogin.attr('data-xstat-id', xstat.login);
                $elts.iLogin.contents().find(':submit').attr('data-xstat-id', xstat.login);
            } else {
                //$elts.socLogin.removeAttr('data-xstat-id');
                $elts.iLogin.contents().find(':submit').removeAttr('data-xstat-id');
            }
            if (xstat.register) {
                //$elts.socRegister.attr('data-xstat-id', xstat.register);
                $elts.iRegister.contents().find(':submit').attr('data-xstat-id', xstat.register);
            } else {
                //$elts.socRegister.removeAttr('data-xstat-id');
                $elts.iRegister.contents().find(':submit').removeAttr('data-xstat-id');
            }
            UI_logreg.needRefresh = false;
        });
    },
};
window.UI_logreg = UI_logreg;

MSG.on('modal-passlost', function(data) {     hideReject = false;
    $('.modal:not(#modal-passlost)').modal('hide');
    $('#modal-passlost').modal('show');
});
MSG.on('notify-register-success', function(result) {     hideReject = false;
    $('#modal-logreg').modal('hide');
    UI.notify({
        title: 'Запрос отправлен',
        message: 'На ваш электронный адрес выслана ссылка. Пройдите по ней, чтобы подтвердить регистрацию.'
    }).always(function() {
        UI.filterRegister(result).then(function() {
            flowDeferred.resolve('register', result);
        });
    });
    try { fbq('track', 'CompleteRegistration'); } catch (e) {} // М -- Маркетологи (не XSTAT)
});
MSG.on('notify-orgregister-success', function(result) {     hideReject = false;
    $('#modal-orglogreg').modal('hide');
    UI.notify({
        title: 'Запрос отправлен',
        message: 'На ваш электронный адрес выслана ссылка. Пройдите по ней, чтобы подтвердить регистрацию.'
    }).always(function() {
        UI.filterRegister(result).then(function() {
            flowDeferred.resolve('register', result);
        });
    });
});
MSG.on('notify-orgcreate-success', function(result) {     hideReject = false;
    $('#modal-orglogreg').modal('hide');
    flowDeferred.resolve('register', result);
});
MSG.on('notify-login-success', function(result) {     hideReject = false;
    $('#modal-logreg').modal('hide');
    flowDeferred.resolve('login', result);
});
MSG.on('notify-orglogin-success', function(result) {     hideReject = false;
    $('#modal-orglogreg').modal('hide');
    flowDeferred.resolve('login', result);
});
MSG.on('notify-passlost-success', function(result) {     returnToMain = false;
    hideReject = false;
    $('#modal-passlost').modal('hide');
    UI.notify({
        title: 'Запрос отправлен',
        message: 'На ваш электронный адрес выслана ссылка. Пройдите по ней, чтобы восстановить пароль.'
    }).always(function() {
        flowDeferred.reject('passlost', result);
    });
    return false;
});
MSG.on('notify-passlost-dismiss', function() {     $('#modal-passlost').modal('hide');
    return false;
});
$('#modal-logreg').on('show.bs.modal', function() {
    returnToMain = true;
    hideReject = true;
});
$('#modal-orglogreg').on('show.bs.modal', function() {
    returnToMain = false;
    returnToOrg = true;
    hideReject = true;
    $('.loading-process').toggleClass('hidden', false);
    $('#modal-orglogreg-register').find('iframe').on('load', function(e) {
        $('.loading-process').toggleClass('hidden', true);
    });
    $('#modal-orglogreg-register').find('iframe').attr('src', $('#modal-orglogreg-register').find('iframe').attr('src'));
});
$('#modal-logreg').on('hide.bs.modal', function(event) {
    if (hideReject) flowDeferred.reject('cancel', {});
});
$('#modal-orglogreg').on('hide.bs.modal', function(event) {
    if (hideReject) flowDeferred.reject('cancel', {});
});
$('#modal-passlost').on('hide.bs.modal', function() {
    if (returnToMain) $('#modal-logreg').modal('show');
    if (returnToOrg) $('#modal-orglogreg').modal('show');
});

$(window).on('hashnav.hashnav', function(event, hash) {
    if (($.type(hash) == 'string') && hash == 'logreg') {
        UI_logreg.open();
        return false;
    }
});

})();


$.modals.regDone = (function() {
    var $modal = $('#modal-reg-done'),
        handler = $.noop;
    $modal.on('href-check', '[data-marker="share"]', function(evt, result) {
        handler();
    });
    MSG.on('soccbdone', function(data) {
        handler();
    });
    return function(data) {
        var share = data && data['share'];
        if (!share) return $.Deferred().reject().promise();
        return $modal.promisedModal({
            clone: false,
            defaultResolve: false,
            beforeStart: function() {
                var crs = data && data['crs'] && data['crs'].shift();
                this.find('[data-marker="crs_name"]').html(crs ? ['&laquo;', $('<span>').text(crs['name']), '&raquo;'] : '');
                                var targets = share['targets'] || [],
                    $btns = this.find('[data-marker="share"]'),
                    soc;
                $btns.empty();
                for (var i = 0; i < targets.length; ++i) {
                    if (!(soc = share[targets[i]])) continue;
                    $('<a makepopup>').attr({
                        socid: soc['socid'],
                        href: soc['href'],
                        'href-check': soc['soccb'] || null,
                        target: '_blank',
                        title: soc['title'] || soc['socid']
                    }).appendTo($btns);
                }
                handler = (function() {
                    this.setDismiss(null, true, null).modal('hide');
                }).bind(this);
            }
        }).always(function() {
            handler = $.noop;
        });
    };
})();
$.modals.regShareDone = (function() {
    var $modal = $('#modal-reg-share-done');
    return function(data) {
        return $modal.promisedModal({
            clone: false,
            defaultResolve: false,
            beforeStart: function() {
                var crs = data && data['crs'] && data['crs'].shift();
                this.find('[data-marker="crs_name"]').html(crs ? ['&laquo;', $('<span>').text(crs['name']), '&raquo;'] : '');
                this.find('[data-marker="crs_href"]').attr('href', crs ? crs['href'] : 'https://smotriuchis.ru/moi-kursy');
            }
        });
    };
})();
