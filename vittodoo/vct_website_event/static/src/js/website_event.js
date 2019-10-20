odoo.define('vct_website_event.website_event', function (require) {

    var ajax = require('web.ajax');
    var Widget = require('web.Widget');
    var web_editor_base = require('web_editor.base')

// Catch registration form event, because of JS for attendee details
    var EventRegistrationForm = Widget.extend({
        start: function() {
            console.log("start")
            var self = this;
            var res = this._super.apply(this.arguments).then(function() {
                $('#registration_form2 .a-submit')
                    .off('click')
                    .removeClass('a-submit')
                    .click(function (ev) {
                        self.on_click(ev);
                    });
            });
            return res
        },
        on_click: function(ev) {
            console.log("on_click")
            ev.preventDefault();
            ev.stopPropagation();
            var $form = $(ev.currentTarget).closest('form');
            var post = {};
            $("#registration_form2 select").each(function() {
                post[$(this).attr('name')] = $(this).val();
            });
            return ajax.jsonRpc($form.attr('action'), 'call', post).then(function (modal) {
                var $modal = $(modal);
                $form.addClass('hidden')
                $form.after($modal)
                $modal.on('click', '.js_goto_event', function () {
                    $form.removeClass('hidden')
                    $modal.remove()
                });
            });
        },
    });

    web_editor_base.ready().then(function(){
        var event_registration_form = new EventRegistrationForm().appendTo($('#registration_form2'));
    });

    return { EventRegistrationForm: EventRegistrationForm };

});