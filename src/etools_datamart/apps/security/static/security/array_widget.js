$('.dynamic-array-widget').each(function() {
    $(this).find('.add-array-item').click((function($last) {
        return function() {
            var $new = $last.clone();
            var id_parts = $new.find('input').attr('id').split('_');
            var id = id_parts.slice(0, -1).join('_') + '_' + String(parseInt(id_parts.slice(-1)[0]) + 1);
            $new.find('input').attr('id', id);
            $new.find('input').prop('value', '');
            $new.insertAfter($last);
        };
    })($(this).find('.array-item').last()));
});
