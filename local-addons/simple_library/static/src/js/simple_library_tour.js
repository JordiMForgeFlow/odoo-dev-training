odoo.define('simple_library.tour', function (require) {
    "use strict";

    var core = require('web.core');
    var tour = require('web_tour.tour');

    var _t = core._t;

    tour.register('library_tour', {
        url: "/web",
        rainbowManMessage: "Congratulations, you are now a master of library management.",
        }, [tour.stepUtils.showAppsMenuItem(), {
            trigger: '.o_app[data-menu-xmlid="simple_library.library_base_menu"]',
            content: _t('Manage books and authors in <b>Library app</b>.'),
            position: 'right'
            }, {
            trigger: '.o_list_button_add',
            content: _t("Let's create a new book."),
            position: 'bottom'
            }, {
            trigger: 'input[name="name"]',
            extra_trigger: '.o_form_editable',
            content: _t('Set the book title'),
            position: 'right'
            }, {
            trigger: '.o_int_colorpicker',
            extra_trigger: '.o_form_editable',
            content: _t('Set the book color'),
            position: 'right'
            }, {
            trigger: '.o_form_button_save',
            content: _t('Save this book record'),
            position: 'bottom',
            }
        ]);
});