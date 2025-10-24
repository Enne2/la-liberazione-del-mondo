#!/usr/bin/env python3
"""Script per creare libro_completo.md con struttura corretta"""

import re

# Aggiungo il PRELUDIO (già in formato corretto con ##)
with open('prelude_completo_IT.md', 'r') as f:
    content = f.read()
    
    with open('libro_completo.md', 'a') as out:
        out.write(content)
        out.write('\n\n\\newpage\n\n')

# Aggiungo i capitoli
capitoli = [
    ('capitolo_01_completo_IT.md', 'Capitolo 1', 'La Nuova Fonte di Energia'),
    ('capitolo_02_completo_IT.md', 'Capitolo 2', 'L\'Ultima Guerra'),
    ('capitolo_03_completo_IT.md', 'Capitolo 3', 'La Fine della Guerra'),
    ('capitolo_04_completo_IT.md', 'Capitolo 4', 'La Nuova Fase'),
    ('capitolo_05_completo_IT.md', 'Capitolo 5', 'Gli Ultimi Giorni di Marcus Karenin')
]

for filename, numero, titolo in capitoli:
    with open(filename, 'r') as f:
        content = f.read()
        
        # Rimuovo il titolo esistente se c'è
        lines = content.split('\n')
        if lines[0].startswith('#'):
            lines = lines[1:]
        content = '\n'.join(lines).strip()
        
        # Aggiungo il titolo corretto
        chapter_text = f'# {numero}: {titolo}\n\n{content}\n\n\\newpage\n\n'
        
        with open('libro_completo.md', 'a') as out:
            out.write(chapter_text)

print("libro_completo.md creato con successo!")
