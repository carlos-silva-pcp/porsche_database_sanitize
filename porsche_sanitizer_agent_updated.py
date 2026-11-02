#!/usr/bin/env python3
import sys, re, math, calendar
from datetime import datetime, date
import pandas as pd

MONTHS = {m.lower(): i for i, m in enumerate(calendar.month_name) if m}
MONTHS.update({m.lower(): i for i, m in enumerate(calendar.month_abbr) if m})
US_STATES = {
"alabama":"AL","alaska":"AK","arizona":"AZ","arkansas":"AR","california":"CA","colorado":"CO",
"connecticut":"CT","delaware":"DE","florida":"FL","georgia":"GA","hawaii":"HI","idaho":"ID",
"illinois":"IL","indiana":"IN","iowa":"IA","kansas":"KS","kentucky":"KY","louisiana":"LA",
"maine":"ME","maryland":"MD","massachusetts":"MA","michigan":"MI","minnesota":"MN",
"mississippi":"MS","missouri":"MO","montana":"MT","nebraska":"NE","nevada":"NV",
"new hampshire":"NH","new jersey":"NJ","new mexico":"NM","new york":"NY","north carolina":"NC",
"north dakota":"ND","ohio":"OH","oklahoma":"OK","oregon":"OR","pennsylvania":"PA",
"rhode island":"RI","south carolina":"SC","south dakota":"SD","tennessee":"TN","texas":"TX",
"utah":"UT","vermont":"VT","virginia":"VA","washington":"WA","west virginia":"WV",
"wisconsin":"WI","wyoming":"WY","district of columbia":"DC"}
US_STATES.update({v.lower():v for v in list(US_STATES.values())})
PAYMENTS = {"creditcard":"Credit Card","credit card":"Credit Card","credit-card":"Credit Card",
"debitcard":"Debit Card","debit card":"Debit Card","debit-card":"Debit Card",
"banktransfer":"Bank Transfer","bank transfer":"Bank Transfer","bank-transfer":"Bank Transfer",
"wiretransfer":"Wire Transfer","wire transfer":"Wire Transfer","wire-transfer":"Wire Transfer",
"financing":"Financing","financing plan":"Financing","finance":"Financing","lease":"Lease","cash":"Cash",
"ach":"ACH Payment","ach payment":"ACH Payment","ach-payment":"ACH Payment",
"cryptopayment":"Crypto Payment","crypto payment":"Crypto Payment","crypto-payment":"Crypto Payment"}
DELIVERIES = {"delivered":"Delivered","pending":"Pending","in transit":"In Transit","transit":"In Transit",
"cancelled":"Cancelled","canceled":"Cancelled","awaiting delivery":"Awaiting Delivery",
"awaiting pickup":"Awaiting Pickup","pending approval":"Pending Approval","pending review":"Pending Review",
"shipped":"Shipped","awaiting review":"Awaiting Review"}
MODELS = ["911 Carrera","911 Carrera S","911 Carrera GTS","911 Turbo","911 Turbo S","911 GT3","911 GT3 RS",
"911 Dakar","911 Targa 4","911 Targa 4S","718 Cayman","718 Cayman S","718 Cayman GT4 RS","718 Boxster",
"718 Boxster GTS","718 Spider RS","Cayenne","Cayenne S","Cayenne Coupe","Cayenne E-Hybrid","Cayenne Turbo",
"Cayenne Turbo GT","Macan","Macan S","Macan T","Macan GTS","Macan Eletric","Panamera","Panamera 4S",
"Panamera Turbo","Panamera Turbo S","Panamera 4 E-Hybrid","Taycan","Taycan 4S","Taycan GTS",
"Taycan Turbo","Taycan Turbo S","Taycan Cross Turismo"]
MODEL_MAP={re.sub(r"[^a-z0-9]+","",x.lower()):x for x in MODELS}
def txt(v): return "" if pd.isna(v) else re.sub(r"\s+"," ",str(v).strip())
def words_num(s):
    d={"zero":0,"one":1,"two":2,"three":3,"four":4,"five":5,"six":6,"seven":7,"eight":8,"nine":9,
    "ten":10,"eleven":11,"twelve":12,"thirteen":13,"fourteen":14,"fifteen":15,"sixteen":16,
    "seventeen":17,"eighteen":18,"nineteen":19,"twenty":20,"thirty":30,"forty":40,"fifty":50,
    "sixty":60,"seventy":70,"eighty":80,"ninety":90,"hundred":100,"thousand":1000}
    total=cur=0; found=False
    for w in re.findall(r"[a-z]+",s.lower()):
        if w=="and": continue
        if w not in d: return None
        found=True; n=d[w]
        if n==100: cur=max(1,cur)*100
        elif n==1000: total+=max(1,cur)*1000; cur=0
        else: cur+=n
    return total+cur if found else None
def date_clean(v):
    if pd.isna(v) or txt(v)=="": return "INVALID"
    if isinstance(v,(datetime,date,pd.Timestamp)): return v.strftime("%Y-%m-%d")
    s=txt(v)
    for f in ("%Y-%m-%d","%Y/%m/%d","%Y.%m.%d","%m/%d/%Y","%m/%d/%y","%m-%d-%y"):
        try: return datetime.strptime(s,f).strftime("%Y-%m-%d")
        except ValueError: pass
    m=re.fullmatch(r"([A-Za-z]+)\\s+(\\d{1,2})(?:st|nd|rd|th|sh)?[,]?\\s+(\\d{4})",s,re.I)
    if m and m.group(1).lower() in MONTHS:
        try: return date(int(m.group(3)),MONTHS[m.group(1).lower()],int(m.group(2))).strftime("%Y-%m-%d")
        except ValueError: pass
    return "INVALID"
def year_clean(v):
    s=txt(v).lower()
    if re.fullmatch(r"\\d{4}",s): n=int(s)
    elif re.fullmatch(r"20[\\s-]?2[0-9]|19[\\s-]?\\d{2}",s): n=int(re.sub(r"[\\s-]","",s))
    else: n=words_num(s)
    return str(n) if n is not None and 1990<=n<=2035 else "INVALID"
def price_clean(v):
    s=txt(v).lower().replace("usd","").replace("dollars","").replace("dollar","").strip()
    if not s: return "INVALID"
    mult=1000 if re.search(r"k\b|\bthousand\b",s) else 1
    s=re.sub(r"k\b|\bthousand\b","",s).strip()
    n=words_num(s)
    if n is None:
        raw=re.sub(r"[^0-9.,-]","",s)
        if not raw: return "INVALID"
        if "," in raw and "." in raw:
            if raw.rfind(",") > raw.rfind(".") and len(raw.rsplit(",",1)[1]) == 2: raw=raw.replace(".","").replace(",",".")
            else: raw=raw.replace(",","")
        elif "," in raw: raw=raw.replace(",","") if len(raw.rsplit(",",1)[1])==3 else raw.replace(",",".")
        elif "." in raw and len(raw.rsplit(".",1)[1])==3: raw=raw.replace(".","")
        try: n=float(raw)
        except ValueError: return "INVALID"
    n=float(n)*mult
    return round(n,2) if math.isfinite(n) and n>=0 else "INVALID"
def mileage_clean(v):
    s=txt(v).lower()
    if s in {"new","new car","zero miles","0 mi","0 mile","0 miles"}: return 0
    if not s: return "INVALID"
    km=bool(re.search(r"\\bkm\\b",s)); n=words_num(s)
    if n is None:
        raw=re.sub(r"[^0-9.,-]","",s).replace(",","").replace(".","")
        if not raw: return "INVALID"
        try: n=float(raw)
        except ValueError: return "INVALID"
    if n<0: return "INVALID"
    return int(round(n*0.621371)) if km else int(round(n))
def model_clean(v):
    s=txt(v)
    if not s: return "INVALID"
    k=re.sub(r"[^a-z0-9]+","",s.lower())
    if k=="macanelectric": return "Macan Eletric"
    return MODEL_MAP.get(k," ".join(w.capitalize() for w in s.split()))
def payment_clean(v):
    s=txt(v).lower().replace("_"," ")
    k=re.sub(r"\s+"," ",s).strip()
    return PAYMENTS.get(k,PAYMENTS.get(re.sub(r"[^a-z0-9]","",k)," ".join(w.capitalize() for w in k.split()) if k else "INVALID"))
def city_clean(v):
    s=txt(v)
    return " ".join(w[:1].upper()+w[1:].lower() for w in s.split()) if s else "INVALID"
def state_clean(v): return US_STATES.get(txt(v).lower(),"INVALID")
def delivery_clean(v):
    s=re.sub(r"[!?.,;:]","",txt(v).lower())
    s=re.sub(r"[_-]+"," ",s); s=re.sub(r"\s+"," ",s).strip()
    return DELIVERIES.get(s," ".join(w.capitalize() for w in s.split()) if s else "INVALID")
NAME_PARTICLES = {"da", "de", "do", "das", "dos", "van"}
NAME_PLACEHOLDERS = {"n/a", "null", "none", "unknown"}

def name_clean(value):
    """Normalize names without guessing identity or correcting spelling."""
    if pd.isna(value):
        return "INVALID"
    name = re.sub(r"\s+", " ", str(value).strip())
    if not name or name.casefold() in NAME_PLACEHOLDERS:
        return "INVALID"
    def normalize_piece(piece):
        return piece[:1].upper() + piece[1:].lower() if piece else piece
    words = []
    for index, word in enumerate(name.split(" ")):
        if index > 0 and word.casefold() in NAME_PARTICLES:
            words.append(word.lower())
        else:
            # Capitalize individual segments after apostrophes and hyphens.
            words.append(re.sub(r"[^'’\-]+", lambda m: normalize_piece(m.group()), word))
    return " ".join(words)

RULES={"customer_name":("CustomerNameSanitized",name_clean),"sales_person":("SalesPersonSanitized",name_clean),"salesperson":("SalesPersonSanitized",name_clean),"sale_date":("SaleDateSanitized",date_clean),"porsche_model":("PorscheModelSanitized",model_clean),
"model_year":("ModelYearSanitized",year_clean),"sale_price":("SalePriceSanitized",price_clean),
"vehicle_mileage":("VehicleMileageSanitized",mileage_clean),"payment_method":("PaymentMethodSanitized",payment_clean),
"city":("CitySanitized",city_clean),"state":("StateSanitized",state_clean),
"delivery_status":("DeliveryStatusSanitized",delivery_clean)}
REQUIRED=["sale_id","sale_date","customer_name","porsche_model","model_year","sale_price",
"vehicle_mileage","payment_method","city","state","delivery_status"]
def sanitize(input_xlsx,schema_md,output_xlsx):
    with open(schema_md,encoding="utf-8") as f:
        if not f.read().strip(): raise ValueError("schema.md está vazio")
    book=pd.ExcelFile(input_xlsx)
    with pd.ExcelWriter(output_xlsx,engine="openpyxl") as writer:
        for sh in book.sheet_names:
            df=pd.read_excel(input_xlsx,sheet_name=sh)
            missing=[c for c in REQUIRED if c not in df.columns]
            if missing: raise ValueError(f"Colunas obrigatórias ausentes em {sh}: {missing}")
            if not any(c in df.columns for c in ("sales_person", "salesperson")):
                raise ValueError(f"Coluna de vendedor ausente em {sh}: sales_person ou salesperson")
            out=df.copy()
            for src,(dest,fn) in RULES.items():
                if src in df.columns: out[dest]=df[src].apply(fn)
            cols=[]
            for c in df.columns:
                cols.append(c)
                if c in RULES: cols.append(RULES[c][0])
            out=out[cols]; name=sh[:31]; out.to_excel(writer,sheet_name=name,index=False)
            ws=writer.book[name]; ws.freeze_panes="A2"; ws.auto_filter.ref=ws.dimensions
            price_col=out.columns.get_loc("SalePriceSanitized")+1
            for row in range(2, ws.max_row+1): ws.cell(row,price_col).number_format="0.00"
            for col in ws.columns:
                width=min(max(max(len(str(x.value or "")) for x in col)+2,12),35)
                ws.column_dimensions[col[0].column_letter].width=width
    return output_xlsx
if __name__=="__main__":
    if len(sys.argv)<3: raise SystemExit("Uso: python porsche_sanitizer_agent.py porsche_database.xlsx schema.md [saida.xlsx]")
    dest=sys.argv[3] if len(sys.argv)>3 else "porsche_database_sanitized.xlsx"
    print("Arquivo gerado:",sanitize(sys.argv[1],sys.argv[2],dest))
