$(document).ready(function() {
    $("#questionnaireline_set-group tbody td.original p").hide();
    $("#questionnaireline_set-group tbody tr.has_original td").css("padding-top","0.75em");
    $("#questionnaireline_set-group tbody tr input[name$='-position']").hide()
    var pos=1
    $("#questionnaireline_set-group tbody tr.has_original").each(function(index){
        input = $(this).find("input[name$='-position']");
        input.attr('value', pos);
        pos=pos+1
        icon = $('<span class="ui-icon ui-icon-arrowthick-2-n-s"  style="float:left;"></span>');
        label = $('<strong style="float:left;padding:1px">' + input.attr('value') + '</span>');
        input.parent().append(icon).append(label);
    });
    $("#questionnaireline_set-group tbody").sortable({
        items:".has_original",
        cursor: 'move',
        update: function(event, ui) {
            items = $(this).find('tr.has_original').get();
            $(items).each(function(index) {
                input = $(this).find("input[name$='-position']").first();
                input.attr('value', index+1);
                input.parent().children('strong').first().text(index+1);
            });
            // Update row classes
            $(this).find('tr').removeClass('row1').removeClass('row2');
            $(this).find('tr:even').addClass('row1');
            $(this).find('tr:odd').addClass('row2');
        }
    }).disableSelection();
});
