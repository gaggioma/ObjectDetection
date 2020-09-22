@ECHO OFF 

cd C:\Backup\Develop\Python\ObjectDetection\images
echo Creating myImages...
::python3 .\listCreator.py -r "output" -n train --type cutImages --numberofsamples 100
::python3 .\listCreator.py -r "output" -n validation --type cutImages --numberofsamples 10
echo Create myImages succesfully!!

echo Resizing image...
python3 .\imageResize.py -r "EmptyDataset" -n train -s 620
python3 .\imageResize.py -r "EmptyDataset" -n validation -s 620
echo Resizing succesfully!!

echo Listing file...
python3 .\listCreator.py -r "EmptyDataset" -n train --type list
python3 .\listCreator.py -r "EmptyDataset" -n validation --type list
echo Listing succesfully!!

echo Creating cfg...
python3 .\listCreator.py -r "EmptyDataset" -n train --type cfg
echo Create cfg succesfully!!

pause
