# AdTech React Consumer

This React application fetches ad data from a backend service (an API that aggregates and returns ads based on user actions). The backend is powered by a simulated Kafka event stream and MongoDB to store and retrieve relevant ads. When you refresh the page or click the **Get Another Ad** button, the app makes a request for a random user ID to demonstrate how ads might be personalized based on user behavior.

## Key Features

1. **Random User Selection**  
   - Picks a user ID between 1 and 10.

2. **API Integration**  
   - Sends a GET request to `https://<YOUR_API_URL>/ad` with the user ID as a query parameter.
   - Displays the response, including:
     - User ID
     - User Action (e.g., `click`, `page_view`, `purchase`)
     - Title of the ad
     - Ad Image

3. **Interactive UI**  
   - Provides a **Get Another Ad** button to request fresh ad data without reloading the entire page.

4. **Full Stack Concept**  
   - Illustrates how Kafka, MongoDB, and a Node/Express API could work together with a React front-end.

## Requirements

- **Node.js** (version 14 or above recommended)
- **npm** (or Yarn) for managing dependencies

## Getting Started

1. **Clone or Download**  
   - Copy this repository or download it as a ZIP.

2. **Install Dependencies**  
   ```bash
   npm install
   ```
   This will install React, axios, and other required packages.

3. **Run the Development Server**  
   ```bash
   npm start
   ```
   - By default, this starts the app at `http://localhost:3000/`.

4. **Open the App**  
   - Visit `http://localhost:3000` in your browser.
   - You’ll see the home page with a “Dynamic Ad Display” header.

## Configuration

- **API Endpoint**  
  - The script currently points to `https://<YOUR_API_URL>/ad`.  
  - If you need to change the endpoint, update the `axios.get()` call in `App.js`.  
  - You can also store this URL in an environment variable (e.g., using `.env` in a real project) if you need more flexibility.

## Usage

- **On page load**, the app automatically requests an ad for a random user ID (between 1 and 10).  
- **Click the “Get Another Ad” button** to see a new ad.  
- **Check console logs** (in your browser’s DevTools) to see the raw JSON response from the server.

## Project Structure

- **`App.js`**  
  - The primary component that manages state (current ad), makes an API request via `axios`, and renders the UI.
- **`App.css`**  
  - Contains basic styling for the page, including layout and classes for the ad details.

## Deployment

- **Production Build**  
  ```bash
  npm run build
  ```
  This command creates an optimized build in the `build/` folder, ready for deployment to static hosting or integration with a server.

- **Kubernetes or Other Orchestration**  
  - Wrap the build output in a Docker image or host it on a static server, then configure your platform (e.g., Kubernetes Deployment or Helm chart) to serve the React files.
  - Make sure the API endpoint is accessible from within your environment.

## Troubleshooting

- **API Access Errors**: Confirm the endpoint (`https://<YOUR_API_URL>/ad`) is reachable from your environment and that CORS settings permit requests from your React app.
- **Blank Screen**: Ensure Node modules are installed properly (`npm install`) and there are no console errors.
- **Random Data**: If you’re always getting the same ad or unexpected results, verify that the backend logic is correctly handling multiple user IDs/events.

## License

This project is provided as-is for demonstration purposes. Feel free to adapt or extend it as needed for your own solutions.
