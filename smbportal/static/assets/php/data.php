<?php
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Headers: Origin, X-Requested-With, Content-Type, Accept");
date_default_timezone_set('Asia/Kolkata');

$currencies = array();
$file = fopen("../data/data.csv", "r");
while (!feof($file)) {
    $currency = fgetcsv($file);
    $currencies[] = array(
        'flag'             => "assets/img/flags/" . strtolower($currency[0]) . ".svg",
        'country_fullname' => $currency[1],
        'currency_code'    => $currency[2],
        'currency_name'    => $currency[3],
        'country_name'     => $currency[4],
    );
}
fclose($file);
$half = round(sizeof($currencies) / 2);
//echo '<pre>';
print_r(json_encode($currencies));
?>
