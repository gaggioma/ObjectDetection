@ECHO OFF 

cd C:\Backup\Develop\Python\ObjectDetection\images
echo Creating myImages...
::python3 .\listCreator.py -r "C:\\Users\\magaggio\\Desktop\\MNIST-JPG-master\\MNIST-JPG-master\\output" -n train --type cutImages --numberofsamples 100
::python3 .\listCreator.py -r "C:\\Users\\magaggio\\Desktop\\MNIST-JPG-master\\MNIST-JPG-master\\output" -n validation --type cutImages --numberofsamples 10
echo Create myImages succesfully!!

echo Resizing image...
python3 .\imageResize.py -r "C:\\Users\\magaggio\\Desktop\\NumberDataset" -n train
python3 .\imageResize.py -r "C:\\Users\\magaggio\\Desktop\\NumberDataset" -n validation
echo Resizing succesfully!!

echo Listing file...
python3 .\listCreator.py -r "C:\\Users\\magaggio\\Desktop\\NumberDataset" -n train --type list
python3 .\listCreator.py -r "C:\\Users\\magaggio\\Desktop\\NumberDataset" -n validation --type list
echo Listing succesfully!!

echo Creating cfg...
python3 .\listCreator.py -r "C:\\Users\\magaggio\\Desktop\\NumberDataset" -n train --type cfg
echo Create cfg succesfully!!

pause
