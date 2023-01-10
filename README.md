# DEEP FAKE DETECTION

1) Install anaconda prompt from https://www.anaconda.com/
2) Open anaconda prompt and type conda create -n tf python==3.7.9
3) Enter to tf from base type conda activate tf
4) Install all the required libraries
   
   pip install tensorflow==1.15.0 ( enter ) 
   pip install scikit-learn==0.22.1 ( enter )
   pip install keras==2.2.4
   pip install h5py==2.10.0
   pip install pandas
   pip install matplotlib
   pip install opencv-contrib-python
   pip install imutils
   pip install notebook
   pip install protobuf==3.20

5) Now type the code save it as .py format file
6) Open anaconda prompt and type cd fakeface
7) Now type python app.py and press enter you will get ip address copy that link and paste in chrome website (http://127.0.0.1:5000/ )
8) Upload image form this paths C:\Users\Admin\fakeface\datasets\test

To run algorihtm with own data 

1) Copy new files in to this folder as fake and real folders 
   C:\Users\Admin\fakeface\datasets\train fake images in to fake folder, real images in to real folder 
2) Then follow these steps to train model it will take 1-2 hrs time based on size of dataset 
3) Open anaconda prompt form search and type 
   conda activate tf (enter )

4) Then type cd fakeface ( enter )
5) Now type python fakealgo.py ( press enter then training will start, after training is done model will get stored in the folder ) 
