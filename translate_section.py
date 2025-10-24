#!/usr/bin/env python3
"""
Script per tradurre una sezione alla volta dall'inglese all'italiano.
Questo approccio ottimizza l'uso dei token gestendo il contenuto in chunk più piccoli.
"""

import os
import sys
import json
from pathlib import Path


# Regole di traduzione e stile
TRANSLATION_INSTRUCTIONS = """
Traduci il seguente testo dall'inglese all'italiano seguendo queste linee guida:

1. STILE E TONO:
   - Mantieni uno stile letterario elevato, adatto a un romanzo di fantascienza classico
   - Usa un tono che rifletta l'epoca edoardiana dell'originale
   - Preserva la solennità e il ritmo narrativo

2. TERMINI TECNICI E SCIENTIFICI:
   - "atomic bombs" → "bombe atomiche"
   - "aeroplanes" → "aeroplani"
   - "Carolinum" → "Carolinio" (elemento immaginario)
   - "inducive" → "induttivo"
   - "degenerator" → "degeneratore"

3. NOMI E LUOGHI:
   - Mantieni i nomi propri in inglese (Frederick Barnet, Holsten, etc.)
   - I luoghi geografici vanno tradotti quando hanno una forma italiana standard
   - Titoli militari: "Marshal" → "Maresciallo", "General" → "Generale"

4. FORMATTAZIONE:
   - Mantieni tutti i marcatori markdown (##, ###, ecc.)
   - Preserva i paragrafi e la struttura originale
   - Non aggiungere note o commenti del traduttore

5. ADATTAMENTO CULTURALE:
   - Adatta modi di dire e espressioni idiomatiche all'italiano
   - Mantieni però il flavour britannico del testo originale
   - Usa forme verbali appropriate al contesto narrativo
"""


def translate_section(section_file, output_file):
    """
    Mostra le istruzioni per tradurre manualmente una sezione.
    In futuro potrebbe essere integrato con un API di traduzione.
    
    Args:
        section_file: path del file della sezione da tradurre
        output_file: path dove salvare la traduzione
    """
    # Leggi il contenuto
    with open(section_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"\n{'='*80}")
    print(f"SEZIONE DA TRADURRE: {section_file}")
    print(f"OUTPUT: {output_file}")
    print(f"{'='*80}\n")
    
    # Conta parole per stimare il lavoro
    word_count = len(content.split())
    print(f"Lunghezza: ~{word_count} parole\n")
    
    print(TRANSLATION_INSTRUCTIONS)
    print(f"\n{'='*80}\n")
    print("CONTENUTO DA TRADURRE:")
    print(f"\n{'-'*80}\n")
    print(content)
    print(f"\n{'-'*80}\n")
    
    print("\nDopo aver tradotto il contenuto:")
    print(f"1. Salva la traduzione in: {output_file}")
    print("2. Verifica che la formattazione markdown sia preservata")
    print("3. Rileggi per coerenza stilistica\n")


def batch_translate_directory(input_dir, output_dir):
    """
    Prepara per la traduzione di tutte le sezioni in una directory.
    
    Args:
        input_dir: directory contenente le sezioni da tradurre
        output_dir: directory dove salvare le traduzioni
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # Trova tutti i file di sezione
    section_files = sorted(Path(input_dir).glob("sezione_*.md"))
    
    if not section_files:
        print(f"Nessuna sezione trovata in {input_dir}")
        return
    
    print(f"\nTrovate {len(section_files)} sezioni da tradurre:")
    for i, section_file in enumerate(section_files, 1):
        output_file = Path(output_dir) / section_file.name
        status = "✓ TRADOTTA" if output_file.exists() else "○ DA TRADURRE"
        print(f"{i}. {section_file.name} → {status}")
    
    # Trova la prima sezione non ancora tradotta
    for section_file in section_files:
        output_file = Path(output_dir) / section_file.name
        if not output_file.exists():
            print(f"\n{'='*80}")
            print("PROSSIMA SEZIONE DA TRADURRE:")
            print(f"{'='*80}\n")
            translate_section(str(section_file), str(output_file))
            return
    
    print("\n✓ Tutte le sezioni sono state tradotte!")


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--batch":
        # Modalità batch: mostra quale sezione tradurre
        input_dir = sys.argv[2]
        output_dir = input_dir.replace("_chapters/", "_tradotto/")
        batch_translate_directory(input_dir, output_dir)
    elif len(sys.argv) == 3:
        # Modalità singola sezione
        section_file = sys.argv[1]
        output_file = sys.argv[2]
        translate_section(section_file, output_file)
    else:
        print("Uso:")
        print("  Singola sezione: python translate_section.py <input_file> <output_file>")
        print("  Batch: python translate_section.py --batch <directory>")
        print("\nEsempio:")
        print("  python translate_section.py 'The World set Free_chapter02/sezione_01.md' 'tradotto/sezione_01.md'")
        print("  python translate_section.py --batch 'The World set Free_chapter02'")
        sys.exit(1)
