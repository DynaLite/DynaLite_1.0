<?php
require_once 'DB_Functions.php';
$db = new DB_Functions();
 
// json response array
$response = array("error" => FALSE);
 
$db->updateColor($_POST['location'], $_POST['color']);

echo json_encode($response)

?>