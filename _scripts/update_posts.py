import pathlib
import yaml
import re

from utils import format_authors, get_date

metadata_dir = pathlib.Path('_data/paper_metadata')
posts_dir = pathlib.Path('_posts')

metadata_dir.mkdir(exist_ok=True)
posts_dir.mkdir(exist_ok=True)

#existing_metadata_files = {f.name for f in metadata_dir.glob("*.yml")}


for metadata_file in metadata_dir.glob("*.yml"):
    with open(metadata_file) as file:
        metadata = yaml.safe_load(file)

    header_keys = ['title', 'venue', 'citationCount']
    body_keys = ['abstract']
    header = {'layout': 'post',
              'excerpt_image': 'NO_EXCERPT_IMAGE',
              'author': format_authors(metadata.get('authors', [])),
              'title': metadata.get('title'),
              'date': get_date(metadata),
              'venue': metadata.get('venue'),
              'citationCount': metadata.get('citationCount'),
              'doi': metadata['externalIds']['DOI'],
              'categories': None,
              'tags': None
              }
    # print('---')
    # print(yaml.safe_dump(header))
    # print('---')
    # print(metadata['abstract'])
    # print(metadata_file.with_suffix('.md').name)

    # jekyll only allow '-' as special characters in filenames
    post_filename = metadata_file.with_suffix('.md').name
    name, ext = post_filename.rsplit('.', 1)
    filename_jekyllFormat = re.sub(r'[^a-zA-Z0-9]', '-', name)
    post_filename = f'{filename_jekyllFormat}.{ext}'

    # now save
    with open(posts_dir / post_filename, 'w') as file:
        file.write('---\n')
        yaml.safe_dump(header, file)
        file.write('---\n')
        file.write(metadata['abstract'])
        file.write('\n')