# X-RAY-CHATBOT
🛠️ How It Works
This application, EMRChains - Medical AI Assistant, is a web-based medical chatbot built using Streamlit. It allows users to upload medical images (like X-rays, CT scans, or MRIs) and ask questions related to the uploaded image. The app uses an external AI model through an API to analyze the image and provide intelligent medical feedback. Here's how it works step-by-step:

User Interface Design
The app has a modern, dark-themed user interface customized with CSS. It is organized into two columns — one for image upload and one for chatbot interaction. The design is responsive and visually optimized for better user experience.

Image Upload Functionality
Users can upload medical images in JPG, PNG, or DICOM formats. Once uploaded, the image is previewed within the app, and a confirmation message appears.

Session Management
The app uses session state to remember the uploaded image and previous chat messages. This allows a smooth, continuous interaction without data loss during refreshes or interactions.

Chat Interface
A chat section allows the user to type in questions about the medical image, such as asking for a diagnosis or explanation of observed features.

Backend Communication
When a question is submitted, the app packages both the uploaded image and the text query and sends them to a backend AI server through an HTTP POST request. The server processes the image and the question using a medical AI model and returns a relevant response.

Displaying Responses
Once the AI returns a response, the app displays it in the chat area, right below the user’s query. All interactions are stored in the session so the conversation history remains visible.

Error Handling
If no image is uploaded or if there’s a problem with the API response, the app shows appropriate warnings or error messages to guide the user.

This makes EMRChains a simple yet powerful interface that bridges medical imaging and AI-powered diagnostics, enabling users to explore their medical scans in an interactive and informative way.










