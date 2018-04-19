import cv2
import numpy as np

cap = cv2.VideoCapture("SampleVideo_1280x720_1mb.mp4")
frames = list()
while (cap.isOpened()):
    ret, frame = cap.read()
    if ret == True:
        frames.append(frame)
    else:
        break
print(len(frames))
cap.release()


def getMacroblocks(frame):
    # print(frame.shape)
    mb = list()
    # print(frame.shape[0]/16, frame.shape[1]/16)
    for i in range(0, int(frame.shape[0]), 16):
        for j in range(0, int(frame.shape[1]), 16):
            # print(i, j)
            mb.append(frame[i:i+16,j:j+16])

    mb = np.array(mb)
    # print(mb[0])
    # print(len(mb[:,0]))
    return mb


def calculateSFD(frame1, frame0):
    sfd = list()
    sum0 = 0
    for i in range(len(frame1)):
        for j in range(16):
            for k in range(16):
                # print(type(frame1[i][j][k][0]))
                if frame1[i][j][k][0] >= frame0[i][j][k][0]:
                    sum0 = sum0 + (int(frame1[i][j][k][0]) - int(frame0[i][j][k][0]))
                else:
                    sum0 = sum0 + (int(frame0[i][j][k][0]) - int(frame1[i][j][k][0]))

                if frame1[i][j][k][1] >= frame0[i][j][k][1]:
                    sum0 = sum0 + (int(frame1[i][j][k][1]) - int(frame0[i][j][k][1]))
                else:
                    sum0 = sum0 + (int(frame0[i][j][k][1]) - int(frame1[i][j][k][1]))

                if frame1[i][j][k][0] >= frame0[i][j][k][0]:
                    sum0 = sum0 + (int(frame1[i][j][k][2]) - int(frame0[i][j][k][2]))
                else:
                    sum0 = sum0 + (int(frame0[i][j][k][2]) - int(frame1[i][j][k][2]))

        sfd.append(sum0)
        sum0 = 0

    return sfd


def encode_type(mb, type_mode):
    pass


def encode_pred(mb, pred_mode):
    pass


def rdo_cost(original_mb, encoded_mb):
    pass


def ifIntra(fd, frame_mb,i,prev_mb, mb, ct, sfdt):
    type_modes = list()
    pred_modes = list()
    selected = list()
    settings = list()
    # for i in range(len(=frame_mb)):
    if fd[i] == 0: #checking if macroblock is from stable background
        for j in range(len(type_modes)):    #for jth typ modes
            mb[i][j] = encode_type(frame_mb[i], type_modes[j]) #return encoded macroblock
            sfdt[i][j] = [type_modes[j], calculateSFD(mb[i][j], prev_mb[i][j])]  #sfd between encoded block form this frame and previous
            ct[i][j] = [rdo_cost(frame_mb[i], mb[i][j]), sfdt[i][j]]  # rdo cost for ith macblock using jth type mode
        sorted_sfd=sorted(sfdt[i], key=lambda x:x[1])
        #valid no of Ptop = 50% so NTtop = 2
        pTtop = .5
        NTtop = int(len(type_modes)*pTtop)
        #so sfdi <= sfd2
        SFDTth = sorted_sfd[i][NTtop]
        sorted_cost = sorted(ct[i],key=lambda x:x[0])
        for k in range(len(sorted_cost)):
            if(sorted_cost[k][1][1]<=SFDTth):
                selected.append(sorted_cost[k][1][0])


        #for prediction mode in selected typemode
        for j in range(len(pred_modes[selected[0]])):    #for jth pred modes
            mb[i][j] = encode_pred(frame_mb[i], pred_modes[j]) #return encoded macroblock
            sfdt[i][j] = [pred_modes[j], calculateSFD(mb[i][j], prev_mb[i][j])]  #sfd between encoded block form this frame and previous
            ct[i][j] = [rdo_cost(frame_mb[i], mb[i][j]), sfdt[i][j]]  # rdo cost for ith macblock using jth type mode
        sorted_sfd=sorted(sfdt[i], key=lambda x:x[1])
        #valid no of Ptop = 50% so NTtop = 2
        pPtop = .5
        NPtop = int(len(pred_modes[selected[0]])*pPtop)
        #so sfdi <= sfd2
        SFDPth = sorted_sfd[i][NPtop]
        sorted_cost = sorted(ct[i],key=lambda x:x[0])
        for k in range(len(sorted_cost)):
            if(sorted_cost[k][1][1]<=SFDPth):
                selected.append(sorted_cost[k][1][0])
        settings.append(selected)
        selected[:]=[]


mbs = list()
for i in range(len(frames)):
    mbs.append(getMacroblocks(frames[i]))
# getMacroblocks(frames[0])
print(len(mbs))

fd = calculateSFD(mbs[1], mbs[0])
