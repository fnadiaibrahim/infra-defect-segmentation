from ultralytics import YOLO


def main():
    model = YOLO("weights/best.pt")

    metrics = model.val(
        data="training/dataset.yaml",
        split="test",
        imgsz=640,
        conf=0.25,
        iou=0.45
    )

    print(metrics)


if __name__ == "__main__":
    main()