#!/usr/bin/env python

import os
from sys import argv
from subprocess import call
from face_client import FaceClient
import pprint
import pyNotificationCenter

#https://api.skybiometry.com/fc/faces/recognize.json?api_key=33f9c5446fef45e6b16acc3ce7dab0d8&api_secret=6dd4226bbf4c4dd18dc3efda8cde8d41&urls=https://fbcdn-sphotos-b-a.akamaihd.net/hphotos-ak-ash4/p206x206/247653_10151605077307147_608037281_n.jpg&attributes=all

julie_id = "juls@ss.test"
eric_id = "bigjumbo@ss.test"

pp = pprint.PrettyPrinter(indent=4)

photo = 'http://sandalsoft.com/snapshot.jpg'
local_photo = '/Users/Eric/scripts/facedetect/snapshot.jpg'
client = FaceClient('33f9c5446fef45e6b16acc3ce7dab0d8', '6dd4226bbf4c4dd18dc3efda8cde8d41')

def detect_face():
	detect = client.faces_detect(file=local_photo, aggressive=True)
	pp.pprint(detect)
	face_tags = detect['photos'][0]['tags'][0]
	if face_tags:
		attributes = face_tags['attributes']

		dark_glasses = attributes['dark_glasses']['value']
		dark_glasses_confidence = attributes['dark_glasses']['confidence']
		is_face = attributes['face']['value']
		face_confidence = attributes['face']['confidence']
		gender = attributes['gender']['value']
		gender_confidence = attributes['gender']['confidence']
		glasses = attributes['glasses']['value']
		glasses_confidence = attributes['glasses']['confidence']
		smiling = attributes['smiling']['value']
		smiling_confidence = attributes['smiling']['confidence']
		print "SMILING: " + smiling
		if smiling:
			smiling_str = "smiling"
		else:
			smiling_str = "not smiling"
		# smiling_str = "smiling" if smiling is 'true' else "not smiling"
		if is_face:
			notification_text = "You are a " + gender + " who is " + smiling_str

			notify(notification_text)
		pp.pprint(attributes)
	else:
		print "Face not detected"


def recognize_face():
	recog = client.faces_recognize(uids='all', file=local_photo, aggressive=True, namespace='ss.test')
	tags = recog['photos'][0]['tags']

	# pp.pprint(tags);
	
	if (tags):
		uids = tags[0]['uids']#['confidence']

		## Get highest confidence uid tag
		highest_confidence_uid = max(uids, key=lambda x:x['confidence'])
		if highest_confidence_uid['confidence'] < 60 :
			print "Unable to determine who this is"
			print uids
			exit()
		else:
			print "we are confident: " + str(highest_confidence_uid['confidence'])

		print highest_confidence_uid['uid']
		if highest_confidence_uid['uid'] == eric_id:
			# print "hi is eric"
			send_greeting("Eric", 501)
		if highest_confidence_uid['uid'] == julie_id:
			send_greeting("Julie", 502)
			
		# pp.pprint(uids)
	else:
		print "Face not recognized"

def send_greeting(name, uid):
	current_uid = os.getuid()
	# print current_uid
	if uid == current_uid:
		notify("Welcome back " + name)
	else:
		# notify("Please login " + name)
		switch_user(str(uid))

def switch_user(uid):
	exec_cmd = "/System/Library/CoreServices/Menu Extras/User.menu/Contents/Resources/CGSession"
	print exec_cmd
	call([exec_cmd, "-switchToUserID", uid])


def notify(message):
	print message
	exec_cmd = "terminal-notifier"
	call([exec_cmd, "-message", message, "-title", "Human Detected"])


def main():
	# detect_face()
	recognize_face()

if  __name__ =='__main__':main()


