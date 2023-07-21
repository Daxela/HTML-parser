import bs4
from bs4 import BeautifulSoup


def selection_of_tags(soup: BeautifulSoup, name_parent_teg, name_super_parent_teg=None):  # ЛИСТЬЯ С РЕКУРСИЕЙ нев

    global foliage
    if name_super_parent_teg == None:
        name_super_parent_teg = soup.name
    if type(soup) == bs4.element.Tag:  # добавить элс чтобы если есть тупо текст тоже брать как лист проверить нужен ли последний иф
        i = len(soup.contents)
        tag = soup
    for j in range(i):
        information_foliage = []
        new_tag = tag.contents[j]
        if type(new_tag) == bs4.element.Tag:
            non_empty = [1 for c in new_tag.contents if
                         c.text.replace(' ', '').replace('\n', '').replace('\t', '') != '']
            new_name_super = new_tag.name
            if sum(non_empty) <= 1:
                new_name_super = name_super_parent_teg
            selection_of_tags(new_tag, tag.name, new_name_super)
        else:
            information_foliage.append(tag.name)
            information_foliage.append(name_parent_teg)
            information_foliage.append(name_super_parent_teg)
            information_foliage.append(tag.contents[j].text)
        foliage.append(information_foliage)

    return foliage


def start_sof(soup: BeautifulSoup):
    global foliage
    foliage = []
    return selection_of_tags(soup, 'html')
