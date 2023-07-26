import cv2
import pytesseract
import imutils
import numpy as np

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def encontrarRoiPlaca(img):
    imgWindow("Original", img)
    img = imutils.resize(img, height=500)
    imgWindow("Recorte", img)

    #Filtro Cinza
    cinza = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgWindow("Filtro1", cinza)

    #Filtro Desfoque
    desfoque = cv2.GaussianBlur(cinza, (5,5),0)
    imgWindow("Filtro2", desfoque)

    #Filtro Canny
    edged = cv2.Canny(desfoque, 75,200)
    imgWindow("Filtro3", edged)

    #Contornar
    screenCnt = contourPlate(edged)

    #Mascarar imagem
    mask = np.zeros(desfoque.shape, np.uint8)
    new_image = cv2.drawContours(mask, [screenCnt], 0,255,-1,)
    new_image = cv2.bitwise_and(img, img, mask=mask)

    imgWindow("PRE-ROI", new_image)

    #Recorte ROI
    (x,y) = np.where(mask == 255)
    (topx,topy) = (np.min(x), np.min(y))
    (bottomx, bottomy) = (np.max(x), np.max(y))
    cropped = edged[topx:bottomx+1, topy:bottomy+1]

    imgWindow("ROI", cropped)

    config = r'-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 --psm 11'

    saida = pytesseract.image_to_string(cropped, lang='eng', config=config)
    saida = subRegex(saida)
            
    print("Placa:" +saida)

    
def imgWindow(string, img):
    cv2.imshow(string, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def contourPlate(edged):
    contorno = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contorno = imutils.grab_contours(contorno)
    contorno = sorted(contorno, key = cv2.contourArea, reverse = True)[:10]
    screenCnt = None
    for c in contorno:
        perimetro = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.018 * perimetro, True)
        if len(approx) == 4:
            screenCnt = approx
            break
    if screenCnt is None:
        detected = 0
        print("Sem contorno detectado")
        return
    else:
        detected = 1
    if detected == 1:
        cv2.drawContours(img, [screenCnt], -1,(0,0,255),3)
    return screenCnt

def isNumber(value):
    try:
         float(value)
    except ValueError:
         return False
    return True

def subRegex(saida):
    saidaC = list(saida)
    count = 0
    for n in range(len(saida)):
        if (isNumber(saida[n])== True):
            if (n == 0 or n == 1 or n == 2 or n == 4):
                if(saida[n] == "4"):
                    saidaC[n] = "G"
        else:
            if(n == 3 or n == 5 or n == 6):
                if(saida[n] == "S"):
                    if(count == 0):
                        saidaC[n] = "3"
                        count = 1
                    else:
                        saidaC[n] = "5"
                if(saida[n] == "A"):
                    saidaC[n] = "1"
                if(saida[n] == "D"):
                    saidaC[n] = "9"
                if(saida[n] == "G"):
                    saidaC[n] = "4"
                if(saida[n] == "Z"):
                    saidaC[n] = "2"
    saida = saidaC[0]+saidaC[1]+saidaC[2]+saidaC[3]+saidaC[4]+saidaC[5]+saidaC[6]
    return saida
if __name__ == "__main__":
    #img = cv2.imread("data/carro1.jpg")
    #img = cv2.imread("data/carro2.jpg")
    #img = cv2.imread("data/carro3.jpg")
    #img = cv2.imread("data/carro4.jpg")

    encontrarRoiPlaca(img)