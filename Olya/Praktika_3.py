from bs4 import BeautifulSoup as bs
import codecs
import datetime

doc = bs(codecs.open('what.html', encoding='utf-8').read(), 'html.parser')
title = doc.select('div.pgs-sinfo_list span')[0].decode_contents().strip()
about = doc.select('.pgs-sinfo-info p')[0].decode_contents().strip()
rating = {'IMDB': float(doc.select('.pgs-sinfo_list.rating span ')[0].decode_contents().strip()), 'КиноПоиск': float(doc.select('.pgs-sinfo_list.rating span ')[1].decode_contents().strip())}
yegs = list(map(lambda x: x.decode_contents().strip(), doc.select('div.b-taglist.dl div a')))
act = list(map(lambda x: x.decode_contents().strip(), doc.select('a.tooltipstered span')))

print('Название:', title)
print('Аннотация:', about)
print('Рейтинг:', rating)
print('Теги:', yegs)
print('Актеры', act)




reviews = list(map(lambda x: x.decode_contents().strip(),doc.select('div.pgs-review-post ')))
author_reviews = list(map(lambda x: x.decode_contents().strip(),doc.select('div.pgs-review-name a')))#[0].decode_contents().strip()
print('Рецензий на странице: ', len(reviews))
print('Авторы рецензиий:', author_reviews)


comments = []
for node in doc.select('div.svc_comment'):
    text = node.select('div.svc_msg')[0].decode_contents().strip()
    #date = datetime.datetime.strptime(node.select('div.svc_nick span.svc_date')[0].decode_contents().strip(), )
    author = node.select('div.svc_info a')[0].decode_contents().strip()
    comments.append({'text': text, 'author': author})

print('Комментариев на странице: ', len(comments))
print('Самый маленький комментарий:', sorted(comments, key=lambda x: len(x['text']))[0]['text'],comments[0]['author'])

