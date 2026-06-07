import { useState } from "react";
import axios from "axios";
import "./App.css";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [result, setResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  const handleFileChange = (event) => {
    const file = event.target.files[0];

    setResult(null);
    setErrorMessage("");

    if (!file) return;

    if (!["image/jpeg", "image/png"].includes(file.type)) {
      setErrorMessage("Please upload a JPEG or PNG image.");
      return;
    }

    setSelectedFile(file);
    setPreviewUrl(URL.createObjectURL(file));
  };

  const handlePredict = async () => {
    if (!selectedFile) {
      setErrorMessage("Please select an image first.");
      return;
    }

    setIsLoading(true);
    setErrorMessage("");
    setResult(null);

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const response = await axios.post(`${API_BASE_URL}/predict`, formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      if (response.data.error) {
        setErrorMessage(response.data.error);
      } else {
        setResult(response.data);
      }
    } catch (error) {
      setErrorMessage(
        "Prediction request failed. Please check if the backend server is running."
      );
      console.error(error);
    } finally {
      setIsLoading(false);
    }
  };

  const overlayImageUrl = result
    ? `data:image/jpeg;base64,${result.overlay_image}`
    : null;

  return (
    <main className="app-container">
      <section className="hero">
        <div>
          <p className="eyebrow">Computer Vision Prototype</p>
          <h1>Infrastructure Defect Segmentation</h1>
          <p className="subtitle">
            Upload a concrete or infrastructure image to detect pixel-level defects
            such as cracks and spalling using a fine-tuned YOLOv8 segmentation model.
          </p>
        </div>
      </section>

      <section className="card upload-card">
        <h2>Upload Image</h2>
        <p className="helper-text">Supported formats: JPEG and PNG</p>

        <input
          className="file-input"
          type="file"
          accept="image/jpeg,image/png"
          onChange={handleFileChange}
        />

        <button
          className="predict-button"
          onClick={handlePredict}
          disabled={isLoading}
        >
          {isLoading ? "Running segmentation..." : "Run Prediction"}
        </button>

        {errorMessage && <p className="error-message">{errorMessage}</p>}
      </section>

      <section className="results-grid">
        <div className="card image-card">
          <h2>Original Image</h2>
          {previewUrl ? (
            <img src={previewUrl} alt="Original upload" />
          ) : (
            <div className="placeholder">No image selected</div>
          )}
        </div>

        <div className="card image-card">
          <h2>Segmentation Overlay</h2>
          {overlayImageUrl ? (
            <img src={overlayImageUrl} alt="Segmentation overlay" />
          ) : (
            <div className="placeholder">Prediction result will appear here</div>
          )}
        </div>
      </section>

      <section className="card summary-card">
        <h2>Prediction Summary</h2>

        {result ? (
          <>
            <p>
              <strong>Filename:</strong> {result.filename}
            </p>
            <p>
              <strong>Processing time:</strong> {result.processing_time_ms} ms
            </p>

            {result.detections.length > 0 ? (
              <table>
                <thead>
                  <tr>
                    <th>Class</th>
                    <th>Confidence</th>
                    <th>Area %</th>
                  </tr>
                </thead>
                <tbody>
                  {result.detections.map((detection, index) => (
                    <tr key={index}>
                      <td>{detection.class_name}</td>
                      <td>{(detection.confidence * 100).toFixed(2)}%</td>
                      <td>{detection.area_percentage}%</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            ) : (
              <p>No defect detected above the configured confidence threshold.</p>
            )}
          </>
        ) : (
          <p className="helper-text">
            Run prediction to view detected defect classes, confidence scores,
            affected area percentage, and inference time.
          </p>
        )}
      </section>

      <section className="note">
        <strong>Prototype note:</strong> This tool is designed for technical
        assessment and demonstration purposes. It should not be used as the sole
        basis for structural safety decisions.
      </section>
    </main>
  );
}

export default App;