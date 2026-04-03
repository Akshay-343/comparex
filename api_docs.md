# CompareX API Documentation

This document outlines the backend API endpoints available for the frontend to interact with the reconciliation engine.

**Base Path:** `/api`
(e.g., if the server is running on `http://localhost:8000`, endpoints are relative to `http://localhost:8000/api`)

---

## 1. Get Available Configurations
Retrieves a list of available YAML configuration names. Use this to populate a configuration dropdown on the frontend.

- **Endpoint:** `/configs`
- **Method:** `GET`
- **Response Format:** `application/json`
- **Success Response Examples:**
  - **Code:** `200 OK`
  - **Body:**
    ```json
    {
      "configs": [
        "fimmda_slv",
        "fortnightly"
      ]
    }
    ```

---

## 2. Run Reconciliation
Uploads two Excel files alongside a selected configuration to process the reconciliation.

- **Endpoint:** `/reconcile`
- **Method:** `POST`
- **Content-Type:** `multipart/form-data`
- **Form Parameters:**
  - `file_a` (File): The first/left Excel file.
  - `file_b` (File): The second/right Excel file.
  - `config_name` (Text): The configuration name selected from the `/configs` list (e.g., `fimmda_slv`).
- **Success Response Examples:**
  - **Code:** `200 OK`
  - **Body:**
    ```json
    {
      "status": "success",
      "run_id": "20240401_191500_123456",
      "rows": 45,
      "download_url": "/api/download/20240401_191500_123456"
    }
    ```
- **Error Response Examples:**
  - **Code:** `500 Internal Server Error`
  - **Body:**
    ```json
    {
      "status": "error",
      "message": "Specific error explanation"
    }
    ```

---

## 3. Download Report
Downloads the generated reconciliation `.xlsx` report using the `run_id`.

- **Endpoint:** `/download/{run_id}`
- **Method:** `GET`
- **URL Parameters:**
  - `run_id`: The unique execution ID returned by the `/reconcile` endpoint.
- **Success Response Examples:**
  - **Code:** `200 OK`
  - **Response:** The Excel file binary stream with appropriate `Content-Disposition` headers to prompt a file download.
- **Error Response Examples:**
  - **Code:** `404 Not Found`
  - **Body:**
    ```json
    {
      "status": "error",
      "message": "Report not found"
    }
    ```
