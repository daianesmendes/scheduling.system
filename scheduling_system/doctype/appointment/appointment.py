import frappe
from frappe.model.document import Document
from frappe.utils import get_datetime

class Appointment(Document):
    def validate(self):
        # Validações principais para garantir a integridade do agendamento
        self.validate_appointment_conflict()
        self.calculate_end_date()

    def validate_appointment_conflict(self):
        # Verifica se já existe um compromisso agendado para o vendedor no mesmo horário.
        overlapping_appointments = frappe.db.get_all('Appointment', filters={
            'seller': self.seller,
            'start_date': ['<=', self.end_date],
            'end_date': ['>=', self.start_date],
            'status': 'Scheduled'
        })

        if overlapping_appointments:
            conflict = ', '.join([appt.name for appt in overlapping_appointments])
            frappe.throw(f'Conflito de agendamento para o vendedor. Já existem compromissos em: {conflict}')
    
    def calculate_end_date(self):
        # Calcula a data e hora de término automaticamente com base no horário de início e na duração.
        if self.start_date and self.duration:
            self.end_date = get_datetime(self.start_date) + self.duration
        elif not self.start_date:
            frappe.throw("A data de início (Start Date) é obrigatória.")
        elif not self.duration:
            frappe.throw("A duração (Duration) é obrigatória.")
    
    def on_update(self):
        # Atualiza o status de um compromisso para 'Finished' automaticamente, após a conclusão.
        if self.status == 'Scheduled' and self.end_date < frappe.utils.now():
            self.status = 'Finished'
