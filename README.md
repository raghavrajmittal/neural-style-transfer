Neural Style Transfer with OpenCV

Credit:
  - Adrian Rosebrock
  - https://www.pyimagesearch.com/2018/08/27/neural-style-transfer-with-opencv/


Applying neural style transfer to images and videos(real-time using webcam).
   - Makes use of openCV and Python
   - imutils?

Eg: Running style transfer on one image
    $ python neural_style_transfer.py --image images/jurassic_park.jpg --model models/instance_norm/the_scream.t7


Eg: Running style transfer on webcam video
    $ python neural_style_transfer_video.py --models models
    - Press 'N' key to dynamically change style
    - Press 'Q' key to quit

Eg: Running all style transfers on one image
    $ python neural_style_transfer_examine.py --models models --image images/giraffe.jpg
    - Press any key to change style and generate another image
