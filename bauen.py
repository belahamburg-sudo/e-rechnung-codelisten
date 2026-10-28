#!/usr/bin/env python3
"""Erzeugt die JSON-Codelisten aus den offiziellen XML-Quellen (OpenPeppol BIS 3, UN/CEFACT, UN/ECE).

Quelle der XMLs: ../werkzeuge/codelisten/ (aus den Peppol-BIS-3-Validierungsartefakten).
Deutsche Erklärungen: eigene Texte von erechnungswandler.de/e-rechnung-codes.
"""
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

NS = {"c": "urn:fdc:difi.no:2017:vefa:structure:CodeList-1"}
QUELLE = Path(__file__).resolve().parent.parent / "werkzeuge" / "codelisten"
ZIEL = Path(__file__).resolve().parent / "daten"

DEUTSCH = {
    "rechnungsarten": {
        "380": "Normale Rechnung. Der Standard für fast alle Rechnungen.",
        "326": "Teilrechnung, zum Beispiel bei Lieferung in mehreren Teilen.",
        "384": "Korrigierte Rechnung, ersetzt eine fehlerhafte Rechnung. In der XRechnung soll dann ein Verweis auf die ursprüngliche Rechnung stehen (BR-DE-26).",
        "381": "Rechnungskorrektur zugunsten des Kunden, etwa Storno, Rückgabe oder nachträglicher Rabatt (kaufmännische Gutschrift).",
        "389": "Gutschrift im umsatzsteuerlichen Sinn: Der Käufer rechnet ab, nicht der Verkäufer (Gutschriftverfahren).",
        "875": "Abschlagsrechnung für Bauleistungen.",
        "876": "Teilschlussrechnung für Bauleistungen.",
        "877": "Schlussrechnung für Bauleistungen.",
    },
    "zahlungsmittel": {
        "58": "SEPA-Überweisung. Der häufigste Code in Deutschland.",
        "59": "SEPA-Lastschrift. Verlangt in der XRechnung die Gläubiger-ID (BR-DE-30) und die IBAN des Kunden (BR-DE-31).",
        "30": "Überweisung ohne SEPA, zum Beispiel ins Ausland außerhalb des SEPA-Raums.",
        "42": "Zahlung auf ein Bankkonto.",
        "49": "Lastschrift ohne SEPA.",
        "48": "Kartenzahlung.",
        "54": "Kreditkarte.",
        "55": "Debitkarte.",
        "68": "Bezahldienst im Internet.",
        "10": "Barzahlung.",
        "57": "Dauerauftrag oder feste Vereinbarung.",
        "97": "Verrechnung zwischen den Geschäftspartnern.",
        "ZZZ": "Individuell vereinbart.",
    },
    "steuerkategorien": {
        "S": "Umsatzsteuer wird berechnet, egal ob Regelsatz oder ermäßigter Satz (zum Beispiel 19 % oder 7 %).",
        "Z": "Steuersatz 0 %.",
        "E": "Steuerbefreit. Der Befreiungsgrund muss angegeben werden.",
        "AE": "Umkehrung der Steuerschuldnerschaft: Der Kunde schuldet die Umsatzsteuer (§ 13b UStG).",
        "K": "Steuerfreie innergemeinschaftliche Lieferung oder Leistung an Unternehmen in anderen EU-Staaten.",
        "G": "Steuerfreie Ausfuhr außerhalb der EU.",
        "O": "Nicht steuerbar, die Leistung fällt nicht unter die Umsatzsteuer.",
        "L": "Steuer der Kanarischen Inseln (IGIC).",
        "M": "Steuer in Ceuta und Melilla (IPSI).",
    },
    "mengeneinheiten": {
        "C62": "Stück (Einheit „eins“), der übliche Code für Stück",
        "H87": "Stück",
        "EA": "je Stück (each)",
        "HUR": "Stunde",
        "MIN": "Minute",
        "DAY": "Tag",
        "E49": "Arbeitstag",
        "WEE": "Woche",
        "MON": "Monat",
        "ANN": "Jahr",
        "KGM": "Kilogramm",
        "GRM": "Gramm",
        "TNE": "Tonne",
        "MTR": "Meter",
        "CMT": "Zentimeter",
        "MMT": "Millimeter",
        "KMT": "Kilometer",
        "MTK": "Quadratmeter",
        "MTQ": "Kubikmeter",
        "LTR": "Liter",
        "KWH": "Kilowattstunde",
        "LS": "Pauschale",
        "SET": "Set, Satz",
        "PR": "Paar",
        "P1": "Prozent",
        "E48": "Serviceeinheit",
        "XPK": "Packung",
        "XPP": "Stück (Verpackungscode)",
        "XBX": "Box, Schachtel",
        "XCT": "Karton",
    },
}

DATEIEN = {
    "rechnungsarten": "UNCL1001-inv.xml",
    "zahlungsmittel": "UNCL4461.xml",
    "steuerkategorien": "UNCL5305.xml",
    "mengeneinheiten": "UNECERec20-11e.xml",
}


def glatt(text):
    return re.sub(r"\s+", " ", text or "").strip()


def main():
    ZIEL.mkdir(exist_ok=True)
    for name, datei in DATEIEN.items():
        baum = ET.parse(QUELLE / datei)
        wurzel = baum.getroot()
        meta = {feld: glatt(wurzel.findtext(f"c:{feld}", namespaces=NS)) for feld in ("Title", "Identifier", "Version", "Agency")}
        eintraege = []
        for code in wurzel.findall("c:Code", NS):
            eintrag = {
                "code": glatt(code.findtext("c:Id", namespaces=NS)),
                "name": glatt(code.findtext("c:Name", namespaces=NS)),
            }
            beschreibung = glatt(code.findtext("c:Description", namespaces=NS))
            if beschreibung:
                eintrag["beschreibung_en"] = beschreibung
            de = DEUTSCH[name].get(eintrag["code"])
            if de:
                eintrag["deutsch"] = de
            eintraege.append(eintrag)
        inhalt = {
            "titel": meta["Title"],
            "liste": meta["Identifier"],
            "version": meta["Version"],
            "herausgeber": meta["Agency"],
            "quelle": "OpenPeppol BIS Billing 3.0 Validierungsartefakte",
            "deutsche_erklaerungen": "erechnungswandler.de/e-rechnung-codes",
            "codes": eintraege,
        }
        ziel = ZIEL / f"{name}.json"
        ziel.write_text(json.dumps(inhalt, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(f"{ziel.name}: {len(eintraege)} Codes")


if __name__ == "__main__":
    main()
