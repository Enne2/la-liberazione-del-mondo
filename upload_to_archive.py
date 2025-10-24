#!/usr/bin/env python3
"""Upload PDF to Internet Archive"""

from internetarchive import upload

# Metadata for the item
metadata = {
    'title': 'La Liberazione del Mondo - The World Set Free (Traduzione Italiana)',
    'creator': 'H.G. Wells',
    'translator': 'Matteo Benedetto',
    'date': '2025',
    'language': 'Italian',
    'subject': ['science fiction', 'H.G. Wells', 'atomic energy', 'Italian translation', 'The World Set Free'],
    'description': 'Traduzione italiana completa del romanzo profetico "The World Set Free" di H.G. Wells (1914). Il romanzo previde l\'energia atomica e le sue conseguenze sulla civiltà umana. Include PRELUDIO + 5 capitoli, 56 sezioni totali, circa 375.000 caratteri. Traduzione di Matteo Benedetto tramite workflow agentico LLM, completata il 25 ottobre 2025.',
    'licenseurl': 'http://creativecommons.org/licenses/by/4.0/',
    'mediatype': 'texts',
    'collection': 'opensource',
}

# Upload file
identifier = 'la-liberazione-del-mondo-hg-wells-2025'
file_path = 'La_Liberazione_del_Mondo.pdf'

print(f"Uploading {file_path} to archive.org...")
print(f"Identifier: {identifier}")

r = upload(identifier, files=[file_path], metadata=metadata, access_key='y1IqqXC1HK5xPNQL', secret_key='lYjUjJWyVxGsA3FX')

print(f"\nUpload complete!")
print(f"URL: https://archive.org/details/{identifier}")
