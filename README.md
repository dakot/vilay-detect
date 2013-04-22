vilay-detect
============

A spatiotemporal Annotation Framework with customizable Detectors

Requirements
------------
* Python 2.7
* NumPy
* PyQt
* OpenCV (with Python-Bindings)

Installation
------------

1.	Use terminal go to main directory

2.	Use setup.py for installation

		python setup.py build_py

3.	Start program via console

		PYTHONPATH=. bin/vilay show [mediafile]

	or if not working

		PYTHONPATH=. python bin/vilay show [mediafile]

Sample Usage
------------

1.	Open a video-file (e.g. indi_short.m4v) using the "New file" Button. 
	(Larger videos may take some time)

2.	Select "Shot Detector" and press "Start Detector" Button. After a while
	you see elements comming up in the right Box.

3.	You can add Description Schemes to the File. Do "Right mouse click" on 
	"Feature Film" and select "Add new Description Scheme", name it and 
	press Ok. You now can move Descriptors in there or restructure your 
	file.

4.	Use the small items in the bar under the Control section to make you 
	working area smaller. Choose just a few seconds and try the "Face
	Detector".
	
