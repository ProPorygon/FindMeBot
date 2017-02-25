import cognitive_face as CF
import webbrowser


#Return URLs, option to open in a new window, of top x recognized faces
def findURLs(query_face,face_urls,api_key="32b1306905ff4a7dba1502d45876a7cf",number=2,open_picture=False):

	"""
	Params:
		query_face: URL of the face we are trying to match. Probably want to run this with all the faces in the group.
		face_urls: List of URLs of all the faces in our sample.
		api_key: API key for our calls. Set default to Ziwei's free trial key, but please use your own
		number: Number of faces you want to match- the lower the better tbh
		open_picture: True if you want to open your matched faces in another window. False otherwise.
	Returns:
		indices- indices of most matched faces
		confidence- confidence of those indices

	"""

	KEY = api_key  # Replace with a valid Subscription Key here.
	CF.Key.set(KEY)

	#URL for the target face
	result_query = CF.face.detect(query_face,True,False,'age,gender,smile')

	#URLs for the added faces
	#face_urls = ["http://i.imgur.com/0FBIdSN.jpg","http://i.imgur.com/cVFo6fc.jpg","http://i.imgur.com/AlG7wEC.jpg","http://i.imgur.com/t1SofqS.jpg","http://i.imgur.com/OrK5Hob.jpg"]

	CF.face_list.delete('sample_list')
	face_list = CF.face_list.create('sample_list')

	persistent_ids = []

	for picture in face_urls:
		faces = CF.face.detect(picture,True,False,'age,gender,smile')
		rectangle = faces[0]['faceRectangle']
		persistent_id = CF.face_list.add_face(picture,'sample_list',rectangle)
		persistent_ids.append(persistent_id['persistedFaceId'])

	#response = requests.post("https://westus.api.cognitive.microsoft.com/face/v1.0/detect",data = {'key':'value'},headers=headers)
	query_id = result_query[0]['faceId']
	#print (persistent_ids)

	indices = []
	confidence = []
	matched_faces = CF.face.find_similars(query_id,'sample_list',None,number,'matchFace')
	for face in matched_faces:
		confidenceInt = face['confidence']
		confidence.append(confidenceInt)
		picindex = persistent_ids.index(face['persistedFaceId'])
		indices.append(picindex)
		url = face_urls[picindex]
		if open_picture == True:
			webbrowser.open_new(url)
	return indices,confidence

def main():
	query_url = 'http://i.imgur.com/XuvapFY.jpg'
	face_urls = ["http://i.imgur.com/0FBIdSN.jpg","http://i.imgur.com/cVFo6fc.jpg","http://i.imgur.com/AlG7wEC.jpg","http://i.imgur.com/t1SofqS.jpg","http://i.imgur.com/OrK5Hob.jpg"]

	ind, conf = findURLs(query_url,face_urls)
	print(ind)

#main()
