<?php
/**
 * Firebase Configuration
 * This file contains Firebase connection settings and utilities.
 */

/**
 * Firebase Web SDK Configuration
 * (Used in JS client, safe for frontend)
 */
$firebaseConfig = [
    'apiKey'            => getenv('FIREBASE_API_KEY') ?: 'your-api-key',
    'authDomain'        => getenv('FIREBASE_AUTH_DOMAIN') ?: getenv('FIREBASE_PROJECT_ID') . '.firebaseapp.com',
    'databaseURL'       => getenv('FIREBASE_DATABASE_URL') ?: '',
    'projectId'         => getenv('FIREBASE_PROJECT_ID') ?: 'your-project-id',
    'storageBucket'     => getenv('FIREBASE_STORAGE_BUCKET') ?: getenv('FIREBASE_PROJECT_ID') . '.appspot.com',
    'messagingSenderId' => getenv('FIREBASE_MESSAGING_SENDER_ID') ?: 'your-messaging-sender-id',
    'appId'             => getenv('FIREBASE_APP_ID') ?: 'your-app-id',
    'measurementId'     => getenv('FIREBASE_MEASUREMENT_ID') ?: null,
];

/**
 * Firebase Admin SDK Service Account Configuration
 * (Used for secure backend operations in PHP)
 */
$serviceAccountConfig = [
    'type'                        => 'service_account',
    'project_id'                 => getenv('FIREBASE_PROJECT_ID'),
    'private_key_id'             => getenv('FIREBASE_PRIVATE_KEY_ID'),
    'private_key'                => str_replace("\\n", "\n", getenv('FIREBASE_PRIVATE_KEY')),
    'client_email'               => getenv('FIREBASE_CLIENT_EMAIL'),
    'client_id'                  => getenv('FIREBASE_CLIENT_ID'),
    'auth_uri'                   => getenv('FIREBASE_AUTH_URI') ?: 'https://accounts.google.com/o/oauth2/auth',
    'token_uri'                  => getenv('FIREBASE_TOKEN_URI') ?: 'https://oauth2.googleapis.com/token',
    'auth_provider_x509_cert_url' => getenv('FIREBASE_AUTH_PROVIDER_X509_CERT_URL') ?: 'https://www.googleapis.com/oauth2/v1/certs',
    'client_x509_cert_url'       => getenv('FIREBASE_CLIENT_X509_CERT_URL'),
    'universe_domain'            => getenv('FIREBASE_UNIVERSE_DOMAIN') ?: 'googleapis.com',
];

/**
 * Return Firebase client config as JSON
 */
function getFirebaseClientConfig()
{
    global $firebaseConfig;
    return json_encode($firebaseConfig, JSON_UNESCAPED_SLASHES | JSON_PRETTY_PRINT);
}

/**
 * Return Firebase Admin SDK service account credentials
 */
function getServiceAccountConfig()
{
    global $serviceAccountConfig;
    return $serviceAccountConfig;
}

/**
 * Output Firebase SDK initialization script for frontend
 */
function getFirebaseScript()
{
    global $firebaseConfig;
    return "
    <!-- Firebase SDK -->
    <script src='https://www.gstatic.com/firebasejs/10.7.1/firebase-app-compat.js'></script>
    <script src='https://www.gstatic.com/firebasejs/10.7.1/firebase-auth-compat.js'></script>
    <script src='https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore-compat.js'></script>

    <script>
      const firebaseConfig = " . json_encode($firebaseConfig) . ";

      // Initialize Firebase
      firebase.initializeApp(firebaseConfig);
      const auth = firebase.auth();
      const db = firebase.firestore();

      // Google Sign-In
      const provider = new firebase.auth.GoogleAuthProvider();
      provider.addScope('email');
      provider.addScope('profile');
    </script>
    ";
}
?>
