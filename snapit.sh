#!/bin/bash

/Users/Eric/scripts/facedetect/imagesnap -q -o /Users/Eric/scripts/facedetect/snapshot.jpg
sips -Z 600 /Users/Eric/scripts/facedetect/snapshot.jpg
#scp -q /Users/Eric/scripts/facedetect/snapshot.jpg eric@sandalsoft.com:www

