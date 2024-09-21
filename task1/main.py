import argparse
import asyncio
import logging
import shutil
import sys
from pathlib import Path

logging.basicConfig(level=logging.ERROR, format='%(asctime)s %(levelname)s:%(message)s')


async def copy_file(file_path, source_folder, destination_folder):
    try:
        extension = file_path.suffix[1:] if file_path.suffix else 'no_extension'
        dest_folder = destination_folder / extension

        dest_folder.mkdir(parents=True, exist_ok=True)

        dest_file_path = dest_folder / file_path.relative_to(source_folder)

        dest_file_path.parent.mkdir(parents=True, exist_ok=True)

        await asyncio.to_thread(shutil.copy2, file_path, dest_file_path)
    except Exception as e:
        logging.error(f'Помилка при копіюванні файлу {file_path}: {e}')


async def read_folder(folder_path, source_folder, destination_folder):
    tasks = []
    try:
        for path in folder_path.iterdir():
            if path.is_dir():
                tasks.append(read_folder(path, source_folder, destination_folder))
            elif path.is_file():
                tasks.append(copy_file(path, source_folder, destination_folder))
    except Exception as e:
        logging.error(f'Помилка при читанні папки {folder_path}: {e}')
    if tasks:
        await asyncio.gather(*tasks)


def parse_args():
    parser = argparse.ArgumentParser(description='Асинхронне сортування файлів за розширенням.')
    parser.add_argument('source', help='Вихідна папка для сканування')
    parser.add_argument('destination', help='Цільова папка для копіювання файлів')
    return parser.parse_args()


async def main():
    args = parse_args()
    source_folder = Path(args.source).resolve()
    destination_folder = Path(args.destination).resolve()

    if not source_folder.is_dir():
        logging.error(f'Вихідна папка "{source_folder}" не існує або не є папкою.')
        sys.exit(1)

    await read_folder(source_folder, source_folder, destination_folder)


if __name__ == '__main__':
    asyncio.run(main())
