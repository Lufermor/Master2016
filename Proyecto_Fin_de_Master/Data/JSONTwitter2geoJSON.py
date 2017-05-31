jsonFile = "D:\\tGIS3\\GoogleDrive\\z98WORKING\\z17cCatalunya\\CATv1b.json"
geoJsonFile = "D:\\tGIS3\\GoogleDrive\\z98WORKING\\z17cCatalunya\\CATGeov1b.json"
maxFeatures = 100000
tableFormat = True #it splits dictionary in fields

#------
#Function from http://gis.stackexchange.com/questions/115733/converting-json-to-geojson-or-csv
import json

def inJSON(data, prevKey):
    tempDict = {}
    
    for key in data.keys():
        if key not in ('coordinates', 'geo'):
            if prevKey != "":
                newKey = prevKey + "-" + key
            else:
                newKey = key
                
            if data[key] in ([], {}):
                pass
            elif 'created_at' in key:
                    tempDict[newKey] = data[key]["$date"]
            else:
                if isinstance(data[key], dict) and tableFormat:
                    tempDict.update(inJSON(data[key], newKey))
                else:
                    tempDict[newKey] = data[key]

    return tempDict

def closeFile():
    newFile.write('],\n"bbox": '+ str(bbox) + '}')
    newFile.close() 
    

def convert_json_feature(feature):
    feature = json.loads(feature)
    properties = inJSON(feature, "")

    if feature["coordinates"]["coordinates"][0] < bbox[0]:
        bbox[0] = feature["coordinates"]["coordinates"][0]
    elif feature["coordinates"]["coordinates"][0] > bbox[2]:
        bbox[2] = feature["coordinates"]["coordinates"][0]

    if feature["coordinates"]["coordinates"][1] < bbox[1]:
        bbox[1] = feature["coordinates"]["coordinates"][1]
    elif feature["coordinates"]["coordinates"][1] > bbox[3]:
        bbox[3] = feature["coordinates"]["coordinates"][1]
    
    return json.dumps({"type": "Feature",
                       "geometry": {"type": "Point",
                                    "coordinates": [feature["coordinates"]["coordinates"][0],
                                                    feature["coordinates"]["coordinates"][1]]},
                                    "properties": properties
                       }, ensure_ascii=False).encode('utf8')

geoJsonFileTemp = geoJsonFile.split(".")
data = open(jsonFile, "r")
fileCount = 0
starter = True

for i in data:
    if starter:
        starter = False
        name = geoJsonFileTemp[0] + "_" + str(fileCount) + "." + geoJsonFileTemp[1]
        geoJsonFile = name
        global newFile, bbox
        bbox = [9999999, 9999999, -9999999, -9999999]
        newFile = open(geoJsonFile, "w")
        newFile.write('{ "type": "FeatureCollection", "features": [')
        featureCount = 0
        print name        

    featureCount += 1
    text2File = "\n" + str(convert_json_feature(i))
    
    if featureCount == 1:
        newFile.write(text2File)
    else:
        newFile.write("," + text2File)

    if featureCount >= maxFeatures:
        starter = True
        fileCount += 1
        closeFile()             

if not newFile.closed:
    closeFile()
    
data.close()

