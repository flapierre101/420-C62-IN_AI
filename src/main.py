import re

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    count = {}
    i = 0
    for w in re.findall('\w+', open('../textes/LesTroisMousquetairesUTF8.txt', 'r', encoding="UTF-8").read()):
        if w.upper() in count:
            pass
        else:
            count[w.upper()] = i
            i += 1

    print(count)
