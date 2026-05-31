import os
import shutil
import glob

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BASE_DIR)
PHASES_DIR = os.path.join(ROOT, 'phases')
DOCS_OUT = os.path.join(BASE_DIR, 'docs')
PROMPTS_OUT = os.path.join(BASE_DIR, 'outputs', 'prompts')
SKILLS_OUT = os.path.join(BASE_DIR, 'outputs', 'skills')


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)


def copy_files():
    ensure_dir(DOCS_OUT)
    ensure_dir(PROMPTS_OUT)
    ensure_dir(SKILLS_OUT)

    stats = {'doc': 0, 'prompt': 0, 'skill': 0}

    for phase_name in sorted(os.listdir(PHASES_DIR)):
        phase_path = os.path.join(PHASES_DIR, phase_name)
        if not os.path.isdir(phase_path):
            continue

        for chapter_name in sorted(os.listdir(phase_path)):
            chapter_path = os.path.join(phase_path, chapter_name)
            if not os.path.isdir(chapter_path):
                continue

            prefix = f'{phase_name}+{chapter_name}'

            # 1. en.md -> doc.md
            en_path = os.path.join(chapter_path, 'docs', 'en.md')
            if os.path.isfile(en_path):
                dst = os.path.join(DOCS_OUT, f'{prefix}+doc.md')
                shutil.copy2(en_path, dst)
                stats['doc'] += 1

            # 2. outputs/prompt*.md
            outputs_dir = os.path.join(chapter_path, 'outputs')
            if os.path.isdir(outputs_dir):
                for prompt_file in sorted(glob.glob(os.path.join(outputs_dir, 'prompt*.md'))):
                    basename = os.path.basename(prompt_file)
                    dst = os.path.join(PROMPTS_OUT, f'{prefix}+{basename}')
                    shutil.copy2(prompt_file, dst)
                    stats['prompt'] += 1

                # 3. outputs/skill*.md
                for skill_file in sorted(glob.glob(os.path.join(outputs_dir, 'skill*.md'))):
                    basename = os.path.basename(skill_file)
                    dst = os.path.join(SKILLS_OUT, f'{prefix}+{basename}')
                    shutil.copy2(skill_file, dst)
                    stats['skill'] += 1

    print(f'Copied {stats["doc"]} doc files, {stats["prompt"]} prompt files, {stats["skill"]} skill files.')


if __name__ == '__main__':
    copy_files()