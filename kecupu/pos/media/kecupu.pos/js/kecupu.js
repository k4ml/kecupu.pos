$(document).ready(function() {
    $("#txt-customer-search").autocomplete({
        source: "/customer/autocomplete",
        minLength: 2,
        select: function(event, ui) {
            $("#txt-customer-search").val(ui.item.value + "-" + ui.item.label);
            return false;
        }
    });

    $("#txt-item-search").autocomplete({
        source: "/item/autocomplete",
        minLength: 2,
        select: function(event, ui) {
            $("#txt-item-search").val(ui.item.value + "-" + ui.item.label);
            return false;
        }
    });
});
