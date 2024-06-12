og_category_dic = {'Paper/Cardboard': 23.2,
                   'Textiles': 3.9,
                   'Food waste': 33.9}

category_names = ['Paper/Cardboard','blaaaa','Textiles',  'Food waste']

new_dict = {}

for element in category_names:
    if element in og_category_dic.keys():
        new_dict[element] = og_category_dic[element]
    else:
        new_dict[element] = 0

values = new_dict.values()

print(values)
