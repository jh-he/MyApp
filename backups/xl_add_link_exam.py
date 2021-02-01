# -*- coding: utf-8 -*-

import xlwings as xw

app = xw.App(visible=True, add_book=False)
app.display_alerts = False
app.screen_updating = True

wb = app.books.open('./Track.xlsm')
ws = wb.sheets['Test']

'''alt_number_link_list = []
for i in range(4):
    hyperlink = 'hyp' + str(i)
    alt_number_link_list.append(hyperlink)
print(alt_number_link_list)
'''
ntests = 2
ws.range(f'2:{ntests+1}').api.Insert()
rng = ws.range(f'A2:H{ntests+1}')

# Set Format of inserted rows
rng.color = None
rng.api.Font.Bold = False
rng.api.HorizontalAlignment = -4131
number = ['AA', 'BB', 'CC', 'DD']
dic = {'AA': 'A', 'BB': 'B', 'CC': 'C', 'DD': 'D'}

for j in range(ntests):
    num = number[j]
    link = dic[num]
    print(num, link)
    # cell_value = str(j)
    ws[j + 1, 1].add_hyperlink(link, num)
rng2 = 'B2:B'+str(ntests+1)
ws.range(rng2).api.Font.Name = 'Arial'
ws.range(rng2).api.Font.Size = 9

wb.save()
app.quit()
