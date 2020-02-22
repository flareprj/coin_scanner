import numpy as np

itemT = [['1', 'Fox Trading', 'FOXT', '$75 189', '$0,002970', '-27,89%'],
         ['2', 'Fucking2', 'NII2', '$21 189', '$0,7411570', '-7,89%'],
         ['3', 'Fucking3', 'NII3', '$21 189', '$0,7411570', '-7,89%'],
         ['4', 'Fucking4', 'NII4', '$21 189', '$0,7411570', '-7,89%']
         ]
nestedT = [['Mercatox1', 'FOXT/BTC'], ['Nsosa2', 'XXS/TZX'], ['Mercatox3', 'FOXT/BTC'], ['Nsosa4', 'XXS/TZX']]

# for i in range(1, 8):
#     item.append([])
#     for k in range(1, 7):
#         item[i - 1].append(k)

# for i in range(1, 4):
#     arr.append([])
#     for k in range(1, 7):
#         arr[i - 1].append(k)
#     arr[i - 1].append(item)
#
# for i in range(1, 4):  # вывод k-элементов i-раз
#     for k in range(1, 7):
#         print(arr[i - 1])

c = np.concatenate((itemT, nestedT), axis=1)
print(c)

# for i in range(0, 1):
#     for td in item:
#         for i in range(0, 6):
#             print(td[i])
#         for tx in nested:
#             for k in range(0, 2):
#                 print(tx[k])
#



# print("\n")
# print(arr[0][6])
# print(arr[0][6][1])


# {% for td in items %}
#           {% if loop.index == 2 %}
#             <div class="col"><a href="{{ td.get_attribute('href') }}">{{ td.text }}</a></div>
#           {% else %}
#             <div class="col">{{ td }}</div>
#           {% endif %}
#       {% endfor %}


# <div class="container mt-5">
# <div class="row ext1">
# {% for item in items %}
# <div class="col">{{ item }}</div>
# {% endfor %}
# </div>
# <div class="row ext2">
# {% for tds in nested %}
# <div class="col">{{ tds }}</div>
# {% endfor %}
# </div>
# </div>


# {% for item in c %}
#     <div class="row ext1">
#     {% for x in item %}
#         {% if loop.index > 7 %}
#         <div class="col">
#              <div class="col"><a href="{{ x.get_attribute('href') }}">{{ x.text }}</a></div>
#         </div>
#         {% else %}
#             <div class="col">{{ x }}</div>
#         {% endif %}
#     {% endfor %}
#     </div>
#     {% endfor %}