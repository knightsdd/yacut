from random import randint


def get_unique_short_id() -> str:
    rand_list = []
    for _ in range(6):
        i = randint(0, 2)
        if i == 0:
            rand_list.append(chr(randint(48, 57)))
        elif i == 1:
            rand_list.append(chr(randint(65, 90)))
        else:
            rand_list.append(chr(randint(97, 122)))

    return ''.join(rand_list)


if __name__ == '__main__':
    print(get_unique_short_id())
