<table width="100%" cellpadding="0" cellspacing="0" border="0"
       style="font-family: Arial, Helvetica, sans-serif; color:#222; line-height:1.5;">
  <tr>
    <td>
      <p style="margin:0 0 12px 0;">Szanowni Państwo,</p>

      <p style="margin:0 0 12px 0;">
        Informujemy, że płatność za poniższą fakturę jest 
        <strong>przeterminowana</strong>. Prosimy o jak najszybsze uregulowanie należności.
      </p>

      <table cellpadding="6" cellspacing="0" border="0" 
             style="background:#f7f7f7; border:1px solid #ddd; margin:12px 0; font-size:14px;">
        <tr>
          <td><strong>Numer faktury:</strong></td>
          <td>{{ doc.name }}</td>
        </tr>
        <tr>
          <td><strong>Termin płatności:</strong></td>
          <td>{{ doc.due_date }}</td>
        </tr>
        <tr>
          <td><strong>Kwota zaległości:</strong></td>
          <td>{{ doc.outstanding_amount }} {{ doc.currency }}</td>
        </tr>
        <tr>
          <td><strong>Dni po terminie:</strong></td>
          <td>{{ frappe.utils.date_diff(frappe.utils.nowdate(), doc.due_date) }}</td>
        </tr>
      </table>

      <p style="margin:0 0 18px 0;">
        Uprzejmie prosimy o niezwłoczne dokonanie płatności.  
        Jeżeli należność została już uregulowana, prosimy zignorować tę wiadomość.
      </p>
    </td>
  </tr>
</table>
