<?php
require_once 'DB_Functions.php';
$db = new DB_Functions();
 
// json response array
$response = array("error" => FALSE);
 
$db->updateLocation($_POST['id'], $_POST['location']);

?>