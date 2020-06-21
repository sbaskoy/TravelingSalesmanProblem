# -*- coding: utf-8 -*-
"""
Created on Sat Oct 12 19:04:12 2019

@author: Salim
"""

import pandas 
import numpy as np
import random
import Con_3
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from datetime import datetime

import xlrd
""" GRAFİK GÖRÜNÜMÜ """
#style.use("seaborn-whitegrid")
#style.use("dark_background")
style.use("ggplot")
""" KULLANICI DEĞERLERİ """
xlsx_dosya_yolu="CON_3.xlsx"
baş_cözüm_sayısı=100
çarp_oranı=0.90
mut_oranı=0.90
matrix_boyutu=[51,51]
durdurma_kriteri=1100

""" -----------------"""


#con_3=Con_3.Array().liste()
carp=Con_3.Array()


workbook = xlrd.open_workbook(xlsx_dosya_yolu)
sheet = workbook.sheet_by_index(0)
con=list()
for rowx in range(1,sheet.nrows):
    values = sheet.row_values(rowx)
    for i in values:
        con.append(i)

con_3=np.reshape(con,matrix_boyutu)

#con_3=np.reshape(con_3,[51,51])

#df=pandas.read_excel('CON_3.xlsx')  


yeni_genler=pandas.DataFrame(columns=list(range(con_3.shape[0]+1)))

def cözüm_oluştur(liste,baş_cözüm_sayısı):
    baş_cözümleri=pandas.DataFrame(columns=list(range(con_3.shape[0]+1)))
    for j in range(baş_cözüm_sayısı):
        ilk_şehir=1
        liste=[ilk_şehir]
        for i in range(con_3.shape[0]-1):
            rand=random.randint(1,con_3.shape[0]-1)
            while( rand in liste):
                rand=random.randint(0,con_3.shape[0]-1)
            liste.append(rand)
        liste.append(ilk_şehir)
        baş_cözümleri.loc[j]=liste
    return baş_cözümleri



def uygunluk_hesapla(liste=None,tek_liste=None,gen_sayısı=None):
    toplam_list=list()
    if liste is not None and gen_sayısı is not None:
        for i in range(gen_sayısı):
            cözüm=liste.loc[i]
            toplam=0
            toplam=float(toplam)
            for i in range(len(cözüm)-1):
                toplam+=con_3[cözüm.iloc[i]][cözüm.iloc[i+1]]
            toplam_list.append(toplam)
        return toplam_list
    elif tek_liste is not None:
        toplam=0
        toplam=float(toplam)
        #tek_liste.pop()
        for i in range(len(tek_liste)-1):
            toplam+=con_3[tek_liste[i]][tek_liste[i+1]]
        return toplam

def çarplazlama(liste,gen_sayısı,çarp_oranı):
    randomlar={"s1":[],"s2":[]}
    for i in range(0,int((len(liste.index))*(çarp_oranı))):
            s1=random.randint(0,gen_sayısı)
            s2=random.randint(0,gen_sayısı)
            while(s1 is  s2):
                s1=random.randint(0,gen_sayısı)
                s2=random.randint(0,gen_sayısı)
            randomlar["s1"].append(s1)
            randomlar["s2"].append(s2)
            p1=list(liste.loc[s1].values)
            p2=list(liste.loc[s2].values)
        
            yeni_gen=carp.carplazlama(p1,p2)
            p1_uy=uygunluk_hesapla(tek_liste=p1)
            p2_uy=uygunluk_hesapla(tek_liste=p2)
            yeni_gen_uy=uygunluk_hesapla(tek_liste=yeni_gen)
            yeni_genler.loc[i]=yeni_gen
            if yeni_gen_uy<p1_uy:
                liste.loc[s1]=yeni_gen
            elif yeni_gen_uy<p2_uy:
                liste.loc[s2]=yeni_gen
            else:
                continue
            
    return liste

def Mutasyon(liste,gen_sayısı,M_oranı):
    for i in range(0,int((gen_sayısı)*(M_oranı))):
        p1=list(liste.loc[i].values)
        eski_gen_uygunluk=uygunluk_hesapla(tek_liste=p1)
        yeni_gen=carp.mutasyon(p1)
        yeni_gen_uygunluk=uygunluk_hesapla(tek_liste=yeni_gen)
        if yeni_gen_uygunluk < eski_gen_uygunluk:
            liste.loc[i]=yeni_gen
        else:
            continue
    return liste
""" GRAFİK İLE GÖSTERMEDEN PRİNT EDER """ 
def main():
    çözümler=cözüm_oluştur(con_3,baş_cözüm_sayısı)
    #uygunluk=pandas.DataFrame()
    #çözümler=çarplazlama(çözümler,len(çözümler.index)-1,çarp_oranı)
    
    iterasyon=0
    while True:
        iterasyon+=1
        çözümler=çarplazlama(çözümler,len(çözümler.index)-1,çarp_oranı)
        çözümler=Mutasyon(çözümler,len(çözümler.index),mut_oranı)
        uzunluklar=uygunluk_hesapla(liste=çözümler,gen_sayısı=len(çözümler.index))
        result=sorted(uzunluklar)
        print(f"{iterasyon}. iteresyon sonucunda en iyi çözüm {result[0]}")
        if result[0]<durdurma_kriteri:
            ind=uzunluklar.index(result[0])
            en_iyi_yol=çözümler.loc[ind]
            print(result[0])
            print("---------")
            print(en_iyi_yol.values)
            break

#main()
#grafiğe çizdirmeden çalıştıma için alt kısmı yorum satırı yapınız ve main() fonksiyonunu çalıştırın
""" GRAFİK KODLARI """

fig, (ax) = plt.subplots(1,1)
ax = plt.axes(autoscale_on=True,xlim=(0,10), ylim=(0,1750))
line, = ax.plot([], [], lw=2,color='red')
t1 = ax.text(0, 0, '')


def init():
    line.set_data([], [])
    plt.title("Genetik Algoritma CON_3.0")
    plt.xlabel("İterasyon")
    plt.ylabel("Sonuç")
    #t1.set_text("")
    return line


iterasyon=0
çözümler=cözüm_oluştur(con_3,baş_cözüm_sayısı)
dakika=datetime.now().minute
xs=[]
ys=[]
def animate(i):
    global iterasyon,çözümler,dakika
    süre=datetime.now().minute
    geçen_dakika=abs(dakika-süre)
    iterasyon+=1
    çözümler=çarplazlama(çözümler,len(çözümler.index)-1,çarp_oranı)
    çözümler=Mutasyon(çözümler,len(çözümler.index),mut_oranı)
    uzunluklar=uygunluk_hesapla(liste=çözümler,gen_sayısı=len(çözümler.index))
    result=sorted(uzunluklar)
    #print(f"{iterasyon}. iteresyon sonucunda en iyi çözüm {result[0]}")
    if result[0]<durdurma_kriteri:
        ind=uzunluklar.index(result[0])
        en_iyi_yol=çözümler.loc[ind]
        print("BULUNAN EN İYİ ÇÖZÜM")
        print(f"sonuç:{result[0]}")
        print("---------")
        print(en_iyi_yol.values)
        anim.event_source.stop()
    if iterasyon>10:
        ax.set_xlim(0,iterasyon)
    xs.append(iterasyon)
    ys.append(result[0])

    ax.set_ylabel("En İyi Sonuç: "+str("%.3f" % result[0]))
    ax.set_xlabel('İterasyon: ' + str(iterasyon)+" Geçen süre: "+str( geçen_dakika)+":"+str(datetime.now().second))
    ax.collections.clear()
    ax.fill_between(xs,ys,0, facecolor='yellow', alpha=0.4)
    #ax.text(xs[-1],1750,"Salim Başköy",fontsize=10)
    #t1.set_position(xs[-1],1750)
    #t1.set_text("Salim Başköy")
    line.set_data(xs,ys)
    return line,

anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=200, interval=100, blit=False)
plt.show()

    

        




            
            
            
            
