# Groove Bank FX

**MIDI-Sequencer als Insert-Effekt** · Spielt den Akkord, den du ihm schickst, im Rhythmus einer Groove-Bibliothek nach Genres. · Hersteller in MPC/Force: Mission Minnow · Lizenz: MIT

Insert-Effekt-Variante von [mpc-vst-groovebank](https://github.com/saustin2010/mpc-vst-groovebank) (Port des Schwung-Moduls
[Groove Bank](https://github.com/mission-minnow/groovebank) v0.1.16). Gleiche Engine, gleiche 97 Grooves in 14 Genres – aber
als Insert-Effekt, belegt also keinen der 8 Instrument-Plugin-Plätze der Force. Das Audio der Spur läuft unverändert durch.

## Was anders ist als beim Instrument

| | Groove Bank (Instrument) | Groove Bank FX (Insert) |
|---|---|---|
| Plugin-Liste | `[SEQ] Groove Bank`, uid `GrvB` | `[SEQ] Groove Bank FX`, uid `GrvF`, Kategorie Effect |
| Akkord-Eingang | Noten der eigenen Spur | eigener MIDI-Port **`[SEQ] Groove Bank FX MIDI In`** (die Force gibt Insert-Effekten keine Noten) |
| Ausgang | Port `… MIDI Out` | Port **`[SEQ] Groove Bank FX MIDI Out`** (unverändert) |
| Audio | Stille | Spur-Audio unverändert durch, keine Latenz |
| Neu | – | **GENRE** (springt zum ersten Groove eines Genres, wie Knob 8 am Move), **MIDI IN CH** (Omni/1–16), **CC 20–27** |
| Q-Links | VARIANT, SWING, GATE · STRUM, ACCENT, LATCH · GROOVE | GENRE, GROOVE · VARIANT, SWING · GATE, STRUM · ACCENT, MIDI IN CH (nur Regler, LATCH nur per Touch) |

Beide Plugins können nebeneinander installiert sein (eigener Ordner, eigene uid).

## Auf der Force einrichten

1. **Insert setzen:** Groove Bank FX als Insert-Effekt auf eine beliebige Spur legen – am einfachsten auf die Synth-Spur,
   die den Groove spielen soll. Ihr Audio läuft unverändert durch.
2. **Ports freischalten:** *Menu → Preferences → MIDI*: bei **`[SEQ] Groove Bank FX MIDI Out`** (Eingang) **Track**
   einschalten; falls **`[SEQ] Groove Bank FX MIDI In`** in der Ausgangsliste auftaucht, dort ebenfalls.
3. **Akkordquelle:** eine MIDI-Spur anlegen, deren **MIDI Out** auf `[SEQ] Groove Bank FX MIDI In` zeigt (Kanal passend zu
   MIDI IN CH, bei IN OMNI egal). Darauf Pads/Keyboard spielen oder einen Clip mit gehaltenen Akkorden laufen lassen.
4. **Zielspur(en):** **MIDI Input** = `[SEQ] Groove Bank FX MIDI Out`, **Monitor** = **In** (nicht Auto).
5. **Play drücken:** Der Groove läuft im Force-Tempo und folgt dem Transport. Akkord halten – oder LATCH einschalten.

Ohne laufenden Transport spielt Groove Bank nichts (wie im Original).

## Bedienung

- **GENRE** (Stepper oben): HOUSE, TECHNO, GARAGE, DNB, HIPHOP, TRAP, FUNK, SOUL, JAZZ, LATIN, REGGAE, ROCK, AFRO, WORLD –
  springt zum ersten Groove des Genres und zeigt immer das Genre des aktuellen Grooves.
- **GROOVE** (Stepper darunter): alle 97 Grooves der Reihe nach, Anzeige „Name GENRE“.
- **VARIANT, SWING, GATE, STRUM, ACCENT** wie im Original; **LATCH** hält den Akkord nach dem Loslassen.
- **MIDI IN CH** (unten rechts): `IN OMNI` oder `IN CH 1…16` – filtert Noten **und** CCs am MIDI-In-Port. Bei mehreren
  Sequencer-Plugins bekommt so jedes seinen eigenen Kanal.

### CC-Steuerung (auf dem MIDI-IN-CH-Kanal, über den MIDI-In-Port)

| CC | 20 | 21 | 22 | 23 | 24 | 25 | 26 | 27 |
|---|---|---|---|---|---|---|---|---|
| Ziel | GENRE | GROOVE | VARIANT | SWING | GATE | STRUM | ACCENT | LATCH (≥ 64 = an) |

Der Bildschirm folgt den CC-Änderungen. Alle anderen CCs, Pitchbend und Aftertouch gehen an den Ausgang weiter
(zum Zielsynth), wie im Original.

## Groove-Bibliothek: Abgleich mit dem Schwung-Repo

Geprüft am 2026-10-09 gegen das hochgeladene `groovebank-main` (Schwung-Modul v0.1.16):

- **97 Grooves in 14 Genres, vollständig.** Die Release-Builds holen `src/patterns/*.groove` per `release/fetch-library.py`
  vom Upstream-Commit `4edfa2f` (prüft jede Datei gegen ihren Git-Hash). Dieser Commit ist der aktuelle Upstream-Stand,
  und alle 14 Dateien sind bytegleich mit dem Schwung-Repo. Die Engine (`src/`) ist ebenfalls unverändert.
- Je Genre: HOUSE 7 · TECHNO 6 · GARAGE 6 · DNB 7 · HIPHOP 7 · TRAP 6 · FUNK 8 · SOUL 7 · JAZZ 7 · LATIN 9 · REGGAE 7 ·
  ROCK 8 · AFRO 6 · WORLD 6.
- **Fallstrick im Instrument-Repo:** dessen Ordner `deploy/` enthält nur `groovebank.so` und den Skin, **nicht** den Ordner
  `groovebank/patterns/`. Wer von dort von Hand installiert, bekommt nur die 3 eingebauten Notfall-Grooves (Offbeat, Four
  Floor, Tresillo). Das Release-ZIP aus GitHub Actions enthält die Bibliothek. Dieses Repo hat deshalb kein `deploy/` mehr.
- Nicht mitportiert (gehört zur Move-Oberfläche, nicht zur Engine): das Grid-Bild der Grooves (`canvas.js`) und der
  Jog-Wheel-Browser; das Genre-Springen gibt es jetzt als GENRE-Regler.

## Bauen

Wie das Instrument, über GitHub Actions: *Actions → „Release (draft)“ → Run workflow*, Version eingeben (z. B. `1.0.0`).
Heraus kommt `SEQ-Groove-Bank-FX-<version>-mpc-armv7.zip` im Draft-Release; auf die Force kopieren, entpacken,
`sh install.sh` als root. Das Plugin landet in `/sdcard/Synths/Mission Minnow - VST - [SEQ] Groove Bank FX/`
mit `groovebank_fx.so` und `groovebank/patterns/`.

Lokal (Docker nötig) mit den Werkzeugen aus [saustin2010/mpc-vst-plugins](https://github.com/saustin2010/mpc-vst-plugins) am
Commit aus `.github/workflows/release.yml`:

```
python3 release/fetch-library.py library
bash "$MPC_VST/tools/build_port.sh" vst.json
rm -rf build/groovebank && cp -R library build/groovebank && bash "$MPC_VST/tools/test_port.sh" vst.json
```

## Stand

- Offline-Host-Test (ASan/UBSan, x86): **PASSED** – u. a. Audio läuft durch, NULL-Eingang, Q-Link-Weg, Chunk-Restore.
- Eigener Funktionstest: Genre-Sprung, CC 20–27, Kanalfilter, State mit `in_ch`, Groove-Ausgabe auf gehaltenen Akkord.
- Skin lokal gebaut, keine Warnungen von `skin_check`.
- **Noch offen auf der Force:** ob sie den Port `… MIDI In` als Ziel einer MIDI-Spur anbietet (gleicher Ansatz wie bei
  Oneiroi FX) und ob die Force-Q-Link-Bank alle acht Regler auf einmal zeigt.

## Dateien

| Pfad | Was |
|---|---|
| `mpc/schwung_midi_fx.c` | Adapter: Schwung-MIDI-FX → Engine, jetzt mit `process()` (Audio durch), ALSA-MIDI-In, IN CH, GENRE, CCs |
| `mpc/engine.h` | Engine-Schnittstelle des Frameworks (mit `process` für Effekte) |
| `src/` | die Engine, unverändert vom Upstream |
| `vst.json` | `"effect": true`, uid `GrvF`, `HAS_DISPLAY_REV` |
| `params.json` | 16 Parameter (die ersten 10 wie beim Instrument, dann GENRE, MIDI IN CH und deren Pfeile) |
| `layout.conf` | Bildschirm; `design/fx_bg_edit.py` hat dafür Platz im Hintergrundbild geschaffen |
| `release/` | Bibliothek: Quelle und Commit (`library.json`), Abruf-Skript |

Herkunft: [`UPSTREAM`](UPSTREAM), Framework-Änderungen: [`FRAMEWORK.md`](FRAMEWORK.md).
