;(function($) {
    $(function(){

        $(document).ready(function() {

            $( ".multi-widget" ).each(function( index ) {
                var field_ids = [], field_names = [];
                var dt = '', dd = '';

                // loop over currect languagefields
                $(this).find( ".multi-widget-field" ).each(function( index ) {
                  field_ids.push($( this ).attr('id'));
                  field_names.push($( this ).find(":selected").text());
                });
                console.log(field_ids);
                console.log(this);
                // make header
                $(field_ids).each(function( index, value) {
                    dt += '<dt id="fieldsetlegend-' + value +'">' + field_names[index] + '</dt>';
                });
                // copy over html for content
                $(field_ids).each(function( index, value) {
                    dd += '<dd id="fieldset-' + value +'"> '+ $('#'+value).html() +' </dd>';
                });
                // put it all together
                $(this).prepend(
                    '<dl class="enableFormTabbing multilingualtabbing">' + dt + dd + '</dl>'
                );
            });
            // enable tabbing
            $('body').each(function() {
                var item = $(this);
                item.find("dl.multilingualtabbing").each(ploneFormTabbing.initializeDL);

                //Select tab if it's part of the URL or designated in a hidden input
                var targetPane = item.find('.enableFormTabbing input[name="fieldset"]').val() || window.location.hash;
                if (targetPane) {
                    item.find('.enableFormTabbing .formTabs [id="' +
                     targetPane.replace('#','').replace('"', '').replace(/^fieldset-/, "fieldsetlegend-") + '"]').click();
                }

            });

            // remove existing fields
            $('.multi-widget-field').remove();
            // remove unused fields
            $('.multi-widget select, .multi-widget label, .multi-widget br').hide();
            // remove unused buttons
            $('.multi-widget-buttons').remove();
            // remove remove checkbox
            $( ".multi-widget input:checkbox" ).remove();

        });
    });
}(jQuery));
