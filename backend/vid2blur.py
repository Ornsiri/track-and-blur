import cv2
import os
from retinaface import RetinaFace

path = os.getcwd() + "/"

def blurvid(inpath, outpath, filename):

    # vidcap = cv2.VideoCapture("/Users/guytanakrit/Documents/Documents - Tanakrit’s MacBook Pro/Zoom/2022-10-07 20.01.04 Tanakrit Jaichuen's Zoom Meeting/video1055454992.mp4")
    # vidcap = cv2.VideoCapture(r"D:\project\retinaface\data\test1.mp4")
    vidcap = cv2.VideoCapture(inpath)
    success, img = vidcap.read()
    count = 0
    # output_path = r'D:\project\retinaface\output'  # Windows )
    # output_path = r'/Users/guytanakrit/Google Drive/NSTDA_Intern/output_frame'  # Mac
    os.chdir(path + outpath)

    fps = vidcap.get(cv2.CAP_PROP_FPS)
    length = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    width  = int(vidcap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    # print('frames per second = ',fps)
    # print('length = ', length)
    # print('width = ', width)
    # print('height = ', height)

    fps = int(fps)

    frameSize = (width, height)
    # out = cv2.VideoWriter('output_video1.mp4',cv2.VideoWriter_fourcc(*'H264'), 1, frameSize)
    out = cv2.VideoWriter(path+outpath + 'output_' + filename, cv2.VideoWriter_fourcc(*'H264'), 1, frameSize)

    count = 0

    while success:
        os.chdir(path + outpath)
        # print(os.getcwd())
        # cv2.imwrite("test_out%d.jpg" % count, image)     # save frame as JPEG file
        # success,image = vidcap.read()
        for i in range(fps):
            success,img = vidcap.read()
        success, img = vidcap.read()
    

        # img = cv2.imread("data/fortest.JPG")
        try:
            resp = RetinaFace.detect_faces(img)

            ksize = 200
            pixSize = 5
            for i in range(len(resp)):
                face = (resp['face_'+str(i+1)]['facial_area'])
                x1 = face[0]
                y1 = face[1]
                x2 = face[2]
                y2 = face[3]

                start = (x1, y1)
                stop = (x2, y2)
                # print(start, " ", stop)

                x, y = start[0], start[1]
                w, h = stop[0] - start[0], stop[1] - start[1]
                ROI = img[y:y+h, x:x+w]
                # print (ROI)
                # blur = cv2.GaussianBlur(ROI, (51, 51), 0)     # gaussian blur
                # blur = cv2.blur(ROI, (ksize, ksize))          # avg blur

                # pixelate blur
                height, width = ROI.shape[:2]
                pre = cv2.resize(ROI, (pixSize, pixSize),
                                interpolation=cv2.INTER_LINEAR)
                blur = cv2.resize(pre, (width, height),
                                interpolation=cv2.INTER_NEAREST)
                # assign blured ROI back to image
                img[y:y+h, x:x+w] = blur

            # print("Output frame %d" % count)
            # print('Read a new frame: ', success)
            # cv2.imwrite("test_out%d.jpg" % count, img)     # save frame as JPEG file
            # count += 1
        except:
            print("Error!")
    
    
        out.write(img)
        print('processing')
        count+=1

    out.release
    print('Done')

    # print('Count: ',count)


    # minutes = 0
    # seconds = 2
    # frame_id = int(fps*(minutes*60 + seconds))
    # print('frame id =',frame_id)
    # t_msec = 1000*(minutes*60 + seconds)
    # vidcap.set(cv2.CAP_PROP_POS_MSEC, t_msec)
    # success,frame = vidcap.read()
    # cv2.imshow('frame', frame); cv2.waitKey(0)
    # print(type(frame))


# config input video's path & output's video path
# inpath = path+"tomp.mp4"
# outpath = path


# # print(os.path.isfile('test.mp4'))
# print(os.path.realpath('app.py'))


# run function
# blurvid(inpath, outpath,"tomp")
