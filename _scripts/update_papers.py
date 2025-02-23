import pathlib
import requests
import time
import yaml

from utils import read_included_dois, safe_doi, get_date

doi_filename = '_data/dois.csv'
metadata_dir = pathlib.Path('_data/paper_metadata')
posts_dir = pathlib.Path('_posts')

metadata_dir.mkdir(exist_ok=True)
posts_dir.mkdir(exist_ok=True)

df = read_included_dois(doi_filename)
existing_metadata_files = {f.name for f in metadata_dir.glob("*.yml")}

def download_metadata(doi):
    '''Download paper metadata from semanticscholar.'''
    params = {
        "fields": "referenceCount,citationCount,title,abstract,externalIds,year,publicationDate,authors,venue"
    }
    headers = {}

    r = requests.get(
        f'https://api.semanticscholar.org/graph/v1/paper/{doi}',
        headers=headers,
        params=params,
    )

    if r.status_code == 200:
        return r.json()
    return None

# check for each doi if we have the metadata yet
for doi in df['doi']:
    doi_safe = safe_doi(doi)
    
    if not any(doi_safe.lower() in filename.lower() for filename in existing_metadata_files):
        metadata = download_metadata(doi)
        firstAuthor_lastName = metadata['authors'][0]['name'].split(' ')[-1]
        date = get_date(metadata)

        metadata_filename = metadata_dir / f'{date}_{firstAuthor_lastName}_{doi_safe}.yml'
        with open(metadata_filename, 'w') as file:
            yaml.safe_dump(metadata, file)
        time.sleep(.1)

# delete metadata that is no longer on the doi list
current_dois = df['doi'].apply(safe_doi).apply(lambda x: x.lower())
for metadata_file in metadata_dir.glob("*.yml"):
    if not any(doi in metadata_file.name.lower() for doi in current_dois):
        metadata_file.unlink()  # Delete the file
