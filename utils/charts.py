from budget.models import CATEGORY_OPTIONS

MONTHS =[
    'January',
    'February',
    'March',
    'April',
    'May',
    'June',
    'July',
    'August',
    'September',
    'October',
    'November',
    'December',
]

MONTH_DICT = {
        1:'January',
        2:'February',
        3:'March',
        4:'April',
        5:'May',
        6:'June',
        7:'July',
        8:'August',
        9:'September',
        10:'October',
        11:'November',
        12:'December',
}

CATEGORIES = [pair[0] for pair in CATEGORY_OPTIONS][:-1]

COLOR_PALETTE = ['#55efc4','#81ecec','#a29bfe','#ffeaa7','#fab1a0','#ff7675','#fd798a']

color_primary, color_success, color_danger = '#5ab275', COLOR_PALETTE[0], COLOR_PALETTE[5]

def get_year_dict():
    year_dict = dict()

    for month in MONTHS:
        year_dict[month] = 0

    return year_dict

def get_category_dict():
    category_dict = dict()

    for cat in CATEGORIES:
        category_dict[cat] = 0

    return category_dict

def generate_color_palette(amount):
    palette = []

    iter = 0
    while iter < len(COLOR_PALETTE) and len(palette) < amount:
        palette.append(COLOR_PALETTE[iter])
        iter += 1
        if iter == len(COLOR_PALETTE) and len(palette) < amount:
            iter = 0
        
    return palette
