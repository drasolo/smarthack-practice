# Unelte și pregătirea laptopului

Ce aducem, ce pachete acoperă fiecare tip de temă și cum economisim cotele agenților.

Surse: documentul de pregătire din 3 noiembrie. Sunt recomandări: nu am verificat ce este instalat pe
fiecare laptop. Setup-ul repo-ului este în `README.md` din rădăcină. Ultima verificare: 2026-11-06.

## Ce aducem

Încărcător, prelungitor, căști și telefon cu hotspot, în caz că Wi-Fi-ul e slab.

## Pachete pe tip de temă

Sâmbătă nu mai instalăm nimic nou, dacă se poate evita. Adăugarea unui pachet în repo se face cum
scrie în `AGENTS.md`.

| Dacă tema e | Pachete |
| --- | --- |
| Prognoză, serii de timp | pandas, duckdb, lightgbm 4.6.0 (4.7.0 a crăpat în Anaconda lui Dragoș), statsforecast, holidays |
| Anomalii | scikit-learn (Isolation Forest), statsmodels (STL) |
| Text, chatbot, RAG | pydantic pentru ieșire structurată, LanceDB sau chromadb, embeddings multilingve |
| Documente, PDF | PyMuPDF, Tesseract cu limba română, docling |
| Voce | faster-whisper și un TTS |
| Hărți | folium sau pydeck |
| Evaluare, red teaming | promptfoo |

Ollama cu un model mic este rezerva dacă rețeaua e slabă sau datele nu au voie să iasă.

## Ce adăugăm la agenți

Adăugăm puțin. Fiecare server MCP costă context în fiecare sesiune, deci preferăm un CLI când face
același lucru.

| Unealtă | Tip | La ce ajută |
| --- | --- | --- |
| Context7 | MCP | Documentație la zi pentru biblioteci |
| duckdb | CLI | Agentul primește agregate, nu fișierul întreg |
| openai/codex-plugin-cc | Plugin Claude Code | `/codex:review`, `/codex:rescue --background`, `/codex:transfer` când se termină cota |
| promptfoo | CLI | Evaluare LLM și red teaming dintr-un YAML |

Nu adăugăm un alt MCP de browser sau MCP-ul GitHub, pentru că avem deja `chrome-devtools` și `gh`.

## Cum economisim cotele

- Începe o sesiune nouă pentru fiecare felie de lucru. O sesiune lungă plătește tot istoricul la
  fiecare cerere.
- Agenții citesc agregate, niciodată fișiere întregi de date.
- Oprește serverele MCP și conectorii pe care nu îi folosești.
- Alege modelul după sarcină: cel mai bun pentru plan și bug-uri grele, unul mai ieftin pentru
  sarcini mecanice.
- Cere ieșiri scurte: `pytest -q`, `| tail -50`, jurnale în fișiere.
- Dacă o cotă se apropie de limită, mută sarcina la alt agent prin `AGENTS.md` și `CONTEXT.md`.

## Când folosim alte tehnici

- **Același task la doi agenți:** doar pe bucăți riscante, de exemplu modelul de anomalii sau ecranul
  principal, pentru că dublează consumul.
- **Sarcini lungi pe timpul somnului:** teste sau documentație, pe branch-uri separate, verificate la
  trezire.
- **Slide „Cum am folosit AI-ul”:** worktree-uri, review încrucișat, comenzi distructive blocate,
  conținut AI etichetat. Răspunde la grija PPC din slide-ul 23.
