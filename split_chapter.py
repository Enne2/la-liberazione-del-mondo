#!/usr/bin/env python3
"""
Script per dividere un capitolo in sezioni separate.
Ogni sezione viene salvata in un file separato per ottimizzare la traduzione.
"""

import re
import sys
import os
from pathlib import Path


def split_chapter(chapter_file, output_dir):
    """
    Divide un capitolo in sezioni basandosi sui titoli ### Section
    
    Args:
        chapter_file: path del file del capitolo da dividere
        output_dir: directory dove salvare le sezioni
    """
    # Leggi il contenuto del capitolo
    with open(chapter_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Estrai il titolo del capitolo (prima riga con ##)
    chapter_title_match = re.search(r'^## (.+)$', content, re.MULTILINE)
    if not chapter_title_match:
        print("Errore: Titolo del capitolo non trovato")
        return
    
    chapter_title = chapter_title_match.group(1)
    print(f"Capitolo: {chapter_title}")
    
    # Dividi per sezioni usando ### Section come delimitatore
    # Pattern che cattura "### Section" seguito da numero o testo
    sections = re.split(r'(### Section[^\n]*)', content)
    
    # Crea la directory di output se non esiste
    os.makedirs(output_dir, exist_ok=True)
    
    # Il primo elemento è il preambolo (titolo del capitolo e testo prima della prima sezione)
    preambolo = sections[0].strip()
    
    # Processa le sezioni
    section_count = 0
    for i in range(1, len(sections), 2):
        if i + 1 < len(sections):
            section_header = sections[i].strip()
            section_content = sections[i + 1].strip()
            
            section_count += 1
            
            # Estrai il numero o nome della sezione
            section_match = re.search(r'### Section\s+(\w+)', section_header)
            if section_match:
                section_id = section_match.group(1)
            else:
                section_id = str(section_count)
            
            # Crea il nome del file
            if section_id.isdigit():
                filename = f"sezione_{int(section_id):02d}.md"
            else:
                filename = f"sezione_{section_id}.md"
            filepath = os.path.join(output_dir, filename)
            
            # Scrivi il file della sezione
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"## {chapter_title}\n\n")
                f.write(f"{section_header}\n\n")
                f.write(section_content)
            
            print(f"  ✓ Creata sezione {section_id}: {filepath}")
    
    print(f"\nTotale sezioni create: {section_count}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python split_chapter.py <chapter_file> <output_directory>")
        print("Esempio: python split_chapter.py 'The World set Free_chapters/chapter_02.md' 'The World set Free_chapter02'")
        sys.exit(1)
    
    chapter_file = sys.argv[1]
    output_dir = sys.argv[2]
    
    if not os.path.exists(chapter_file):
        print(f"Errore: File {chapter_file} non trovato")
        sys.exit(1)
    
    split_chapter(chapter_file, output_dir)
