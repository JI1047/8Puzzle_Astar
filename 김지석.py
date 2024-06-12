import cv2
import random
import numpy as np
import matplotlib.pyplot as plt
import pyautogui
from queue import PriorityQueue

# 정답 이미지 파일 리스트 정의
imgList11 = ['num_1.png', 'num_2.png', 'num_3.png']
imgList12 = ['num_8.png', 'num_0.png', 'num_4.png']
imgList13 = ['num_7.png', 'num_6.png', 'num_5.png']
imgList1 = imgList11 + imgList12 + imgList13  # 3개의 리스트를 하나의 리스트로 변경한다.


# imgList1에 있는 이미지 파일들을 읽어들이고, 타겟 크기로 조정후 RGB 형식으로 반환
def load_images(target_size=(224, 224)):
    # 이미지의 사이즈를 224x224로 맞춘다.
    return [cv2.resize(cv2.cvtColor(cv2.imread(img), cv2.COLOR_BGR2RGB), target_size) for img in imgList1]
    # 읽어들인 이미지를 RGB 형식으로 변환

# 이미지 파일 읽어들어서 리스트에 저장한다.
images = load_images()

# 목표 이미지 이게 결과이다.
goal = images.copy()


# 이미지를 그리는 함수 정의
def draw_images(puzzle):
    for i in range(3):
        for j in range(3):
            plt.subplot(3, 3, i * 3 + j + 1)  # 3*3의 서브플롯 지정
            plt.gca().axes.xaxis.set_visible(False)  # 서브플롯의 x축을 숨긴다.
            plt.gca().axes.yaxis.set_visible(False)  # 서브플롯의 y축을 숨긴다.
            plt.imshow(puzzle[i * 3 + j])  # 현재 인덱스에 해당하는 이미지를 서브플롯에 표시
    plt.draw()

fig, axes = plt.subplots(3, 3, figsize=(5, 5))  # 3*3의 틀을 만든다.
# fig는 전체 그림(figure) 객체를, axes는 각각의 서브플롯에 대한 객체 배열을 나타낸다.
# 그림의 크기는 5*5사이즈


i = 4

def shuffle_puzzle():
    global i  # i를 함수 내에서 사용할 수 있도록 전역변수로 변경

    for _ in range(10):  # 몇번 섞을지 설정
        r = random.randrange(4)  # 4로 나눈 나머지는(0,1,2,3)이므로 랜덤으로 r변수는 0,1,2,3중 하나의 값을 갖게 된다.

        if r == 0 and (i != 0 and i != 3 and i != 6):  # Move left i != 0 or i!=3 or i!= 6이면 왼쪽으로 못가니까
            images[i], images[i-1] = images[i-1], images[i]
            i = i-1  # 한칸 왼쪽으로 갔으니까

        elif r == 1 and (i != 2 and i != 5 and i != 8):  # Move right i != 2 or i!=5 or i!= 8이면 오른쪽으로 못가니까
            images[i], images[i+1] = images[i+1], images[i]
            i = i+1  # 한칸 오른쪽으로 갔으니까

        elif r == 2 and (i != 0 and i != 1 and i != 2):  # Move up i != 0 or i!=1 or i!= 2이면 위쪽으로 못가니까
            images[i], images[i-3] = images[i-3], images[i]
            i = i-3  # 한칸 위쪽으로 갔으니까

        elif r == 3 and (i != 6 and i != 7 and i != 8):  # Move right i != 6 or i!=7 or i!= 8이면 아래쪽으로 못가니까
            images[i], images[i+3] = images[i+3], images[i]
            i = i+3  # 한칸 아래쪽으로 갔으니까


shuffle_puzzle()  # images를 섞는다 랜덤으로

draw_images(images)  # 섞인 이미지를 일단 처음에 띄워놓는다.

cur = images.copy()


# 휴리스틱 함수
def h(puzzle, goal):
    return sum([1 if not np.array_equal(puzzle[i], goal[i]) else 0 for i in range(len(puzzle))])
    #puzzle의 길이만큼 puzzle[i], goal[i]가 같으면 0을 다르면 1을 리스트에 추가하여 더한다.
    #puzzle과 goal의 다른 위치 개수를 나타낸다.
x = 0

def on_click(event):
    global x
    # 절대 좌표를 기준으로 클릭된 숫자를 반환
    if (128 <= event.x <= 378) and (634 <= event.y <= 874):
        x = 0
        return x
    elif (390 <= event.x <= 636) and (634 <= event.y <= 874):
        x = 1
        return x
    elif (650 <= event.x <= 896) and (634 <= event.y <= 874):
        x = 2
        return x
    elif (128 <= event.x <= 378) and (374 <= event.y <= 614):
        x = 3
        return x
    elif (390 <= event.x <= 636) and (374 <= event.y <= 614):
        x = 4
        return x
    elif (650 <= event.x <= 896) and (374 <= event.y <= 614):
        x = 5
        return x
    elif (128 <= event.x <= 378) and (114 <= event.y <= 354):
        x = 6
        return x
    elif (390 <= event.x <= 636) and (114 <= event.y <= 354):
        x = 7
        return x
    elif (650 <= event.x <= 896) and (114 <= event.y <= 354):
        x = 8
        return x
    



def movePuzzle(puzzle, zero_idx):  # 현재 퍼즐, 0의 위치, 방향을 매개변수로 가진다.
    global x
    puzzle = puzzle.copy()  # 원본 배열을 변경하지 않도록 복사
    if zero_idx == x + 3:  # 클릭한 숫자가 위에 있을 때
        puzzle[zero_idx], puzzle[zero_idx - 3] = puzzle[zero_idx - 3], puzzle[zero_idx]
        zero_idx -= 3
    elif zero_idx == x - 3:  # 클릭한 숫자가 아래에 있을 때
        puzzle[zero_idx], puzzle[zero_idx + 3] = puzzle[zero_idx + 3], puzzle[zero_idx]
        zero_idx += 3
    elif zero_idx == x - 1 :  # 클릭한 숫자가 오른쪽에 있을 때
        puzzle[zero_idx], puzzle[zero_idx + 1] = puzzle[zero_idx + 1], puzzle[zero_idx]
        zero_idx += 1
    elif zero_idx == x + 1:  # 클릭한 숫자가 왼쪽에 있을 때
        puzzle[zero_idx], puzzle[zero_idx - 1] = puzzle[zero_idx - 1], puzzle[zero_idx]
        zero_idx -= 1
    else:
        return None, None  # 이동할 수 없는 경우 None 반환
    return puzzle, zero_idx  # 바뀐 퍼즐과 0의 위치를 반환한다.


def update_and_solve(event):
    on_click(event)  # 클릭 이벤트 처리하여 x 값 설정
    if x is not None:
        global cur, i  # 현재 퍼즐 상태와 i는 0의 위치를 나타내는 전역 변수로 사용
        new_puzzle, new_i = movePuzzle(cur, i)  # 퍼즐 상태 업데이트
        if new_puzzle is not None and new_i is not None:  # 이동이 성공적으로 이루어진 경우에만 업데이트
            cur, i = new_puzzle, new_i
            draw_images(cur)  # 업데이트된 퍼즐 상태를 그림
        if h(cur, goal) == 0:  # 퍼즐이 goal의 모양과 같아졌을때
            print("Goal reached!")    

# 이벤트 핸들러 등록 및 그림 표시
fig.canvas.mpl_connect('button_press_event', update_and_solve)
plt.subplots_adjust(wspace=0.01, hspace=0.02)
plt.show()
