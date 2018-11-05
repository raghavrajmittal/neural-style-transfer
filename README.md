# Neural Style Transfer with OpenCV

Credit:
  - Adrian Rosebrock
  - https://www.pyimagesearch.com/2018/08/27/neural-style-transfer-with-opencv/


### Applying neural style transfer to images and videos(real-time using webcam).
   - Makes use of openCV and Python
   - imutils?

**Running style transfer on one image** <br/>
    $ python neural_style_transfer.py --image images/jurassic_park.jpg --model models/instance_norm/the_scream.t7


**Running style transfer on webcam video** <br/>
    $ python neural_style_transfer_video.py --models models<br/>
    - Press 'N' to go to next style<br/>
    - Press 'P' to go to previous style
    - Press 'A' to save the actual image (in screenshots folder)
    - Press 'S' to save the styled image
    - Press 'B' to save both (actual and styled iamges)
    - Press 'Q' to quit<br/>

**Running all style transfers on one image** <br/>
    $ python neural_style_transfer_examine.py --models models --image images/giraffe.jpg<br/>
    - Press any key to change style and generate another image
