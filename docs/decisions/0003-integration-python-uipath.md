# ADR-0003: Hybride Integration zwischen Python und UiPath

## Status
Akzeptiert

## Kontext
Im Rahmen der "Python-First"-Strategie (siehe ADR-0001) wird UiPath nur bei Ausnahmen eingesetzt. Dennoch wird es in Enterprise-Prozessen unweigerlich zu Szenarien kommen, in denen ein Python-Bot Aufgaben an einen UiPath-Roboter übergeben muss (oder umgekehrt), beispielsweise weil ein bestimmter Legacy-Schritt im Prozess zwingend über UiPath erfolgen muss. Ein unkontrolliertes, synchrones "Ping-Pong" zwischen Systemen führt zu Fragilität und schwer aufspürbaren Deadlocks.

## Entscheidung
Wir etablieren für die hybride RPA-Entwicklung das Paradigma der **losen Kopplung**.
- **Asynchrone Kommunikation (bevorzugt):** Die primäre Interaktion zwischen Python-Bots und UiPath erfolgt ereignisgesteuert und asynchron über Message Queues. Zukünftig übernimmt hier der **NATS Message Broker** die orchestrierende Rolle, um Teil-Tasks statusüberwacht zu verteilen. Kurzfristig wird die Orchestrator REST API für asynchrone Queue-Items genutzt.
- **Vermeidung direkter Aufrufe:** Ein synchrones Warten des einen Systems auf das andere ist zu vermeiden, da es Blockaden im Cluster (z. B. Azure AKS) verursacht und wertvolle Laufzeit blockiert.
- **Python Scope (Ausnahme):** Nur wenn ein enger Prozessfluss dies aus Performance- oder Sicherheitsgründen erfordert und ein starker architektonischer Vorteil vorliegt, darf das UiPath-Activity "Python Scope" für direkte Aufrufe verwendet werden. Solche Fälle sind kritisch zu prüfen.

## Konsequenzen
- **Positiv:** Robuste, hochskalierbare Prozesse. Einzelne Teil-Tasks können bei Fehlern isoliert neu gestartet werden. Bessere Übersicht im NATS/Orchestrierer-System (analog BPMN).
- **Negativ/Risiken:** Prozesse müssen granularer und mit bedachtem State-Management (Zustandserhaltung) modelliert werden. Die Architekturkomplexität der Infrastruktur (Message Broker) steigt leicht an.
