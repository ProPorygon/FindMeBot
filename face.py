import cognitive_face as CF
import webbrowser


#Return URLs, option to open in a new window, of top x recognized faces 
def findURLs(query_face,face_urls,api_key,number=2,open_picture=False):
	
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

#
def matchFace(query_faces, face_urls,api_key):

	"""
		Returns an array containing the most likely face for each face in the face urls, stored as an index.
		Params
		query_faces: array of URLS for source faces to match 
		face_urls: faces submitted to the groupchat. Will match each with a query face.
		api_key: API key for the arrays. Use the one that's 10 calls per second.

		Returns:
		mostlikely: Array of indices of query_face that corresponds to the matched face.

	"""
	mostlikely = [0 for i in range(len(face_urls))]
	highestconf = [0 for i in range(len(face_urls))]
	for query_face in query_faces:
		ind,conf = findURLs(query_face,face_urls,api_key,len(face_urls),False)
		for i in range(len(ind)):
			if conf[i] > highestconf[i]:
				mostlikely[ind[i]] = query_faces.index(query_face)
				highestconf[ind[i]] = conf[ind[i]]
	return mostlikely

def main():
	query_urls = ['http://i.imgur.com/XuvapFY.jpg','http://i.imgur.com/AW2x9Z6.png']
	face_urls = ["http://i.imgur.com/0FBIdSN.jpg","http://i.imgur.com/t1SofqS.jpg","http://i.imgur.com/cVFo6fc.jpg","http://i.imgur.com/AlG7wEC.jpg","http://i.imgur.com/OrK5Hob.jpg"]

	api_key = "bb9ec8fa29aa4c95b2952db12635cd1e"
	matched_indices = matchFace(query_urls,face_urls,api_key)
	print(matched_indices)
	for face in matched_indices:
		if (face == 0):
			print "Ziwei"
		else:
			print "Kevin"
main()

