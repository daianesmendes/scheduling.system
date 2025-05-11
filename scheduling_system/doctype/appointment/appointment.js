frappe.ui.form.on('Appointment', {
    refresh: function(frm) {
        frm.add_custom_button(__('Ver Compromissos'), function() {
            frappe.set_route('List', 'Appointment', {'view': 'Calendar'});
        });

        if (frm.doc.status === 'Scheduled' && frm.doc.end_date < frappe.datetime.now_datetime()) {
            frm.set_df_property('status', 'read_only', 1);  // Bloqueia a alteração de status se já passou o horário
            frappe.msgprint(__('Este compromisso já passou e não pode ser alterado.'));
        }
    },

    start_date: function(frm) {
        // Atualiza a data de término automaticamente quando a data de início for alterada
        if (frm.doc.start_date && frm.doc.duration) {
            const end_date = frappe.datetime.add_days(frm.doc.start_date, frm.doc.duration);
            frm.set_value('end_date', end_date);
        }
    }
});
