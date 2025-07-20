<?php
/**
 * Firebase Configuration
 * This file contains Firebase connection settings and utilities
 */

/**
 * Firebase configuration
 * Replace with your actual Firebase project configuration
 */
$firebaseConfig = [
    'apiKey' => $_ENV['FIREBASE_API_KEY'] ?? 'your-api-key',
    'authDomain' => $_ENV['FIREBASE_PROJECT_ID'] . '.firebaseapp.com' ?? 'your-project.firebaseapp.com',
    'projectId' => $_ENV['FIREBASE_PROJECT_ID'] ?? 'your-project-id',
    'storageBucket' => $_ENV['FIREBASE_PROJECT_ID'] . '.appspot.com' ?? 'your-project.appspot.com',
    'messagingSenderId' => $_ENV['FIREBASE_SENDER_ID'] ?? 'your-sender-id',
    'appId' => $_ENV['FIREBASE_APP_ID'] ?? 'your-app-id'
];

/**
 * Service Account Configuration for Admin SDK
 */
$serviceAccountConfig = [
    'type' => 'service_account',
    'project_id' => $_ENV['FIREBASE_PROJECT_ID'] ?? 'your-project-id',
    'private_key_id' => $_ENV['FIREBASE_PRIVATE_KEY_ID'] ?? 'your-private-key-id',
    'private_key' => $_ENV['FIREBASE_PRIVATE_KEY'] ?? 'your-private-key',
    'client_email' => $_ENV['FIREBASE_CLIENT_EMAIL'] ?? 'your-client-email',
    'client_id' => $_ENV['FIREBASE_CLIENT_ID'] ?? 'your-client-id',
    'auth_uri' => 'https://accounts.google.com/o/oauth2/auth',
    'token_uri' => 'https://oauth2.googleapis.com/token',
    'auth_provider_x509_cert_url' => 'https://www.googleapis.com/oauth2/v1/certs',
    'client_x509_cert_url' => $_ENV['FIREBASE_CLIENT_CERT_URL'] ?? 'your-cert-url'
];

/**
 * Get Firebase client configuration as JSON
 */
function getFirebaseClientConfig() {
    global $firebaseConfig;
    return json_encode($firebaseConfig);
}

/**
 * Get Firebase service account configuration
 */
function getServiceAccountConfig() {
    global $serviceAccountConfig;
    return $serviceAccountConfig;
}

/**
 * Firebase Web SDK JavaScript
 */
function getFirebaseScript() {
    global $firebaseConfig;
    return "
    <!-- Firebase SDK -->
    <script src='https://www.gstatic.com/firebasejs/10.7.1/firebase-app-compat.js'></script>
    <script src='https://www.gstatic.com/firebasejs/10.7.1/firebase-auth-compat.js'></script>
    <script src='https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore-compat.js'></script>
    
    <script>
    // Firebase configuration
    const firebaseConfig = " . json_encode($firebaseConfig) . ";
    
    // Initialize Firebase
    firebase.initializeApp(firebaseConfig);
    const auth = firebase.auth();
    const db = firebase.firestore();
    
    // Google Sign-In provider
    const provider = new firebase.auth.GoogleAuthProvider();
    provider.addScope('email');
    provider.addScope('profile');
    </script>
    ";
}
?>