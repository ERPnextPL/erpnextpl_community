<table width="100%" cellpadding="0" cellspacing="0" border="0" 
       style="font-family: Arial, Helvetica, sans-serif; color:#222; line-height:1.5;">
  <tr>
    <td>

      <p style="margin:0 0 12px 0;">Szanowni Państwo,</p>

      <p style="margin:0 0 12px 12px;">
        Informujemy, że poniższy dokument magazynowy posiada 
        <strong>oczekujące wydanie towaru</strong> i nie został jeszcze zrealizowany.
      </p>

      <table cellpadding="6" cellspacing="0" border="0" 
             style="background:#f7f7f7; border:1px solid #ddd; margin:12px 0; font-size:14px; width:100%;">
        <tr>
          <td><strong>Typ dokumentu:</strong></td>
          <td>{{ doc.doctype }}</td>
        </tr>
        <tr>
          <td><strong>Numer dokumentu:</strong></td>
          <td>{{ doc.name }}</td>
        </tr>
        <tr>
          <td><strong>Data utworzenia:</strong></td>
          <td>{{ doc.posting_date }}</td>
        </tr>
        <tr>
          <td><strong>Status:</strong></td>
          <td>{{ doc.status }}</td>
        </tr>
        {% if doc.customer %}
        <tr>
          <td><strong>Klient:</strong></td>
          <td>{{ doc.customer }}</td>
        </tr>
        {% endif %}
        {% if doc.purpose %}
        <tr>
          <td><strong>Cel dokumentu:</strong></td>
          <td>{{ doc.purpose }}</td>
        </tr>
        {% endif %}
      </table>

      <p style="margin:16px 0 8px 0;"><strong>Pozycje oczekujące na wydanie:</strong></p>

      {% for item in doc.items %}
      {% if item.qty != item.delivered_qty or item.delivered_qty == None %}
      <table cellpadding="6" cellspacing="0" border="0"
             style="background:#fff; border:1px solid #ddd; margin:12px 0; font-size:14px; width:100%;">
        <tr>
          <td><strong>Produkt:</strong></td>
          <td>{{ item.item_code }} – {{ item.item_name }}</td>
        </tr>
        <tr>
          <td><strong>Ilość do wydania:</strong></td>
          <td>{{ item.qty }}</td>
        </tr>
        <tr>
          <td><strong>Ilość już wydana:</strong></td>
          <td>{{ item.delivered_qty or 0 }}</td>
        </tr>
        <tr>
          <td><strong>Pozostała ilość:</strong></td>
          <td>{{ item.qty - (item.delivered_qty or 0) }}</td>
        </tr>
      </table>
      {% endif %}
      {% endfor %}

      <p style="margin:0 0 18px 0;">
        Prosimy o przygotowanie i wydanie towaru zgodnie z dokumentem.  
      </p>

    </td>
  </tr>
</table>
