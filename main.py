import pytesseract
import pyautogui
import ctypes
import time
import random
import cv2
from PIL import Image
import keyboard
import traceback
from threading import Thread



WORKING = True
pytesseract.pytesseract.tesseract_cmd = r'Tesseract-OCR/tesseract.exe'
custom_config = r'-l rus --oem 3 --psm 6'
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
WM_LBUTTONDOWN = 0x0201
WM_LBUTTONUP = 0x0202
WM_KEYUP = 0x0100
BACKSPACE_VIRTUAL_CODE = 0x08
window_handle = ctypes.windll.user32.FindWindowW(None, 'STALCRAFT')


def testScroll():

    pagesQ = pagesQuantity()
    for page in range(pagesQ):
        page += 1
        if page != 1:
            pagesNavigation(page)
        stage = 0
        while stage <= 4:
            currentBalanace = getCurrentBalance()
            if WORKING:
                scroll(stage)
                match = searchOnPage(65500)
                if match:
                    buy()
                    match = False
                else:
                    stage += 1
                    
def imageRecognition(Simage, Limage):
    method = cv2.TM_SQDIFF_NORMED

    small_image = cv2.imread(Simage)
    large_image = cv2.imread(Limage)

    result = cv2.matchTemplate(small_image, large_image, method)

    mn, _, mnLoc, _ = cv2.minMaxLoc(result)

    MPx, MPy = mnLoc

    return MPx, MPy

def pagesQuantity():
    pyautogui.screenshot('screenshots/screenshot.jpeg')

    pageX, pageY = imageRecognition('blueprints/balanceRecognition.png', 'screenshots/screenshot.jpeg')
    pageX -= 250
    pageY -= 39
    pyautogui.screenshot('screenshots/pages.jpg', region=(pageX, pageY, 308, 18))

    pagesQ = pytesseract.image_to_string(Image.open(f'screenshots/pages.jpg'), config=custom_config)

    if "@>" in pagesQ:
        print('сработала страница 2')
        return 2

    pagesQ = "".join(c for c in pagesQ if c.isdecimal())
    print(len(pagesQ))


    if len(pagesQ) == 0:
        print('страница только одна')
        return 1
    if len(pagesQ) <= 5:
        return int(pagesQ[-1])
    if len(pagesQ) > 5:
        return 5
        #int('1'+pagesQ[-1])



def initAuction():
    ctypes.windll.user32.SendMessageW(window_handle, 0x0100, 0x50, 0)
    time.sleep(0.2)
    pyautogui.screenshot('screenshots/screenshot.jpeg')

    aucX, aucY = imageRecognition('blueprints/auctionRecognition.png', 'screenshots/screenshot.jpeg')
    print(aucX, aucY)
    pyautogui.moveTo(random.randint(aucX+30, aucX+50), random.randint(aucY+3, aucY+10), random.uniform(0.2, 0.4))
    click()
    pyautogui.screenshot('screenshots/screenshot.jpeg')

    buyX, buyY = imageRecognition('blueprints/buyoutRecognition.png', 'screenshots/screenshot.jpeg')
    pyautogui.moveTo(random.randint(buyX+3, buyX+20), random.randint(buyY+5, buyY+10), random.uniform(0.2, 0.4))
    click()
    time.sleep(random.uniform(0.2, 0.4))
    click()


def click():
    ctypes.windll.user32.SendMessageW(window_handle, WM_LBUTTONDOWN, MOUSEEVENTF_LEFTDOWN, 0)
    time.sleep(random.uniform(0.2, 0.4))
    ctypes.windll.user32.SendMessageW(window_handle, WM_LBUTTONUP, MOUSEEVENTF_LEFTUP, 0)


def getCurrentBalance():
    pyautogui.screenshot('screenshots/screenshot.jpeg')

    balanceX, balanceY = imageRecognition('blueprints/balanceRecognition.png', 'screenshots/screenshot.jpeg')

    pyautogui.screenshot('screenshots/currentBalance.jpeg', region=(balanceX, balanceY, 221, 29))
    balanceImg = pytesseract.image_to_string(Image.open('screenshots/currentBalance.jpeg'), config=custom_config)
    balance = "".join(c for c in balanceImg if c.isdecimal())
    if balance == '':
        balance += '1'

    if balance[0] == '0':
        balance == '1'
    return int(balance)


def searchOnPage(desiredPrice,itemName):
    pyautogui.screenshot('screenshots/screenshot.jpeg')

    amountX, amountY = imageRecognition('blueprints/amountRecognition.png', 'screenshots/screenshot.jpeg')
    priceX, priceY = imageRecognition('blueprints/buyoutRecognition.png', 'screenshots/screenshot.jpeg')

    amountX -= 10
    priceX -=18
    priceY -=22

    STEP_FOR_AMOUNT = 37
    STEP_FOR_PRICE = 37

    for i in range(9):
        pyautogui.screenshot(f'screenshots/amount{i}.jpeg', region=(amountX, (amountY + (STEP_FOR_AMOUNT * (i + 1))), 20, 16))
        pyautogui.screenshot(f'screenshots/buyoutprice{i}.jpeg', region=(priceX, (priceY + (STEP_FOR_PRICE * (i + 1))), 120, 37))

        amount = pytesseract.image_to_string(Image.open(f'screenshots/amount{i}.jpeg'), config=custom_config)
        price = pytesseract.image_to_string(Image.open(f'screenshots/buyoutprice{i}.jpeg'), config=custom_config)

        filteredAmount = "".join(c for c in amount if c.isdecimal())
        filteredPrice = "".join(c for c in price if c.isdecimal())
        print('Ищу цены')
        if filteredAmount == '':
            filteredAmount += '1'

        if filteredAmount[0] == '0':
            filteredAmount = '1'

        if filteredPrice:
            threshold = desiredPrice * 0.70
            coeff = (int(filteredPrice) / int(filteredAmount))
            if desiredPrice >= coeff and threshold <= coeff:
                cursorX1 = priceX+4
                cursorX2 = priceX+60
                cursorY1 = (priceY + (STEP_FOR_PRICE * (i + 1)))+8
                cursorY2 = (priceY + (STEP_FOR_PRICE * (i + 1)))+20
                pyautogui.moveTo(random.randint(cursorX1, cursorX2), random.randint(cursorY1, cursorY2), random.uniform(0.2, 0.4))
                click()
                return True

    return False

def pagesNavigation(page):
    pyautogui.screenshot('screenshots/screenshot.jpeg')
    print('Листаю страницы')
    pageX, pageY = imageRecognition('blueprints/balanceRecognition.png', 'screenshots/screenshot.jpeg')
    pageX -= 256
    pageY -= 39
    pyautogui.screenshot('screenshots/pages.jpg', region=(pageX, pageY, 308, 18))

    method = cv2.TM_SQDIFF_NORMED

    small_image = cv2.imread(f'blueprints/page{page}.png')
    large_image = cv2.imread('screenshots/pages.jpg')

    result = cv2.matchTemplate(small_image, large_image, method)

    mn, _, mnLoc, _ = cv2.minMaxLoc(result)

    MPx, MPy = mnLoc

    x = pageX + MPx + random.randint(1,4)
    y = pageY + MPy + random.randint(1,4)

    pyautogui.moveTo(x, y, random.uniform(0.2, 0.4))
    click()


def buy():
    pyautogui.screenshot('screenshots/screenshot.jpeg')

    X, Y = imageRecognition('blueprints/buyRecognition.png', 'screenshots/screenshot.jpeg')

    buyX = random.randint(X+2,X+60)
    buyY = random.randint(Y,Y+10)

    pyautogui.moveTo(buyX, buyY, random.uniform(0.2, 0.4))

    click()

    pyautogui.screenshot('screenshots/screenshot.jpeg')

    X, Y = imageRecognition('blueprints/confirmRecognition.png', 'screenshots/screenshot.jpeg')

    confirmX = random.randint(X + 2, X + 60)
    confirmY = random.randint(Y, Y + 10)

    pyautogui.moveTo(confirmX, confirmY, random.uniform(0.2, 0.4))

    click()


def searchClick():
    pyautogui.screenshot('screenshots/screenshot.jpeg')

    X, Y = imageRecognition('blueprints/searchRecognition.png', 'screenshots/screenshot.jpeg')

    x = random.randint((X + 3), (X + 40))
    y = random.randint((Y + 4), (Y + 13))

    pyautogui.moveTo(x, y, random.uniform(0.2, 0.4))

    click()


def search(require):
    pyautogui.screenshot('screenshots/screenshot.jpeg')
    print("Ищу товар")
    X, Y = imageRecognition('blueprints/searchRecognition.png', 'screenshots/screenshot.jpeg')
    x = random.randint((X-17), (X-11))
    y = random.randint((Y+2), (Y+13))

    pyautogui.moveTo(x, y, random.uniform(0.2, 0.4))

    click()

    for i in range(random.randint(40, 55)):
        ctypes.windll.user32.SendMessageW(window_handle, WM_KEYUP, BACKSPACE_VIRTUAL_CODE, 0)
        time.sleep(random.uniform(0.1, 0.2))

    for i in require:
        unicodeSymbol = ord(i)
        ctypes.windll.user32.SendMessageW(window_handle, 0x0102, unicodeSymbol, 0)
        time.sleep(random.uniform(0.3, 0.6))
    searchClick()

def scroll(stage):
    pyautogui.screenshot('screenshots/screenshot.jpeg')
    print(f'Скролю на позицию: {stage}')
    ScrollBarX, ScrollBarY = imageRecognition('blueprints/scrollRecognition.png', 'screenshots/screenshot.jpeg')
    startScrollX, startScrollY = imageRecognition('blueprints/searchRecognition.png', 'screenshots/screenshot.jpeg')

    startScrollX += 82
    startScrollY += 14

    scrollX1 = 4+ScrollBarX
    scrollX2 = 8+ScrollBarX
    scrollY1 = 10+ScrollBarY
    scrollY2 = 30+ScrollBarY

    step = 90

    pyautogui.moveTo(scrollX2,scrollY2, random.uniform(0.2, 0.4))

    ctypes.windll.user32.SendMessageW(window_handle, WM_LBUTTONDOWN, MOUSEEVENTF_LEFTDOWN, 0)

    match stage:
        case 0:
            pyautogui.moveTo(startScrollX, startScrollY-(step*(stage+1)), random.uniform(0.2, 0.4))
        case 1:
            pyautogui.moveTo(startScrollX, startScrollY+step, random.uniform(0.2, 0.4))
        case 2:
            pyautogui.moveTo(startScrollX, startScrollY+(step*2), random.uniform(0.2, 0.4))
        case 3:
            pyautogui.moveTo(startScrollX, startScrollY+(step*3), random.uniform(0.2, 0.4))
        case 4:
            pyautogui.moveTo(startScrollX, startScrollY + (step * 4), random.uniform(0.2, 0.4))

    ctypes.windll.user32.SendMessageW(window_handle, WM_LBUTTONUP, MOUSEEVENTF_LEFTUP, 0)

def scrollOLD(stage):
    pyautogui.screenshot('screenshots/screenshot.jpeg')

    startScrollX, startScrollY = imageRecognition('blueprints/scrollRecognition.png', 'screenshots/screenshot.jpeg')
    scrollX1 = 4+startScrollX
    scrollX2 = 8+startScrollX
    scrollY1 = 10+startScrollY
    scrollY2 = 30+startScrollY

    y = random.randint(scrollY1, scrollY2)
    step = 90
    if stage != 0:
        pyautogui.moveTo(random.randint(scrollX1, scrollX2), y, random.uniform(0.2, 0.4))

        ctypes.windll.user32.SendMessageW(window_handle, WM_LBUTTONDOWN, MOUSEEVENTF_LEFTDOWN, 0)

        pyautogui.moveTo(random.randint(scrollX1, scrollX2), y + (step), random.uniform(0.2, 0.4))

        ctypes.windll.user32.SendMessageW(window_handle, WM_LBUTTONUP, MOUSEEVENTF_LEFTUP, 0)


def exit_check():
    global WORKING
    while WORKING:
        if keyboard.is_pressed("esc"):
            WORKING = False


thread1 = Thread(target=exit_check)


def main():
    global WORKING

    requestsArr = []
    requestsAmount = int(input('Введите кол-во искомых айтемов: '))
    lowestDesiredPrice = 9000000000
    for i in range(requestsAmount):
        itemName = input('Введите название искомого айтема: ')
        desiredPrice = int(input(f'Введите максимальную цену выкупа для "{itemName}": '))
        if desiredPrice < lowestDesiredPrice:
            lowestDesiredPrice = desiredPrice
        requestsArr.append([itemName, desiredPrice])

    initAuction()
    while WORKING:
        for item in requestsArr:
            if not WORKING:
                print('выход из цикла')
                break
            search(item[0])
            pagesQ = pagesQuantity()
            for page in range(pagesQ):
                if not WORKING:
                    print('выход из цикла')
                    break
                page += 1
                if page != 1:
                    pagesNavigation(page)
                stage = 0
                while stage < 5:
                    currentBalanace = getCurrentBalance()
                    if currentBalanace < lowestDesiredPrice:
                        print('недостаточно средств')
                        WORKING = False
                    if not WORKING:
                        break
                    scroll(stage)
                    match = searchOnPage(item[1],item[0])
                    if not WORKING:
                        break
                    if match:
                        buy()
                        match = False
                    else:
                        stage += 1


main()
