from ultralytics import YOLO


def main():
    model = YOLO("yolov8n-seg.pt")

    model.train(
        data="training/dataset.yaml",
        imgsz=640,
        epochs=50,
        batch=8,
        patience=10,
        project="runs/infra_defect_seg",
        name="yolov8n_seg_baseline"
    )


if __name__ == "__main__":
    main()