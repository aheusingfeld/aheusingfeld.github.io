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
image: 2026-03-10-subagents-mit-claude-code-praktisch-einsetzen.png
---

# Subagents mit Claude Code praktisch einsetzen um den Kontext sauber zu halten

In den letzten Wochen habe ich einige Muster in meiner Arbeit erkannt, die ich als Referenz für mich selbst notieren möchte, damit ich verstehen kann, wie sie sich im Laufe der Zeit entwickeln. Dennoch werde ich sie hier teilen, da ich gerne Ihr Feedback erhalten und dies gemeinsam weiterentwickeln möchte. Lassen Sie uns eintauchen:

Angenommen, Sie arbeiten mit einem Co-Agenten Ihrer Wahl (Claude Code, Codex, was auch immer). Während Sie die anstehende Aufgabe beschreiben, stellen Sie fest, dass es an anderen Stellen einige relevante Informationen gibt, die Ihr Agent zuerst überprüfen sollte, um einen besseren Kontext für die Erstellung eines Implementierungsplans zu haben.

Wenn Sie eine komplexe Vorbereitungsaufgabe haben – wie die Suche in Confluence, das Ausführen von CLI-Skripten oder die Recherche im Internet –, führt die Ausführung all dieser Aufgaben in der Hauptsitzung von Claude Code dazu, dass das Kontextfenster mit rohem HTML-Code, unübersichtlichen CLI-Ausgaben und irrelevanten Suchergebnissen überladen wird.

Hier ist ein Vorschlag, wie Sie diese „Context Engineering”-Pipeline mithilfe von Subagenten **praktisch** orchestrieren können, sodass der Hauptagent nur den destillierten, perfekten Kontext erhält.

### Das „Context Engineering”-Subagent-Muster

Sie müssen die Subagenten nicht manuell im Detail verwalten. Sie agieren als Orchestrator und weisen Ihren Hauptagenten (oder mich) an, spezialisierte Worker zu erstellen.

### Schritt 1: Die Orchestrierungsaufforderung

Sie würden Claude Code eine Eingabeaufforderung wie diese geben:

> „Ich muss [Feature X] erstellen. Bevor wir Code schreiben, brauchen wir einen sauberen, makellosen Implementierungsplan. Verunreinigen Sie diese Hauptsitzung nicht mit rohen Recherchen. Erzeugen Sie stattdessen drei isolierte Subagenten, um Kontext zu sammeln:
> 
> 1. **Agent 1 (Confluence):** Erstellen Sie einen Agenten, der in Confluence nach dem Dokument „Auth Architecture API” sucht und die Endpunktspezifikationen zusammenfasst.
> 2. **Agent 2 (CLI/Repo):** Erstellen Sie einen Agenten, der `grep-` und AST-Tools auf dem lokalen Repo ausführt, um alle aktuellen Implementierungen des `AuthModule` zu finden.
> 3. **Agent 3 (Web Research):** Erstellen Sie einen Agenten, der die neuesten Best Practices für „OAuth2-Token-Rotation in Next.js” recherchiert.
> 
> Warten Sie, bis alle drei fertig sind. Nehmen Sie dann ihre zusammengefassten Zusammenfassungen, synthetisieren Sie sie und schreiben Sie eine saubere `IMPLEMENTATION_PLAN.md`. Zeigen Sie mir nur die endgültige Markdown-Datei.”
> 

### Schritt 2: Wie das System dies ausführt

Im Hintergrund verwendet Claude Code das Tool `sessions_spawn`.

- **Isolation:** Jeder erzeugte Agent erhält ein eigenes neues, leeres Kontextfenster.
- **Ausführung:** Agent 1 ruft Confluence-HTML ab (verbrennt Tausende von Tokens) und fasst es zu einer 200-Wort-Zusammenfassung zusammen.
- **Rückgabe:** Der Unteragent wird beendet und gibt *nur die 200-Wort-Zusammenfassung* an die übergeordnete Sitzung zurück.

### Schritt 3: Das Ergebnis

Die übergeordnete Sitzung (Ihr Hauptfenster von Claude Code) erhält drei saubere, prägnante Textblöcke. Sie sieht niemals die unübersichtlichen `Grep-Fehler` oder den 10-seitigen Confluence-Sidebar-HTML-Code. Sie verwendet diese sauberen Zusammenfassungen, um den Implementierungsplan zu entwerfen.


Hast du gute Erfahrungen gesammelt wie du den Context deines Orchestrators sauber halten kannst? Teil sie gern mit mir auf Linkedin oder als Github Issue.
