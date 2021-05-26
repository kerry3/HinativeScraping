import urllib.request
from bs4 import BeautifulSoup
import re
import openpyxl #엑셀 라이브러리

excel_file=openpyxl.Workbook()
excel_sheet=excel_file.active

excel_sheet.column_dimensions['A'].width=70
excel_sheet.column_dimensions['B'].width=160
excel_sheet.append(['Question','answer'])


url='https://hinative.com/en-US/profiles/4045677/questions' #first page
pageNum=1

html=urllib.request.urlopen(url).read()
soup=BeautifulSoup(html,'html.parser')

#https://hinative.com/en-US/profiles/4045677/questions?page=2 2번째 페이지 부터는 ?page=2가 붙는다.

helpurl='https://hinative.com' #i.attrs['href']로는 이게 안나와서 이거 추가를 해줌.
while pageNum<115: 
    if pageNum==1:
        quest=soup.find_all(class_='d_block') #class 태그가 d_block이인 애들에 질문들로 들어가는 링크가 있어서 얘네들만 싹찾음.
        for i in quest: #질문창 하나하나
            questurl=helpurl+i.attrs['href'] # helpurl 결합 https://hinative.com/en-US/questions/숫자
            html=urllib.request.urlopen(questurl).read() #각 질문 창 html 파일 받기
            soup=BeautifulSoup(html,'html.parser')
            questlist=soup.find_all("span",{"class":"keyword"})#<span class="keyword">이사이에있는텍스트 출력해야함</span>
            answlist=soup.find_all("div",{"id":re.compile('hide-editing.*')})
            
            o=0

            for question in questlist:
                if(len(answlist))==0:
                    excel_sheet.append([question.get_text(), "답변 없음"])
                for answer in answlist:

                    if o==0:
                        excel_sheet.append([question.get_text(), answer.get_text()])
                    else:
                        excel_sheet.append([None, answer.get_text()])
                    o+=1
                excel_sheet.append([None, None])
    
        pageUrl=url+'?page='
    else:
        numUrl=pageUrl+str(pageNum)#pageUrl에 숫자붙이기
        html=urllib.request.urlopen(numUrl).read()
        soup=BeautifulSoup(html,'html.parser')

        quest=soup.find_all(class_='d_block') #class 태그가 d_block이인 애들에 질문들로 들어가는 링크가 있어서 얘네들만 싹찾음.
        for i in quest: #질문창 하나하나
            questurl=helpurl+i.attrs['href'] # helpurl 결합 https://hinative.com/en-US/questions/숫자
            html=urllib.request.urlopen(questurl).read() #각 질문창 html 파일 받기
            soup=BeautifulSoup(html,'html.parser')
            questlist=soup.find_all("span",{"class":"keyword"}) #<span class="keyword">이사이에있는텍스트 출력해야함</span>
            answlist=soup.find_all("div",{"id":re.compile('hide-editing.*')})

            o=0

            for question in questlist:
                if(len(answlist))==0:
                    excel_sheet.append([question.get_text(),"답변 없음"])
                for answer in answlist:
                    if o==0:
                        excel_sheet.append([question.get_text(), answer.get_text()])
                    else:
                        excel_sheet.append([None, answer.get_text()])
                    o+=1                     
                excel_sheet.append([None, None])

    pageNum+=1

excel_file.save('hinative.xlsx')
excel_file.close()



