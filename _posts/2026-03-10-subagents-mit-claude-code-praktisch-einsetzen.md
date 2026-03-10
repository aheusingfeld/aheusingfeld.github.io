---
layout: post
title: "Subagents mit Claude Code praktisch einsetzen um den Kontext sauber zu halten"
date: 2026-03-10T22:41:00+0100
categories: 
  - engineering
tags: 
  - contextengineering
  - agenticengineering
  - claudecode
  - ki
  - tipps 
image: subagents-mit-claude-code-praktisch-einsetzen.png
---

In den letzten Wochen habe ich einige Muster in meiner Arbeit erkannt, die ich als Referenz für mich selbst notieren möchte, damit ich verstehen kann, wie sie sich im Laufe der Zeit entwickeln. Dennoch werde ich sie hier teilen, da ich gerne Ihr Feedback erhalten und dies gemeinsam weiterentwickeln möchte. Lassen Sie uns eintauchen:

## Das Szenario
Angenommen, du arbeitest mit einem Coding-Agenten deiner Wahl (Claude Code, Codex, name your favorite). Während du die anstehende Aufgabe beschreibst, stellst du fest, dass es an anderen Stellen einige relevante Informationen gibt, die der Agent zuerst überprüfen sollte, um einen besseren Kontext für die Erstellung eines Implementierungsplans zu haben.

Wenn du eine komplexe Vorbereitungsaufgabe hast – wie die Suche in Confluence, das Ausführen von CLI-Skripten oder die Recherche im Internet –, führt die Ausführung all dieser Aufgaben in der Hauptsession von Claude Code dazu, dass das Kontextfenster mit HTML-Responses, unübersichtlichen CLI-Ausgaben und irrelevanten Suchergebnissen zugemüllt wird.

Hier ist ein Vorschlag, wie du diese „Context Engineering”-Pipeline mithilfe von Subagenten **praktisch** steuern kannst, sodass der Hauptagent nur den destillierten, sauberen Kontext erhält.

### Das „Context Engineering”-Subagent-Muster

Du musst die Subagenten nicht manuell im Detail verwalten. Sie agieren als Orchestrator und weisen Ihren Hauptagenten an, spezialisierte Worker zu erstellen.

### Schritt 1: Die Orchestrierungsaufforderung

Du würdest Claude Code eine Eingabeaufforderung wie diese geben:

> „Ich möchte [Feature X] in dem Repository erstellen, in dem du dich gerade befindest. Diese Feature soll folgende Funktion erfüllen [Feature Beschreibung].
>
> Bevor du Code schreiben kannst, brauchen wir einen sauberen Implementierungsplan für den du noch Informationen aus verschiedenen Quellen zusammentragen musst. WICHTIG: Verunreinige nicht diese Hauptsession mit diesen Recherchen, sondern erzeuge stattdessen isolierte Subagenten, um den Kontext zu sammeln und nur die relevanten Informationen in diese Hauptsession zurückzugeben:
>
> Folgende Datenquellen wollen wir einbeziehen
> 1. **Agent 1 (Confluence):** Erstelle einen Agenten, der in Confluence die Dokumentation zur „Auth Architecture API” sucht und die Endpunktspezifikationen zusammenfasst.
> 2. **Agent 2 (CLI/Repo):** Erstelle einen Agenten, der `grep-` und AST-Tools auf dem lokalen Repo ausführt, um alle aktuellen Implementierungen des `AuthModule` zu finden.
> 3. **Agent 3 (Web Research):** Erstelle einen Agenten, der die aktuellen Best Practices für „OAuth2-Token-Rotation in Next.js” recherchiert.
> 4. **Agent 3 (Repository Analysis):** Erstelle einen Agenten, der das aktuelle Repository nach ähnlichen Implementierungen durchsucht und sich eine Übersicht verschafft, wo welche Teile der Implementierung platziert und welche existierenden Artefakte (Spezifikation, Code, Tests, etc.) angepasst werden müssen.
> 5. Halte in jedem Fall die Design Principles und Constraints aus deiner ARCHITECTURE.md ein.
> 
> Warte, bis alle drei fertig sind. Nimm dann ihre zusammengefassten Zusammenfassungen, synthetisiere sie und schreiben sie eine saubere `IMPLEMENTATION_PLAN.md`. Zeige mir nur die endgültige Markdown-Datei.”
> 

### Schritt 2: Wie das System dies ausführt

Im Hintergrund verwendet Claude Code das Tool `sessions_spawn`.

- **Isolation:** Jeder erzeugte Agent erhält ein eigenes neues, leeres Kontextfenster.
- **Ausführung:** Agent 1 ruft Confluence-HTML ab (verbrennt Tausende von Tokens) und fasst es zu einer 200-Wort-Zusammenfassung zusammen.
- **Rückgabe:** Der Unteragent wird beendet und gibt *nur die 200-Wort-Zusammenfassung* an die übergeordnete Sitzung zurück.

### Schritt 3: Das Ergebnis

Die übergeordnete Sitzung (Ihr Hauptfenster von Claude Code) erhält drei saubere, prägnante Textblöcke. Sie sieht niemals die unübersichtlichen `Grep-Fehler` oder den 10-seitigen Confluence-Sidebar-HTML-Code. Sie verwendet diese sauberen Zusammenfassungen, um den Implementierungsplan zu entwerfen.

Hast du gute Erfahrungen gesammelt wie du den Context deines Orchestrators sauber halten kannst? Teil sie gern mit mir auf Linkedin oder als Github Issue.

Im nächsten Post werde ich über Erfahrungen bei der Qualitäts-Sicherung durch Skills und Subagents eingehen.
