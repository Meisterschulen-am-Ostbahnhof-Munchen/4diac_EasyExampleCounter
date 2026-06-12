# Dokumentation: IEC 61499 Keywords & Structured Text (ST) Syntax

Dieses Dokument beschreibt die reservierten Keywords in IEC 61499 XML-Dateien und die Syntaxregeln für den darin enthaltenen Structured Text (ST).

---

## 1. Reservierte Schlüsselwörter (Reserved Keywords)

In IEC 61499 und IEC 61131-3 sind bestimmte Wörter für die Sprache reserviert. Sie dürfen **nicht** als Bezeichner (Namen von Variablen, Funktionsbausteinen, Events, Adaptern, Ressourcen oder Algorithmen) verwendet werden (Case-Insensitive).

Die häufigsten Fehlerquellen sind Bezeichner wie `LEFT` oder `RIGHT`, da diese Standard-Stringfunktionen sind.

### Liste der reservierten Keywords
* **Datentypen:** `BOOL`, `SINT`, `INT`, `DINT`, `LINT`, `USINT`, `UINT`, `UDINT`, `ULINT`, `REAL`, `LREAL`, `TIME`, `DATE`, `TOD`, `TIME_OF_DAY`, `DT`, `DATE_AND_TIME`, `STRING`, `WSTRING`, `BYTE`, `WORD`, `DWORD`, `LWORD`.
* **Stringfunktionen:** `LEFT`, `RIGHT`, `MID`, `CONCAT`, `INSERT`, `DELETE`, `REPLACE`, `FIND`, `LEN`.
* **Mathematische & Standardfunktionen:** `ABS`, `SQRT`, `LN`, `LOG`, `EXP`, `SIN`, `COS`, `TAN`, `ASIN`, `ACOS`, `ATAN`, `ADD`, `MUL`, `SUB`, `DIV`, `MOD`, `EXPT`, `MOVE`, `LIMIT`, `MUX`, `SEL`, `MAX`, `MIN`, `ADR`, `SIZEOF`.
* **Operatoren:** `AND`, `OR`, `XOR`, `NOT`, `MOD`.
* **Kontrollfluss & Strukturen:** `IF`, `THEN`, `ELSE`, `ELSIF`, `END_IF`, `CASE`, `OF`, `END_CASE`, `FOR`, `TO`, `BY`, `DO`, `END_FOR`, `WHILE`, `END_WHILE`, `REPEAT`, `UNTIL`, `END_REPEAT`, `EXIT`, `RETURN`, `ALGORITHM`, `END_ALGORITHM`, `VAR`, `END_VAR`, `VAR_INPUT`, `VAR_OUTPUT`, `VAR_IN_OUT`, `VAR_TEMP`, `TRUE`, `FALSE`, `CONSTANT`.
* **IEC 61499 Standard-Events/Blöcke:** `E_DELAY`, `E_CYCLE`, `E_START`, `E_STOP`, `E_RESTART`, `E_SPLIT`, `E_JOIN`, `E_RENDEZVOUS`, `E_MERGE`, `E_F_TRIG`, `E_R_TRIG`, `E_SR`, `E_RS`, `E_SELECT`, `E_SWITCH`, `E_TABLE`, `E_D_FF`, `E_T_FF`.

---

## 2. Structured Text (ST) Syntax-Regeln

Der in Algorithmen verwendete Structured Text folgt strengen Syntax-Regeln:

### Zuweisungen
* **Falsch:** `OUT = IN;` (Das Gleichheitszeichen `=` ist in ST ausschließlich ein Vergleichsoperator).
* **Richtig:** `OUT := IN;` (Zuweisungen müssen immer mit `:=` erfolgen).

### Semicolons
* Jede Anweisung (Zuweisungen, Funktionsaufrufe) **muss** mit einem Semikolon `;` abgeschlossen werden.
* Kontrollstrukturen (`IF ... THEN`, `ELSIF ... THEN`, `ELSE`, `WHILE ... DO`, `REPEAT`, `CASE ... OF`) dürfen **kein** Semikolon am Zeilenende haben.
* Die schließenden Schlüsselwörter (`END_IF;`, `END_CASE;`, `END_FOR;`, `END_WHILE;`, `END_REPEAT;`) **müssen** mit einem Semikolon enden.

### Kommentare
* Einzeilige Kommentare starten mit `//`.
* Mehrzeilige Kommentare werden von `(*` und `*)` umschlossen.

---

## 3. Typ-Kompatibilität & Zuweisungen (Implicit vs. Explicit Conversion)

Verbindungen in FB-Netzwerken und Variablen-Zuweisungen im Structured Text müssen der IEC 61131-3 Typkompatibilität entsprechen:

### Grundregel
Eine Zuweisung/Verbindung von **Source** nach **Target** ist erlaubt, wenn der Target-Typ den Source-Typ verlustfrei aufnehmen kann.

### Kompatibilitätsmatrix (Auswahl)
* **Ganzzahlen:** Signed und Unsigned sind nicht kompatibel (z. B. `INT` $\rightarrow$ `UINT` verboten). Kleinere Datentypen dürfen auf größere Datentypen zugewiesen werden (z. B. `INT` $\rightarrow$ `DINT` erlaubt; `DINT` $\rightarrow$ `INT` verboten).
* **Gleitkommazahlen (Floats):**
  * `REAL` akzeptiert: `SINT`, `INT`, `USINT`, `UINT` und `REAL`.
  * `LREAL` akzeptiert: `SINT`, `INT`, `DINT`, `USINT`, `UINT`, `UDINT`, `REAL` und `LREAL`.
* **Bit-Typen:** `BOOL` darf auf alle Bit-Typen (`BYTE`, `WORD`, `DWORD`, `LWORD`) zugewiesen werden.

### Implizite vs. Explizite Konvertierung
Wenn die Zuweisung laut Matrix nicht implizit zulässig ist, **muss** eine explizite Konvertierungsfunktion im ST-Code verwendet werden:

* **Zulässig (implizit, `_TO_` kann weggelassen werden):**
  ```pascal
  real_var := uint_var; // Erlaubt!
  ```
* **Unzulässig (erfordert explizites Casting):**
  ```pascal
  real_var := udint_var; // FEHLER! REAL akzeptiert kein UDINT implizit.
  real_var := UDINT_TO_REAL(udint_var); // RICHTIG!
  ```
