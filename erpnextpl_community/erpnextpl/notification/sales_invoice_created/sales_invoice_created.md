<table width="100%" cellpadding="0" cellspacing="0" border="0" 
       style="font-family: Arial, Helvetica, sans-serif; color:#222; line-height:1.5;">
  <tr>
    <td>
      <p style="margin:0 0 12px 0;">Szanowni Państwo,</p>

      <p style="margin:0 0 12px 0;">
        Informujemy, że została utworzona nowa faktura sprzedaży w systemie ERPNext:
      </p>

      <table cellpadding="6" cellspacing="0" border="0" 
             style="background:#f7f7f7; border:1px solid #ddd; margin:12px 0; font-size:14px;">
        <tr>
          <td><strong>Numer faktury:</strong></td>
          <td>{{ doc.name }}</td>
        </tr>
        <tr>
          <td><strong>Data wystawienia:</strong></td>
          <td>{{ doc.posting_date }}</td>
        </tr>
        <tr>
          <td><strong>Kwota:</strong></td>
          <td>{{ doc.grand_total }} {{ doc.currency }}</td>
        </tr>
        <tr>
          <td><strong>Klient:</strong></td>
          <td>{{ doc.customer }}</td>
        </tr>
      </table>
    </td>
  </tr>
</table>
