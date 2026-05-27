# ERPNextPL Community

ERPNextPL Community to lekka aplikacja dla Frappe / ERPNext. Zakres tej edycji obejmuje podstawową polską lokalizację danych, gotowe szablony komunikacji oraz szablony faktur.

## Zakres

- komunikaty walidacji NIP,
- komunikaty podstawowych pól,
- dodatkowe pola na standardowych DocType,
- szablony e-mail,
- szablony faktur,
- powiadomienia.

## Custom Fields

Aplikacja dodaje pola przez patch migracyjny, tylko jeśli ich jeszcze nie ma. Nie używa plików `custom/*.json`, dzięki czemu `bench migrate` nie nadpisuje lokalnych zmian formularzy.

Dodawane pola:

- `Customer`: `REGON`, `KRS`, `PESEL`, `VAT Tax Status`,
- `Sales Invoice`: `service_delivery_date`.

## Walidacje

### Customer

Aplikacja waliduje NIP kontrahenta, gdy:

- `territory` to `Polska` albo `Poland`,
- `customer_type` to `Company`,
- pole `tax_id` jest uzupełnione.

Walidacja sprawdza, czy NIP ma 10 cyfr i poprawną sumę kontrolną. Nie blokuje zapisu dokumentu, tylko pokazuje komunikat ostrzegawczy.

### Sales Invoice

Aplikacja obsługuje podstawowe wartości i walidacje faktury sprzedaży:

- jeśli `service_delivery_date` jest puste, ustawia je na `posting_date`,
- jeśli `due_date` jest puste, ustawia je na `posting_date`,
- blokuje zapis, gdy `due_date` jest wcześniejsze niż `posting_date`.

## Szablony i powiadomienia

Szablony e-mail, szablony faktur i powiadomienia są tworzone przez patch `erpnextpl_community.erpnextpl.patches.create_community_documents`.

Patch działa według zasady:

- jeśli dokument już istnieje, nie jest zmieniany,
- jeśli dokumentu brakuje, jest tworzony z pliku JSON w aplikacji,
- powiadomienia są tworzone jako wyłączone, żeby nie uruchamiać gotowej konfiguracji bez decyzji administratora.

To podejście chroni lokalne modyfikacje szablonów przed nadpisaniem przy `bench migrate`.

## Najważniejsze pliki

- `erpnextpl_community/hooks.py` - aktywne hooki aplikacji,
- `erpnextpl_community/customer.py` - walidacja NIP klienta,
- `erpnextpl_community/sales_invoice.py` - walidacje i wartości domyślne faktury sprzedaży,
- `erpnextpl_community/public/js/erpnextpl_fixes.js` - komunikaty podstawowych pól w UI,
- `erpnextpl_community/erpnextpl/patches/create_community_documents.py` - tworzenie pól, szablonów i powiadomień,
- `erpnextpl_community/erpnextpl/patches/remove_pro_artifacts.py` - sprzątanie artefaktów spoza zakresu Community.

## Instalacja

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app $URL_OF_THIS_REPO --branch develop
bench install-app erpnextpl_community
bench --site $SITE_NAME migrate
```

## Rozwój

Przed zmianami w aktywnym zakresie warto uruchomić testy dotyczące:

- walidacji klienta,
- walidacji faktury sprzedaży,
- patcha tworzącego dokumenty Community.

## Licencja

MIT
