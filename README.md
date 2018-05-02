
## SkyFall : Gesture Controlled Web based Game using Tensorflow Object Detection Api

> Control the game paddle by waving your hand in from of a web cam.

<img src="static/img/handtrack.gif" width="100%">

Skyfall is a physics based game in which users can control an onscreen paddle simply by moving their hands in front of a web cam. Light weight Convolutional Neural Networks (MobileNet, SSD) are used to detect the users hands which is then mapped to the controls of the game. The structure of the interaction supports multiple players (provided they can be accommodated in the field of view of the camera). The system demonstrates how the integration of a well-trained and light weight hand detection model is used to robustly track player hands and enable “body as an input” interaction in real-time (up to  20 fps).
 

## Installation

Install requirements.

```
pip install -r requirements.txt
```

## Run  Application

```
python app.py
```

View the game in your browser - `http://localhost:5005` 
