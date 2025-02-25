import pathlib
import yaml
import re
import pandas as pd

from utils import format_authors, get_date

metadata_dir = pathlib.Path('_data/paper_metadata')
posts_dir = pathlib.Path('_posts')
tag_filename = '_data/tags.csv'

metadata_dir.mkdir(exist_ok=True)
posts_dir.mkdir(exist_ok=True)

# delete all existing posts
for item in posts_dir.iterdir():
    if item.is_file() or item.is_symlink():
        item.unlink()

df_tags = pd.read_csv(tag_filename, sep=";")
df_tags.set_index('doi', inplace=True)
df_tags.index = df_tags.index.str.lower()

# create posts anew
for metadata_file in metadata_dir.glob("*.yml"):
    with open(metadata_file) as file:
        metadata = yaml.safe_load(file)

    paper_tags = df_tags.columns[df_tags.loc[metadata['externalIds']['DOI'].lower()] == 1].tolist()

    header = {'layout': 'post',
              'excerpt_image': 'NO_EXCERPT_IMAGE',
              'author': format_authors(metadata.get('authors', [])),
              'title': metadata.get('title'),
              'date': get_date(metadata),
              'venue': metadata.get('venue'),
              'citationCount': metadata.get('citationCount'),
              'doi': metadata['externalIds']['DOI'],
              'categories': metadata.get('categories', None),
              'tags': paper_tags
              }

    # format the post title to match metadata and comply with jekyll
    # jekyll only allows '-' as special characters in filenames
    post_filename = metadata_file.with_suffix('.md').name
    name, ext = post_filename.rsplit('.', 1)
    filename_jekyllFormat = re.sub(r'[^a-zA-Z0-9]', '-', name)
    post_filename = f'{filename_jekyllFormat}.{ext}'

    # now save
    with open(posts_dir / post_filename, 'w') as file:
        file.write('---\n')
        yaml.safe_dump(header, file)
        file.write('---\n')
        file.write(f"{metadata.get('abstract','')}\n")
