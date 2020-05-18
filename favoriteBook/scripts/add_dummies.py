

"""
py manage.py runscripts add_dummies.py

"""

# from django.utils import timezone
from book.models import RecommendedBook
import random,string
from faker import Faker
from PIL import Image,ImageDraw, ImageFont
from django.contrib.auth.models import User
# User=get_user_model()
fakegen=Faker("ja_JP")



colors = [(255,0,0), (0,255,0), (0,0,255),(0,0,0),(255,255,255)]

def make_image(N):
    """
    画像ファイルを作成
    返り値はファイルの名前
    """
    screen = (200+random.randint(0,100), 200+random.randint(0,100))    # QVGA
    pen_color=random.choice(colors)
    bg_color=random.choice(colors)
    img = Image.new('RGB', screen, bg_color)
    x, y = img.size
    u = x - 1
    v = y - 1
    draw = ImageDraw.Draw(img)
    draw.line((0, 0, u, 0), pen_color)
    draw.line((0, 0, u, v), pen_color)
    draw.line((0, 0, 0, v), pen_color)
    draw.line((u, 0, 0, v), pen_color)
    draw.line((u, 0, u, v), pen_color)
    draw.line((0, v, u, v), pen_color)
    filename="/sample_{}.jpg".format(N)
    img.save("media"+filename)
    return filename

# n文字のランダムな文字列の生成
# def randomstring(n):
#    randlst = [random.choice(string.ascii_letters + string.digits) for i in range(n)]
#    return ''.join(randlst)

genres=["技術書","英語","数学","小説","感動","楽しい"]

fakegen = Faker()



def run():
    N=5
    for entry in range(N):
        imgfile=make_image(entry)
        bookGenre=random.choice(genres)+" "+random.choice(genres)
        dummy=RecommendedBook(author=fakegen.name(), bookTitle=fakegen.word(),
                              content=fakegen.text(), genre=bookGenre,
                              bookImage=imgfile
                              )
        dummy.save()
	print("データ生成に成功しました")
