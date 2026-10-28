# e-rechnung-codelisten

Die Codelisten der deutschen E-Rechnung (XRechnung, ZUGFeRD) als fertige JSON-Dateien, mit deutschen Erklärungen für die gängigen Codes. Für alle, die in Software Codes wie `380`, `58`, `S` oder `C62` anzeigen oder validieren wollen, ohne selbst XML-Codelisten zu parsen.

| Datei | Codeliste | Feld in der Rechnung | Codes |
|---|---|---|---|
| `daten/rechnungsarten.json` | UNTDID 1001 (Peppol-Subset für Rechnungen) | Rechnungsart (BT-3) | 27 |
| `daten/zahlungsmittel.json` | UNTDID 4461 | Zahlungsmittel (BT-81) | 84 |
| `daten/steuerkategorien.json` | UNTDID 5305 (Peppol-Subset) | Umsatzsteuerkategorie (BT-95-1, BT-102, BT-118, BT-151) | 10 |
| `daten/mengeneinheiten.json` | UN/ECE Recommendation 20 und 21 (Rev. 11e) | Mengeneinheit (BT-130) | 2.162 |

## Format

```json
{
 "titel": "Invoice type code (UNCL1001 subset)",
 "liste": "UNCL1001-inv",
 "version": "D.16B",
 "herausgeber": "UN/CEFACT",
 "codes": [
  {
   "code": "389",
   "name": "Self-billed invoice",
   "beschreibung_en": "An invoice the invoicee is producing instead of the seller.",
   "deutsch": "Gutschrift im umsatzsteuerlichen Sinn: Der Käufer rechnet ab, nicht der Verkäufer (Gutschriftverfahren)."
  }
 ]
}
```

Das Feld `deutsch` gibt es für die Codes, die in Deutschland tatsächlich vorkommen. Hinweis für die XRechnung: In BT-3 sollen laut Regel BR-DE-17 nur die Codes 326, 380, 381, 384, 389, 875, 876 und 877 stehen.

## Verwendung

Direkt laden, keine Abhängigkeiten:

```js
import rechnungsarten from "./daten/rechnungsarten.json" with { type: "json" };

const art = rechnungsarten.codes.find((c) => c.code === "389");
console.log(art.deutsch);
```

Oder per `npm install github:belahamburg-sudo/e-rechnung-codelisten` und aus `node_modules` lesen.

## Alle Codes nachschlagen, Rechnungen prüfen

- Codes mit Suche und Erklärung: [erechnungswandler.de/e-rechnung-codes](https://erechnungswandler.de/e-rechnung-codes)
- E-Rechnung (XRechnung, ZUGFeRD) kostenlos prüfen, komplett im Browser: [erechnungswandler.de](https://erechnungswandler.de)
- Wann 381, 384 oder 389 in eine Gutschrift gehört: [erechnungswandler.de/e-rechnung-gutschrift](https://erechnungswandler.de/e-rechnung-gutschrift)

## Quellen und Lizenz

Die Codes, englischen Namen und Beschreibungen stammen aus den Validierungsartefakten von [OpenPeppol BIS Billing 3.0](https://docs.peppol.eu/poacc/billing/3.0/) (Herausgeber der Listen: UN/CEFACT bzw. UN/ECE). Die deutschen Erklärungen sind eigene Texte von [erechnungswandler.de](https://erechnungswandler.de/e-rechnung-codes). `bauen.py` erzeugt die JSON-Dateien aus den XML-Quellen.

Code und deutsche Texte: MIT-Lizenz (siehe LICENSE). Die zugrunde liegenden UN-Codelisten sind frei verwendbar.
