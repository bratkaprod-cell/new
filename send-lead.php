<?php
// Обработчик заявок: письмо на почту + уведомления в Telegram и VK.
// Все контакты/токены настраиваются в lead-config.php.
header('Content-Type: application/json; charset=utf-8');
require __DIR__ . '/lead-config.php';

function respond($ok, $error = '') {
    echo json_encode(['ok' => $ok, 'error' => $error], JSON_UNESCAPED_UNICODE);
    exit;
}

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    http_response_code(405);
    respond(false, 'method');
}

// Honeypot: боты заполняют скрытое поле — молча "принимаем"
if (!empty($_POST['company'])) {
    respond(true);
}

$name  = trim(mb_substr((string)($_POST['name'] ?? ''), 0, 60));
$site  = trim(mb_substr((string)($_POST['site'] ?? ''), 0, 200));
$phone = trim(mb_substr((string)($_POST['phone'] ?? ''), 0, 30));
$cms   = trim(mb_substr((string)($_POST['cms'] ?? ''), 0, 40));
$page  = trim(mb_substr((string)($_POST['page'] ?? ''), 0, 200));

if ($site === '' || $phone === '') {
    respond(false, 'fields');
}
if ($name === '') {
    $name = 'Не указано';
}
$digits = preg_replace('/\D/', '', $phone);
if (strlen($digits) < 10) {
    respond(false, 'phone');
}

// Rate limit по IP (файловый, без БД)
$ip = $_SERVER['REMOTE_ADDR'] ?? '0.0.0.0';
$rlFile = sys_get_temp_dir() . '/leads_' . md5($ip) . '.json';
$now = time();
$hits = [];
if (is_file($rlFile)) {
    $hits = json_decode((string)file_get_contents($rlFile), true) ?: [];
}
$hits = array_values(array_filter($hits, fn($t) => $now - $t < LEAD_RATE_WINDOW));
if (count($hits) >= LEAD_RATE_LIMIT) {
    respond(false, 'rate');
}
$hits[] = $now;
file_put_contents($rlFile, json_encode($hits));

$when = date('d.m.Y H:i');
$lines = [
    "Новая заявка с сайта",
    "Имя: {$name}",
    "Сайт: {$site}",
    "Телефон: {$phone}",
];
if ($cms !== '')  $lines[] = "CMS: {$cms}";
if ($page !== '') $lines[] = "Страница: {$page}";
$lines[] = "IP: {$ip}";
$lines[] = "Время: {$when}";
$text = implode("\n", $lines);

function http_post_json($url, $params) {
    if (function_exists('curl_init')) {
        $ch = curl_init($url);
        curl_setopt_array($ch, [
            CURLOPT_POST => true,
            CURLOPT_POSTFIELDS => http_build_query($params),
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_TIMEOUT => 8,
        ]);
        $res = curl_exec($ch);
        curl_close($ch);
        return $res;
    }
    $ctx = stream_context_create(['http' => [
        'method' => 'POST',
        'header' => "Content-Type: application/x-www-form-urlencoded\r\n",
        'content' => http_build_query($params),
        'timeout' => 8,
    ]]);
    return @file_get_contents($url, false, $ctx);
}

$sent = false;

// 1) Email
$subject = '=?UTF-8?B?' . base64_encode('Заявка с сайта: ' . $name) . '?=';
$headers = "From: " . LEAD_EMAIL_FROM . "\r\n"
         . "MIME-Version: 1.0\r\n"
         . "Content-Type: text/plain; charset=UTF-8\r\n";
if (@mail(LEAD_EMAIL_TO, $subject, $text, $headers)) {
    $sent = true;
}

// 2) Telegram
if (TG_BOT_TOKEN !== '' && TG_CHAT_ID !== '') {
    $res = http_post_json('https://api.telegram.org/bot' . TG_BOT_TOKEN . '/sendMessage', [
        'chat_id' => TG_CHAT_ID,
        'text' => $text,
    ]);
    if ($res && strpos($res, '"ok":true') !== false) $sent = true;
}

// 3) VK
if (VK_TOKEN !== '' && VK_USER_ID !== '') {
    $res = http_post_json('https://api.vk.com/method/messages.send', [
        'access_token' => VK_TOKEN,
        'user_id' => VK_USER_ID,
        'random_id' => random_int(1, PHP_INT_MAX),
        'message' => $text,
        'v' => '5.199',
    ]);
    if ($res && strpos($res, '"response"') !== false) $sent = true;
}

respond($sent, $sent ? '' : 'delivery');
