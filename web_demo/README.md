# Pose-estimation
Base on "https://github.com/yuyoujiang/Exercise-Counter-with-YOLOv8-on-NVIDIA-Jetson"'s work
#本專案是基於Yolov8 pose estimation在VMWare中建立Ubuntu OS來執行運動檢測
#Disk size reccommand > 24 Gb

# Step 1:
Install VMWare & Ubuntu ios file

# Step 2:
Create VM with disk size >24 Gb

# Step 3:
sudo apt update &
sudo apt install -y python3-pip &
pip3 install --upgrade pip

# Step 4:
git clone https://github.com/yuyoujiang/exercise-counting-with-YOLOv8.git

# Step 5:
pip install these:  
numpy==2.0.0
opencv_python==4.10.0.84
torch==2.3.1
ultralytics==8.0.100

# Step 6 (on webcam) :
python3 demo.py --sport <exercise_type> --model yolov8s-pose.pt --show True --input 0
