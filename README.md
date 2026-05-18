# Autocorect

O aplicație lightweight de autocompletare și corectare ortografică realizată în Python folosind PyQt5.

Proiectul monitorizează input-ul tastaturii la nivel global și oferă sugestii în timp real printr-o fereastră flotantă.
Sugestiile sunt generate folosind o structură trie combinată cu algoritmi bazați pe distanța Levenshtein.

## Funcționalități

* sugestii autocomplete în timp real
* detectare și corectare de greseli gramaticale
* căutare eficientă folosind trie
* ranking bazat pe Levenshtein distance/ratio
* suport pentru limba română și diacritice
* inserare automată sau manuală a sugestiilor
* fereastră overlay always-on-top
* opțiuni configurabile prin meniul de setări
* păstrarea capitalizării originale
* cache local pentru lista de cuvinte

## Tehnologii folosite

* Python
* PyQt5
* pynput
* wordfreq
* Levenshtein

## Structura proiectului

```text
gui.py
    interfața grafică, ascultare input de tastatură/mouse,
    logica overlay-ului și gestionarea input-ului

funcvar.py
    structura trie, încărcarea dicționarului,
    generarea sugestiilor și logica de autocompletare/corectare ortografică
```

## Cum funcționează

1. input-ul tastaturii este monitorizat global folosind `pynput`
2. cuvântul curent este urmărit în timp real
3. sugestiile sunt căutate în trie pe baza prefixului
4. candidații sunt comparați folosind Levenshtein ratio/distance
5. cele mai bune sugestii sunt afișate în overlay
6. sugestiile pot fi inserate automat sau manual

## Instalare

Instalarea librăriilor necesare:

```
pip install pyqt5 pynput wordfreq python-Levenshtein
```

## Rulare

```
python gui.py
```

## Observații

* aplicația este gândită în principal pentru Windows
* la prima rulare poate dura mai mult deoarece este generat cache-ul local al cuvintelor
* lista de cuvinte este salvată în `wordlist.txt`
