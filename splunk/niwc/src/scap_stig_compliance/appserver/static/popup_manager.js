require([
    'underscore',
    'jquery',
    'splunkjs/mvc',
    'splunkjs/mvc/tableview',
    'splunkjs/mvc/simplexml/ready!'
], function(_, $, mvc, TableView) {

    // Get reference to the compliance table
    var complianceTable = mvc.Components.get('compliance_table');

    if (complianceTable) {
        complianceTable.on('click', function(e) {
            e.preventDefault();
            
            // Extract click context from event
            var rowData = e.data; // Contains all fields for the clicked row
            
            var host = rowData['row.host'] || rowData['host'] || 'N/A';
            var ruleId = rowData['row.rule_id'] || rowData['rule_id'] || 'N/A';
            var title = rowData['row.title'] || rowData['title'] || 'N/A';
            var status = rowData['row.status'] || rowData['status'] || 'N/A';
            var severity = rowData['row.severity'] || rowData['severity'] || 'N/A';
            var description = rowData['row.description'] || rowData['description'] || 'No detailed description provided.';

            // Render popup with scope header and body
            renderModal(host, ruleId, title, status, severity, description);
        });
    }

    function renderModal(host, ruleId, title, status, severity, description) {
        // 1. Clear previous content to prevent stale/blank flashes
        $('#modal-container .modal-body').empty();

        // 2. Scope Context Banner (Explaining the scope of what is displayed)
        var scopeBanner = 
            '<div class="popup-scope-header" style="background: #ebf5ff; border-left: 4px solid #0052cc; padding: 10px 14px; margin-bottom: 15px; borderRadius: 3px;">' +
                '<strong style="color: #0052cc; display: block; font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px;">Active Inspection Scope</strong>' +
                '<span style="font-size: 13px; color: #172b4d;">Target Host: <strong>' + _.escape(host) + '</strong> | Rule ID: <strong>' + _.escape(ruleId) + '</strong></span>' +
            '</div>';

        // 3. Main Detail Content
        var contentHtml = 
            scopeBanner +
            '<div class="popup-details">' +
                '<h4 style="margin-top:0;">' + _.escape(title) + '</h4>' +
                '<p><strong>Status:</strong> <span class="badge-' + _.escape(status.toLowerCase()) + '">' + _.escape(status) + '</span> &nbsp;|&nbsp; <strong>Severity:</strong> ' + _.escape(severity) + '</p>' +
                '<hr style="border: 0; border-top: 1px solid #e0e0e0; margin: 12px 0;"/>' +
                '<p><strong>Description & Remediation:</strong></p>' +
                '<div style="background: #f8f9fa; padding: 10px; border-radius: 4px; font-family: monospace; font-size: 12px; max-height: 200px; overflow-y: auto;">' + 
                    _.escape(description) + 
                '</div>' +
            '</div>';

        // 4. Inject and display modal
        $('#modal-container .modal-body').html(contentHtml);
        $('#modal-container').modal('show');
    }
});