import json
import re
import argparse


def helper_nlh(num):
    dict_num_to_word = {0:"", 1:"one ", 2:"two ", 3:"three ", 4:"four ", 5:"five ", 6:"six ", 7:"seven ", 8:"eight ", 9:"nine ", 10:"ten ", 
                      11:"eleven ", 12:"twelve ", 13:"thirteen ", 14:"fourteen ", 15:"fifteen ", 16:"sixteen ", 17:"seventeen ", 18:"eighteen ", 
                      19:"nineteen ", 20: "twenty ", 30:"thirty ",40:"forty ", 50:"fifty ", 60:"sixty ", 70:"seventy ", 80:"eighty ", 90:"ninety "}
    if num == 0 or num >=1000:
        return ""

    word = ""
    hundred = num//100
    if hundred != 0:
        word+= dict_num_to_word[hundred] + "hundred "
    tens = num % 100
    if tens <= 19:
        word+= dict_num_to_word[tens]
    else:
        ten = (tens//10)*10
        ones = tens % 10
        word+= dict_num_to_word[ten] + dict_num_to_word[ones]
    return word


def num_to_ordinal(num):
    dict_num_to_word = {0:"", 1:"one ", 2:"two ", 3:"three ", 4:"four ", 5:"five ", 6:"six ", 7:"seven ", 8:"eight ", 9:"nine ", 10:"ten ", 
                      11:"eleven ", 12:"twelve ", 13:"thirteen ", 14:"fourteen ", 15:"fifteen ", 16:"sixteen ", 17:"seventeen ", 18:"eighteen ", 
                      19:"nineteen ", 20: "twenty ", 30:"thirty ",40:"forty ", 50:"fifty ", 60:"sixty ", 70:"seventy ", 80:"eighty ", 90:"ninety "}

    dict_ordinal = {0: "",1:"first", 2: "second", 3:"third", 4: "fourth", 5:"fifth", 6:"sixth", 7:"seventh", 8:"eighth", 9:"ninth", 10: "tenth",
                  11: "eleventh", 12 :"twelfth", 13:"thirteenth", 14: "fourteenth", 15: "fifteenth", 16:"	sixteenth",17:"seventeenth", 18:"eighteenth",
                 19: "nineteenth", 20:"twentieth", 30:"thirtieth",40:"fortieth",50:"fiftieth",60:"sixtieth",70:"seventieth",80:"eightieth",90:"ninetieth"}

    if num == 0 or num >=1000:
        return ""

    word = ""
    hundred = num//100
    if hundred != 0:
        word+= dict_num_to_word[hundred] + "hundred "
        if num%100 == 0:
            word = word[:-1]+"th"
    tens = num % 100
    if tens <= 19:
        word+= dict_ordinal[tens]
    else:
        ten = (tens//10)*10
        ones = tens % 10
        if ones != 0:
            word+= dict_num_to_word[ten] + dict_ordinal[ones]
        else:
            word+= dict_ordinal[ten]
    return word

    if num <= 20:
        return dict_ordinal[num]
    else:
        out1 = num_to_word((num//10)*10)
        #print(out1)
        return out1+ dict_ordinal[num%10]

def num_to_word(num, ordinal = False):
    word = ""
    if helper_nlh((num // 1000000000000) % 1000) != "":
        word = helper_nlh((num // 1000000000000) % 1000)+ "trillion " 
    if helper_nlh((num // 1000000000) % 1000) != "":
        word += helper_nlh((num // 1000000000) % 1000)+ "billion " 
    if helper_nlh((num // 1000000) % 1000) != "":
        word += helper_nlh((num // 1000000) % 1000) + "million " 
    if helper_nlh(((num // 1000) % 1000)) != "":
        word += helper_nlh(((num // 1000) % 1000)) + "thousand "
    if ordinal == False:   
        word += helper_nlh(((num % 1000)))
        if num == 0:
            word = "zero "
    if ordinal:
        if num%1000 == 0:
            word = word[:-1]+"th"
        else:
            word+= num_to_ordinal(num%1000)
        if num == 0:
            word = "zeroth"
    return word    


def roman_to_word(token, person_flag):
    dict_unique_roman = { "I" : 1, "V" : 5, "X" : 10, "L": 50}
    number_value = 0
    token_reverse = token[::-1]
    for idx, e in enumerate(token_reverse):
        if idx == 0:
            number_value+= dict_unique_roman[e]
        elif idx != 0:
            if dict_unique_roman[e] >= dict_unique_roman[token_reverse[idx-1]]:
                number_value+= dict_unique_roman[e]
            else:
                number_value-= dict_unique_roman[e]
    if person_flag:
        word = "the "+ num_to_word(number_value, True)
    else:
        word = num_to_word(number_value)
    return word.strip()



def num_to_word_percent(token):
    token_out = ""
    pattern1 = r'^(\d+)(\.?)(\d*)$'
    m = re.match(pattern1, token)
    before_decimal = m.group(1)
    after_decimal = ""
    if m.group(3)!= None:
        after_decimal = m.group(3)
    out = num_to_word(int(before_decimal))
    token_out += out.strip()
    if m.group(2)== ".":
        token_out+=" point"
        if after_decimal =="0":
            token_out+= " zero"
        else:
            dict_num = {0: " o", 1: " one", 2:" two", 3:" three", 4:" four", 5:" five", 6:" six", 7: " seven", 8:" eight", 9:" nine"}
            for num in after_decimal:
                token_out+= dict_num.get(int(num), "")
    return token_out    

def year_to_word(token, ends_with_s = False):
    token_out = ""
    if int(token)%100 <= 9:
        if int(token)%1000 <= 9:
            century = (int(token)//1000)*1000
            last_digit = int(token)%1000
            token_out = num_to_word(century)
            if last_digit != 0:
                token_out+= num_to_word(last_digit)
            else:
                if ends_with_s:
                    token_out = token_out.strip()
                    token_out+="s"
        else:
            century = (int(token)//100)
            last_digit = int(token)%100
            if last_digit != 0:
                token_out = num_to_word(century)+"o "+ num_to_word(last_digit)
            else:
                token_out = num_to_word(century)+ "hundred"
                if ends_with_s:
                    token_out+="s"
        token_out = token_out.strip()
    else:
        token_out = num_to_word(int(token[0:2]))+ num_to_word(int(token[2:4]))
        token_out = token_out.strip()
        if int(token)%10 == 0 and ends_with_s:
            token_out = token_out[:-1]+"ies"
    return token_out   



class spoken_text_convertor_system:
    def is_Punctuation(self, token):
        input_token = token
        Flag = False
        pattern = r'^[—\\()\.,:;"/\'-]*$'

        if re.match(pattern, token):
            Flag = True
            return "sil", Flag
        else:
            return "", Flag


    def is_year(self, token):
        Flag = False
        pattern = r'^(\d\d\d\d)(s)?$'
        token_out = ""
        if re.match(pattern, token):
            Flag = True
            m = re.match(pattern, token)
            token1 = m.group(1)
            if m.group(2) != None:
                #print(token)
                token_out = year_to_word(token1, True)
            else: 
                #print(token)
                token_out = year_to_word(token1)
        return token_out, Flag

    def is_Number(self, token):
        Flag = False
        pattern = r'^([-]?)([\d,]+)(\.?)(\d*)(\s?)$'
        pattern2 = r'^([\d,]+)(\.\d+)?(\s[A-Z]?[a-z]{4,})$'
        token_out = ""
        if re.match(pattern, token):
            if token[0] == "0" and token[1] != '.' and len(token) > 3:
                token_out, Flag = self.is_code(token)
                return token_out, Flag
            Flag = True
            token = re.sub(r',','', token)
            pattern = r'^([-]?)([\d]+)(\.?)(\d*)(\s?)$'
            m = re.match(pattern, token)
            #before_decimal = m.group(2)
            #after_decimal = m.group(4)
            #print(m.group(1))
            #print(m.group(2))
            #print(m.group(3))
            if m.group(1) == "-":
                token_out+= "minus "
            #out = num_to_word(int(before_decimal))
            #token_out += out.strip()
            #if m.group(3)== ".":
            #    token_out+=" point"
            #    dict_num = {0: " zero", 1: " one", 2:" two", 3:" three", 4:" four", 5:" five", 6:" six", 7: " seven", 8:" eight", 9:" nine"}
            #    for num in after_decimal:
            #        token_out+= dict_num[int(num)]
            value = m.group(2)+m.group(3)+m.group(4)
            token_out+= num_to_word_percent(value)
        elif re.match(pattern2, token):
            Flag = True
            token = re.sub(r',','', token)
            pattern = r'^([\d]+)(\.\d+)?(\s?[A-Z]?[a-z]{4,})$'
            m = re.match(pattern, token)
            value = m.group(1)
            if m.group(2) != None:
                value += m.group(2)   
            symb2 = m.group(3).strip()         

            number = num_to_word_percent(value)
  
            token_out = number +" "+ symb2.lower()
        return token_out, Flag

    def is_percent(self, token):
        Flag = False
        pattern0 = r'^(\d+)(.?)(\d*)(\s?percent)$'
        pattern1 = r'^(\d+)(.?)(\d*)(\s?%|\s?pc)$'
        token_out = ""
        if re.match(pattern1, token) or re.match(pattern0, token):
            Flag = True
            #print(Flag)
            if re.match(pattern1, token):
                m = re.match(pattern1, token)
            else:
                m = re.match(pattern0, token)
            value = ""
            if m.group(1)!= None:
                value+= m.group(1)
            if m.group(2)!= None:
                value+= m.group(2)
            if m.group(3)!= None:
                value+= m.group(3)
            token_out += num_to_word_percent(value)
            token_out+=" percent"
        return token_out, Flag

    def is_time(self, token):
        Flag = False
        pattern = r'^(\d?\d)(\s?:\s?\d\d)(\s?AM|\s?am|\s?a\.m\.|\s?PM|\s?pm|\s?p\.m\.)?(\s?[A-Z]{2,})?$'
        pattern2 = r'^(\d?\d)(\s?AM|\s?am|\s?a\.m\.|\s?PM|\s?pm|\s?p\.m\.)(\s?[A-Z]{2,})?$'
        pattern1 = r'^(\d?\d)(:\d\d)(:\d\d)$'
        token_out = ""
        if re.match(pattern, token):
            Flag = True    
            m = re.match(pattern, token)
            hour = m.group(1)
            minutes = ""
            if m.group(2) != None:
                minutes = m.group(2)
                minutes = minutes[-2:]
            token_out+=num_to_word(int(hour))
            if minutes == "00" and m.group(3)== None and minutes !="":
                if int(hour) <= 12 and int(hour) != 0:
                    token_out+="o'clock"
                else:
                    token_out +="hundred"
            elif minutes != "" and minutes != "0" and minutes != "00":
                token_out+=num_to_word(int(minutes))

            if m.group(3) != None:
                a_p = m.group(3)
                if re.match(r'\s?AM|\s?am|\s?a\.m\.', a_p):
                    token_out+="a m"
                elif re.match(r'\s?PM|\s?pm|\s?p\.m\.', a_p):
                    token_out+="p m"
            if m.group(4) != None:
                token_out+= " "
                time_zone = m.group(4).strip()
                for e in time_zone:
                    token_out += e.lower() + " "
        elif re.match(pattern1, token):
            Flag = True    
            m = re.match(pattern1, token)
            hour = m.group(1)
            minute = m.group(2)[1:]
            second = m.group(3)[1:]
            if int(hour) > 1:
                token_out+=num_to_word(int(hour))+ "hours "
            else:
                token_out+=num_to_word(int(hour))+ "hour "
            if int(minute) > 1:
                token_out+=num_to_word(int(minute))+ "minutes and "
            else:
                token_out+=num_to_word(int(minute))+ "minute and "
            if int(second) > 1:
                token_out+=num_to_word(int(second))+ "seconds"
            else:
                token_out+=num_to_word(int(second))+ "second"


        elif re.match(pattern2, token):
            Flag = True    
            m = re.match(pattern2, token)
            hour = m.group(1)
            token_out+=num_to_word(int(hour))

            if m.group(2) != None:
                a_p = m.group(2)
                if re.match(r'\s?AM|\s?am|\s?a\.m\.', a_p):
                    token_out+="a m"
                elif re.match(r'\s?PM|\s?pm|\s?p\.m\.', a_p):
                    token_out+="p m"
            if m.group(3) != None:
                token_out+= " "
                time_zone = m.group(3).strip()
                for e in time_zone:
                    token_out += e.lower() + " "


        token_out = token_out.strip()
        return token_out, Flag

    def is_code(self, token):
        Flag = False
        pattern = r'^(\d+[-\s])*(\s?\(\d+\)\s?)*(\d+[-\s])*(\s?\(\d+\)\s?)*(\d+)$'
        token_out = ""
        if re.match(pattern, token):
            Flag = True 
            #token = re.sub("[\(\)]", "", token) 
            dict_code = {" ": "sil ",'-': "sil ", '0': "o ", '1': "one ", '2':"two ", '3':"three ", '4':"four ", '5':"five ", '6':"six ", '7': "seven ", '8':"eight ", '9':"nine "}
            for e in token:
                token_out+= dict_code.get(e,"")
            token_out = token_out.strip()
        return token_out, Flag

    def is_abbre(self, token):
        Flag = False
        pattern = r'^([A-Z]\.?\s?){2,}[a-z]*$'
        pattern2 = r'[A-Z]\.'
        pattern3 = r'([A-Za-z]+)(\-)'
        token_out = ""
        lower = token.lower()
        list_common_word = ["tv", "mes", "usb", "pc", "ups", "usa", "uk", "nlp", "ac", "dc", "iot", "ai", "bps", "cc"]
        if re.match(pattern, token):
            Flag = True
            token = re.sub(r'\.', "", token)
            Flag_s = False
            if token[-1] == "s" and token[-2] != "s":
                Flag_s = True
                token = token[:-1]

            token = token.lower()
            for e in token:
                if e == " ":
                    continue
                token_out+= e
                token_out+= " "
            token_out = token_out.strip()
            if Flag_s:
                token_out += "'s"
        elif re.match(pattern2, token):
            Flag = True
            token = re.sub(r'\.', "", token)
            token_out = token.lower()
            token_out = token_out.strip()
        
        elif re.match(pattern3, token):
            Flag = True
            token = re.sub(r'\.', "", token)
            token = token[:-1]
            token = token.lower()
            for e in token:
                if e == " ":
                    continue
                token_out+= e
                token_out+= " "
            token_out = token_out.strip()

        elif lower in list_common_word:
            Flag = True
            for e in lower:
                if e == " ":
                    continue
                token_out+= e
                token_out+= " "
            token_out = token_out.strip()

        return token_out, Flag
  
    def is_date(self, token):
        Flag = False
        pattern = r'^(\d?\d)?(st|nd|rd|th)?(\s?[A-Z][a-z]*\s)(\d\d\d\d)$'
        pattern1 = r'^([A-Z][a-z]*\s)(\d?\d)(st|nd|rd|th)?(,\s)?(\d\d\d\d)?$'
        pattern2 = r'^(\d\d\d\d)([-\/])(\d\d)([-\/])(\d\d)$'
        pattern3 = r'^(\d\d)([-\/])(\d\d)([-\/])(\d\d\d\d)$'
        pattern4 = r'^(\d?\d)(\s?[A-Z][a-z]*)$'

        token_out = ""
        dict_month = {1:"january", 2:"february", 3:"march", 4:"april", 5:"may", 6:"june", 7:"july",8:"august", 9:"september", 10:"october",
                      11:"november", 12:"december"}
        if re.match(pattern, token):
            Flag = True
            m = re.match(pattern, token)
            day = "0"
            if m.group(1)!=None:
                day = m.group(1)
            month = m.group(3).lower()
            year = m.group(4)
      
            day_w = num_to_word(int(day), True)
            year_w, F = self.is_year(year) 
            if day_w != "zeroth":
                token_out = "the "+day_w + " of "+ month.strip()+" "+year_w
            else:
                token_out = month.strip()+" "+year_w
            token_out = token_out.strip()

        elif re.match(pattern1, token):
            Flag = True
            m = re.match(pattern1, token)
            month = m.group(1).lower()
            day = m.group(2)
            #year = m.group(5)
            day_w = num_to_word(int(day), True)
            #year_w, F = self.is_year(year) 
            token_out = month.strip()+ " "+day_w

            if m.group(5) != None:
                year = m.group(5)
                year_w, F = self.is_year(year) 
                token_out += " "+year_w
            token_out = token_out.strip()

        elif re.match(pattern2, token):
            Flag = True
            m = re.match(pattern2, token)
            month = m.group(3)
            day = m.group(5)
            year = m.group(1)
            day_w = num_to_word(int(day), True)
            year_w, F = self.is_year(year) 
            token_out = "the "+day_w + " of "+ dict_month.get(int(month),"")+" "+ year_w
            token_out = token_out.strip()
        
        elif re.match(pattern3, token):
            Flag = True
            m = re.match(pattern3, token)
            month = m.group(1)
            day = m.group(3)
            year = m.group(5)
            year_w, F = self.is_year(year)
            if int(month) >  12:
                temp = month
                month = day
                day = temp
                day_w = num_to_word(int(day), True)
                token_out = "the "+day_w + " of "+ dict_month.get(int(month), "") + " "+year_w
            else:
                day_w = num_to_word(int(day), True)
                token_out = dict_month.get(int(month), "")+ " "+day_w + " "+year_w
            token_out = token_out.strip()

        elif re.match(pattern4, token):
            Flag = True
            m = re.match(pattern4, token)
            day = m.group(1)
            month = m.group(2).lower()
            day_w = num_to_word(int(day), True)
            token_out = "the "+day_w + " of "+ month.strip()
            token_out = token_out.strip()
        return token_out, Flag

    def is_frac(self, token):
        Flag = False
        pattern = r'^([-]?)(\d\s)?(\d*)(/)(\d*)$'
        token_out = ""
        if re.match(pattern, token):
            Flag = True    
            m = re.match(pattern, token)
            if m.group(1) == "-":
                token_out += "minus "
            nem = m.group(3)
            denom = m.group(5)
            #print(nem)
            #print(denom)
            #token_out = convert(int(nem))+num_to_ordinal(int(denom))+"s"
            mix = m.group(2)
            if mix != None:
                token_out += num_to_word(int(mix)) + "and "
            if int(nem) == 1 and int(denom)==2:
                token_out+= "a half"
            else:
                #token_out += num_to_word(int(nem))+num_to_word(int(denom), True)+"s"
                token_out += num_to_word(int(nem))
                if int(denom) == 4:
                    token_out += "quarters"
                else:
                    token_out += num_to_word(int(denom), True)+"s"
        return token_out, Flag
  
    def is_per(self, token):
        Flag = False
        #pattern = r'^([\d]+)(\.?)(\d*)(/)(km.)$'
        pattern = r'^([\d,]+)(\.?)(\d*)(\s?)(/)(da|\u00b5|[yzafpnmcdhkKMGTPEZY])?(m|M|mi|in|ft|yd|ha|g|G|lb|q|oz|A|N|l|L|min|h|K|\u00b0C|\u00b0F|s|J|V|b|B)(2|3|\u00b2|\u00b3)?$'
        dict_metric = {"m":"meter","M":"meter", "mi": "mile", "in":"inch", "ft":"foot", 
                    "yd": "yard","ha":"hectare", "g":"gram","G":"gram", "lb":"pound", 
                    "q":"quintal", "oz":"ounce","A":"ampere", "N":"newton",
                     "l":"liter","L":"liter", "s":"second", "min": "minute", 
                     "h":"hour", "K":"kelvin", "\u00b0C":"degree celsius", "\u00b0F":"degree farenheit",
                     "J":"joule", "V":"volt", "b": "bit", "B": "byte"}

        dict_symbol = {"y":"yocto","z":"zepto","a":"atto","f":"femto","p":"pico","n":"nano",
                    "\u00b5":"micro","m":"milli","c":"centi","d":"deci","da":"deca","h":"hecto",
                    "k":"kilo","K":"kilo","M":"mega","G":"giga","T":"tera","P":"peta","E":"exa",
                    "Z":"zetta","Y":"yotta"}
        
        token_out = ""
        if re.match(pattern, token):
            Flag = True  
            token = re.sub(r',', '', token)
            pattern2 = r'^([\d]+)(\.?)(\d*)(\s?)(/)(da|\u00b5|[yzafpnmcdhkKMGTPEZY])?(m|M|mi|in|ft|yd|ha|g|G|lb|q|oz|A|N|l|L|min|h|K|\u00b0C|\u00b0F|s|J|V|b|B)(2|3|\u00b2|\u00b3)?$'
            m = re.match(pattern2, token)
            num = m.group(1)+m.group(2)+m.group(3)
            token_out = num_to_word_percent(num).strip()
            token_out+= " per"
           
            metric2 = " "
            power2 = ""
                
            #print(token_out)
            if m.group(6) != None:
                metric2+= dict_symbol.get(m.group(6), "")
                #print(metric2)
            if m.group(7) != None:
                metric2 += dict_metric.get(m.group(7), "")
                #print(metric2)
            if m.group(8)!= None:
                if m.group(8) == "2" or m.group(8) == '\u00b2':
                    power2 += " square"
                    #print(power2)
                elif m.group(8) == "3" or m.group(8) == '\u00b3':
                    power2 += " cubic"
                    #print(power2)
            token_out +=  power2 + metric2
            if float(num) > 1:
                if metric2[-4:] == "foot":
                    token_out= token_out[:-4] + "feet"
                elif metric2[-4:] == "inch":
                    token_out+="es"
                elif metric2[:7] == " degree":
                    token_out = num_to_word_percent(num).strip() + " per" +power2+ " degrees" + metric2[7:]
                else:
                    token_out+="s"

        return token_out, Flag
  
    def is_currency(self, token):
        Flag = False
        token_out = ""
        pattern1 = r'^(\$|\u00a3|\u20ac|Rs|Rs\.)(\s?)([\d,]+)(\.\d+)?$'
        pattern2 = r'^(\$|\u00a3|\u20ac|Rs|Rs\.)(\s?)([\d,]+)(\.\d+)?(\s?[A-Za-z][a-z]?)$'
        pattern3 = r'^(\$|\u00a3|\u20ac|Rs|Rs\.)(\s?)([\d,]+)(\.\d+)?(\s[A-Za-z]*)$'
        if re.match(pattern1, token):
            Flag = True
            token = re.sub(r',','', token)
            #pattern = r'^(\W|Rs|Rs.)(\s?)([\d]+)(\.?)(\d*)?$'
            pattern = r'^(\$|\u00a3|\u20ac|Rs|Rs.)(\s?)([\d]+)(\.\d*)?$'
            m = re.match(pattern, token)
            symbol = m.group(1)
            value = m.group(3)
            number, F = self.is_Number(value)
            dict_symbol ={"\u0024" : "dollar", "\u00a3": "pound", "\u20ac":"euro", "Rs": "rupee", "Rs.": "rupee"}
            #dict_symbol ={"$" : "dollar", "£": "pound", "€":"euro"} 
            token_out = number + " "+ dict_symbol.get(symbol,"")
            if int(value) >= 1:
                token_out+="s"

            if m.group(4) != None:
                dec = m.group(4)
                decimal_value = int(dec[1:])

                if symbol == "\u0024" or symbol == "\u20ac":
                    if decimal_value <= 1:
                        token_out+= " and " + num_to_word(decimal_value).strip() + " cent"
                    else:
                        token_out+= " and " + num_to_word(decimal_value).strip() + " cents"
                    #token+= " and " + num_to_word(int(m.group(5))).strip() + " cents"
                elif symbol == "Rs" or symbol == "Rs.":
                    if decimal_value <= 1:
                        token_out+= " and " + num_to_word(decimal_value).strip() + " paisa"
                    else:
                        token_out+= " and " + num_to_word(decimal_value).strip() + " paise"
                    #token+= " and " + num_to_word(int(m.group(5))).strip() + " paisa"
                elif symbol == "\u00a3" :
                    if decimal_value <= 1:
                        token_out+= " and " + num_to_word(decimal_value).strip() + " penny"
                    else:
                        token_out+= " and " + num_to_word(decimal_value).strip() + " pence"

        elif re.match(pattern2, token):
            Flag = True
            token = re.sub(r',','', token)
            pattern = r'^(\$|\u00a3|\u20ac|Rs|Rs\.)(\s?)([\d]+)(\.\d+)?(\s?[A-Za-z][a-z]?)$'
            m = re.match(pattern, token)
            symbol = m.group(1)
            value = m.group(3)
            if m.group(4) != None:
                value += m.group(4)
            symb2 = m.group(5)
            symb2 = symb2.strip()
            symb2 = symb2.lower()
            #print(symb2)
            number, F = self.is_Number(value)
            dict_symbol ={"\u0024" : "dollars", "\u00a3": "pounds", "\u20ac":"euros", "Rs": "rupees", "Rs.": "rupees"}
            #dict_symbol ={"$" : "dollars", "£": "pounds", "€":"euros"}
            dict_symb2 ={"m" : "million", "b": "billion", "M":"million", "cr": "crore"} 
            token_out = number + " "+ dict_symb2.get(symb2,"")+" "+ dict_symbol.get(symbol,"")

        elif re.match(pattern3, token):
            Flag = True
            token = re.sub(r',','', token)
            pattern = r'^(\$|\u00a3|\u20ac|Rs|Rs\.)(\s?)([\d]+)(\.\d+)?(\s[A-Za-z]*)$'
            m = re.match(pattern, token)
            symbol = m.group(1)
            value = m.group(3)
            if m.group(4) != None:
                value += m.group(4)   
            symb2 = m.group(5)         
            #print(symb2)
            number, F = self.is_Number(value)
            dict_symbol ={"\u0024" : "dollars", "\u00a3": "pounds", "\u20ac":"euros", "Rs": "rupees", "Rs.": "rupees"}
            #dict_symbol ={"$" : "dollars", "£": "pounds", "€":"euros"}
            dict_symb2 ={"m" : "million", "b": "billion", "M":"million", "cr": "crore"} 
            token_out = number + symb2.lower()+" "+ dict_symbol.get(symbol,"")

        return token_out, Flag
  
    def is_ordinal(self, token):
        Flag = False
        pattern = r'^([\d]+)(th|st|nd|rd)$'
        token_out = ""
        if re.match(pattern, token):
            Flag = True    
            num = token[:-2]
            #print(num)
            token_out = num_to_word(int(num), True)
        return token_out, Flag 


    def is_metric1(self, token):
        Flag = False
        pattern = r'([\d,]+)(\.?)(\d*)(\s?)(da|\u00b5|[yzafpnμmcdhkKMGTPEZY])?(m|M|mi|in|ft|yd|ha|g|G|lb|q|oz|A|N|l|L|min|h|K|\u00b0C|\u00b0F|s|J|V|b|B)(2|3|\u00b2|\u00b3)?$'
        pattern2 = r'^([\d,]+)(\.?)(\d*)(\s?)(da|\u00b5|[yzafpnmcdhkKMGTPEZY])?(m|M|mi|in|ft|yd|ha|g|G|lb|q|oz|A|N|l|L|min|h|K|\u00b0C|\u00b0F|s|J|V|b|B)(2|3|\u00b2|\u00b3)?(/)(da|\u00b5|[yzafpnmcdhkKMGTPEZY])?(m|M|mi|in|ft|yd|ha|g|G|lb|q|oz|A|N|l|L|min|h|K|\u00b0C|\u00b0F|s|J|V|b|B)(2|3|\u00b2|\u00b3)?$'
        pattern4 = r'([\d,]+)(\.?)(\d*)(\ssq\s)(da|\u00b5|[yzafpnmcdhkKMGTPEZY])?(m|M|mi|in|ft|yd|ha|g|G|lb|q|oz|A|N|l|L|min|h|K|\u00b0C|\u00b0F|s|J|V|b|B)$'

        dict_metric = {"m":"meter","M":"meter", "mi": "mile", "in":"inch", "ft":"foot", 
                    "yd": "yard","ha":"hectare", "g":"gram","G":"gram", "lb":"pound", 
                    "q":"quintal", "oz":"ounce","A":"ampere", "N":"newton",
                     "l":"liter","L":"liter", "s":"second", "min": "minute", 
                     "h":"hour", "K":"kelvin", "\u00b0C":"degree celsius", "\u00b0F":"degree farenheit",
                     "J":"joule", "V":"volt", "b": "bit", "B": "byte"}

        dict_symbol = {"y":"yocto","z":"zepto","a":"atto","f":"femto","p":"pico","n":"nano",
                    "\u00b5":"micro","m":"milli","c":"centi","d":"deci","da":"deca","h":"hecto",
                    "k":"kilo","K":"kilo","M":"mega","G":"giga","T":"tera","P":"peta","E":"exa",
                    "Z":"zetta","Y":"yotta"}
        token_out = ""
        if re.match(pattern, token):
            Flag = True  
            token = re.sub(r',','', token)
            pattern1 = r'^([\d]+)(\.?)(\d*)(\s?)(da|\u00b5|[yzafpnmcdhkKMGTPEZY])?(m|M|mi|in|ft|yd|ha|g|G|lb|q|oz|A|N|l|L|min|h|K|\u00b0C|\u00b0F|s|J|V|b|B)(2|3|\u00b2|\u00b3)?$'
            m = re.match(pattern1, token)  
            num = m.group(1)+m.group(2)+m.group(3)
            num_wrd = num_to_word_percent(num).strip()
            metric = " "
            power = ""
            if m.group(5) != None:
                metric+= dict_symbol.get(m.group(5), "")
            if m.group(6) != None:
                metric += dict_metric.get(m.group(6), "")
            if m.group(7)!= None:
                if m.group(7) == "2" or m.group(7) == '\u00b2':
                    power += " square"
                elif m.group(7) == "3" or m.group(7) == '\u00b3':
                    power += " cubic"
            token_out = num_wrd + power + metric
            if float(num) > 1:
                if metric[-4:] == "foot":
                    token_out= token_out[:-4] + "feet"
                elif metric[-4:] == "inch":
                    token_out+="es"
                elif metric[:7] == " degree":
                    token_out = num_wrd +power+ " degrees" + metric[7:]
                else:
                    token_out+="s"
        
        elif re.match(pattern2, token):
            Flag = True  
            token = re.sub(r',','', token)
            pattern3 = r'^([\d]+)(\.?)(\d*)(\s?)(da|\u00b5|[yzafpnmcdhkKMGTPEZY])?(m|M|mi|in|ft|yd|ha|g|G|lb|q|oz|A|N|l|L|min|h|K|\u00b0C|\u00b0F|s|J|V|b|B)(2|3|\u00b2|\u00b3)?(/)(da|\u00b5|[yzafpnμmcdhkKMGTPEZY])?(m|M|mi|in|ft|yd|ha|g|G|lb|q|oz|A|N|l|L|min|h|K|\u00b0C|\u00b0F|s|J|V|b|B)(2|3|\u00b2|\u00b3)?$'
            m = re.match(pattern3, token)  
            num = m.group(1)+m.group(2)+m.group(3)
            num_wrd = num_to_word_percent(num).strip()
            metric = " "
            power = ""
            if m.group(5) != None:
                metric+= dict_symbol.get(m.group(5), "")
            if m.group(6) != None:
                metric += dict_metric.get(m.group(6), "")
            if m.group(7)!= None:
                if m.group(7) == "2" or m.group(7) == '\u00b2':
                    power += " square"
                elif m.group(7) == "3" or m.group(7) == '\u00b3':
                    power += " cubic"
            token_out = num_wrd + power + metric
            if float(num) > 1:
                if metric[-4:] == "foot":
                    token_out= token_out[:-4] + "feet"
                elif metric[-4:] == "inch":
                    token_out+="es"
                elif metric[:7] == " degree":
                    token_out = num_wrd +power+ " degrees" + metric[7:]
                else:
                    token_out+="s"
            #print(token_out)
            metric2 = " "
            power2 = ""
            token_out+= " per"
            #print(token_out)
            if m.group(9) != None:
                metric2+= dict_symbol.get(m.group(9), "")
                #print(metric2)
            if m.group(10) != None:
                metric2 += dict_metric.get(m.group(10), "")
                #print(metric2)
            if m.group(11)!= None:
                if m.group(11) == "2" or m.group(11) == '\u00b2':
                    power2 += " square"
                    #print(power2)
                elif m.group(11) == "3" or m.group(11) == '\u00b3':
                    power2 += " cubic"
                    #print(power2)
            token_out +=  power2 + metric2
            #print(token_out)

        elif re.match(pattern4, token):
            Flag = True  
            token = re.sub(r',','', token)
            pattern5 = r'^([\d]+)(\.?)(\d*)(\ssq\s)(da|\u00b5|[yzafpnmcdhkKMGTPEZY])?(m|M|mi|in|ft|yd|ha|g|G|lb|q|oz|A|N|l|L|min|h|K|\u00b0C|\u00b0F|s|J|V|b|B)$'
            m = re.match(pattern5, token)  
            num = m.group(1)+m.group(2)+m.group(3)
            num_wrd = num_to_word_percent(num).strip()
            metric = " "
            power = ""
            if m.group(5) != None:
                metric+= dict_symbol.get(m.group(5), "")
            if m.group(6) != None:
                metric += dict_metric.get(m.group(6), "")
            if m.group(4)== ' sq ':
                power += " square"
            token_out = num_wrd + power + metric
            if float(num) > 1:
                if metric[-4:] == "foot":
                    token_out= token_out[:-4] + "feet"
                elif metric[-4:] == "inch":
                    token_out+="es"
                elif metric[:7] == " degree":
                    token_out = num_wrd +power+ " degrees" + metric[7:]
                else:
                    token_out+="s"
        return token_out, Flag        


    def is_roman(self, token, preceeding_token):
        Flag = False
        pattern_name = r'^[A-Z][a-z]+$'
        pattern = r'^(XL|L?X{0,3})(IX|IV|V?I{0,3})$'
        token_out = ""
        person_flag = False
        if re.match(pattern, token):
            if re.match(pattern_name, preceeding_token):
                person_flag = True
            Flag = True  
            token_out = roman_to_word(token, person_flag)
        return token_out, Flag             





def solution(input_tokens):
    convertor  = spoken_text_convertor_system()
    output_list = []
    for idx, token in enumerate(input_tokens):
        try:
            token_out, Flag0 = convertor.is_year(token)
        except:
            token_out = "<self>"
            Flag0 = "False"
        if Flag0:
            output_list.append(token_out)
        else:
            try:
                token_out, Flag1 = convertor.is_Punctuation(token)
            except:
                token_out = "<self>"
                Flag1 = "False"

            if Flag1:
                output_list.append(token_out)
            else:
                try:
                    token_out, Flag2 = convertor.is_Number(token)
                except:
                    token_out = "<self>"
                    Flag2 = "False"
                if Flag2:
                    output_list.append(token_out)
                else:
                    try:
                        token_out, Flag3 = convertor.is_percent(token)
                    except:
                        token_out = "<self>"
                        Flag3 = "False"
                    if Flag3:
                        output_list.append(token_out)
                    else:
                        try:
                            token_out, Flag4 = convertor.is_time(token)
                        except:
                            token_out = "<self>"
                            Flag4 = "False"
                        if Flag4:
                            output_list.append(token_out)
                        else:
                            try:
                                token_out, Flag5 = convertor.is_date(token)
                            except:
                                token_out = "<self>"
                                Flag5 = "False"
                            if Flag5:
                                output_list.append(token_out)
                            else:
                                try:
                                    prec = "abc"
                                    if idx!= 0:
                                        prec = input_tokens[idx -1]
                                    token_out, Flag6 = convertor.is_roman(token, prec)
                                except:
                                    token_out = "<self>"
                                    Flag6 = "False"
                                if Flag6:
                                    output_list.append(token_out)
                                else:
                                    try:
                                        token_out, Flag7 = convertor.is_code(token)
                                    except:
                                        token_out = "<self>"
                                        Flag7 = "False"
                                    if Flag7:
                                        output_list.append(token_out)
                                    else:
                                        try:
                                            token_out, Flag8 = convertor.is_frac(token)
                                        except:
                                            token_out = "<self>"
                                            Flag8 = "False"
                                        if Flag8:
                                            output_list.append(token_out)
                                        else:
                                            try:
                                                token_out, Flag9 = convertor.is_per(token)
                                            except:
                                                token_out = "<self>"
                                                Flag9 = "False"
                                            if Flag9:
                                                output_list.append(token_out)
                                            else:
                                                try:
                                                    token_out, Flag10 = convertor.is_currency(token)
                                                except:
                                                    token_out = "<self>"
                                                    Flag10 = "False"
                                                if Flag10:
                                                    output_list.append(token_out)
                                                else:
                                                    try:
                                                        token_out, Flag11 = convertor.is_ordinal(token)
                                                    except:
                                                        token_out = "<self>"
                                                        Flag11 = "False"
                                                    if Flag11:
                                                        output_list.append(token_out)
                                                    else:
                                                        try:
                                                            token_out, Flag12 = convertor.is_metric1(token)
                                                        except:
                                                            token_out = "<self>"
                                                            Flag12 = "False"
                                                        if Flag12:
                                                            output_list.append(token_out)
                                                        else:
                                                            try:
                                                                token_out, Flag13 = convertor.is_abbre(token)
                                                            except:
                                                                token_out = "<self>"
                                                                Flag13 = "False"
                                                            if Flag13:
                                                                output_list.append(token_out)
                                                            else:
                                                                output_list.append('<self>')
    return output_list #todo: write your own solution


def solution_dump(solution_file_path, input_data):
    solution_data = []
    for input_sentence in input_data:
        solution_sid = input_sentence['sid']
        #print(f"solution_sid {solution_sid}")
        solution_tokens = solution(input_sentence['input_tokens'])
        solution_data.append({'sid':solution_sid,
                              'output_tokens':solution_tokens})

    with open(solution_file_path,'w') as solution_file:
        json.dump(solution_data, solution_file, indent=2, ensure_ascii=False)
        solution_file.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='COL 772 Assignment 1')
    parser.add_argument('--input_path', required = True, type=str, help='Path to input file')
    parser.add_argument('--solution_path',required = True,  type=str, help='Path to solution file')
    args = parser.parse_args()
    with open(args.input_path,'r', encoding='utf-8') as input_file:
        input_data = json.load(input_file)
        input_file.close()

    solution_dump(args.solution_path, input_data)
    