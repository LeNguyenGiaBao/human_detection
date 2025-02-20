import cv2
from constants import MODEL_PATH, PERSON_CLASS_INDEX, THRESHOLD_DETECT


def detect(model, image):
    results = model(image)
    num_person = 0

    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = box.conf[0].item()
            cls = int(box.cls[0].item())
            if cls == PERSON_CLASS_INDEX and conf > THRESHOLD_DETECT:
                num_person += 1
                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(
                    image,
                    f"Person {conf:.2f}",
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 255, 0),
                    2,
                )
    return image, num_person


if __name__ == "__main__":
    from ultralytics import YOLO

    model = YOLO(MODEL_PATH)

    image_path = "./test_data/images/img_3.jpg"
    image = cv2.imread(image_path)
    result, count_person = detect(model, image)
    cv2.imwrite("./test_data/result_images/result.jpg", result)
