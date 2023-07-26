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
    imgWindows("Filtro2", desfoque)

    #Filtro Canny
    edged = cv2.Canny(desfoque, 75,200)
    imgWindows("Filtro3", edged)

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


if __name__ == "__main__":
    img = cv2.imread("data/carro1.jpg")
    #img = cv2.imread("data/carro2.jpg")
    #img = cv2.imread("data/carro3.jpg")
    #img = cv2.imread("data/carro4.jpg")

    encontrarRoiPlaca(img)
    print(len(ocr))
    print(ocr)
    cv2.waitKey(0)
    cv2.destroyAllWindows()