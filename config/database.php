<?php
/**
 * Database Configuration
 * This file contains database connection settings for different environments
 */

// Environment detection
$environment = $_ENV['APP_ENV'] ?? 'production';

// Database configurations for different environments
$config = [
    'development' => [
        'host' => 'localhost',
        'dbname' => 'apniholidays_dev',
        'username' => 'root',
        'password' => '',
        'charset' => 'utf8mb4',
        'options' => [
            PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
            PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
            PDO::ATTR_EMULATE_PREPARES => false,
        ]
    ],
    'production' => [
        'host' => $_ENV['DB_HOST'] ?? 'localhost',
        'dbname' => $_ENV['DB_NAME'] ?? 'apniholidays',
        'username' => $_ENV['DB_USER'] ?? 'username',
        'password' => $_ENV['DB_PASS'] ?? 'password',
        'charset' => 'utf8mb4',
        'options' => [
            PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
            PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
            PDO::ATTR_EMULATE_PREPARES => false,
        ]
    ]
];

// Get current environment config
$dbConfig = $config[$environment] ?? $config['production'];

/**
 * Create database connection
 */
function getDbConnection() {
    global $dbConfig;
    
    try {
        $dsn = "mysql:host={$dbConfig['host']};dbname={$dbConfig['dbname']};charset={$dbConfig['charset']}";
        $pdo = new PDO($dsn, $dbConfig['username'], $dbConfig['password'], $dbConfig['options']);
        return $pdo;
    } catch (PDOException $e) {
        error_log("Database connection failed: " . $e->getMessage());
        throw new Exception("Database connection failed. Please try again later.");
    }
}

/**
 * Test database connection
 */
function testDbConnection() {
    try {
        $pdo = getDbConnection();
        $stmt = $pdo->query("SELECT 1");
        return true;
    } catch (Exception $e) {
        return false;
    }
}
?>