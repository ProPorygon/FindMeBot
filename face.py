import cognitive_face as CF
#import requests

KEY = '32b1306905ff4a7dba1502d45876a7cf'  # Replace with a valid Subscription Key here.
CF.Key.set(KEY)

headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': KEY,
}

#URL for the target face
query_url = 'http://i.imgur.com/XuvapFY.jpg'

result_query = CF.face.detect(query_url,True,False,'age,gender,smile')

#URLs for the added faces
face_urls = ["http://i.imgur.com/0FBIdSN.jpg","http://i.imgur.com/cVFo6fc.jpg","http://i.imgur.com/AlG7wEC.jpg","http://i.imgur.com/t1SofqS.jpg","http://i.imgur.com/OrK5Hob.jpg"]

CF.face_list.delete('sample_list')
face_list = CF.face_list.create('sample_list')

persistent_ids = []


for picture in face_urls:
	faces = CF.face.detect(picture,True,False,'age,gender,smile')
	rectangle = faces[0]['faceRectangle']
	print(rectangle)
	persistent_id = CF.face_list.add_face(picture,'sample_list',rectangle)
	persistent_ids.append(persistent_id['persistedFaceId'])

#response = requests.post("https://westus.api.cognitive.microsoft.com/face/v1.0/detect",data = {'key':'value'},headers=headers)
query_id = result_query[0]['faceId']
print (persistent_ids)

matched_faces = CF.face.find_similars(query_id,'sample_list',None,2,'matchFace')
print(matched_faces)
