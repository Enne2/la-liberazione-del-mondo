#!/usr/bin/env python3
"""
Script per riassemblare le sezioni tradotte in un unico file capitolo.
Uso: python3 merge_sections.py <directory_sezioni> <file_output>
"""

import os
import sys
import re
from pathlib import Path


def extract_section_number(filename):
    """Estrae il numero di sezione dal nome del file."""
    # Gestisce sia sezione_I.md che sezione_02.md
    match = re.search(r'sezione[_-](\w+)\.md', filename, re.IGNORECASE)
    if match:
        section = match.group(1)
        # Converte numeri romani in numeri per l'ordinamento
        roman_to_int = {
            'I': 1, 'II': 2, 'III': 3, 'IV': 4, 'V': 5,
            'VI': 6, 'VII': 7, 'VIII': 8, 'IX': 9, 'X': 10
        }
        if section in roman_to_int:
            return roman_to_int[section]
        try:
            return int(section)
        except ValueError:
            return 0
    return 0


def merge_sections(input_directory, output_file):
    """Unisce tutti i file di sezione in un unico file."""
    input_path = Path(input_directory)
    
    if not input_path.exists():
        print(f"❌ Errore: Directory '{input_directory}' non trovata")
        return False
    
    # Trova tutti i file .md nella directory
    section_files = sorted(
        [f for f in input_path.glob('*.md')],
        key=lambda x: extract_section_number(x.name)
    )
    
    if not section_files:
        print(f"❌ Errore: Nessun file .md trovato in '{input_directory}'")
        return False
    
    print(f"📚 Trovati {len(section_files)} file da unire:")
    for f in section_files:
        print(f"   - {f.name}")
    
    # Leggi il primo file per ottenere il titolo del capitolo
    with open(section_files[0], 'r', encoding='utf-8') as f:
        first_content = f.read()
    
    # Estrai il titolo del capitolo (prima riga con ##)
    chapter_title_match = re.search(r'^##\s+(.+)$', first_content, re.MULTILINE)
    chapter_title = chapter_title_match.group(0) if chapter_title_match else ""
    
    # Prepara il contenuto unificato
    merged_content = []
    
    # Aggiungi il titolo del capitolo una sola volta
    if chapter_title:
        merged_content.append(chapter_title)
        merged_content.append("")  # Riga vuota
    
    # Processa ogni file
    for section_file in section_files:
        with open(section_file, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        
        # Rimuovi il titolo del capitolo se presente (lo abbiamo già aggiunto)
        if chapter_title:
            content = re.sub(r'^##\s+.+$\n*', '', content, flags=re.MULTILINE)
        
        # Aggiungi il contenuto della sezione
        merged_content.append(content.strip())
        merged_content.append("")  # Riga vuota tra le sezioni
    
    # Scrivi il file di output
    output_path = Path(output_file)
    final_content = "\n".join(merged_content).strip() + "\n"
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(final_content)
    
    print(f"\n✅ File unificato creato: {output_file}")
    print(f"   📊 Dimensione: {len(final_content)} caratteri")
    print(f"   📄 Sezioni unite: {len(section_files)}")
    
    return True


def main():
    if len(sys.argv) != 3:
        print("Uso: python3 merge_sections.py <directory_sezioni> <file_output>")
        print("\nEsempio:")
        print('  python3 merge_sections.py "The World set Free_chapter02_IT" "capitolo_02_completo_IT.md"')
        sys.exit(1)
    
    input_directory = sys.argv[1]
    output_file = sys.argv[2]
    
    success = merge_sections(input_directory, output_file)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
