import pandas as pd
import json
import openpyxl
import numpy as np

print(pd.__version__)

#creat the json file with default values
def create_json(data,tag,DSType):
#Loop Dictionary
    list1 = []
    Js_dictData = pd.DataFrame(data)
    sectionkey = (Js_dictData.loc[Js_dictData['Key'] == tag])
    #print(sectionkey.replace({pd.NA: None}))
    loop = Js_dictData.loc[Js_dictData['Key'] == tag]
    lp = (loop['Loop'].max())
    uniquelp = (loop['Loop'].unique())
 
    for l in uniquelp:
        dict1={}
        for key,value in zip(sectionkey[sectionkey['Loop']==l]['InputFile'],sectionkey[sectionkey['Loop']==l]['FixedValue'].replace({pd.NA:None})):
            if isinstance(value,str):
                value = value.replace(" ","")
            dict1[key] = value
        list1.append(dict1)
    if DSType == 'Dict':
        return dict1
    else:
        return list1

def get_value_from_nested_structure(data, key_path):
    current_value = data
    for key in key_path:
        if isinstance(current_value, dict) and key in current_value:
            current_value = current_value[key]
        elif isinstance(current_value, list) and isinstance(key, int) and 0 <= key < len(current_value):
            current_value = current_value[key]
        else:
            return None  # or raise an exception if the key path is invalid
    return current_value

def set_nested_value(d, keys, value):
    current_dict = d
    for key in keys[:-1]:
        if isinstance(key,int):
            current_dict = current_dict[key]
        else:
            current_dict = current_dict.setdefault(key, {})
    lastkey = keys[-1]
    if isinstance(lastkey,int):
        current_dict[lastkey] = value
    else:
        current_dict[lastkey] = value

def count_items(data,key):
    keylist = []
    InputJsonKey = key.split(',')
    for k in InputJsonKey:
                if k.isnumeric() == True:
                    keylist.append(int(k))
                else:
                    keylist.append(k) 
    for key in keylist:
        if isinstance(data[key],dict):
            data = data[key]
        elif isinstance(data[key],list):
            data= data[key]
        
    return len(data)

def get_keylist(Keys):
    InputJsonKey = Keys.split(',') 
    keylist = []
    for k in InputJsonKey:
        if k.isnumeric() == True:
            keylist.append(int(k))
        else:
            keylist.append(k)
    return keylist

def update_json(data,HxData,InputJson,OutputJson,Refdata,key,Loop,BusinessSegment,l1=0,l2=0,l3=0,l4=0,l5=0,l6=0,l7=0,l8=0,l9=0):

    JsData = InputJson
    HxInputData = HxData
    dsExtract = Refdata
    dsOutputdata = OutputJson

    #PrisyncInputJson
    dataset = data.loc[data['Key'] == key].fillna("")
    InputJsondata = dataset[dataset['InputJsonValue']!= ""]
    filterdata = InputJsondata[InputJsondata['Flag']== Loop]
    for row in filterdata.itertuples():
        
        KeyValue = row.InputJsonValue.replace('$',str(l1)).replace('#',str(l2)).replace('@',str(l3)).replace('α',str(l4)).replace('β',str(l5)).replace('γ',BusinessSegment)
        keylist = []
        keylist = get_keylist(KeyValue)
        InputJsonVal = get_value_from_nested_structure(JsData,keylist)
        SetVal = row.HxSetValue.replace('$',str(l1)).replace('#',str(l2)).replace('@',str(l3)).replace('α',str(l4)).replace('β',str(l6))
        Hxkeylist = []
        Hxkeylist = get_keylist(SetVal)
        if InputJsonVal is None:
            InputJsonVal = ""
        #print(row.Key,'-',row.InputFile,'-',row.InputJsonValue,'-',keylist,'-',row.Hierarchy,'-',Hxkeylist,'-',InputJsonVal)
        set_nested_value(HxInputData,Hxkeylist,InputJsonVal)
        
    DataExtractJson = dataset[dataset['DataExtractionValue']!= ""]
    filterExtractdata = DataExtractJson[DataExtractJson['Flag']== Loop]

    for row in filterExtractdata.itertuples():
        keyval = row.DataExtractionValue.split('|')
        keylist = ''
        if len(keyval) > 1:
            for k in keyval:
                JsonKey = get_keylist(k.replace('$',str(l1)).replace('#',str(l2)).replace('@',str(l3)).replace('α',str(l4)).replace('β',str(l4)).replace('γ',BusinessSegment))
                val = get_value_from_nested_structure(JsData,JsonKey)
                if val is None:
                    keylist = keylist + str(k) + ','
                else:
                    keylist = keylist + str(val) + ','

            datakeylist = []
            datakeylist = get_keylist(keylist.rstrip(','))
            DataExtractJsonVal = get_value_from_nested_structure(dsExtract,datakeylist)
        else :
            DataExtractionValue = row.DataExtractionValue
            datakeylist = get_keylist(DataExtractionValue)
            DataExtractJsonVal = get_value_from_nested_structure(dsExtract,datakeylist)

        Hxkeylist = get_keylist(row.HxSetValue)
        SetVal = row.HxSetValue.replace('$',str(l1)).replace('#',str(l2)).replace('@',str(l3)).replace('α',str(l4)).replace('β',str(l4))
        SetExKey = []
        SetExKey = get_keylist(SetVal)
        if DataExtractJsonVal is None:
            DataExtractJsonVal = ""
        #print(row.Key,'-',row.InputFile,'-',row.DataExtractionValue,'-',DataExtractJsonVal,'-',row.Hierarchy,'-',SetExKey)
        set_nested_value(HxInputData,SetExKey,DataExtractJsonVal)
    
    #PrisyncOutput Json
    OPJsondata = dataset[dataset['OutputJsonValue']!= ""]
    OPfilterdata = OPJsondata[OPJsondata['Flag']== Loop]
    for row in OPfilterdata.itertuples():
        
        KeyValue = row.OutputJsonValue.replace('$',str(l1)).replace('#',str(l2)).replace('@',str(l3)).replace('α',str(l4)).replace('β',str(l5)).replace('γ',BusinessSegment)
        keylist = []
        keylist = get_keylist(KeyValue)
        OPJsonVal = get_value_from_nested_structure(dsOutputdata,keylist)
        SetVal = row.HxSetValue.replace('$',str(l1)).replace('#',str(l2)).replace('@',str(l3)).replace('α',str(l4)).replace('β',str(l6))
        Hxkeylist = []
        Hxkeylist = get_keylist(SetVal)
        if OPJsonVal is None:
            OPJsonVal = ""
        #print(row.Key,'-',row.InputFile,'-',row.InputJsonValue,'-',keylist,'-',row.Hierarchy,'-',Hxkeylist,'-',InputJsonVal)
        set_nested_value(HxInputData,Hxkeylist,OPJsonVal)


def rename_keys(data,KeyPath,OldKey,NewKey):
    current_dict = data
    temp_dict = data
    for key in KeyPath:
        if isinstance(key,int):
            current_dict = current_dict[key]
        elif key in current_dict:
            current_dict = current_dict[key]
    current_dict[NewKey] = current_dict.pop(OldKey)

df = pd.read_excel(r"OutputMappingSheet.xlsx")

loopdf = pd.read_excel(r"OutputMappingSheet.xlsx",sheet_name="Loops")

dfCreatJson = pd.read_excel(r"OutputMappingSheet.xlsx",sheet_name="Creation")

dfRenameKeys = pd.read_excel(r"OutputMappingSheet.xlsx",sheet_name="RenameKeys")

segment = pd.read_excel(r"OutputMappingSheet.xlsx",sheet_name="BusinessSegment")

with open(r"PriSyncInput.json") as jsread:
    JsData = json.load(jsread)

with open(r"DataExtraction.json") as dsread:
    dsExtract = json.load(dsread)

with open(r"PriSyncOutput.json") as OutRead:
    OutJson = json.load(OutRead)

data = pd.DataFrame(df)

data = data.astype({'Loop' : int})

distinctkeys = data['Key'].unique()

Hierarchy = data['Hierarchy'].fillna(" ").unique()

distinctHierarchy = []

for k in Hierarchy:
    if k !=" " and k!="NaN":
        distinctHierarchy.append(k)

list1 = []
finaldict = {}
dict3={}

#create key-value pair from mapping sheet

for key in distinctkeys:
    Datakey = data[data['Key']==key]
    DsType = Datakey['DSType'].unique()
    list1.append(create_json(data,key,DsType))
    finaldict[key] = create_json(data,key,DsType)

#Create Empty Json Files

if distinctkeys[0] == 'Root':
    dict3 = finaldict['Root']

for key in distinctHierarchy:
    keylist = []
    keylist = get_keylist(key)
    set_nested_value(dict3,keylist,finaldict[keylist[-1]])  
    
Renamekeys = pd.DataFrame(dfRenameKeys)
for row in Renamekeys.itertuples():
    KeyPath = get_keylist(row.KeyPath)
    rename_keys(dict3,KeyPath,row.OldKey,row.NewKey)



# print(finaldict['Sections'])
jsonstructure = pd.DataFrame(dfCreatJson)

for key in distinctkeys:
    Jsonstruct = jsonstructure.loc[jsonstructure['Keys'] == key]
    for row in Jsonstruct.itertuples():
        keys = row.Keys
        Loop = count_items(OutJson,row.Loop)
        keylist = []
        keylist = get_keylist(row.PlacementKeys)
        tempdict = {}
        tempdict = finaldict[key]
        if isinstance(tempdict,list):
            set_nested_value(dict3,keylist,tempdict*Loop)
        else:
            set_nested_value(dict3,keylist,tempdict)

out_file = open(r"HxOutputTemplate.json","w")

json.dump(dict3,out_file,indent=6)

out_file.close()

#BusinessSegemtn for Additional CENDMob_Additional

BSKey = segment['SegmentKey'].unique()

BusinessSegment = ''
if len(BSKey)>0:

    BSegment = get_value_from_nested_structure(JsData,BSKey)

    SegmentKey = pd.DataFrame(segment)

    dictBS = {}
    
    for row in SegmentKey.itertuples():
        dictBS.setdefault(row.Segment,row.Key)

    BusinessSegment = dictBS[BSegment]

#Updating the JsonFile

with open(r"HxOutputTemplate.json") as HxInput:
    HxInputData = json.load(HxInput)

LoopValues = pd.DataFrame(loopdf)

for key in distinctkeys:
    update_json(data,HxInputData,JsData,OutJson,dsExtract,key,'NotInLoop',BusinessSegment)

Levels = {}

for row in LoopValues.itertuples():
    #print(row.Key,count_items(JsData,row.InputKey))
    #print(type(row.InputKey),row.InputKey,len(row.InputKey))

    if isinstance(row.InputKey,str) and len(row.InputKey) > 0:
        Levels[row.Key] = count_items(OutJson,row.InputKey)
    else:
        Levels[row.Key] = 1

Levellist = []
Valuelist = []

for key,value in Levels.items():
    Levellist.append(key)
    Valuelist.append(value)


for l1 in range(Valuelist[0]):   #Sections
    update_json(data,HxInputData,JsData,OutJson,dsExtract,Levellist[0],'InLoop',BusinessSegment,l1)
    for l2 in range(Valuelist[1]): #SectionFinancialTypes
        update_json(data,HxInputData,JsData,OutJson,dsExtract,Levellist[1],'InLoop',BusinessSegment,l1,l2)
    for l3 in range(Valuelist[2]): #Coverages
        update_json(data,HxInputData,JsData,OutJson,dsExtract,Levellist[2],'InLoop',BusinessSegment,l1,l3)
        for l4 in range(Valuelist[3]):   #CoverageFinancialTypes
            update_json(data,HxInputData,JsData,OutJson,dsExtract,Levellist[3],'InLoop',BusinessSegment,l1,l3,l4)
             

out_file = open(r"HxOutput_test.json","w")

json.dump(HxInputData,out_file,indent=6)

out_file.close()
