function checkFields(form) {
    var checks_radios = form.find(':checkbox, :radio'),
        inputs = form.find(':input').not(checks_radios).not('[type="submit"],[type="button"],[type="reset"]');

    var checked = checks_radios.filter(':checked');
    var filled = inputs.filter(function () {
        return $.trim($(this).val()).length > 0;
    });

    if (checked.length + filled.length === 0) {
        return false;
    }

    return true;
}

$(function () {
    $('#search_form').on('submit', function (e) {
        e.preventDefault();
        var oneFilled = checkFields($(this));

        if (oneFilled) {
            var selected = new Array();
            $(".check-genre:checked").each(function () {
                selected.push($(this).val());

            });

            if (selected.length > 0) {
                document.getElementById("genres").value = selected.toString();
            }

            fields = $(this).find(':input').not(':button, :submit, :reset, :checkbox');

            for (i = 0; i < fields.length; i++) {
                if (fields[i].value == "") {
                    fields[i].removeAttribute("name");
                }
            }

            $(this).unbind('submit').submit();
        } else {
            alert('At least 1 field required!');
        }
    });
});

$(document).ready(function () {
    $('#reset').click(function () {
        $('#search_form').find(':input').not(':button, :submit, :reset, :checkbox').attr('value', '');
        $('#search_form').find(':checkbox').attr('checked', false);

        options = $('#film_type');
        options.find('option').removeAttr("selected");

        $('#default').attr("selected", "selected");
    })


});

function openLink(link) {
    window.open(link, '_blank');
}



