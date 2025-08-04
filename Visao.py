import cv2 


cap = cv2.VideoCapture(0)


face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')


if face_cascade.empty():
    print("Erro: Não foi possível carregar o classificador de face. Verifique o caminho do arquivo 'haarcascade_frontalface_default.xml'.")
    exit()
if eye_cascade.empty():
    print("Erro: Não foi possível carregar o classificador de olhos. Verifique o caminho do arquivo 'haarcascade_eye.xml'.")
    exit()

while True:
    
    ret, video = cap.read()
    if not ret:
        print("Erro: Não foi possível ler o frame da câmera.")
        break

   
    gray = cv2.cvtColor(video, cv2.COLOR_BGR2GRAY)

    
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
       
        cv2.rectangle(video, (x, y), (x+w, y+h), (255, 0, 0), 2) 

    
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = video[y:y+h, x:x+w]

       
        eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 3)
        for (ex, ey, ew, eh) in eyes:
          
            cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2) 

        
        print(f"Centro da Face: (X={int(x + w/2)}, Y={int(y + h/2)})")

  
    cv2.imshow('Reconhecimento Facial e de Olhos', video)
    
    
    key = cv2.waitKey(1) & 0xFF
    if key == 27:
        break


cap.release()
cv2.destroyAllWindows()