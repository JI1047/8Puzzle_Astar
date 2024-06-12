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
imgList1 = imgList11 + imgList12 + imgList13#3개의 리스트를 하나의 리스트로 변경한다.


# imgList1에 있는 이미지 파일들을 읽어들이고, 타겟 크기로 조정후 RGB 형식으로 반환
def load_images(target_size=(224, 224)):
    # 이지미의 사이즈를 224x224로 맞춘다.
    return [cv2.resize(cv2.cvtColor(cv2.imread(img), cv2.COLOR_BGR2RGB), target_size) for img in imgList1]
    #읽어들인 이미지를 RGB 형식으로 변환

# 이미지 파일 읽어들어서 리스트에 저장한다.
images = load_images()

#목표 이미지 이게 결과이다.
goal=images.copy()



# 이미지를 그리는 함수 정의
def draw_images(puzzle):
    for i in range(3):
        for j in range(3):
            plt.subplot(3, 3, i * 3 + j + 1)#3*3의 서브플롯 지정
            plt.gca().axes.xaxis.set_visible(False)#서브플롯의 x축을 숨긴다.
            plt.gca().axes.yaxis.set_visible(False)#서브플롯의 y축을 숨긴다.
            plt.imshow(puzzle[i * 3 + j])#현재 인덱스에 해당하는 이미지를 서브플롯에 표시
    plt.draw()
fig, axes = plt.subplots(3, 3, figsize=(5, 5))#3*3의 틀을 만든다.
#fig는 전체 그림(figure) 객체를, axes는 각각의 서브플롯에 대한 객체 배열을 나타낸다.
# 그림의 크기는 5*5사이즈 


i=4
def shuffle_puzzle():
    global i# i를 함수 내에서 사용할 수 있도록 전역변수로 변경
  
    
    for _ in range(20):#몇번 섞을지 설정
        r = random.randrange(4)#4로 나눈 나머지는(0,1,2,3)이므로 랜덤으로 r변수는 0,1,2,3중 하나의 값을 갖게 된다. 
        
        if r == 0 and (i != 0 and i!=3 and i!= 6):  # Move left i != 0 or i!=3 or i!= 6이면 왼쪽으로 못가니까
            images[i], images[i-1] = images[i-1], images[i]
            i=i-1#한칸 왼쪽으로 갔으니까
           
        elif r == 1 and (i != 2 and i!=5 and i!= 8):  # Move right i != 2 or i!=5 or i!= 8이면 오른쪽으로 못가니까
            images[i], images[i+1] = images[i+1], images[i]
            i=i+1#한칸 오른쪽으로 갔으니까
          
        elif r == 2 and (i != 0 and i!=1 and i!= 2):  # Move up i != 0 or i!=1 or i!= 2이면 위쪽으로 못가니까
            images[i], images[i-3] = images[i-3], images[i]
            i=i-3#한칸 위쪽으로 갔으니까
            
        elif r == 3 and (i != 6 and i!=7 and i!= 8):  # Move right i != 6 or i!=7 or i!= 8이면 아래쪽으로 못가니까
            images[i], images[i+3] = images[i+3], images[i]
            i=i+3#한칸 아래쪽으로 갔으니까
        
            
            
shuffle_puzzle()#images를 섞는다 랜덤으로


draw_images(images)#섞인 이미지를 일단 처음에 띄워놓는다.


cur=images.copy()


oper = ['up', 'down', 'right', 'left']#0 이미지가 움직이는 방향은 4가지이다.(위,아래,왼쪽,오른쪽)

def movePuzzle(puzzle, zero_idx, oper):#현재 퍼즐,0의위치,방향을 매개변수로 가진다.
    puzzle = puzzle.copy()  # 원본 배열을 변경하지 않도록 복사
    if oper == 'up' and zero_idx - 3 >= 0:#윗 방향이고 위로 움직일 수 있을 때
        puzzle[zero_idx], puzzle[zero_idx - 3] = puzzle[zero_idx - 3], puzzle[zero_idx]
        zero_idx -= 3
    elif oper == 'down' and zero_idx + 3 < 9:#아래 방향이고 아래로 움직일 수 있을 때
        puzzle[zero_idx], puzzle[zero_idx + 3] = puzzle[zero_idx + 3], puzzle[zero_idx]
        zero_idx += 3
    elif oper == 'right' and zero_idx % 3 != 2:#오른쪽 방향이고 오른쪽으로 움직일 수 있을 때
        puzzle[zero_idx], puzzle[zero_idx + 1] = puzzle[zero_idx + 1], puzzle[zero_idx]
        zero_idx += 1
    elif oper == 'left' and zero_idx % 3 != 0:#왼쪽 방향이고 왼쪽으로 움직일 수 있을 때
        puzzle[zero_idx], puzzle[zero_idx - 1] = puzzle[zero_idx - 1], puzzle[zero_idx]
        zero_idx -= 1
    return puzzle, zero_idx#바뀐 퍼즐과 0의 위치를 반환한다.

def h(puzzle, goal):
    return sum([1 if not np.array_equal(puzzle[i], goal[i]) else 0 for i in range(len(puzzle))])
    #puzzle의 길이만큼 puzzle[i], goal[i]가 같으면 0을 다르면 1을 리스트에 추가하여 더한다.
    #puzzle과 goal의 다른 위치 개수를 나타낸다.
class Node:
    def __init__(self, data,hval, level,id):#클래스선언
        self.data = data#퍼즐의 상태를 저장
        self.hval = hval#노드가 목표의 상태에 얼마나 가까운지를 나타냄
        self.level = level#노드의 깊이 레벨을 나타냄
        self.id=id#zero_idx의 위치를 업데이트하기 위함
# 평가 함수: 현재 노드의 비용 함수
def f(node, goal):
    return node.level + h(node.data, goal)
#현재 노드의 레벨과 히유리스틱(h)의 값을 더해서 비용을 구한다.

def draw_puzzle(puzzle):
    draw_images(puzzle)
    plt.pause(2) # 각 단계마다 몇초동안 멈출지 설정하는 단계

def astar(puzzle, goal):# 초기 퍼즐 상태를 나타내는 리스트,목표 퍼즐 상태를 나타내는 리스트
    
    visit = []#방문한 노드를 저장하는 리스트
    queue = []#탐색할 노드를 저장하는 우선순위 큐 ('f')값에 따라 정렬된다.
    start = Node(data=puzzle, hval=h(puzzle=puzzle, goal=goal), level=0, id=i)
    # 초기 퍼즐 상태를 나타내는 'node'객체 초기레벨은 0 id는 변경된 0의 위치를 나타낸다.
    queue.append(start)
   
    
    while queue:
        
        current = queue.pop(0)#비용이 적은 순으로 정렬할 것중에 가장 앞에있는것을 호출
        draw_puzzle(current.data)  # 현재 퍼즐 상태를 시각화
        
        
        
        if h(current.data, goal) == 0:# 퍼즐이 goal의 모양과 같아졌을때
            print("Goal reached!")
            return visit
        else:
            visit.append(current.data)#방문한 노드 리스트에 현재 노드의 퍼즐 상태를 추가
            zero_idx=current.id#바뀐 0의 위치를 zero_idx에 대입
            
          

            for op in oper:#가능한 모든 연산을 반복('up','down','right','left')
                
                next_puzzle,id = movePuzzle(current.data, zero_idx, op)#이동연산을 적용하여 새로운 퍼즐 상태를 생성한다.
                
                if next_puzzle and not any(np.array_equal(next_puzzle, visited) for visited in visit):#방문하지 않은 퍼즐상태라면
                    queue.append(Node(next_puzzle, h(next_puzzle,goal), current.level + 1, id))
                    #바뀐 퍼즐, 바뀔 퍼즐과 goal의 히유리스틱 값, 노드의 레벨은 현재 노드에 1더한값,0의 위치를 반환
                          
            queue.sort(key=lambda x: f(x,goal))# ('f')비용이 가장 낮은 노드가 먼저처리되도록 한다.
        
    return -1
print(i)
# 마우스 클릭 이벤트 핸들러
def on_click(event):
    astar(cur, goal)




# 마우스 클릭 이벤트 연결
fig.canvas.mpl_connect('button_press_event', on_click)
plt.subplots_adjust(wspace=0.01, hspace=0.02)
plt.show()