#!/usr/bin/env python3
"""
Script per ripulire le traduzioni da intestazioni ripetute, piè di pagina e numeri di pagina.
"""

import re
import sys
import os
from pathlib import Path


def clean_translation(content):
    """
    Rimuove intestazioni ripetute, numeri di pagina e elementi paratestuali.
    
    Args:
        content: il contenuto del file da pulire
        
    Returns:
        contenuto pulito
    """
    lines = content.split('\n')
    cleaned_lines = []
    skip_next_empty = False
    
    for i, line in enumerate(lines):
        # Salta intestazioni ripetute "### La Liberazione del Mondo"
        if line.strip() == "### La Liberazione del Mondo":
            skip_next_empty = True
            continue
            
        # Salta numeri di pagina standalone
        if line.strip().isdigit():
            skip_next_empty = True
            continue
        
        # Salta righe vuote subito dopo elementi rimossi
        if skip_next_empty and line.strip() == "":
            skip_next_empty = False
            continue
            
        skip_next_empty = False
        cleaned_lines.append(line)
    
    # Rimuovi righe vuote multiple consecutive alla fine di paragrafi
    result = '\n'.join(cleaned_lines)
    
    # Rimuovi spazi multipli consecutivi
    result = re.sub(r'\n\n\n+', '\n\n', result)
    
    # Assicurati che il file termini con una sola newline
    result = result.rstrip() + '\n'
    
    return result


def clean_file(file_path):
    """
    Pulisce un singolo file di traduzione.
    
    Args:
        file_path: path del file da pulire
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    cleaned = clean_translation(content)
    
    # Salva solo se ci sono modifiche
    if cleaned != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(cleaned)
        print(f"✓ Pulito: {file_path}")
        return True
    else:
        print(f"○ Già pulito: {file_path}")
        return False


def clean_directory(directory):
    """
    Pulisce tutti i file .md in una directory.
    
    Args:
        directory: path della directory contenente i file da pulire
    """
    files = sorted(Path(directory).glob("*.md"))
    
    if not files:
        print(f"Nessun file .md trovato in {directory}")
        return
    
    print(f"\nTrovati {len(files)} file da verificare:\n")
    
    modified_count = 0
    for file_path in files:
        if clean_file(str(file_path)):
            modified_count += 1
    
    print(f"\n{'='*60}")
    print(f"File modificati: {modified_count}/{len(files)}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python clean_translations.py <directory>")
        print("Esempio: python clean_translations.py 'The World set Free_chapter02_IT'")
        sys.exit(1)
    
    directory = sys.argv[1]
    
    if not os.path.exists(directory):
        print(f"Errore: Directory {directory} non trovata")
        sys.exit(1)
    
    clean_directory(directory)
