require([
    'underscore',
    'jquery',
    'splunkjs/mvc',
    'splunkjs/mvc/simplexml/ready!'
], function(_, $, mvc) {

    var defaultTokenModel = mvc.Components.get('default');

    // Watch for the 'show_drawer' token to trigger the Modal Popup
    defaultTokenModel.on('change:show_drawer', function(model, value) {
        if (value === 'true' || value === true) {
            showModal();
        } else {
            hideModal();
        }
    });

    function showModal() {
        // Prevent duplicate overlays
        if ($('#splunk_custom_modal_overlay').length > 0) {
            $('#splunk_custom_modal_overlay').show();
            return;
        }

        // Target the existing drawer panel in Simple XML and wrap it into a floating modal
        var $drawerPanel = $('[depends="$show_drawer$"]').first();

        var overlayHtml = 
            '<div id="splunk_custom_modal_overlay" style="position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(0, 0, 0, 0.75); z-index: 9999; display: flex; align-items: center; justify-content: center;">' +
                '<div id="splunk_custom_modal_content" style="background: #1e252b; width: 85vw; max-height: 85vh; border-radius: 8px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); display: flex; flex-direction: column; overflow: hidden; border: 1px solid #3c444d;">' +
                    '<div id="modal_header" style="padding: 12px 20px; background: #11171d; border-bottom: 1px solid #3c444d; display: flex; justify-content: space-between; align-items: center;">' +
                        '<h3 style="margin: 0; color: #ffffff; font-weight: 500;">Drilldown Details</h3>' +
                        '<button id="close_custom_modal_btn" style="background: transparent; border: none; color: #a0a0a0; font-size: 20px; cursor: pointer; line-height: 1;">&times;</button>' +
                    '</div>' +
                    '<div id="modal_body" style="padding: 20px; overflow-y: auto; flex: 1;">' +
                    '</div>' +
                '</div>' +
            '</div>';

        $('body').append(overlayHtml);

        // Move the drawer contents into the modal body
        $drawerPanel.appendTo('#modal_body');

        // Attach event listener to close modal
        $('#close_custom_modal_btn').on('click', function() {
            defaultTokenModel.set('show_drawer', undefined);
            // Reset individual view tokens
            defaultTokenModel.set('show_host_benchmarks', undefined);
            defaultTokenModel.set('show_rule_details', undefined);
            defaultTokenModel.set('show_sev_rules', undefined);
            defaultTokenModel.set('show_status_rules', undefined);
            defaultTokenModel.set('show_regression_rules', undefined);
            defaultTokenModel.set('show_rule_hosts', undefined);
        });
    }

    function hideModal() {
        $('#splunk_custom_modal_overlay').hide();
    }
});