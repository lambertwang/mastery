import util
import travel
import combat

TARGET_WORD_COUNT = 50000

chapter_number = 1
chapter_titles = []
book_title = ''

def chapter(args):
    args.update({
        'armor_name': util.name(),
        'town_name': util.town(),
        'monster_name': util.monster_name(),
        'pc_weapon': 'sword'
    })

    result = ''

    chapter_title_plain = util.expand(util.chapter_title_plain(), **args)
    global chapter_titles
    chapter_titles.append(chapter_title_plain)

    # Actual chapter contents
    result += util.expand(util.chapter_title(chapter_title_plain), **args)
    # Town intro
    result += util.expand(util.town_intro(), **args)
    # Armory intro
    result += util.expand(util.armory_intro(), **args)

    # Armory explanation
    descriptions = util.monster_description(args['monster_name'])
    for description in descriptions:
        args['description'] = description
        result += util.expand(util.armory_explanation(), **args)
        result += util.expand(util.armory_more(), **args)

    # Leave armory
    result += util.expand(util.armory_no_more(), **args)

    # Get a new weapon
    old_weapon = args['pc_weapon']
    args['pc_weapon'] = util.expand('<weapon>', **args)
    result += util.expand(util.armory_new_weapon(old_weapon), **args)

    # Travelling to combat
    result += util.expand(travel.leave_town(), **args)

    # Combat intro
    result += util.expand(combat.combat_intro(args['monster_name']), **args)
    # Actual Combat
    result += util.expand(combat.combat(), **args)
    return result

def book():
    args = {
        'pc_name': util.name(),
        'wiz_name': util.name(),
    }
    global book_title
    book_title = util.expand(util.book_title(), **args)
    result = ''
    word_count = len(result.split(' '))

    global chapter_number
    global TARGET_WORD_COUNT
    while word_count < TARGET_WORD_COUNT:
        args['chapter_number'] = str(chapter_number)
        chapter_text = chapter(args)
        word_count += len(chapter_text.split(' '))
        result += chapter_text
        chapter_number += 1

    return result

def toc():
    global chapter_titles
    global book_title
    result = book_title
    for i in range(1, chapter_number):
        result += '[' + chapter_titles[i - 1] + '](#chapter' + str(i) + ')\n\n'

    return result


book_text = book()

with open('../Hero\'s Journey.md', 'w') as story_file:
    story_file.write(toc())
    story_file.write(book_text)
    # print(toc())
    # print(book_text)
