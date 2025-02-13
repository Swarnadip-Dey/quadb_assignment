# quadb_assignment
# Blockchain Visualizer

This project provides a simple blockchain visualizer with the ability to add transactions and view the blockchain.  It includes backend (Flask) and frontend (React) components.  POW is used and A built-in tampering mechanism is included for demonstration purposes.

## Prerequisites

*   **Docker and Docker Compose:**  Recommended for ease of setup and consistency. [Install Docker](https://docs.docker.com/get-docker/)
*   **Python 3.6+:** (If running the backend outside of Docker).
*   **Node.js and npm:** (If running the frontend outside of Docker).

## Setup (Using Docker Compose - Recommended)

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/Swarnadip-Dey/quadb_assignment.git
    cd quadb_assignment
    ```

2.  **Build and Run with Docker Compose:**
    ```bash
    docker-compose up --build
    ```

    This command builds the Docker images for both the frontend and backend, and then starts the containers.

3.  **Access the Application:**

    *   Frontend: Open your web browser and go to `http://localhost:3000`.

## Setup (Manual - Without Docker)

2.  **Backend Setup:**

    *   Navigate to the `backend` directory: `cd backend`
    *   Create a virtual environment (recommended): `python3 -m venv venv`
    *   Activate the virtual environment: `source venv/bin/activate` (Linux/macOS) or `venv\Scripts\activate` (Windows)
    *   Install dependencies: `pip install Flask Flask-CORS requests`
    *   Run the backend: `flask run --host=0.0.0.0 --port=5000`

3.  **Frontend Setup:**

    *   Navigate to the `frontend` directory: `cd ../frontend`
    *   Install dependencies: `npm install`
    *   Start the frontend: `npm start`

    This will usually open the frontend in your browser at `http://localhost:3000`.

## Usage

1.  **Add Transactions:**

    *   Navigate to the "Add Transactions" tab.
    *   Enter one or more transaction strings in the input fields.
    *   Click "Add Transactions" to submit them.  These transactions will be added to the database and mined into the next block.

2.  **Visualize Blockchain:**

    *   Navigate to the "Visualize Blockchain" tab.
    *   The blockchain data will be fetched from the backend and displayed.  You'll see the blocks with their index, timestamp, previous hash, hash, nonce, and transactions.

## Tampering with the Blockchain

**WARNING:** Tampering with the blockchain will invalidate it and, if running outside of Docker, will shut down the backend server.

1.  **Tamper Endpoint:**

    The backend provides a secret endpoint for tampering with a specific block:

    ```
    POST http://localhost:5000/tamper-secret/<block_index>
    ```

    Replace `<block_index>` with the index of the block you want to tamper with (e.g., `1` to tamper with the second block).

2.  **How to Tamper (Example using `curl`):**

    ```bash
    curl -X POST http://localhost:5000/tamper-secret/1
    ```

    You can also use tools like Postman to send the POST request.  No request body is needed.

3.  **Observable Effects:**

    *   After tampering, refresh the "Visualize Blockchain" tab in the frontend will freeze
    *   The backend server will likely shut down due to the blockchain validation failing (if running outside Docker).
