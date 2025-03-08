import os

info = []


def human_read_format(size):
    count = 0
    list_names = {0: 'Б', 1: 'КБ', 2: 'МБ', 3: 'ГБ'}
    while size >= 1024:
        size /= 1024
        count += 1
    return f'{round(size)}{list_names[count]}'


def get_files_sizes(path):
    all_sizes = []
    result = []
    for currentdir, dirs, files in os.walk(path, topdown=True):
        if '\\' in currentdir:
            new_currentdir = currentdir.split('/')[-1]
        if ':' in currentdir:
            new_currentdir = currentdir.split(':')[-1]
        for f in files:
            full_size = []
            if new_currentdir:
                full_size.append(os.path.getsize(f"{new_currentdir}/{f}"))
            else:
                full_size.append(os.path.getsize(f))
            result.append((f, human_read_format(sum(full_size))))
            all_sizes.append(sum(full_size))
    all_sizes.sort()
    for i in all_sizes[::-1]:
        for k in result:
            if human_read_format(i) in k:
                info.append(k)
    return info


answer = get_files_sizes(input())  # C:
for i in enumerate(answer[:10]):
    print(f'{i[0] + 1} {i[1][0]} - {i[1][1]}')
