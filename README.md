# ERPNextPL

ERPNextPL to lokalny moduł dla Frappe / ERPNext, ktory porządkuje polskie procesy wokół sprzedaży, fakturowania, notyfikacji e-mail i importu wyciągów bankowych.

Dokumentacja poniżej jest spisem funkcjonalności widocznych w kodzie aplikacji.

## Zakres aplikacji

- walidacje dokumentów sprzedażowych i kartotek kontrahentów,
- generowanie pliku XML KSeF dla faktur sprzedaży,
- dedykowane powiadomienia e-mail i szablony wiadomości,
- własne print formaty dla faktury i wydania zamówienia,
- import wyciągów bankowych MT940 z profilem mapowania,
- dodatkowe pola w standardowych DocType ERPNext,
- drobne poprawki interfejsu i zachowania formularzy.

## Główne funkcjonalności

### 1. Sales Invoice

- aplikacja dodaje w formularzu `Sales Invoice` przycisk generowania XML KSeF,
- XML można wygenerować tylko dla zatwierdzonej faktury (`docstatus = 1`),
- generowanie sprawdza uprawnienia do dokumentu,
- dane do XML są budowane dynamicznie z faktury, firmy, kontrahenta, pozycji i danych bankowych,
- do dokumentu dodano pole `service_delivery_date`,
- jeśli `service_delivery_date` nie jest ustawione, aplikacja kopiuje `posting_date`,
- jeśli `due_date` nie jest ustawione, aplikacja kopiuje `posting_date`,
- walidacja blokuje termin płatności wcześniejszy niż data wystawienia,
- aplikacja wysyła też powiadomienia związane z fakturą sprzedaży:
  - utworzenie faktury,
  - faktura wystawiona w KSeF,
  - przypomnienie o terminie płatności,
  - przeterminowana należność,
  - ogólne powiadomienie o wystawionej fakturze za usługi.

### 2. Customer

- aplikacja waliduje numer NIP dla kontrahentów z terytorium Polski,
- walidacja działa dla klientów typu `Company`,
- NIP musi mieć 10 cyfr i poprawną sumę kontrolną,
- do kartoteki klienta dodano sekcję danych polskich:
  - `REGON`,
  - `KRS`,
  - `PESEL`,
  - pole pomocnicze dla danych podatkowych.

### 3. Bank Statement Import

- aplikacja nadpisuje standardowy `Bank Statement Import`,
- dodaje obsługę importu plików MT940,
- parser czyta transakcje, opis, kontrahenta, numer rachunku, IBAN i referencję,
- obsługuje profil mapowania tagów MT940 per bank,
- import działa asynchronicznie przez kolejkę,
- jeśli plik nie zawiera transakcji MT940, import kończy się błędem,
- w interfejsie formularza importu rozszerzane są dozwolone typy plików dla tego scenariusza.

### 4. MT940 Profile

- własny DocType `MT940 Profile` pozwala opisać sposób parsowania pliku MT940,
- profil zawiera:
  - nazwę profilu,
  - kod kraju IBAN,
  - typ formatu (`Tagged` lub `Labelled`),
  - separator tagów,
  - mapowanie tagów w JSON,
  - notatki,
- do DocType `Bank` dodano pole linku do profilu MT940.

### 5. Print Formats

- aplikacja zarządza dwoma własnymi print formatami:
  - `Faktura VAT`,
  - `Wydanie Zamówienia`,
- ich aktywacja jest kontrolowana checkboxami w `ERPNextPL Settings`,
- po migracji lub zapisie ustawień brakujące formaty są odtwarzane z fixture.

### 6. E-mail i notifications

- aplikacja dostarcza zestaw standardowych notyfikacji dla dokumentów ERPNext,
- notyfikacje są ładowane z plików JSON / HTML / MD i włączane lub wyłączane z poziomu `ERPNextPL Settings`,
- wszystkie treści pobierają dane dynamicznie z dokumentu i z systemu.

Lista standardowych notyfikacji:

| Nazwa | Doctype | Zastosowanie |
| --- | --- | --- |
| `Low stock levels` | `Bin` | Alert o niskim stanie magazynowym |
| `Sales Invoice due date` | `Sales Invoice` | Przypomnienie o terminie płatności |
| `Purchase Invoice due date` | `Purchase Invoice` | Przypomnienie o terminie płatności faktury zakupu |
| `Sales invoice created` | `Sales Invoice` | Informacja o utworzeniu faktury |
| `Sales invoice issued in KSeF` | `Sales Invoice` | Informacja o wystawieniu faktury w KSeF |
| `Sales invoice notification` | `Sales Invoice` | Ogólna wiadomość o wystawieniu faktury za usługi |
| `Overdue receivables` | `Sales Invoice` | Alert o przeterminowanej należności |
| `Overdue liabilities (purchase invoices)` | `Purchase Invoice` | Alert o przeterminowanych zobowiązaniach |
| `New ToDo assigned` | `ToDo` | Informacja o nowym zadaniu |
| `Sales order ready for fulfillment` | `Sales Order` | Potwierdzenie przyjęcia zamówienia do realizacji |
| `Delayed deliveries of to customers` | `Delivery Note` | Alert o opóźnionej dostawie |
| `Pending releases from warehouse` | `Stock Entry` | Oczekujące wydanie z magazynu |
| `Pending goods receipts` | `Purchase Order` | Oczekujące przyjęcie towaru |

Szablony wiadomości:

- `Dunning reminder` - szablon przypomnienia o zaległych płatnościach,
- `Sales invoice notification` - szablon ogólnej wiadomości o fakturze za usługi, z tabelą pozycji, danymi firmy i danymi do przelewu, jeśli są dostępne.

### 7. UI i drobne poprawki desk

- `Sales Invoice` dostaje przycisk do pobrania XML KSeF,
- formularz `Bank Statement Import` rozszerza listę dopuszczalnych rozszerzeń plików,
- globalny patch poprawia komunikat walidacji firmy i kontrahenta tak, żeby używał poprawnie przetłumaczonych etykiet.

## Konfiguracja

### ERPNextPL Settings

`ERPNextPL Settings` to singleton sterujący zachowaniem aplikacji.

W praktyce:

- `License Key` jest wymagany przy zapisie,
- checkboxy włączają lub wyłączają:
  - print formaty,
  - standardowe notyfikacje e-mail.

Mapowanie przełączników:

| Pole | Efekt |
| --- | --- |
| `use_invoice_print_format` | Włącza print format `Faktura VAT` |
| `use_delivery_note_format` | Włącza print format `Wydanie Zamówienia` |
| `send_low_stock_notifications` | Aktywuje alert `Low stock levels` |
| `send_delayed_deliveries_notifications` | Aktywuje alert `Delayed deliveries of to customers` |
| `send_pending_stock_entry_notifications` | Aktywuje alert `Pending releases from warehouse` |
| `send_pending_goods_receipt_notifications` | Aktywuje alert `Pending goods receipts` |
| `send_sales_order_submitted_notifications` | Aktywuje alert `Sales order ready for fulfillment` |
| `send_sales_invoice_created_notifications` | Aktywuje alert `Sales invoice created` |
| `send_sales_invoice_ksef_notifications` | Aktywuje alert `Sales invoice issued in KSeF` |
| `send_sales_invoice_due_date_notifications` | Aktywuje alert `Sales Invoice due date` |
| `send_purchase_invoice_due_date_notifications` | Aktywuje alert `Purchase Invoice due date` |
| `send_sales_invoice_after_date_notifications` | Aktywuje alert `Overdue receivables` |
| `send_purchase_invoice_after_date_notifications` | Aktywuje alert `Overdue liabilities (purchase invoices)` |
| `send_todo_assignment_notifications` | Aktywuje alert `New ToDo assigned` |

Po aktualizacji ustawień aplikacja:

- odtwarza brakujące fixture,
- usuwa lub wyłącza standardowe powiadomienia, które nie są już zaznaczone,
- wykonuje commit po synchronizacji fixture.

### Automatyczna synchronizacja

- hook `after_migrate` wywołuje synchronizację fixture po migracji,
- dzięki temu nowa instalacja lub aktualizacja od razu przywraca wymagane dokumenty konfiguracyjne.

## Zależności od standardowych danych ERPNext

Aplikacja pobiera dane dynamicznie z:

- `Company`,
- `Customer`,
- `Bank`,
- `Bank Account`,
- `Sales Invoice`,
- `Sales Order`,
- `Purchase Order`,
- `Purchase Invoice`,
- `Delivery Note`,
- `Stock Entry`,
- `ToDo`.

To oznacza, że szablony i notyfikacje są uniwersalne i nie są przywiązane do jednej firmy.

## Pliki i moduły

Najważniejsze elementy kodu:

- `erpnextpl/sales_invoice.py` - walidacja faktur sprzedaży,
- `erpnextpl/customer.py` - walidacja NIP klienta,
- `erpnextpl/overrides/bank_statement_import.py` - import MT940,
- `erpnextpl/ksef/utils.py` - budowa XML KSeF,
- `erpnextpl/public/js/sales_invoice_ksef.js` - przycisk XML KSeF na formularzu faktury,
- `erpnextpl/public/js/bank_statement_import.js` - rozszerzenie importu bankowego,
- `erpnextpl/public/js/erpnextpl_fixes.js` - poprawka komunikatów UI,
- `erpnextpl/doctype/erpnextpl_settings` - sterowanie fixture i checkboxami,
- `erpnextpl/doctype/mt940_profile` - profil importu MT940,
- `erpnextpl/custom/*` - custom fields dla ERPNext.

## Instalacja

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app $URL_OF_THIS_REPO --branch develop
bench install-app erpnextpl
```

Po instalacji warto wejść w `ERPNextPL Settings`, ustawić licencję i zaznaczyć funkcje, których chcesz używać.

## Rozwój

Repozytorium korzysta z:

- `pre-commit`,
- `ruff`,
- `eslint`,
- `prettier`,
- `pyupgrade`.

Przed większą zmianą warto sprawdzić testy dla:

- `ERPNextPL Settings`,
- `MT940 Profile`,
- KSeF,
- importu MT940.

## Licencja

MIT


## ERPNextPL Community

ERPNextPL Community is an open edition focused on practical day-to-day sales workflows and essential Polish localization.

The Community scope includes:

- NIP validation for company customers in Poland,
- localization fields on Customer (`REGON`, `KRS`, `PESEL`),
- `service_delivery_date` on Sales Invoice,
- automatic `due_date` defaulting from `posting_date`,
- validation that payment due date cannot be earlier than posting date,
- XML export from the `Sales Invoice` form,
- global UI fixes (`erpnextpl_fixes.js`),
- Polish translations focused on sales flows.

### How the community can add new features

We welcome feature contributions from the community. To keep the repository maintainable, please follow this workflow:

1. **Open an issue first** describing the business need, expected behavior, and affected DocTypes.
2. **Propose a minimal implementation** that is broadly useful and does not depend on private deployment specifics.
3. **Create a feature branch** from the current default branch and keep changes scoped to one feature.
4. **Include tests and fixtures only when required** and document migration impact in the PR description.
5. **Update documentation** (`README.md` and/or `docs/*`) for any user-visible behavior.
6. **Submit a PR** with clear before/after behavior and manual test steps for reviewers.

Good candidates for Community contributions:

- data quality validations,
- lightweight UX improvements,
- broadly reusable sales/accounting localization helpers,
- focused translation improvements for real user flows.

