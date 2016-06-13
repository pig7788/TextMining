
# coding: utf-8

# ## N-Gram方法

import codecs, uniout ,operator

def cutSentence(filePath, longTerms): #建立方法(檔案路徑，關鍵字)
        cutlist = '<>/:：;；,、＂’，.。！？「」\"\'\\\n\r《》『』“”!@#$%^&*()'.decode('utf-8') #標點符號要去除
        text = codecs.open(filePath, 'r', 'utf-8') #利用codecs處理編碼並且用utf-8讀入
        sentence = '' #建立空字串，放入單一中文字
        textList = [] #建立空List，會將setence的字串一一放入
        
        for lines in text.readlines(): #讀一行
            lines = lines.strip() #去除空白
            
            for keyword in longTerms:
                lines = ''.join(lines.split(keyword)) #去除長詞中的關鍵字，避免重複
                
            for word in lines: #一一讀取每一個字
                if word not in cutlist: #如果該中文字非標點符號，則一一加進setence內
                    sentence += word
                else: #如果是的話，則將setence內的字串加入textList內，並且同時宣告一個空的setence字串
                    textList.append(sentence)
                    sentence = ''
        
        return textList #回傳list

def ngram(textList, maxTermLength, minFreq):
        words = [] #存放字詞
        words_freq_dict = {} #存放'字詞':詞頻
        result = [] #存放最後的結果
        
        for strList in textList: #從上一個方法中取得回傳值，並且一一取出，['字串', '字串', '字串', '字串'...]
            for length in range(0, len(strList) - (maxTermLength - 1)):
                #假設字詞長度10，想每次要取的字詞長度是3，所以取到最後的索引值應該是10-(3-1)=8才對，可是range是n-1，實際上取到的是[7]
                words.append(strList[length:length + maxTermLength]) #將指定的索引值範圍取出的元素，丟入存放長詞的list
        
        for word in words:
            if word not in words_freq_dict: #如果取出的中文字詞(key)不在dictionary內，則計算有該字詞的數量，並且丟入指定的key
                words_freq_dict[word] = words.count(word)
        
        words_freq_list = sorted(words_freq_dict.iteritems(), key = operator.itemgetter(1), reverse = True)
        #針對存放{'字詞':詞頻}的字典做排序，並轉換成一個list[['字詞',詞頻], ['字詞',詞頻], ['字詞',詞頻]...]
        
        for word in words_freq_list: #針對list中的元素，一一取出[['字詞',詞頻], ['字詞',詞頻], ['字詞',詞頻]...]
            if word[1] >= minFreq: #如果取出來的所對應到索引值[1]的元素≧minFreq，一一將word這個list加進result內
                result.append(word)
        
        return result #回傳result這個list

def longTermPriority(filePath, maxTermLength, minFreq): #(檔案路徑，字詞長度，最少詞頻)
        longTerms = [] #存放長字詞
        longTermsFreq = [] #存放長字詞與詞頻
        
        for termsNum in range(maxTermLength, 1, -1): #從最大的字詞長度開始，直到1為止，每執行一次-1
            text_list = cutSentence(filePath, longTerms) #呼叫方法
            words_freq = ngram(text_list, termsNum, minFreq) #呼叫方法
        
            for word_freq in words_freq: #從回傳result的list中，一一取出元素
                longTerms.append(word_freq[0]) #索引值[0]所對應的元素，則為下一次長字詞中，刪去重複的關鍵字詞
                longTermsFreq.append(word_freq) #將['字詞',詞頻]，一一加入
        
        return longTermsFreq #回傳list

def resultPrintOut(TermFreqResult):
    print '字詞', '\t詞頻'
    print '============'
    for result in TermFreqResult: #印出結果
        print result[0], '\t' + str(result[1])