# Dokumentation: XML-Validierung & XSD-Generierung

Dieses Dokument beschreibt, wie das XSD-Schema für IEC 61499 XML-Dateien generiert wird und wie einzelne Dateien mithilfe des `xml-validator`-Skills validiert werden.

---

## 1. XSD-Generierung (Erzeugen einer neuen XSD)

Das XSD-Schema wird maschinell nach dem **Clean-Room-Prinzip** erzeugt. Das Skript scannt Beispieldateien, analysiert deren Struktur und generiert eine passende XML Schema Definition (XSD).

### Automatische Generierung über Bulk-Mode
Wenn du die XSD neu generieren und gleichzeitig alle Dateien validieren möchtest, führe folgenden Befehl im Hauptverzeichnis des Repositories aus:

```powershell
python .agents/skills/xml-validator/validate.py --bulk
```

#### Funktionsweise des Bulk-Mode:
1. **Ordner-Scan:** Das Skript scannt rekursiv vordefinierte Quellordner nach XML-Dateien mit den Endungen `.fbt`, `.adp`, `.dev`, `.res`, `.sub`, `.SUB` und `.sys`.
2. **Strukturanalyse (`XSDGenerator`):**
   * Es erfasst alle XML-Elemente (Tags) und deren Kindelemente.
   * Es analysiert alle Attribute und ermittelt, ob sie in jeder Instanz vorkommen (`use="required"`) oder optional sind (`use="optional"`).
   * Attribute namens `"Name"` erhalten den benutzerdefinierten XSD-Typ `Name`. Dieser validiert Bezeichner syntaktisch über ein Pattern (erlaubt Buchstaben, Zahlen, Unterstriche, Bindestriche, Punkte und Doppelpunkte, verbietet aber Leerzeichen). Alle anderen Attribute werden als `xs:string` typisiert.
   * Es verwendet ein *Mixed Content Model* (`mixed="true"` und ein `<xs:choice>` der Kindelemente), um Leerzeichen, Formatierungen und CDATA-Blöcke (z. B. strukturierter Text in Algorithmen) flexibel zu erlauben.
3. **XSD-Export:** Das generierte Schema wird in der Datei [fbt_clean.xsd](fbt_clean.xsd) gespeichert.
4. **Validation-Check:** Das Skript prüft abschließend alle gefundenen XML-Dateien gegen die frisch generierte XSD.

---

## 2. Einzeldateivalidierung per Skill

Wenn der Agent (oder ein Entwickler) XML-Dateien (z. B. eine `.fbt`-Datei) erstellt oder ändert, schreibt der `xml-validator`-Skill vor, dass diese Datei validiert werden muss.

### Befehl zur Validierung einer einzelnen Datei
Um eine einzelne XML-Datei gegen ein Schema (entweder die generierte Clean-Room XSD oder ein spezifisches XSD) zu prüfen, wird folgender Befehl ausgeführt:

```powershell
python .agents/skills/xml-validator/validate.py <Pfad_zur_XML> <Pfad_zur_XSD>
```

### Beispiele

#### Validierung gegen die Clean-Room XSD:
```powershell
python .agents/skills/xml-validator/validate.py "Ventilsteuerung/4diacIDE-workspace/.lib/Funk-3.0.0/typelib/io/DI/Funk_IX.fbt" ".agents/skills/xml-validator/fbt_clean.xsd"
```

#### Validierung gegen ein anderes XSD-Schema:
~~~powershell
python .agents/skills/xml-validator/validate.py "4diac-ide/plugins/org.eclipse.fordiac.ide.hierarchymanager.model/model/hierarchy.xml" "4diac-ide/plugins/org.eclipse.fordiac.ide.hierarchymanager.model/model/hierarchy.xsd"
~~~
### Fehlerbehandlung
* Verläuft die Validierung erfolgreich, gibt das Skript `SUCCESS` aus und beendet sich mit dem Exit-Code `0`.
* Schlägt die Validierung fehl (z. B. wegen ungültig strukturiertem XML, fehlenden erforderlichen Attributen oder unerwarteten Tags), gibt das Skript die exakten Fehlerzeilen und -gründe über `stderr` aus und beendet sich mit dem Exit-Code `1`. Der Agent liest diese Fehlermeldung, korrigiert die XML-Datei und führt die Validierung erneut aus.

