import os
import shutil

SRC_DIR = '/home/zhengxueen/github-project/ai-engineering-from-scratch/phases'
DST_DIR = '/home/zhengxueen/github-project/ai-engineering-from-scratch/zheng-docs'

count = 0

for phase_name in sorted(os.listdir(SRC_DIR)):
    phase_path = os.path.join(SRC_DIR, phase_name)
    if not os.path.isdir(phase_path):
        continue

    phase_dst_dir = os.path.join(DST_DIR, phase_name)

    for chapter_dir in sorted(os.listdir(phase_path)):
        chapter_path = os.path.join(phase_path, chapter_dir)
        if not os.path.isdir(chapter_path):
            continue

        zh_md_path = os.path.join(chapter_path, 'docs', 'zh.md')
        if not os.path.isfile(zh_md_path):
            continue

        parts = chapter_dir.split('-', 1)
        if len(parts) == 2:
            chapter_num, chapter_name = parts
        else:
            chapter_num = chapter_name = parts[0]

        os.makedirs(phase_dst_dir, exist_ok=True)

        new_name = f'{chapter_num}_{chapter_name}.md'
        dst_path = os.path.join(phase_dst_dir, new_name)

        shutil.copy2(zh_md_path, dst_path)
        print(f'Copied: {zh_md_path} -> {dst_path}')
        count += 1

print(f'\nDone! {count} files copied.')