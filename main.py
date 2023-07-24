import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def encontrarRoiPlaca(number, img):
    cinza = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #cv2.imshow("cinza", cinza)

    _, bin = cv2.threshold(cinza, number, 255, cv2.THRESH_BINARY)
    #cv2.imshow("binary", bin)

    desfoque = cv2.GaussianBlur(bin, (5, 5), 0)
    #cv2.imshow("desfoque", desfoque)

    contornos, hierarquia = cv2.findContours(desfoque, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    # cv2.drawContours(img, contornos, -1, (0, 255, 0), 1)

    for c in contornos:
        perimetro = cv2.arcLength(c, True)
        if perimetro > 140 :
            aprox = cv2.approxPolyDP(c, 0.03 * perimetro, True)
            if len(aprox) == 4:
                (x, y, alt, lar) = cv2.boundingRect(c)
                cv2.rectangle(img, (x, y), (x + alt, y + lar), (0, 255, 0), 2)
                roi = img[y:y + lar, x:x + alt]
                cv2.imwrite('data/resultado/roi.png', roi)

    #cv2.imshow("contornos", img)
    


def preProcessamentoRoiPlaca(number):
    img_roi = cv2.imread("data/resultado/roi.png")

    if img_roi is None:
        return

    resize_img_roi = cv2.resize(img_roi, None, fx=4, fy=4, interpolation=cv2.INTER_CUBIC)

    # Converte para escala de cinza
    img_cinza = cv2.cvtColor(resize_img_roi, cv2.COLOR_BGR2GRAY)

    # Binariza imagem
    _, img_binary = cv2.threshold(img_cinza, number, 255, cv2.THRESH_BINARY)

    # Desfoque na Imagem
    img_desfoque = cv2.GaussianBlur(img_binary, (5, 5), 0)

    # Grava o pre-processamento para o OCR
    cv2.imwrite("data/resultado/roi-ocr.png", img_desfoque)

    #cv2.imshow("ROI", img_binary)

    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    return img_desfoque


def ocrImageRoiPlaca(number):
    image = cv2.imread("data/resultado/roi-ocr.png")

    config = r'-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 --psm 6'

    saida = pytesseract.image_to_string(image, lang='eng', config=config)
    if saida == "" or len(saida) <5 or len(saida)>9:
        print(200-number)
        if (200-number) <= 0:
            return "0" 
        #cv2.destroyAllWindows()
        encontrarRoiPlaca(200-number, img)
        pre = preProcessamentoRoiPlaca(200-number)
        saida = ocrImageRoiPlaca(number+5)
    else:
        print(saida)
        try:
            if saida[3] == 0 or saida[3] == 1 or saida[3] == 2 or  saida[3] == 3 or saida[3] == 4 or saida[3] == 5 or saida[3] == 6 or saida[3] == 7 or saida[3] == 8 or saida[3] == 9:
                return saida
            else:
                encontrarRoiPlaca(200-number, img)
                pre = preProcessamentoRoiPlaca(200-number)
                saida = ocrImageRoiPlaca(number+5)
        except:
            encontrarRoiPlaca(200-number, img)
            pre = preProcessamentoRoiPlaca(200-number)
            saida = ocrImageRoiPlaca(number+5)
    return saida


if __name__ == "__main__":
    img = cv2.imread("data/carro3.jpg")
    #cv2.imshow("img", img)

    encontrarRoiPlaca(200, img)

    pre = preProcessamentoRoiPlaca(200)

    ocr = ocrImageRoiPlaca(1)
    print(len(ocr))

    print(ocr)
    cv2.waitKey(0)
    cv2.destroyAllWindows()