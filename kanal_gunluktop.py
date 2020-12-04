import pymysql as MySQLdb
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from PIL import Image
from instabot import Bot
import locale
import os
import time



db = MySQLdb.connect("ip","user","password","db_names" )
cursor = db.cursor()

query="Select * from kanal"
df = pd.read_sql(query, con=db)

dun = datetime.today() - timedelta(days=1)
gun_ad = dun.strftime("%A")
dun = dun.strftime("%Y-%m-%d")
print(gun_ad)



try:
    bot = Bot()
    bot.login(username="",password="")
except:
    pass

kanalID_list = df["ID"].unique()
kanalad_list = df["ad"].unique()
kanaltag_list = df["tag"]
kanaluser_list = df["user_id"]



kanalID_list_son=[]
if gun_ad=='Monday':
    kanalID_list_son.append(kanalID_list[0])
    kanalID_list_son.append(kanalID_list[1])
elif gun_ad=='Tuesday':
    kanalID_list_son.append(kanalID_list[2])
    kanalID_list_son.append(kanalID_list[3])
elif gun_ad=='Wednesday':
    kanalID_list_son.append(kanalID_list[4])
    kanalID_list_son.append(kanalID_list[5])
elif gun_ad=='Thursday':
    kanalID_list_son.append(kanalID_list[6])
    kanalID_list_son.append(kanalID_list[7])
elif gun_ad=='Friday':
    kanalID_list_son.append(kanalID_list[8])
    kanalID_list_son.append(kanalID_list[9])
elif gun_ad=='Saturday':
    kanalID_list_son.append(kanalID_list[10])
    kanalID_list_son.append(kanalID_list[11])
elif gun_ad=='Sunday':
    kanalID_list_son.append(kanalID_list[12])
    kanalID_list_son.append(kanalID_list[13])

print(kanalID_list_son)

goruntulenmeler=[]
begenmeler=[]
begenmemeler=[]
yorumlar=[]

for kanalID in kanalID_list_son:
    fotolar=[]
    query=f"SELECT DISTINCT kanal.user_id as tag,kanal.ad as kanalad,data.ad,gunluk.goruntulenme,gunluk.begenme,gunluk.begenmeme,gunluk.yorum FROM `gunluk`,data,kanal where data_videoID=data.videoID AND gunluk.tarih='{dun}' and gunluk.kanal_ID='{kanalID}' AND gunluk.kanal_ID=kanal.ID"
    df = pd.read_sql(query, con=db)
    tag = df['tag'][0]
    kanalad = df['kanalad'][0]
    videoad = df['ad']
    goruntulenmeler= df['goruntulenme']
    begenmeler = df['begenme']
    begenmemeler=df['begenmeme']
    yorumlar = df['yorum']

    liste = [[] for i in range(len(goruntulenmeler))]
    for j in range(0,len(goruntulenmeler)):
        ad= videoad[j]
        liste[j] = [kanalad,ad,goruntulenmeler[j],begenmeler[j],begenmemeler[j],yorumlar[j]]

    df2= pd.DataFrame(list(liste),columns =['KanalAd','Videoad','Goruntulenme', 'Begenme', 'Begenmeme', 'Yorum']) 
    print(df2)
    img = '/home/yonetici/verianaliz/arkaplan.jpg'
    def goruntulenmetop():
        plt.style.use("dark_background")
        for param in ['text.color', 'axes.labelcolor', 'xtick.color', 'ytick.color']:
            plt.rcParams[param] = '0.9'  # very light grey
        for param in ['figure.facecolor', 'axes.facecolor', 'savefig.facecolor']:
            plt.rcParams[param] = '#212946'  # bluish dark grey

        colors = [
            '#BD5E00',
            '#ED7700',
            '#EE8F32',
            '#F7B36D',
            '#F0C091',      
        ]
        explode = (0.1, 0.02, 0.02, 0.02, 0.02)#, 0.01, 0.01, 0.01, 0.01, 0.01)
        figure = plt.gcf()  # get current figure
        figure.set_size_inches(16, 9) 

        x = df2.sort_values('Goruntulenme',ascending=False)

        result = x['Videoad']
        for adlar in result:
            video = adlar
            break;
        result = x['Goruntulenme']
        for adlar in result:
            goruntu = adlar
            break;
        label=[]
        for i in x['Videoad'].head(5):
            label.append(f"{i[:35]}...")

        plt.pie(x['Goruntulenme'].head(5),autopct='%1.1f%%',colors=colors,shadow=True,startangle=90,explode=explode,textprops={'fontsize': 27})
        plt.axis('equal')
        plt.title(f"{dun}\n{x['KanalAd'][0]}\nYouTube kanalının {dun} tarihinde  En Çok İzlenen Videoları\n Top 5 Listesi",fontsize=27)
        plt.legend(labels=label,loc=3,fontsize=15)
        plt.savefig('kanalgunluk_top10.jpg',bbox_inches='tight')
        
        watermark_photo(img, 'g1.jpg',
                        'kanalgunluk_top10.jpg', position=(225,90))
        fotolar.append('g1.jpg')
        
    def begenmetop():
        plt.style.use("dark_background")
        for param in ['text.color', 'axes.labelcolor', 'xtick.color', 'ytick.color']:
            plt.rcParams[param] = '0.9'  # very light grey
        for param in ['figure.facecolor', 'axes.facecolor', 'savefig.facecolor']:
            plt.rcParams[param] = '#212946'  # bluish dark grey

        colors = [
            '#BD5E00',
            '#ED7700',
            '#EE8F32',
            '#F7B36D',
            '#F0C091',      
        ]
        explode = (0.1, 0.02, 0.02, 0.02, 0.02)#, 0.01, 0.01, 0.01, 0.01, 0.01)
        figure = plt.gcf()  # get current figure
        figure.set_size_inches(16, 9) 

        x = df2.sort_values('Begenme',ascending=False)

        result = x['Videoad']
        for adlar in result:
            video = adlar
            break;
        result = x['Begenme']
        for adlar in result:
            goruntu = adlar
            break;
        label=[]
        for i in x['Videoad'].head(5):
            label.append(f"{i[:35]}...")

        plt.pie(x['Begenme'].head(5),autopct='%1.1f%%',colors=colors,shadow=True,startangle=90,explode=explode,textprops={'fontsize': 27})
        plt.axis('equal')
        plt.title(f"{dun}\n{x['KanalAd'][0]}\nYouTube kanalının {dun} tarihinde  En Çok Begenilen Videoları\n Top 5 Listesi",fontsize=27)
        plt.legend(labels=label,loc=3,fontsize=15)
        plt.savefig('kanalgunluk_top10.jpg',bbox_inches='tight')

        watermark_photo(img, 'g2.jpg',
                        'kanalgunluk_top10.jpg', position=(225,90))
                        
        fotolar.append('g2.jpg')
    
    def begenmemetop():
        plt.style.use("dark_background")
        for param in ['text.color', 'axes.labelcolor', 'xtick.color', 'ytick.color']:
            plt.rcParams[param] = '0.9'  # very light grey
        for param in ['figure.facecolor', 'axes.facecolor', 'savefig.facecolor']:
            plt.rcParams[param] = '#212946'  # bluish dark grey

        colors = [
            '#BD5E00',
            '#ED7700',
            '#EE8F32',
            '#F7B36D',
            '#F0C091',      
        ]
        explode = (0.1, 0.02, 0.02, 0.02, 0.02)#, 0.01, 0.01, 0.01, 0.01, 0.01)
        figure = plt.gcf()  # get current figure
        figure.set_size_inches(16, 9) 

        x = df2.sort_values('Begenmeme',ascending=False)

        result = x['Videoad']
        for adlar in result:
            video = adlar
            break;
        result = x['Begenmeme']
        for adlar in result:
            goruntu = adlar
            break;
        label=[]
        for i in x['Videoad'].head(5):
            label.append(f"{i[:35]}...")

        plt.pie(x['Begenmeme'].head(5),autopct='%1.1f%%',colors=colors,shadow=True,startangle=90,explode=explode,textprops={'fontsize': 27})
        plt.axis('equal')
        plt.title(f"{dun}\n{x['KanalAd'][0]}\nYouTube kanalının {dun} tarihinde  En Çok Dislike Alan Videoları\n Top 5 Listesi",fontsize=27)
        plt.legend(labels=label,loc=3,fontsize=15)
        plt.savefig('kanalgunluk_top10.jpg',bbox_inches='tight')

        watermark_photo(img, 'g3.jpg',
                        'kanalgunluk_top10.jpg', position=(225,90))
                        
        fotolar.append('g3.jpg')
    
    def yorumtop():
        plt.style.use("dark_background")
        for param in ['text.color', 'axes.labelcolor', 'xtick.color', 'ytick.color']:
            plt.rcParams[param] = '0.9'  # very light grey
        for param in ['figure.facecolor', 'axes.facecolor', 'savefig.facecolor']:
            plt.rcParams[param] = '#212946'  # bluish dark grey

        colors = [
            '#BD5E00',
            '#ED7700',
            '#EE8F32',
            '#F7B36D',
            '#F0C091',      
        ]
        explode = (0.1, 0.02, 0.02, 0.02, 0.02)#, 0.01, 0.01, 0.01, 0.01, 0.01)
        figure = plt.gcf()  # get current figure
        figure.set_size_inches(16, 9) 

        x = df2.sort_values('Yorum',ascending=False)

        result = x['Videoad']
        for adlar in result:
            video = adlar
            break;
        result = x['Yorum']
        for adlar in result:
            goruntu = adlar
            break;
        label=[]
        for i in x['Videoad'].head(5):
            label.append(f"{i[:35]}...")

        plt.pie(x['Yorum'].head(5),autopct='%1.1f%%',colors=colors,shadow=True,startangle=90,explode=explode,textprops={'fontsize': 27})
        plt.axis('equal')
        plt.title(f"{dun}\n{x['KanalAd'][0]}\nYouTube kanalının {dun} tarihinde  En Çok Yorum Alan Videoları\n Top 5 Listesi",fontsize=27)
        plt.legend(labels=label,loc=3,fontsize=15)
        plt.savefig('kanalgunluk_top10.jpg',bbox_inches='tight')

        watermark_photo(img, 'g4.jpg',
                        'kanalgunluk_top10.jpg', position=(225,90))
                        
        fotolar.append('g4.jpg')

    def watermark_photo(input_image_path,
                    output_image_path,
                    watermark_image_path,
                    position):
        base_image = Image.open(input_image_path)
        watermark = Image.open(watermark_image_path)
        base_image.paste(watermark, position)
        base_image.save(output_image_path)        
    
    goruntulenmetop()
    plt.close()
    begenmetop()
    plt.close()
    begenmemetop()
    plt.close()
    yorumtop()
    plt.close()

    users_to_tag = []
    x = 0.5
    y = 0.1
    print(tag)
    if len(tag.split(","))!=1:
        user = tag.split(",")
        for i in user:
            print(i)
            s = {'user_id': i, 'x': x, 'y': y}
            users_to_tag.append(s)
            x += 0.1
            y += 0.1
    else:
        s = {'user_id': tag, 'x': x, 'y': y}
        users_to_tag.append(s)    

    print(users_to_tag)

    try:
        bot.upload_album(fotolar,user_tags= users_to_tag,caption=f"{kanalad} Kanalının Gün İçinde En Çok Etkileşim Alan Videoları \nTop 5 \n  \n\nKeşfetten Gelenler Takip Etmeyi Unutmasın Her gün Youtube Türkiye hakkında Analizler Paylaşıyoruz\n\n#youtube #youtubetürkiye #enesbatur #basakkarahan #delimine #reynmen #orkunışıtmak #twitchturkiye #wtcnn #hazretiyasuo #hzyasuo #evonmoss #twitch #kafalar #alibicim #mesutcantomay #babala #oguzhanugur #magazin #youtubemagazin")
    except Exception as e:
        print(e)
    os.remove("g1.jpg.REMOVE_ME")
    os.remove("g2.jpg.REMOVE_ME")
    os.remove("g3.jpg.REMOVE_ME")
    os.remove("g4.jpg.REMOVE_ME")


    
    
    
